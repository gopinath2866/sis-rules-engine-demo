"""Report generation for SIS."""
from __future__ import annotations

from typing import Dict, Any, List
from datetime import datetime


def _safe(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def _render_summary(summary: Dict[str, Any]) -> List[str]:
    lines = ["## Summary", ""]
    lines.append(f"Total findings: **{summary.get('total_findings', 0)}**")
    lines.append("")
    lines.append("By type:")
    lines.append("")
    lines.append("| Rule type | Count |")
    lines.append("| --- | ---: |")
    for rule_type, count in (summary.get("by_type", {}) or {}).items():
        lines.append(f"| {rule_type} | {count} |")
    lines.append("")
    return lines


def _render_findings(findings: List[Dict[str, Any]]) -> List[str]:
    lines = ["## Findings", ""]
    if not findings:
        lines.append("No findings detected.")
        lines.append("")
        return lines

    lines.append("| File | Line | Rule | Type | Message | Resource |")
    lines.append("| --- | ---: | --- | --- | --- | --- |")
    for finding in findings:
        file_path = _safe(finding.get("file"))
        line = _safe(finding.get("line"))
        rule_id = _safe(finding.get("rule_id"))
        rule_type = _safe(finding.get("rule_type"))
        message = _safe(finding.get("message")).replace("|", "\\|")
        resource = f"{_safe(finding.get('resource_kind'))}:{_safe(finding.get('resource_name'))}"
        lines.append(f"| {file_path} | {line} | {rule_id} | {rule_type} | {message} | {resource} |")
    lines.append("")
    return lines


def _render_errors(errors: List[Dict[str, Any]]) -> List[str]:
    lines = ["## Errors", ""]
    if not errors:
        lines.append("No errors reported.")
        lines.append("")
        return lines

    lines.append("| File | Error | Message |")
    lines.append("| --- | --- | --- |")
    for error in errors:
        file_path = _safe(error.get("file"))
        code = _safe(error.get("error"))
        message = _safe(error.get("message")).replace("|", "\\|")
        lines.append(f"| {file_path} | {code} | {message} |")
    lines.append("")
    return lines


def render_markdown_report(payload: Dict[str, Any]) -> str:
    """Render a Markdown report from a JSON scan payload."""
    lines: List[str] = []
    lines.append("# SIS Scan Report")
    lines.append("")
    lines.append(f"Generated: {datetime.utcnow().isoformat()}Z")
    lines.append("")
    lines.append("## Scan Context")
    lines.append("")
    lines.append(f"- Target: `{payload.get('target', '')}`")
    lines.append(f"- Rules: `{payload.get('rules', '')}`")
    if payload.get("total_files") is not None:
        lines.append(f"- Total files: `{payload.get('total_files')}`")
    lines.append("")

    summary = payload.get("summary", {}) or {}
    findings = payload.get("findings", []) or []
    errors = payload.get("errors", []) or []

    lines.extend(_render_summary(summary))
    lines.extend(_render_findings(findings))
    lines.extend(_render_errors(errors))

    return "\n".join(lines).strip() + "\n"
