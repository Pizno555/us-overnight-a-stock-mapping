# Route Scorecard

- total cases: `22`
- accuracy: `1.0`
- ambiguous cases: `0`
- no-route accuracy: `1.0`

## Route Metrics

| Route | Expected | Predicted | Precision | Recall | Avg Margin |
| --- | ---: | ---: | ---: | ---: | ---: |
| `us-overnight-a-stock-mapping` | 8 | 8 | 1.0 | 1.0 | 0.874 |
| `no_route` | 14 | 14 | 1.0 | 1.0 | - |

## Confusion Matrix

| Expected \ Predicted | `us-overnight-a-stock-mapping` | `no_route` |
| --- | ---: | ---: |
| `us-overnight-a-stock-mapping` | 8 | 0 |
| `no_route` | 0 | 14 |

## Ambiguous Cases

| Family | Expected | Predicted | Margin |
| --- | --- | --- | ---: |
| - | - | - | - |
