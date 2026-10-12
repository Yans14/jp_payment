# VP Applied AI/ML — Payments Engineering Case

**Technical interview | Python | AI coding assistants allowed**

## Mission

Design and implement a data-to-decision payment intelligence system:

1. Audit payment gateway events and downstream outcomes.
2. Build leakage-safe, strictly historical customer features.
3. Train and evaluate an imbalanced chargeback-risk baseline.
4. Optimize approve / review / block decisions under business costs and review capacity.
5. Classify unstructured payment exceptions with sparse text and 32D text-derived embeddings; implement similarity retrieval and human escalation.
6. Design smart-acquirer routing and identify historical-policy confounding.
7. Defend a fault-tolerant low-latency architecture.

This case is intentionally too broad to finish every stage in a 75–90-minute interview. Prioritize correctness, explicit assumptions, verification, and quality of discussion over implementing every feature. The interviewer releases stages progressively.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/data_smoke.py
pytest -q tests/test_public_data.py
jupyter lab payments_case_notebook.ipynb
```

**Your deliverable is [`payments_case_notebook.ipynb`](payments_case_notebook.ipynb).** It is self-contained (no imports from `src/`), has one section per stage, and embeds the public Stage 2 contract checks. It must run top to bottom with *Restart & Run All*; unfinished stages are reported as "not implemented" instead of stopping the run. Submit it with outputs.

The data smoke test should pass immediately. `src/candidate.py` and `tests/test_public_features.py` remain available if you prefer to prototype in a module, but the final functions must live in the notebook.

## Candidate docs

- [`docs/00_INTERVIEW_OVERVIEW.md`](docs/00_INTERVIEW_OVERVIEW.md): timing, deliverables, AI rules
- [`docs/01_DATA_AUDIT.md`](docs/01_DATA_AUDIT.md)
- [`docs/02_ONLINE_FEATURES.md`](docs/02_ONLINE_FEATURES.md)
- Stages 3–7: released by the interviewer during the session
- [`docs/DATA_DICTIONARY.md`](docs/DATA_DICTIONARY.md)
- [`docs/08_FINAL_HANDOFF.md`](docs/08_FINAL_HANDOFF.md): final presentation template

## Data included

| Filename | Purpose |
|---|---|
| `data/transactions_live.csv` | Gateway events; unsorted, includes retries, historical routing outcomes |
| `data/labels_live.csv` | Delayed outcomes with missing/unobservable labels |
| `data/merchants.csv` | Merchant metadata |
| `data/acquirer_reference.csv` | Fictional acquirer economics and baseline statistics |
| `data/payment_exception_messages.csv` | **18,000 English-only** payment exception messages and labels |
| `data/payment_exception_embeddings.csv` | **32D text-derived embeddings** keyed by message ID |
| `artifacts/text_embedding_pipeline.joblib` | Reusable training-period-only text encoder for new messages |

**Important embedding disclosure:** The bundled 32D vectors are **TF-IDF + truncated SVD embeddings**, *not* pretrained neural sentence embeddings. The projection is fit using **only messages prior to 2026-07-01, without targets**, and then applied to all dates. This makes the case fully offline/reproducible and gives you a way to encode new text. Compare against an independent TF-IDF baseline and discuss trade-offs with a real neural encoder. Do not assume better performance just because a representation is dense.

## Interview-safe constraints

- Treat `2026-10-05` as the dataset extraction date and `45 days` as chargeback-label maturity.
- Risk decisions happen **before routing**; downstream fields are unavailable at this point.
- Datasets are synthetic, sampled and do not represent bank-level real-world prevalence or expected production uplift.
- Candidate may ask AI assistants for code, architecture or debugging help, but must explain and validate the output.
- Do not use network calls or paid APIs for the required tasks.

## Repository hygiene

Never add interviewer answer keys, hidden tests or scoring notes to this repository. Those are distributed **separately** to the interviewer.
