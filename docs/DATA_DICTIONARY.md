# Data Dictionary / Availability

## Gateway events: `transactions_live.csv`

| Column | Description | Available at pre-route risk decision? |
|---|---|---|
| `event_id` | Gateway event/attempt ID; retries may repeat a transaction | Yes |
| `transaction_id` | Logical payment ID; may repeat in raw export | Yes |
| `created_at` | UTC payment event timestamp | Yes |
| `customer_id`, `merchant_id`, `device_id` | Identities | Yes |
| `amount`, `currency` | Requested principal and currency | Yes |
| `customer_country`, `ip_country` | Account home vs observed IP region | Yes |
| `payment_channel`, `card_network`, `card_present` | Payment context | Yes |
| `customer_tenure_days`, `historical_account_risk_score` | Existing features | Yes, under stated assumptions |
| `acquirer` | Historical router-selected action | No; it is not yet selected |
| `authorization_result`, `auth_latency_ms`, `fee_bps` | Realized authorization downstream of action | No |

## Outcomes: `labels_live.csv`

| Column | Description |
|---|---|
| `transaction_id` | Logical payment ID |
| `chargeback_flag` | 0/1 only where observed and mature, otherwise null |
| `chargeback_reported_at` | Delayed future outcome; forbidden pre-decision feature |
| `manual_review_result`, `final_payment_status`, `days_until_chargeback` | Downstream/post-resolution; forbidden pre-decision features |

Labels are extracted on `2026-10-05` with a **45-day maturity** convention. Underlying fraud outcomes on historically declined transactions cannot be assumed observed. This is selective-label bias.

## Merchant metadata: `merchants.csv`

`merchant_id`, `merchant_country`, `merchant_category`, `merchant_age_days`, `merchant_risk_tier`.

## Acquirer reference: `acquirer_reference.csv`

`acquirer`, `base_fee_bps`, `cross_border_surcharge_bps`, `base_approval_rate`, `mean_latency_ms`, `notes`. These are **synthetic illustrative priors**, not causal conditional approval estimates.

## Payment exception NLP: `payment_exception_messages.csv`

`message_id`, `created_at` (UTC), `payment_rail`, `source_system`, `exception_text` (English-only), `exception_type` (training target), `resolution_note` (future information, **not available at prediction time**).

There are nine exception classes. A subset of messages is intentionally ambiguous or sparsely diagnostic. August contains a shift in operational message formats and ambiguity.

## Embeddings: `payment_exception_embeddings.csv`

`message_id` plus `emb_00` … `emb_31`. These are normalized **text-derived TF-IDF/SVD vectors**, with train-period fit and fixed inference projection. They are not label-generated oracle embeddings and they are not neural Transformer embeddings. Encoder: `artifacts/text_embedding_pipeline.joblib` (Python scikit-learn; load only from this trusted repository). Do not fit preprocessing on validation/test data.
