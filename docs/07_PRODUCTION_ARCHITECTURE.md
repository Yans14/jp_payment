# Stage 7 — Fault-Tolerant, Low-Latency Production Architecture

> Reconstructed candidate brief from the public mission, Stage 2 scaling follow-up, and final handoff template. Numerical service targets beyond those already published are design assumptions, not recovered interviewer requirements.

## Objective

Defend a production design for authorization risk and acquirer routing, plus a separate operational path for payment exception classification, retrieval, and human escalation. Prioritize correctness under failure and a clear latency budget.

## Scenario and scope

Use the Stage 2 follow-up of **50,000 requests/second** and events arriving up to **90 seconds late** as a capacity discussion scenario. Clarify peak versus sustained load, region/tenant distribution, and availability goals. No implementation or load test at this scale is required for this stage.

The repository does not define an end-to-end latency SLO, infrastructure vendor, storage platform, or complete failure policy. Choose defensible assumptions and make them visible. Required notebook work remains offline.

## Design discussion

1. Draw the request and event flows. Identify the synchronous authorization critical path: request validation, historical feature lookup, risk scoring, approve/review/block policy, route selection where applicable, and the acquirer interaction. Show which work is asynchronous.
2. Define event identity, payment identity, idempotency, deduplication, and the state transitions for retries. Explain what the caller receives after a timeout with an unknown external outcome and how reconciliation prevents a duplicate financial effect.
3. Describe the online feature state and the historical training path. Address customer partitioning, equal timestamps, late/out-of-order events, window expiry, retention, and replay. Explain how serving availability and event-time correctness interact; a historical replay must not pretend late data was available to a past live decision.
4. Allocate a latency budget to each dependency, distinguish service compute time from external acquirer time, and discuss tail latency, throughput, backpressure, and saturation. Include request deadlines and bounded retries.
5. Explain behavior when features are stale or missing, the model is unavailable, the policy service times out, an acquirer fails, or the human-review queue is full. State who owns fail-open, fail-safe, or guarded-fallback choices and how duplicate side effects are prevented during recovery.
6. Describe model and policy deployment: versioned artifacts and feature schemas, reproducible training data, compatibility checks, shadow evaluation, canaries, rollback, and audit trails linking an action to its inputs, versions, and configuration.
7. Place payment-exception NLP, the historical retrieval index, and operator escalation on their own operational path. Explain index freshness, confidence thresholds, human feedback, and access controls without adding this work to the authorization latency budget.
8. Define monitoring for request success and p95/p99 latency; feature freshness/missingness; score and action distributions; review capacity; per-acquirer outcomes; NLP coverage and errors; and delayed mature-label risk performance. Explain which measurements are immediately available and which require waiting for labels.
9. Cover payment-data privacy, tenant isolation, access controls, retention, and redaction of sensitive information in logs and operator views. Describe recovery, replay, and reconciliation after a regional or state-store failure.

## Deliverable

Add a diagram and a concise design narrative to Stage 7 of `payments_case_notebook.ipynb`. Include:

- chosen load/SLO assumptions and a per-hop latency budget;
- online versus offline boundaries and the separate NLP path;
- a small failure table mapping dependency failure to response, recovery, and monitoring;
- deployment and rollback criteria, plus the most important unresolved trade-offs.

Finish the candidate summary in [`08_FINAL_HANDOFF.md`](08_FINAL_HANDOFF.md) and deliver a **2–3-minute** explanation. Be explicit about which earlier stages you implemented and which are proposed designs.

**Follow-up:** Which guarantees apply only inside your event-processing system, and which require an idempotency or reconciliation contract with an external acquirer?
