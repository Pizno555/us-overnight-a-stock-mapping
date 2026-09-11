#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAILURES: list[str] = []
CHECKS: list[str] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    CHECKS.append(name)
    if not condition:
        FAILURES.append(f"{name}: {detail}" if detail else name)


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


# 1) Required structure and lean references
required = [
    "SKILL.md", "README.md", "agents/openai.yaml",
    "references/discovery-and-driver.md", "references/a-share-validation.md",
    "references/pricing-and-decision.md", "references/data-and-metrics-contract.md",
    "scripts/compute_indicators.py", "evals/cases.jsonl",
    "evals/trigger_cases.json", "evals/validate_skill.py",
]
for path in required:
    check(f"exists:{path}", (ROOT / path).exists(), "missing required file")

removed = [
    "references/routing-and-handoffs.md",
    "references/radar-scan-coverage-contract.md",
    "references/radars-and-attribution.md",
    "references/trading-and-pools.md",
    "references/output-spec.md",
]
for path in removed:
    check(f"removed:{path}", not (ROOT / path).exists(), "superseded file still present")

allowed_files = {
    "SKILL.md", "README.md", "agents/openai.yaml",
    "references/discovery-and-driver.md", "references/a-share-validation.md",
    "references/pricing-and-decision.md", "references/data-and-metrics-contract.md",
    "scripts/compute_indicators.py", "evals/cases.jsonl", "evals/trigger_cases.json",
    "evals/validate_skill.py", "evals/fixtures/golden-case-theme-driver-regression.md",
    "evals/fixtures/unresolved-signal-input.md", "evals/fixtures/indicator-test.csv",
}
actual_files = {str(p.relative_to(ROOT)).replace("\\", "/") for p in ROOT.rglob("*") if p.is_file()}
for extra in sorted(actual_files - allowed_files):
    check(f"no-extra:{extra}", False, "unexpected package artifact")
for expected in sorted(allowed_files):
    check(f"allowed-exists:{expected}", expected in actual_files, "allowed package file missing")
for bad in ROOT.rglob("*"):
    rel = str(bad.relative_to(ROOT)).replace("\\", "/")
    check(f"hygiene:{rel}", "__pycache__" not in rel and not rel.endswith((".pyc", ".pyo", ".DS_Store")), "cache/editor artifact remains")

# 2) No dangling local markdown links
active_docs = [ROOT / "SKILL.md", *sorted((ROOT / "references").glob("*.md")), ROOT / "README.md"]
link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
for doc in active_docs:
    text = doc.read_text(encoding="utf-8")
    for target in link_re.findall(text):
        if target.startswith(("http://", "https://", "#")):
            continue
        check(f"link:{doc.relative_to(ROOT)}->{target}", (doc.parent / target).resolve().exists(), "dangling local link")

# 3) YAO purpose/boundary alignment and anti-regression
skill = read("SKILL.md")
discovery = read("references/discovery-and-driver.md")
validation = read("references/a-share-validation.md")
decision = read("references/pricing-and-decision.md")
data = read("references/data-and-metrics-contract.md")
agent = read("agents/openai.yaml")
all_active = "\n".join([skill, discovery, validation, decision, data, agent])

for term in ["昨夜市场到底在交易什么", "Theme Ranking", "A-share Prior Pricing", "Expectation Gap", "Core / Watch / Exclude"]:
    check(f"purpose:{term}", term in all_active, f"missing purpose anchor {term}")

check("version-1.1.3", 'version: "1.1.3"' in skill)
# YAO: goal lock + stage boundary + resource boundary
check("yao:two-pass-before-theme", "① Blind Event Sweep" in skill and "② Market Radar" in skill and "③ Merge + Cluster Decomposition" in skill and "④ Market Theme / Driver" in skill)
check("yao:event-pass-before-theme", "在任何Theme / Driver / A股候选形成前" in skill and "Theme形成前" in discovery)
check("yao:market-pass-independent", "独立从市场行为出发" in discovery and "不能因为Pass A已经找到几个强事件" in discovery)
check("yao:merge-after-two-pass", "只有Pass A和Pass B都完成后" in discovery and "两套Leads合并以后才允许形成Theme / Driver" in skill)
check("yao:gate-simple", "passed`不等于“零遗漏”" in discovery and "不承担“证明互联网没有遗漏”" in discovery)
check("yao:no-closure-evidence-bloat", all(term not in all_active for term in ["Closure Evidence Record", "closure_evidence:", "Universe-escape", "closure_blockers"]))
check("yao:blank-slate-before-named-targeting", "blank-slate discovery" in discovery and "不得包含任何预设机构名" in discovery and "只有开放搜索已经产生具体线索后" in discovery and "完成分母" in discovery)
check("scope-gate-orthogonal", "search_scope" in data and "discovery_gate" in data and "两者正交" in data)
check("partial-can-pass", "数据`partial`但Blind Event Sweep与Market Radar均已执行" in data and "可以`passed`" in data)
check("blocked-output-ban", all(term in decision for term in ["不得输出Final Theme Ranking", "Final Trading Ranking", "Core"]))

# Preserve v1.1.2 behavior contracts
check("material-event-ledger", "Independent Material Event Ledger" in discovery and "Material Events" in decision)
check("event-theme-many-to-many", all(term in discovery for term in ["Cross-theme Driver Candidate", "Linked Themes", "Causal Status"]))
check("event-does-not-hijack-theme", "不能与Theme Rank混成一个排行榜" in decision)
check("driver-not-event-only", "Industry Trend / Repricing" in skill and "没有单一当日公告，不等于没有可信Driver" in skill)
check("cluster-quality-exit", "解释主要成员与扩散结构" in skill and "形成具体Driver" in discovery)
check("theme-before-stock", "Theme Ranking在A股个股验证之前完成" in skill)
check("fixed-coverage-demoted", "不再要求固定31家公司、13方向" in data)
check("candidate-coverage-gate", "Economic Chain Coverage Gate + Omission Challenge" in validation and "节点集合本身经过独立反查仍然完整" in validation)
check("candidate-omission-two-path", "Physical / Technical Dependency" in validation and "Economic Value / Capex Flow" in validation)
check("candidate-omission-source-backed", "产品架构/BOM/标准接口/工艺流程" in validation and "不能只凭模型记忆宣布完整" in validation)
check("prior-pricing-before-gap", "Expectation Gap的必经步骤" in decision)
check("no-linear-score-rule", "禁止单一线性总分" in decision)
check("e-p-t-semantic-lock", "商业化产业只用E；Biotech只用P；技术/价格位置只用T_static" in validation)
check("auction-not-core-gate", "Auction只决定**今天是否执行**，不决定Core资格" in decision)
check("repricing-can-core", "Catalyst Grade=N/A" in decision and "可以进入Core" in decision)
check("six-module-output", "完整输出：6模块" in decision)
check("no-golden-stock-hardcode-runtime", "澜起科技" not in all_active)
check("no-golden-event-hardcode-runtime", "2026-09-11" not in all_active and "昨夜FCC" not in all_active)

for stale in [
    "routing-and-handoffs.md", "radar-scan-coverage-contract.md", "radars-and-attribution.md",
    "trading-and-pools.md", "output-spec.md", "0–17共18个模块",
]:
    check(f"no-stale:{stale}", stale not in all_active, "stale architecture reference remains")

# 4) Recorded behavioral regressions / contract fixtures
cases_path = ROOT / "evals/cases.jsonl"
try:
    cases = [json.loads(line) for line in cases_path.read_text(encoding="utf-8").splitlines() if line.strip()]
except Exception as exc:
    cases = []
    FAILURES.append(f"parse evals/cases.jsonl: {exc}")

check("eval-count", len(cases) >= 18, f"only {len(cases)} cases")
ids = {c.get("id") for c in cases}
legacy_ids = [
    "premarket-no-future-data", "trend-driver-without-discrete-catalyst",
    "unresolved-signal-research-quality", "theme-ranking-before-stock-evidence",
    "biotech-e-p-t-semantics", "prior-pricing-required", "partial-search-scope",
    "no-linear-score-and-core-auction-separation", "golden-theme-driver-regression",
    "candidate-economic-chain-saturation", "event-radar-independent-ledger",
    "economic-chain-self-closure",
]
for expected_id in legacy_ids:
    check(f"legacy-eval-present:{expected_id}", expected_id in ids)

twopass_ids = [
    "discovery-historical-2026-09-11-fcc-recall",
    "discovery-out-of-seed-regulator",
    "discovery-market-cluster-without-event",
    "discovery-gate-block-event-pass-missing",
    "discovery-gate-block-market-pass-missing",
    "discovery-partial-data-two-pass-passed",
]
for expected_id in twopass_ids:
    check(f"twopass-eval-present:{expected_id}", expected_id in ids)

for case in cases:
    mode = case.get("execution", {}).get("mode")
    if mode != "recorded_fixture":
        continue
    output = case.get("with_skill_output", "")
    check(f"recorded-fixture:has-output:{case['id']}", bool(output))
    check(f"recorded-fixture:has-assertions:{case['id']}", bool(case.get("assertions")))
    for assertion in case.get("assertions", []):
        for term in assertion.get("required", []) or []:
            check(f"eval:{case['id']}:{assertion['id']}:required:{term}", term in output)
        for term in assertion.get("forbidden", []) or []:
            check(f"eval:{case['id']}:{assertion['id']}:forbidden:{term}", term not in output)

# 5) Red Team contracts: attack the architecture, not just wording
red_team = {
    "high_materiality_no_price_cluster": "event-radar-independent-ledger",
    "regulator_outside_fallback_seeds": "discovery-out-of-seed-regulator",
    "strong_cluster_no_event": "discovery-market-cluster-without-event",
    "skip_blind_event_sweep": "discovery-gate-block-event-pass-missing",
    "skip_market_radar": "discovery-gate-block-market-pass-missing",
    "partial_data_false_block": "discovery-partial-data-two-pass-passed",
}
for name, case_id in red_team.items():
    check(f"red-team:{name}", case_id in ids)

# Search order must resist anchoring: no final Theme before Merge in the runtime flow.
flow_pos = {term: skill.find(term) for term in ["① Blind Event Sweep", "② Market Radar", "③ Merge + Cluster Decomposition", "④ Market Theme / Driver", "⑤b Discovery Gate", "⑥ Theme Ranking"]}
check("red-team:flow-order", all(flow_pos[k] >= 0 for k in flow_pos) and list(flow_pos.values()) == sorted(flow_pos.values()), str(flow_pos))
# Regulatory discovery must begin open-ended; named institutions are only allowed after a lead appears.
check("red-team:blank-slate-regulatory", "政府/监管/政策Delta" in discovery and "blank-slate discovery" in discovery and "预设机构名" in discovery and "定向追查" in discovery)
for forbidden_pattern in [r"checked\s*=\s*total", r"fixed_total\s*:\s*31", r"sector_registry_coverage", r"regulator_government:\s*checked/total"]:
    check(f"red-team:no-fixed-coverage:{forbidden_pattern}", re.search(forbidden_pattern, all_active, re.I) is None)

# 6) Contract Evaluator (blind-style behavior contracts).
# These are hidden-output behavior contracts; they do NOT claim an independent-provider live model run.
blind_cases = [c for c in cases if c.get("metadata", {}).get("case_type") == "blind_contract"]
check("blind-contract-count", len(blind_cases) >= 5, f"only {len(blind_cases)} blind contract cases")
for case in blind_cases:
    check(f"blind-contract:holdout:{case['id']}", bool(case.get("execution", {}).get("holdout")), "contract holdout must be marked holdout")
    check(f"blind-contract:has-baseline:{case['id']}", bool(case.get("baseline_output")))
    check(f"blind-contract:has-assertions:{case['id']}", bool(case.get("assertions")))

# Historical Live / Blind benchmark configuration. Static validation must never score Recall.
historical = next((c for c in cases if c.get("id") == "discovery-historical-2026-09-11-fcc-recall"), None)
check("historical-replay-case-present", historical is not None)
if historical:
    execution = historical.get("execution", {})
    ground_truth = historical.get("ground_truth", {})
    live_assertions = historical.get("live_assertions", [])
    prompt = historical.get("prompt", "")
    check("historical-replay-live-mode", execution.get("mode") == "historical_live_replay_required")
    check("historical-replay-prompt-only", execution.get("pass_to_model") == ["prompt"] )
    check("historical-replay-static-cannot-score", execution.get("static_validator_scores_recall") is False)
    check("historical-replay-no-prewritten-output", "with_skill_output" not in historical and "assertions" not in historical)
    check("historical-replay-ground-truth-evaluator-only", ground_truth.get("evaluator_only") is True)
    check("historical-replay-ground-truth-present", bool(ground_truth.get("must_recall")) and bool(live_assertions))
    check("historical-replay-prompt-no-fcc-leak", "FCC" not in prompt.upper())
    check("historical-replay-fcc-benchmark-configured", any("FCC" in term.upper() for item in live_assertions for term in item.get("required", [])))
    check("historical-replay-not-runtime-hardcode", "2026-09-11" not in all_active and "昨夜FCC" not in all_active)

# 7) Explicit gate truth table: simple process gate, not completeness proof.
gate_truth = [
    ((True, True, False), True),   # event pass, market pass, no unresolved HM lead
    ((False, True, False), False),
    ((True, False, False), False),
    ((True, True, True), False),
]
for (event_done, market_done, unresolved_high_materiality), should_pass in gate_truth:
    computed = event_done and market_done and not unresolved_high_materiality
    check(f"gate-truth:{event_done}+{market_done}+{unresolved_high_materiality}", computed is should_pass)

# 8) Golden fixture boundaries (preserve v1.1.2 regression coverage)
golden = read("evals/fixtures/golden-case-theme-driver-regression.md")
check("golden-not-generic-hardcode", "不得硬编码成通用Skill每天都必须出现" in golden)
check("golden-has-a-share-pricing", "A股上一交易日定价事实边界" in golden)
check("golden-has-candidate-coverage", "Candidate经济链充分性边界" in golden and "服务器内存接口/配套芯片" in golden)
check("golden-has-omission-challenge", "Omission Challenge" in golden and "产品/技术必需依赖" in golden and "经济价值/Capex流" in golden)
check("golden-has-event-retention", "Event Radar保底与跨Theme事件边界" in golden and "Material Events" in golden and "Cross-theme Driver Candidate" in golden)
check("golden-no-fixed-stock-answer", "不是固定股票名单" in golden and "不能把某只历史股票写进通用Skill作为答案" in golden)

# 9) Trigger cases
try:
    triggers = json.loads(read("evals/trigger_cases.json"))
    check("trigger-positive", len(triggers.get("should_trigger", [])) >= 8)
    check("trigger-negative", len(triggers.get("should_not_trigger", [])) >= 8)
    check("trigger-near-neighbor", len(triggers.get("near_neighbor", [])) >= 4)
except Exception as exc:
    FAILURES.append(f"parse evals/trigger_cases.json: {exc}")

# 10) Indicator script actually runs
cmd = [sys.executable, str(ROOT / "scripts/compute_indicators.py"), str(ROOT / "evals/fixtures/indicator-test.csv")]
try:
    proc = subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=10)
    payload = json.loads(proc.stdout)
    indicators = payload.get("indicators", {})
    check("indicator-ma5", indicators.get("ma5") is not None)
    check("indicator-ma60", indicators.get("ma60") is not None)
    check("indicator-rsi9", indicators.get("rsi9") is not None)
    check("indicator-bias20", indicators.get("bias20_pct") is not None)
except Exception as exc:
    FAILURES.append(f"indicator script failed: {exc}")

# 11) Resource boundary: keep references compact enough for progressive disclosure.
for path in sorted((ROOT / "references").glob("*.md")):
    lines = path.read_text(encoding="utf-8").count("\n") + 1
    check(f"reference-size:{path.name}", lines <= 220, f"{lines} lines; split only if runtime behavior suffers")

print(f"checks={len(CHECKS)} failures={len(FAILURES)}")
if FAILURES:
    for failure in FAILURES:
        print(f"FAIL: {failure}")
    raise SystemExit(1)
print("PASS: v1.1.3 Two-Pass Frozen Baseline, YAO boundaries, legacy regressions, Red Team contracts, Contract Evaluator cases, live-benchmark configuration, triggers, and indicators")
