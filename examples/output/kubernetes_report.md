# SIS Scan Report

Generated: 2026-05-22T12:01:31.342103Z

## Scan Context

- Target: `examples/kubernetes`
- Rules: `rules/demo.json`
- Total files: `1`

## Summary

Total findings: **4**

By type:

| Rule type | Count |
| --- | ---: |
| IRREVERSIBLE_IDENTITY_BINDING | 1 |
| IRREVERSIBLE_DECISION | 0 |
| ADMIN_OVERRIDE_DEPENDENCY | 3 |

## Findings

| File | Line | Rule | Type | Message | Resource |
| --- | ---: | --- | --- | --- | --- |
| examples/kubernetes/manifest.yaml | 1 | IRR-IDENT-03 | IRREVERSIBLE_IDENTITY_BINDING | Service account token mounted in system namespace. | ServiceAccount:system-sa |
| examples/kubernetes/manifest.yaml | 1 | ADMIN-03 | ADMIN_OVERRIDE_DEPENDENCY | System namespace resource requires elevated authority. | ServiceAccount:system-sa |
| examples/kubernetes/manifest.yaml | 1 | ADMIN-01 | ADMIN_OVERRIDE_DEPENDENCY | ClusterRoleBinding requires cluster-admin to reverse. | ClusterRoleBinding:system-admin |
| examples/kubernetes/manifest.yaml | 1 | ADMIN-03 | ADMIN_OVERRIDE_DEPENDENCY | System namespace resource requires elevated authority. | ClusterRoleBinding:system-admin |

## Operator Impact

### `ServiceAccount:system-sa`

- Rule: `IRR-IDENT-03`
- Pattern: Identity lock-in
- Impact: This can increase dependency on a fixed identity path, making later detachment or replacement more expensive.

### `ServiceAccount:system-sa`

- Rule: `ADMIN-03`
- Pattern: Elevated-access dependency
- Impact: Operational changes may depend on elevated access, which can slow mitigation or rollback.

### `ClusterRoleBinding:system-admin`

- Rule: `ADMIN-01`
- Pattern: Authority dependency
- Impact: Future rollback or policy change may depend on cluster-admin access.

### `ClusterRoleBinding:system-admin`

- Rule: `ADMIN-03`
- Pattern: Elevated-access dependency
- Impact: Operational changes may depend on elevated access, which can slow mitigation or rollback.

## Errors

No errors reported.
