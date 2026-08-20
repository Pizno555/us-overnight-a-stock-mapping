# Output Quality Scorecard

This v0 scorecard compares static without-skill and with-skill outputs using assertion grading.

- Cases: `7`
- Baseline pass rate: `0.0`
- With-skill pass rate: `100.0`
- Delta: `100.0`
- Regressions: `0`
- Blind A/B pairs: `7`
- Gate pass: `True`

Blind review artifacts are generated separately so reviewers can inspect A/B outputs without seeing the answer key.
Run output review adjudication after reviewer decisions are recorded; pending cases should stay pending rather than being counted as human agreement.

## Case Results

| Case | Baseline | With Skill | Delta | Winner | Failed With-Skill Assertions |
| --- | ---: | ---: | ---: | --- | --- |
| premarket-no-future-data | 0.0 | 100.0 | 100.0 | with_skill | None |
| unresolved-signal-not-core | 0.0 | 100.0 | 100.0 | with_skill | None |
| biotech-uses-p-stage | 0.0 | 100.0 | 100.0 | with_skill | None |
| partial-coverage-disclosure | 0.0 | 100.0 | 100.0 | with_skill | None |
| sector-anchor-nonprice-discovery | 0.0 | 100.0 | 100.0 | with_skill | None |
| composite-route-handoff | 0.0 | 100.0 | 100.0 | with_skill | None |
| two-catalyst-three-table-handoff | 0.0 | 100.0 | 100.0 | with_skill | None |

## Failure Taxonomy

- No with-skill assertion failures.

## Next Fixes

- Add holdout cases before using this as a release gate.
- Promote repeated failed assertions into the output-risk profile.
- Keep assertions tied to material deliverables, not phrasing trivia.
