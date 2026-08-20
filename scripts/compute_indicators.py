#!/usr/bin/env python3
"""Compute deterministic MA, Wilder RSI9, and BIAS20 from adjusted closes."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

SCRIPT_INTERFACE = "cli"


def load_closes(path: Path) -> tuple[list[tuple[str, float]], list[str]]:
    rows: dict[str, float] = {}
    warnings: list[str] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"date", "close"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError("CSV must contain date and close columns")
        for line_number, row in enumerate(reader, start=2):
            date = (row.get("date") or "").strip()
            raw_close = (row.get("close") or "").strip()
            if not date or not raw_close:
                raise ValueError(f"line {line_number}: date and close are required")
            try:
                close = float(raw_close)
            except ValueError as exc:
                raise ValueError(f"line {line_number}: invalid close {raw_close!r}") from exc
            if not math.isfinite(close) or close <= 0:
                raise ValueError(f"line {line_number}: close must be finite and positive")
            if date in rows:
                warnings.append(f"duplicate date {date}: kept last value")
            rows[date] = close
    ordered = sorted(rows.items(), key=lambda item: item[0])
    if not ordered:
        raise ValueError("CSV contains no valid rows")
    return ordered, warnings


def simple_ma(closes: list[float], period: int) -> float | None:
    if len(closes) < period:
        return None
    return sum(closes[-period:]) / period


def wilder_rsi(closes: list[float], period: int = 9) -> float | None:
    if len(closes) < period + 1:
        return None
    changes = [current - previous for previous, current in zip(closes, closes[1:])]
    gains = [max(change, 0.0) for change in changes]
    losses = [max(-change, 0.0) for change in changes]
    average_gain = sum(gains[:period]) / period
    average_loss = sum(losses[:period]) / period
    for gain, loss in zip(gains[period:], losses[period:]):
        average_gain = ((period - 1) * average_gain + gain) / period
        average_loss = ((period - 1) * average_loss + loss) / period
    if average_loss == 0:
        return 100.0 if average_gain > 0 else 50.0
    relative_strength = average_gain / average_loss
    return 100.0 - (100.0 / (1.0 + relative_strength))


def calculate(rows: list[tuple[str, float]], warnings: list[str]) -> dict[str, object]:
    closes = [close for _, close in rows]
    values: dict[str, float | None] = {}
    for period in (5, 10, 20, 60):
        values[f"ma{period}"] = simple_ma(closes, period)
    values["rsi9"] = wilder_rsi(closes, 9)
    ma20 = values["ma20"]
    values["bias20_pct"] = None if ma20 is None else (closes[-1] / ma20 - 1.0) * 100.0
    rounded = {key: (None if value is None else round(value, 6)) for key, value in values.items()}
    missing = [key for key, value in rounded.items() if value is None]
    return {
        "as_of": rows[-1][0],
        "close": closes[-1],
        "valid_trading_days": len(rows),
        "adjustment_basis": "caller-declared consistent adjusted close",
        "indicators": rounded,
        "missing_indicators": missing,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compute MA5/10/20/60, Wilder RSI9, and BIAS20 from date,close CSV."
    )
    parser.add_argument("csv_path", type=Path, help="UTF-8 CSV ordered or orderable by ISO date")
    args = parser.parse_args()
    try:
        rows, warnings = load_closes(args.csv_path)
        result = calculate(rows, warnings)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
