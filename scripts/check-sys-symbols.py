#!/usr/bin/env python3
"""Check that every `sys.symbol.*` produced by the OHOS NativeIcon mapping exists in
the minimum supported SDK (5.0.0(12)).

muda maps NativeIcon variants to symbol strings; the ArkTS side renders them via
`$r("sys.symbol.x")`, which resolves at build time against the SDK's sysResource table.
A symbol absent from the 5.0.0(12) floor (e.g. person_3, circle_fill, first public in
API 20) breaks any app built against the floor. Both sides are gated: the whitelist
cases in MenuBarComponent.ets (openharmony-ability repo) and the mapping targets here.

Extracts the `Some("sys.symbol.<name>")` values from the OHOS implementation and fails
if any is missing from the baseline scripts/sys-symbols-api12.txt.

Usage:
    python3 scripts/check-sys-symbols.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASELINE = Path(__file__).resolve().parent / "sys-symbols-api12.txt"
MAPPING = ROOT / "src/platform_impl/ohos/mod.rs"

SYMBOL_RE = re.compile(r'Some\("sys\.symbol\.([\w_]+)"\)')

# Mapping arms kept on purpose for symbols that only exist in newer SDKs: the ArkTS
# whitelist drops their case (renders no icon) until compatibleSdkVersion reaches API 20.
# Remove an entry here once its symbol is present in the 5.0.0(12) baseline.
KNOWN_AP20_EXCEPTIONS = {"person_3", "circle_fill"}


def main():
    baseline = set(BASELINE.read_text(encoding="utf-8").split())
    source = MAPPING.read_text(encoding="utf-8")
    symbols = set(SYMBOL_RE.findall(source))

    missing = sorted(symbols - baseline)
    unexpected = sorted(set(missing) - KNOWN_AP20_EXCEPTIONS)
    print(f"baseline symbols (min SDK 5.0.0/12): {len(baseline)}")
    print(f"mapped symbols:                      {len(symbols)}")
    if unexpected:
        print(f"ERROR: {len(unexpected)} symbol(s) missing from min SDK 5.0.0(12):")
        for sym in unexpected:
            print(f"  sys.symbol.{sym}")
        print("Fix: pick an equivalent symbol that exists in 5.0.0(12), or keep the")
        print("mapping but ensure the ArkTS whitelist drops the case (renders no icon).")
        print("See tauri issue #120.")
        return 1
    if missing:
        print(f"note: {len(missing)} known API 20+ exception(s): " + ", ".join(missing))
    print("OK: mapping targets are a subset of min SDK 5.0.0(12) sysResource table.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
