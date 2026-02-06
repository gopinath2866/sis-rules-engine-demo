# SIS Consulting Statement of Work (SOW)

## 1. Parties
- Provider: [Provider Name], [Jurisdiction]
- Client: [Client Legal Name]
- Effective Date: [YYYY-MM-DD]

## 2. Scope of Work
The Provider will run the Static Irreversibility Scanner (SIS) against client-supplied infrastructure-as-code (IaC) artifacts to identify irreversible decisions, identity bindings, and admin override dependencies.

Included:
- One deterministic scan per defined environment/repository
- Findings report (JSON + Markdown summary)
- Remediation notes for each finding

Excluded (unless added as an add-on):
- Code changes or remediation implementation
- Custom rule development
- Ongoing monitoring

## 3. Client Responsibilities
Client will provide:
- Repository or bundle of IaC manifests
- Scope definition (repos, environments, exclusions)
- Approved file formats (Terraform, CloudFormation, Kubernetes, Docker Compose, ARM)
- Payment confirmation hash (if required)

## 4. Deliverables
- `scan.json` (raw SIS output)
- `report.md` (client-ready report)
- Remediation notes

## 5. Timeline
- Standard turnaround: [X] business days after intake + payment
- Expedited option available as add-on

## 6. Fees & Payment
- Fixed fee per environment/repository (see pricing sheet)
- Payment due before scan execution
- Payment rails provided upon engagement

## 7. Confidentiality
All client artifacts and scan outputs are treated as confidential. Data is processed locally and not retained beyond delivery unless agreed in writing.

## 8. Liability
SIS is a deterministic scanner that reports on configured rules and patterns. It is not a guarantee of security or compliance. Provider liability is limited to fees paid for the engagement.

## 9. Refunds
No refunds after issuance of deliverables.

## 10. Acceptance
Deliverables are deemed accepted upon delivery unless issues are reported within [X] business days.

## 11. Signatures
Provider: _______________________  Date: __________

Client: _________________________  Date: __________
