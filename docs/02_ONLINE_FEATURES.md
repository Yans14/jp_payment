# Stage 2 — Real-Time Feature Engineering

Implement in `src/candidate.py`:

```python
def build_online_features(transactions: pd.DataFrame) -> pd.DataFrame:
    ...
```

For each **unique logical payment** produce:

- `customer_txn_count_10m`: number of earlier transactions from the customer within 10 minutes;
- `customer_amount_sum_1h`: previous customer amount total within 1 hour;
- `customer_unique_merchants_24h`: distinct earlier merchant IDs within 24 hours;
- `seconds_since_customer_prev_txn`: seconds since the most recent strictly earlier customer transaction (`NaN` if none);
- `device_seen_before`: `1` iff this customer's device appeared strictly earlier, otherwise `0`;
- `ip_country_changed_from_prev_txn`: `1` if IP country differs from the most recent earlier payment's IP country, otherwise `0` (`0` if none).

### Required semantics

- Output has **one row per logical `transaction_id`** and retains pre-decision fields.
- The gateway export is unsorted and contains retry events.
- **Strictly before** means events with the exact same customer and timestamp **must not see each other**.
- Window semantics: `(current_timestamp - window, current_timestamp)` (exclusive on both ends). A payment exactly at the left boundary is excluded.
- Avoid quadratic scans; target approximately linearithmic complexity using time-ordered state.
- Use event timestamps in UTC; explain behavior for out-of-order arrival in production.

Write tests for: first transaction, exact time boundary, same-time different logical payments, gateway retries, input-order invariance, cross-customer isolation.

**Follow-up:** What changes for 50,000 requests/s and events arriving 90 seconds late?
