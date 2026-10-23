# Stage 4 — Approve / Review / Block Policy

> Reconstructed candidate brief from the public repository. Original business-cost values are unavailable; state your assumptions rather than presenting invented values as interviewer requirements.

## Objective

Turn chargeback probabilities into **APPROVE**, **REVIEW**, or **BLOCK** decisions under business costs and limited review capacity. Separate model discrimination from the value of the resulting policy.

## Interface

```python
def choose_actions(probabilities: np.ndarray, amounts: np.ndarray,
                   max_review_rate: float = 0.015) -> np.ndarray:
    ...
```

Inputs are aligned, one-dimensional arrays for logical payments. Return one action string per input, in the same order. The default review-rate ceiling is **1.5%**, as specified by the starter signature. Keep this interface; put any additional policy configuration in a documented notebook configuration or fitted policy object used by the function.

## Tasks

1. Define a cost or value model for each action and outcome. Specify assumptions about chargeback loss, legitimate-payment value or false-decline cost, review operating cost, and review effectiveness. State whether review delays or residual loss matter.
2. Explain the monetary unit of every term. `amount` is principal in the payment's `currency`; the interface does not receive currency or an FX table. Document an explicit currency-normalization or same-unit simulation assumption before aggregating monetary values. The repository does not supply conversion rates or a complete business-cost model.
3. Derive and implement an action policy using probabilities and payment amounts. Explain which assumptions allow the Stage 3 probabilities to support your loss calculation, and how probability miscalibration affects the result.
4. Treat `max_review_rate` as a hard bound for the supplied batch: the number of REVIEW actions must not exceed `floor(max_review_rate * n)`. Define deterministic tie behavior. Explain how a batch allocation would become a live queue or per-period quota when future arrivals are unknown.
5. Choose policy parameters and thresholds using validation data and declared business assumptions only. Freeze them before reporting test results. Applying a fixed capacity-allocation rule to test scores is allowed; tuning it against test labels is not.
6. Compare the chosen policy with transparent reference policies, such as approve-all and a simple risk-threshold rule, on the same eligible evaluation population.
7. Explain what can be evaluated from observed labels and what depends on unobserved counterfactuals. Historical review outcomes do not directly reveal what your new review policy would achieve.

Report a compact table:

| Policy / split | APPROVE share | REVIEW share | BLOCK share | Modeled cost or value | Key assumptions |
|---|---|---|---|---|---|
| Validation | | | | | |
| Test | | | | | |

Label monetary results as **modeled offline estimates**, with a sensitivity analysis for important unknown costs or review effectiveness. Do not claim realized causal savings.

## Verification and deliverable

Show small explicit checks for capacity rounding, empty inputs, invalid probabilities or mismatched arrays, ties, and extreme probabilities/amounts. State your input-validation behavior.

Submit an executed Stage 4 section containing the cost assumptions, policy, capacity checks, validation selection procedure, and test comparison. No particular cost values or optimal thresholds can be recovered from the public repository.

**Follow-up:** What happens during a review backlog, and which policy controls should be available without retraining the risk model?
