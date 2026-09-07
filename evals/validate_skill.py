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
    "SKILL.md",
    "README.md",
    "agents/openai.yaml",
    "references/discovery-and-driver.md",
    "references/a-share-validation.md",
    "references/pricing-and-decision.md",
    "references/data-and-metrics-contract.md",
    "scripts/compute_indicators.py",
    "evals/cases.jsonl",
    "evals/trigger_cases.json",
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

# Package hygiene: keep only files that materially serve runtime, maintenance, or regression.
allowed_files = {
    "SKILL.md",
    "README.md",
    "agents/openai.yaml",
    "references/discovery-and-driver.md",
    "references/a-share-validation.md",
    "references/pricing-and-decision.md",
    "references/data-and-metrics-contract.md",
    "scripts/compute_indicators.py",
    "evals/cases.jsonl",
    "evals/trigger_cases.json",
    "evals/validate_skill.py",
    "evals/fixtures/golden-case-theme-driver-regression.md",
    "evals/fixtures/unresolved-signal-input.md",
    "evals/fixtures/indicator-test.csv",
}
actual_files = {str(p.relative_to(ROOT)).replace("\\", "/") for p in ROOT.rglob("*") if p.is_file()}
for extra in sorted(actual_files - allowed_files):
    check(f"no-extra:{extra}", False, "unexpected package artifact; delete or justify")
for expected in sorted(allowed_files):
    check(f"allowed-exists:{expected}", expected in actual_files, "allowed package file missing")
for bad in ROOT.rglob("*"):
    rel = str(bad.relative_to(ROOT)).replace("\\", "/")
    check(f"hygiene:{rel}", "__pycache__" not in rel and not rel.endswith((".pyc", ".pyo", ".DS_Store")) and not rel.startswith("evals/replay"), "cache/replay/build artifact remains")

# 2) No dangling markdown links in active docs
active_docs = [ROOT / "SKILL.md", *sorted((ROOT / "references").glob("*.md")), ROOT / "README.md"]
link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
for doc in active_docs:
    text = doc.read_text(encoding="utf-8")
    for target in link_re.findall(text):
        if target.startswith(("http://", "https://", "#")):
            continue
        target_path = (doc.parent / target).resolve()
        check(f"link:{doc.relative_to(ROOT)}->{target}", target_path.exists(), "dangling local link")

# 3) Purpose alignment / anti-regression in active instructions
skill = read("SKILL.md")
discovery = read("references/discovery-and-driver.md")
validation = read("references/a-share-validation.md")
decision = read("references/pricing-and-decision.md")
data = read("references/data-and-metrics-contract.md")
all_active = "\n".join([skill, discovery, validation, decision, data])

purpose_terms = [
    "昨夜市场到底在交易什么",
    "Theme Ranking",
    "A-share Prior Pricing",
    "Expectation Gap",
    "Core / Watch / Exclude",
]
for term in purpose_terms:
    check(f"purpose:{term}", term in all_active, f"missing purpose anchor {term}")

check("driver-not-event-only", "Industry Trend / Repricing" in skill and "没有单一当日公告，不等于没有可信Driver" in skill)
check("cluster-quality-exit", "解释主要成员与扩散结构" in skill and "形成具体Driver" in discovery)
check("theme-before-stock", "Theme Ranking在A股个股验证之前完成" in skill)
check("prior-pricing-before-gap", "Expectation Gap的必经步骤" in decision)
check("no-linear-score-rule", "禁止单一线性总分" in decision)
check("e-p-t-semantic-lock", "商业化产业只用E；Biotech只用P；技术/价格位置只用T_static" in validation)
check("auction-not-core-gate", "Auction只决定**今天是否执行**，不决定Core资格" in decision)
check("repricing-can-core", "Catalyst Grade=N/A" in decision and "可以进入Core" in decision)
check("fixed-coverage-demoted", "不再要求固定31家公司、13方向" in data)
check("six-module-output", "完整输出：6模块" in decision)
check("candidate-coverage-gate", "Economic Chain Coverage Gate + Omission Challenge" in validation and "节点集合本身经过独立反查仍然完整" in validation)
check("candidate-omission-two-path", "Physical / Technical Dependency" in validation and "Economic Value / Capex Flow" in validation and "不能在这里直接宣布PASS" in validation)
check("candidate-omission-source-backed", "产品架构/BOM/标准接口/工艺流程" in validation and "不能只凭模型记忆宣布完整" in validation)
check("event-ledger-independent", "Independent Material Event Ledger" in discovery and "Material Events" in decision)
check("event-theme-many-to-many", "Cross-theme Driver Candidate" in discovery and "Linked Themes" in discovery and "Causal Status" in discovery and "confirmed common catalyst" in discovery)
check("material-event-linked-high-priority", "第一类不得仅因名额限制被删" in discovery and "Linked Themes" in discovery)
check("event-does-not-hijack-theme", "不能与Theme Rank混成一个排行榜" in decision)
check("version-1.1.2", 'version: "1.1.2"' in skill)
check("no-golden-stock-hardcode-runtime", "澜起科技" not in all_active, "historical stock answer leaked into runtime instructions")
check("no-golden-event-hardcode-runtime", "GPT-6 Astra" not in all_active, "historical event answer leaked into runtime instructions")

for stale in [
    "routing-and-handoffs.md",
    "radar-scan-coverage-contract.md",
    "radars-and-attribution.md",
    "trading-and-pools.md",
    "output-spec.md",
    "0–17共18个模块",
]:
    check(f"no-stale:{stale}", stale not in all_active, "stale architecture reference remains")

# 4) Validate recorded eval fixtures against their own assertions
cases_path = ROOT / "evals/cases.jsonl"
try:
    cases = [json.loads(line) for line in cases_path.read_text(encoding="utf-8").splitlines() if line.strip()]
except Exception as exc:
    cases = []
    FAILURES.append(f"parse evals/cases.jsonl: {exc}")

check("eval-count", len(cases) >= 10, f"only {len(cases)} cases")
ids = {c.get("id") for c in cases}
for expected_id in [
    "trend-driver-without-discrete-catalyst",
    "theme-ranking-before-stock-evidence",
    "prior-pricing-required",
    "no-linear-score-and-core-auction-separation",
    "golden-theme-driver-regression",
    "candidate-economic-chain-saturation",
    "event-radar-independent-ledger",
    "economic-chain-self-closure",
]:
    check(f"eval-present:{expected_id}", expected_id in ids)

for case in cases:
    output = case.get("with_skill_output", "")
    for assertion in case.get("assertions", []):
        for term in assertion.get("required", []) or []:
            check(f"eval:{case['id']}:{assertion['id']}:required:{term}", term in output)
        for term in assertion.get("forbidden", []) or []:
            check(f"eval:{case['id']}:{assertion['id']}:forbidden:{term}", term not in output)

# Golden case should test capability and explicitly warn against generic hardcoding
golden_fixture = read("evals/fixtures/golden-case-theme-driver-regression.md")
check("golden-not-generic-hardcode", "不得硬编码成通用Skill每天都必须出现" in golden_fixture)
check("golden-has-a-share-pricing", "A股上一交易日定价事实边界" in golden_fixture)
check("golden-has-candidate-coverage", "Candidate经济链充分性边界" in golden_fixture and "服务器内存接口/配套芯片" in golden_fixture)
check("golden-has-omission-challenge", "Omission Challenge" in golden_fixture and "产品/技术必需依赖" in golden_fixture and "经济价值/Capex流" in golden_fixture)
check("golden-has-event-retention", "Event Radar保底与跨Theme事件边界" in golden_fixture and "Material Events" in golden_fixture and "Cross-theme Driver Candidate" in golden_fixture)
check("golden-no-fixed-stock-answer", "不是固定股票名单" in golden_fixture and "不能把某只历史股票写进通用Skill作为答案" in golden_fixture)

# 5) Trigger cases are valid JSON and retain near-neighbor negatives
try:
    triggers = json.loads(read("evals/trigger_cases.json"))
    check("trigger-positive", len(triggers.get("should_trigger", [])) >= 6)
    check("trigger-negative", len(triggers.get("should_not_trigger", [])) >= 6)
    check("trigger-near-neighbor", len(triggers.get("near_neighbor", [])) >= 4)
except Exception as exc:
    FAILURES.append(f"parse evals/trigger_cases.json: {exc}")

# 6) Indicator script actually runs on fixture
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

# 7) Resource boundary: references remain small enough for progressive disclosure
for path in sorted((ROOT / "references").glob("*.md")):
    lines = path.read_text(encoding="utf-8").count("\n") + 1
    check(f"reference-size:{path.name}", lines <= 220, f"{lines} lines; consider splitting only if behavior suffers")

print(f"checks={len(CHECKS)} failures={len(FAILURES)}")
if FAILURES:
    for failure in FAILURES:
        print(f"FAIL: {failure}")
    raise SystemExit(1)
print("PASS: structure, package hygiene, purpose alignment, candidate/event recall regressions, golden fixture, triggers, and indicator script")
