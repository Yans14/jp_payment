# Candidate Interview Overview

## Scenario

You are the VP AI/ML lead for a fictional payments platform. Your system processes authorization requests, observes downstream chargeback outcomes with delay, and receives operational exception messages. Design the offline evaluation and production decision path. The business wants to improve payment performance while controlling financial and operational risk.

## Rules

- Language: **English only**.
- Python 3; `pandas`, `numpy`, `scikit-learn` allowed.
- AI coding assistant allowed. Explain what it produced and how you checked it.
- You may ask for clarifications. Declare assumptions when unspecified.
- Avoid leakage and unsupported causal claims.
- You do not need to finish every stage; communicate your trade-offs.

## Stages / suggested allocation

| Stage  |
|---|
| 1. Data audit |
| 2. Online features | 
| 3. Risk model | 
| 4. Decision policy | 
| 5. NLP + embeddings | 
| 6. Acquirer routing | 
| 7. Production architecture |

## Final submission

Submit `payments_case_notebook.ipynb` executed top to bottom with outputs (one section per stage, AI assistant log filled in). Present the code, your chosen train/validation/test boundaries, a table of offline metrics with observed class support, explicit limitations, and a 2–3-minute architecture explanation.
