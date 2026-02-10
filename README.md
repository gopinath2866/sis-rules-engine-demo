# Static Irreversibility Scanner (SIS) v1.0.0 — Public Demo

Deterministic pattern scanner for irreversible infrastructure decisions.

## What It Does
SIS scans infrastructure-as-code manifests to surface irreversible actions, identity bindings, and admin override dependencies before they ship. It is rule-driven, deterministic, and produces JSON/text outputs suitable for CI, audits, and consulting engagements.

## Quick Start
Install dependencies and run a local scan.

```bash
pip install -r requirements.txt
sis scan -t examples/terraform --format json
```

Run the API server:

```bash
sis-api
```

## Paid SIS Scanner Access (Full Core)
The public demo uses a reduced ruleset and example inputs only. Full private core
(expanded rules, deeper IaC coverage, API gating) is available via license token.

**License Token Format**
`LICENSE-<ID>-VALIDUNTIL-YYYYMMDD` (e.g., `LICENSE-ABC123-VALIDUNTIL-20261231`)

**How to Use (Full Core)**
```bash
# CLI (full core)
export SIS_LICENSE="LICENSE-TEST123-VALIDUNTIL-20261231"
sis scan -t /path/to/iac --format json
```

```bash
# API (full core)
curl -X POST "http://localhost:8000/v1/scan" \
  -H "X-SIS-License: LICENSE-TEST123-VALIDUNTIL-20261231" \
  -H "Content-Type: application/json" \
  -d '{"scan_id": "local-test", "files": []}'
```

**Obtain a Token / Full Access**
- DM `@SignalOrient` on X for scoping/pricing or a trial token.
- Or open a GitHub Issue titled `Access Request`.
- See `docs/SIS_Pricing.md` for pilot guidance.

Security notes (full core):
- Prefer header auth to avoid tokens in URLs/logs.
- Token validation is local and deterministic (no external calls).

## CLI Usage

```bash
sis scan -t <path>
```

Options:
- `-r, --rules` Path to rules JSON (default `rules/demo.json`)
- `--type` Force file type: `terraform`, `cloudformation`, `kubernetes`, `docker_compose`, `arm`
- `--format` `text` or `json`
- `--strict` Error on unknown file types
- `-o, --output` Write output to a file

Notes:
- `.yaml/.yml` files default to Kubernetes unless you pass `--type`.
- `.json` files default to ARM unless you pass `--type`.

## Examples
Sample inputs live in `examples/` and expected outputs in `examples/expected/`.

```bash
sis scan -t examples/terraform --format json
sis scan -t examples/kubernetes --format json
sis scan -t examples/cloudformation --type cloudformation --format json
sis scan -t examples/docker_compose --type docker_compose --format json
sis scan -t examples/arm --format json
```

Expected outputs:
- `examples/expected/terraform.json`
- `examples/expected/kubernetes.json`
- `examples/expected/cloudformation.json`
- `examples/expected/docker_compose.json`
- `examples/expected/arm.json`

## Report Generator
Generate a client-ready Markdown report from JSON output.

```bash
sis scan -t examples/terraform --format json -o /tmp/sis-scan.json
sis report -i /tmp/sis-scan.json -o /tmp/sis-report.md
```

## Docker
Build the container and run scans without local Python setup.

```bash
docker build -t sis:local .
docker run --rm -v $(pwd):/work -w /work sis:local scan -t examples/terraform --format json
```

## Consulting Orientation
Use SIS as a deterministic audit engine for paid engagements. The workflow is designed to minimize human effort while producing defensible outputs.

Deliverables:
- Scan report (JSON + human summary)
- Rule coverage map (what rules fired, what didn’t)
- Remediation notes (actionable changes per finding)

Engagement flow:
1. Client provides IaC repo or exported manifests
2. Run SIS in a clean environment
3. Deliver report + remediation notes
4. Optional follow-up scan after fixes

Inputs required:
- Target code or manifest bundle
- Allowed formats (Terraform, CloudFormation, Kubernetes, Compose, ARM)
- Scope boundaries (environments, repos, exclusions)

Report template (suggested sections):
- Executive summary
- Findings by severity/type
- Evidence (file, line, rule id, message)
- Remediation guidance
- Appendix: full JSON output

Pricing guidance:
- Use fixed-fee per environment or per repository
- Add-ons: custom rules, remediation support, re-scan packages

## Paid Engagement Pack (Public Templates)
Templates to run engagements with minimal friction:
- `docs/SIS_SOW_Template.md`
- `docs/SIS_Pricing.md`
- `docs/SIS_Intake_Form.md`

## Request Full Access
To request access to the full operational SIS scanner for paid engagements, DM `@SignalOrient` on X or open a GitHub Issue titled `Access Request` using the issue template.

## Demo Limitations
This public demo is intentionally scoped to example inputs and a reduced ruleset (`rules/demo.json`). For full production scanning and custom engagements, request access to the private release.

## Project Structure
- `src/sis/engine.py`: deterministic rule engine
- `src/sis/parsers/`: format parsers (demo scope)
- `rules/demo.json`: demo rule definitions
- `examples/`: demo inputs and expected outputs
- `tests/`: unit tests

## Status
Operational for deterministic scans with minimal parsers. Extend rules and add custom mappings as needed.
