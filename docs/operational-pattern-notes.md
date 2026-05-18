# Operational Pattern Notes

A collection of recurring operational failure patterns observed across SRE, Kubernetes, platform engineering, and incident-response discussions.

This is not a framework or methodology. It is a working notebook of recurring operational patterns in plain engineering language.

## Decision Memory Loss

### Plain-language definition

Teams resolve the immediate incident, but fail to preserve the reasoning that would make the next similar incident cheaper to diagnose.

### What operators usually experience

- The useful debugging path lives in one person’s head, Slack history, or a half-remembered postmortem.
- Runbooks describe what happened, but not what to check first next time.
- Similar incidents recur and the team re-derives the same root cause path from scratch.

### Common signals

- Repeated first-pass debugging mistakes.
- Escalation to the same people every time an alert fires.
- Incident notes that explain chronology better than diagnosis.

### Example incident types

- Repeated investigation of the same connection pool exhaustion pattern.
- Config or IAM mismatches rediscovered through manual debugging.
- Runbook links present in alerts, but not used during first-pass triage.

### Why debugging becomes expensive

The system may be observable, but the reasoning required to interpret the signals is not preserved in an operationally useful way.

## Declared vs Runtime Divergence

### Plain-language definition

The declared model of the system looks healthy or converged while runtime conditions have already started diverging underneath.

### What operators usually experience

- Dashboards look normal while heartbeats, latency, or underlying dependencies are already degrading.
- Requests and limits look reasonable while startup behavior still overwhelms nodes.
- Desired state appears converged while production has already drifted operationally.

### Common signals

- “Healthy” status indicators that remain green longer than the system is actually stable.
- Runtime symptoms that appear one or two layers below where teams first look.
- Disagreement between cluster state, Git state, and actual behavior under load.

### Example incident types

- `NodeNotReady` where the real cause sits in IO, runtime, network, or kubelet pressure below the obvious symptom.
- Scheduler/runtime contention where the resource model encodes a simplified version of reality.
- GitOps convergence while lower-layer drift or dependency instability is already affecting production.

### Why debugging becomes expensive

Teams trust the declared model too long, so the real failure surface is only investigated after the gap has already widened.

## Authority Drift

### Plain-language definition

Systems gradually accumulate more privileged or harder-to-audit control surfaces than teams originally intended, often through normal operational convenience.

### What operators usually experience

- Broad permissions become the practical default path.
- Approval or execution boundaries become harder to reason about.
- Security or governance controls exist, but their real operational impact is not well understood.

### Common signals

- Cluster-admin or broad RBAC bindings that persist long after the original need is gone.
- Identity propagation paths that are hard to explain end-to-end.
- Automation that quietly expands who can do what, and under which assumptions.

### Example incident types

- ClusterRoleBinding creep across Kubernetes environments.
- Emergency privilege grants that quietly become durable state.
- Chained automation where approval, identity, and execution surfaces are spread across multiple systems.

### Why debugging becomes expensive

The system may still function, but understanding who can change what, and how that change propagates, becomes increasingly difficult under pressure.

## Reversibility Cost

### Plain-language definition

The system remains functional, but changes become harder to undo safely as hidden dependencies, state, and operational assumptions accumulate.

### What operators usually experience

- Rollback paths technically exist, but are operationally risky or expensive.
- Emergency fixes become part of the long-term environment.
- Teams avoid reverting because they no longer trust what else the change is entangled with.

### Common signals

- Safer rollback paths becoming less practical over time.
- Security or traffic-management controls that are hard to tune without fear of collateral damage.
- Deployments that are easy to advance but painful to unwind.

### Example incident types

- GitOps promotion flows that move forward cleanly but are hard to reverse under pressure.
- WAF or seccomp changes where safe rollout behavior is poorly understood.
- Config or runtime choices that quietly increase the blast radius of future change.

### Why debugging becomes expensive

The cost of “just undo it” rises over time, so teams spend more energy reasoning about unintended consequences than correcting the original problem.
