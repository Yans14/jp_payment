# Stage 6 — Smart Acquirer Routing

> Reconstructed candidate brief from the public mission, acquirer reference, and starter interface. Routing costs and causal limitations must be stated explicitly; no original hidden scoring criteria are available.

## Objective

Propose an acquirer choice for a new payment, balancing approval probability, fees, latency, and operational availability. Explain how historical routing policy limits what you can learn from its outcomes.

## Inputs and interface

Use pre-route payment context, the gateway history for offline analysis, and `acquirer_reference.csv`.

```python
def choose_acquirer(transaction: dict, acquirer_reference: pd.DataFrame) -> str:
    ...
```

Return an acquirer identifier from the supplied reference for a valid payment with an eligible route. Document behavior when no route is eligible or required inputs are invalid. The final notebook should demonstrate a **pre-route** input dictionary; the starter's raw exported row also contains downstream fields that must not drive the decision.

The reference contains `base_fee_bps`, `cross_border_surcharge_bps`, `base_approval_rate`, and `mean_latency_ms`. These are fictional illustrative priors. In particular, `base_approval_rate` is not an estimated causal approval probability conditional on a particular payment.

## Tasks

1. Define an understandable objective and any constraints. State how you trade payment value, approval, fees, and latency; identify missing information such as route eligibility, settlement currency, cross-border definitions, contractual fee rules, and live health signals.
2. Build a deterministic baseline router using the reference and fields available when choosing the route. Document business assumptions, unit conversions between basis points and monetary fees, and tie-breaking. Distinguish scenario scores based on reference priors from learned conditional estimates.
3. Demonstrate decisions for several payment contexts. Explain fee and latency trade-offs and how a route would be excluded during an outage. Health or eligibility inputs absent from this dataset must be described as assumptions or simulated inputs, not observed facts.
4. Summarize historical routing by relevant payment segments and by acquirer, with counts as well as approval/latency/fee summaries. State how retries affect the unit of analysis and how you prevent double-counting logical payments.
5. Explain **historical-policy confounding**: different acquirers may receive different payment populations. A higher observed approval rate does not establish that switching every payment to that acquirer would improve outcomes.
6. Identify missing counterfactual information. The dataset does not include logged action propensities or all route-specific potential outcomes. Explain why counterfactual policy value cannot be asserted from naive replay or the reference priors. If proposing off-policy evaluation, state the logging, overlap, and identification assumptions it would require.
7. Propose a controlled validation plan with eligibility controls, risk guardrails, sufficient traffic coverage, and rollback criteria before making a production-uplift claim.

## Deliverable

An executed Stage 6 section with the baseline routing function, explicit objective/assumptions, example decisions and checks, a descriptive historical comparison, and a clear account of which claims the available data can support.

Include behavior for an unavailable route, no eligible routes, invalid amounts or missing context, and equal scores. Do not use `authorization_result`, realized `auth_latency_ms` or realized `fee_bps` as inputs for the payment being routed.

**Follow-up:** A timeout leaves the authorization outcome unknown. How should routing retries avoid creating a second charge, and when is reconciliation preferable to immediate rerouting?
