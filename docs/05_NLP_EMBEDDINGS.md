# Stage 5 — Payment Exceptions: Text, Embeddings and Retrieval

> Reconstructed candidate brief from the public mission, data dictionary, embedding pipeline, and starter interfaces. This is a candidate task, not a recovered original or a solution.

## Objective

Classify payment exception messages, compare sparse and dense text representations, retrieve relevant historical examples, and escalate uncertain cases to a human operator. This operational NLP path is separate from authorization risk scoring.

## Inputs and interfaces

- `payment_exception_messages.csv`: **18,000 English-only** messages across nine classes, with timestamps, payment rail, source system, text, target, and a future resolution note.
- `payment_exception_embeddings.csv`: `message_id` and **32** embedding columns, `emb_00` through `emb_31`.
- `artifacts/text_embedding_pipeline.joblib`: fixed encoder for new messages, produced by `src/embedding_pipeline.py`.

```python
def train_text_baselines(messages: pd.DataFrame, embeddings: pd.DataFrame):
    ...

def classify_with_abstention(model, X, threshold: float):
    ...

def retrieve_similar(query_vector: np.ndarray, index_vectors: np.ndarray,
                     index_ids: list[str], k: int = 3):
    ...
```

Document return structures. Classification with abstention must expose predicted class, a defined confidence score, and a human-escalation flag. Retrieval must return example IDs and similarity scores in ranked order.

## Tasks

1. Audit class support and join messages to embeddings **by `message_id`**, checking uniqueness and coverage. Do not rely on CSV row order. Exclude the target and future `resolution_note` from prediction inputs.
2. Use a chronological comparison: messages before **2026-07-01** for training, July for validation, and August for the final test. These are reconstruction defaults chosen to align with the supplied encoder's training cutoff and the documented August shift. If you use an earlier training cutoff, refit all representation steps on that earlier training period; the bundled encoder would otherwise have seen future text.
3. Train an independent **TF-IDF + linear classifier** baseline and a classifier on the supplied **32D vectors**, using the same splits and evaluation examples. Fit the independent TF-IDF vocabulary and IDF on training text only.
4. Explain the representation accurately: the supplied vectors are normalized **character TF-IDF → truncated SVD** features, fitted on pre-July text without targets. They are not pretrained neural sentence embeddings. Dense features do not guarantee stronger performance or better semantics.
5. Compare macro-F1, per-class precision/recall/F1 and support, a confusion matrix, and a simple overall accuracy reference. Examine errors and format changes in August after the evaluation choices are fixed. If adding rail/source metadata, report it as a separate comparison so representation effects remain interpretable.
6. Implement abstention. Define confidence, select an escalation threshold using validation data, and report coverage, escalation rate, and quality on accepted cases together. If a classifier's native output is a margin, do not describe it as a calibrated probability; explain any confidence calibration procedure.
7. Implement top-k similarity retrieval against an index of eligible earlier examples. Exclude the query itself and messages not yet available at query time. Use an explicitly documented similarity measure; handle zero vectors, ties, small or empty indexes, and invalid dimensions or `k` values.
8. Show retrieval for a held-out query and for a **new English message** encoded with the supplied encoder. Explain how retrieved examples help an operator and what they cannot prove about correctness. Historical target labels or resolution notes may be displayed to an operator only if they were already available; they are not prediction inputs.

## Deliverable

An executed Stage 5 section with split/class support, both fitted baselines, a fair metric comparison, an abstention trade-off table, and retrieval examples. Include simple checks for ID alignment, dimensions, ranking, and exclusion of unavailable examples.

Discuss ambiguity, changing message formats, inference cost, and the trade-offs of replacing the offline encoder with a neural model. Required work must run **offline**, with no network calls or paid APIs; describing a neural alternative does not require downloading one.

**Follow-up:** How would you measure human-fallback quality and detect a new exception category without silently forcing it into an existing class?
