"""Command line interface for SIS."""
from __future__ import annotations

import argparse
import json
import os
from typing import Dict, List, Any, Iterable, Tuple

from sis.engine import RuleEngine
from sis.parsers import parse_file
from sis.report import render_markdown_report


KNOWN_EXTENSIONS = {
    ".tf": "terraform",
    ".tf.json": "terraform",
    ".yaml": "kubernetes",
    ".yml": "kubernetes",
    ".json": "arm",
}


def _iter_files(target: str) -> Iterable[str]:
    if os.path.isfile(target):
        yield target
        return

    for root, _, files in os.walk(target):
        for name in files:
            yield os.path.join(root, name)


def _detect_type(path: str, override: str | None) -> str | None:
    if override:
        return override

    lowered = path.lower()
    if lowered.endswith(".tf.json"):
        return "terraform"

    _, ext = os.path.splitext(lowered)
    return KNOWN_EXTENSIONS.get(ext)


def _scan_file(
    engine: RuleEngine, path: str, file_type: str
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    findings: List[Dict[str, Any]] = []
    errors: List[Dict[str, Any]] = []

    try:
        with open(path, "r", encoding="utf-8") as handle:
            content = handle.read()

        resources = parse_file(file_type, content)
        for resource in resources:
            resource_findings = engine.scan_resource(
                file_type=file_type,
                resource_kind=resource.get("kind", ""),
                resource=resource,
            )

            for finding in resource_findings:
                finding.update({
                    "file": path,
                    "line": resource.get("line", 1),
                })

            findings.extend(resource_findings)
    except Exception as exc:
        errors.append({
            "file": path,
            "error": "PARSE_ERROR",
            "message": str(exc),
        })

    return findings, errors


def _summarize(findings: List[Dict[str, Any]]) -> Dict[str, Any]:
    summary = {
        "total_findings": len(findings),
        "by_type": {
            "IRREVERSIBLE_IDENTITY_BINDING": 0,
            "IRREVERSIBLE_DECISION": 0,
            "ADMIN_OVERRIDE_DEPENDENCY": 0,
        },
    }

    for finding in findings:
        summary["by_type"][finding["rule_type"]] += 1

    return summary


def _write_output(output: str, path: str | None) -> None:
    if not path:
        print(output)
        return
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(output)


def scan_command(args: argparse.Namespace) -> int:
    engine = RuleEngine(args.rules)

    all_findings: List[Dict[str, Any]] = []
    all_errors: List[Dict[str, Any]] = []

    for path in _iter_files(args.target):
        file_type = _detect_type(path, args.type)
        if not file_type:
            if args.strict:
                all_errors.append({
                    "file": path,
                    "error": "UNKNOWN_TYPE",
                    "message": "Cannot infer file type; pass --type",
                })
            continue

        findings, errors = _scan_file(engine, path, file_type)
        all_findings.extend(findings)
        all_errors.extend(errors)

    summary = _summarize(all_findings)

    if args.format == "json":
        payload = {
            "target": args.target,
            "rules": args.rules,
            "total_files": len(list(_iter_files(args.target))),
            "findings": all_findings,
            "summary": summary,
            "errors": all_errors,
        }
        _write_output(json.dumps(payload, indent=2), args.output)
    else:
        lines = [
            f"Target: {args.target}",
            f"Rules: {args.rules}",
            f"Findings: {summary['total_findings']}",
        ]
        for rule_type, count in summary["by_type"].items():
            lines.append(f"  {rule_type}: {count}")
        if all_errors:
            lines.append("Errors:")
            for error in all_errors:
                lines.append(f"  {error['file']}: {error['message']}")
        if all_findings:
            lines.append("Findings:")
            for finding in all_findings:
                lines.append(
                    f"  {finding['file']}:{finding['line']} "
                    f"{finding['rule_id']} {finding['message']}"
                )
        _write_output("\n".join(lines) + "\n", args.output)

    return 0 if not all_errors else 2


def report_command(args: argparse.Namespace) -> int:
    with open(args.input, "r", encoding="utf-8") as handle:
        payload = json.load(handle)

    report = render_markdown_report(payload)
    _write_output(report, args.output)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sis",
        description="Static Irreversibility Scanner",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    scan = subparsers.add_parser("scan", help="Scan a target path")
    scan.add_argument(
        "-r",
        "--rules",
        default="rules/demo.json",
        help="Path to rules JSON",
    )
    scan.add_argument(
        "-t",
        "--target",
        required=True,
        help="File or directory to scan",
    )
    scan.add_argument(
        "--type",
        choices=[
            "terraform",
            "cloudformation",
            "kubernetes",
            "docker_compose",
            "arm",
        ],
        help="Force file type (useful for YAML/JSON)",
    )
    scan.add_argument(
        "--strict",
        action="store_true",
        help="Error on unknown file types",
    )
    scan.add_argument(
        "--format",
        choices=["json", "text"],
        default="text",
        help="Output format",
    )
    scan.add_argument(
        "-o",
        "--output",
        help="Write output to a file instead of stdout",
    )
    scan.set_defaults(func=scan_command)

    report = subparsers.add_parser(
        "report",
        help="Generate a client report from a JSON scan output",
    )
    report.add_argument(
        "-i",
        "--input",
        required=True,
        help="Path to JSON scan output",
    )
    report.add_argument(
        "-o",
        "--output",
        required=True,
        help="Path to write the report (Markdown)",
    )
    report.set_defaults(func=report_command)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
