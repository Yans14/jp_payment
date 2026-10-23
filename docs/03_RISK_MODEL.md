# Stage 3 — Chargeback Risk Modeling

> Reconstructed candidate brief from the public repository. The original interviewer brief is not included in Git history. Requirements below make the published mission and starter functions actionable; they are not an answer key.

## Objective

Train and evaluate an imbalanced chargeback-risk baseline for a payment scored **before acquirer selection**. State precisely which population its probability describes.

## Inputs and interface

Use the logical-payment features from Stage 2, `labels_live.csv`, and, if useful, merchant metadata. The final implementation belongs in `payments_case_notebook.ipynb`; `src/candidate.py` is an optional prototyping aid.

```python
def split_by_time(frame: pd.DataFrame) -> dict[str, pd.DataFrame]:
    ...

def train_chargeback_baseline(features_and_labels: pd.DataFrame):
    ...
```

Return `train`, `validation`, and `test` frames from `split_by_time`. Choose and document the result structure for `train_chargeback_baseline`, including the fitted preprocessing/model, metrics, and held-out probabilities keyed by `transaction_id` for Stage 4.

The notebook currently calls the training function with the Stage 2 feature frame. Join labels inside the function or explicitly prepare the joined frame at the call site. Check join cardinality so one logical payment remains one row.

## Tasks

1. Define the target and eligible label population. Use the extraction date **2026-10-05** and **45-day** maturity convention from the repository. Missing, immature, and unobservable outcomes must not silently become negative labels.
2. Select chronological train/validation/test boundaries and explain their purpose. Keep retries of a logical payment in the same decision unit. Do not randomly split individual gateway events.
3. Distinguish a retrospective benchmark at extraction time from a model that could actually have been trained at a historical deployment date. For an as-of simulation, training labels must have been available at its fitting date; explain label delays and any gaps between fitting, policy selection, and evaluation.
4. Restrict model inputs to fields available before routing. Fit imputers, categorical encoders, scaling, feature selection, and any resampling on training data only. State assumptions about the historical availability of merchant and account features.
5. Build a simple, reproducible baseline using the allowed Python stack. Explain how you handle class imbalance, unknown categories, and missing values. Compare with a no-skill reference.
6. Select model settings using development data. Keep test data untouched until the model and evaluation procedure are fixed. If probabilities will drive monetary decisions, assess their calibration and describe how any calibration is fitted without test leakage.
7. Report discrimination and probability quality: average precision or a clearly defined PR-AUC, ROC-AUC where defined, and a calibration diagnostic such as Brier score or a reliability plot. Include a threshold-based result with the threshold chosen without test data.

For every split, report:

| Split | Event-time range | Eligible payments | Positive labels | Positive rate |
|---|---|---|---|---|
| Train | | | | |
| Validation | | | | |
| Test | | | | |

If a split has no positive or no negative examples, show that support and mark undefined metrics explicitly. Discuss uncertainty when class support is small.

## Deliverable

An executed Stage 3 section with the target definition, feature list, temporal boundaries, label-availability assumptions, fitted baseline, validation/test metric table, and saved held-out scores. Explain why performance on observed historical outcomes does not establish performance on historically declined payments or production uplift.

**Follow-up:** How would you monitor delayed-label performance after deployment, and what evidence would justify replacing this baseline?
