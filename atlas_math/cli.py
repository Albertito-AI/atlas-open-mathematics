"""Command-line interface for the offline demonstration."""

import argparse
import json
from pathlib import Path
import sys

from .engine import generate_case, run_demo, verify


MAX_INPUT_BYTES = 16_384


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_constant(value):
    raise ValueError(f"non-finite JSON value: {value}")


def _load_json(path: Path):
    with path.open("rb") as handle:
        raw = handle.read(MAX_INPUT_BYTES + 1)
    if len(raw) > MAX_INPUT_BYTES:
        raise ValueError(f"JSON input exceeds {MAX_INPUT_BYTES} bytes")
    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs,
                          parse_constant=_reject_constant)
    except (UnicodeError, RecursionError) as exc:
        raise ValueError("JSON input is not valid bounded UTF-8 JSON") from exc


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Offline exact-mathematics workflow pilot; no AI/model calls.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    demo = subparsers.add_parser("demo", help="compare a flawed baseline and exact certificate-checked solver")
    demo.add_argument("--output", required=True, type=Path, help="immutable run directory (identical reruns are safe)")
    demo.add_argument("--seed", type=int, default=7)
    generate = subparsers.add_parser("generate", help="write one public synthetic practice case")
    generate.add_argument("--seed", type=int, required=True)
    generate.add_argument("--output", type=Path, required=True, help="new JSON file; existing files are refused")
    check = subparsers.add_parser("verify", help="check an externally supplied rational linear-system candidate")
    check.add_argument("--case", type=Path, required=True)
    check.add_argument("--candidate", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "verify":
            result = verify(_load_json(args.case), _load_json(args.candidate))
            print(json.dumps(result, sort_keys=True))
            if result["accepted"]:
                return 0
            return 2 if result["reason"].startswith("invalid input:") else 1
        if args.command == "generate":
            result = generate_case(args.seed)
            with args.output.open("x", encoding="utf-8") as handle:
                json.dump(result, handle, sort_keys=True, indent=2)
                handle.write("\n")
            print(json.dumps({"ok": True, "output": str(args.output), "case": result}, sort_keys=True))
            return 0
        result = run_demo(args.output, args.seed)
    except (ValueError, OSError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps({"ok": True, "output": str(args.output), "report": result}, sort_keys=True, indent=2))
    return 0
