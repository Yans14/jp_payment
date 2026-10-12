"""Stage 2 contract tests: fail until candidate builds online features."""
import numpy as np
import pandas as pd
import pytest
from candidate import build_online_features


def sample_events():
    rows = [
        ['E1', 'T1', '2026-06-01T10:00:00Z', 'C1', 'M1', 'D1', 10, 'GB'],
        ['E2', 'T2', '2026-06-01T10:00:00Z', 'C1', 'M2', 'D1', 20, 'FR'],
        ['E3', 'T3', '2026-06-01T10:05:00Z', 'C1', 'M3', 'D1', 30, 'FR'],
        ['E4', 'T4', '2026-06-01T11:05:00Z', 'C1', 'M1', 'D2', 40, 'US'],
        ['E5', 'T5', '2026-06-01T10:05:00Z', 'C2', 'M2', 'D9', 9, 'GB'],
        ['E_RETRY', 'T1', '2026-06-01T10:00:00Z', 'C1', 'M1', 'D1', 10, 'GB'],
    ]
    frame = pd.DataFrame(rows, columns=['event_id', 'transaction_id', 'created_at',
                                        'customer_id', 'merchant_id', 'device_id', 'amount', 'ip_country'])
    frame['created_at'] = pd.to_datetime(frame['created_at'], utc=True)
    return frame


def test_strictly_prior_same_timestamp_and_retries():
    f = build_online_features(sample_events()).set_index('transaction_id')
    assert len(f) == 5
    assert f.loc['T1', 'customer_txn_count_10m'] == 0
    assert f.loc['T2', 'customer_txn_count_10m'] == 0
    assert f.loc['T3', 'customer_txn_count_10m'] == 2
    assert f.loc['T3', 'customer_amount_sum_1h'] == pytest.approx(30.0)
    assert f.loc['T3', 'customer_unique_merchants_24h'] == 2
    assert f.loc['T3', 'seconds_since_customer_prev_txn'] == pytest.approx(300)
    assert f.loc['T3', 'device_seen_before'] == 1
    assert f.loc['T5', 'customer_txn_count_10m'] == 0


def test_exact_window_boundary_and_first_observation():
    f = build_online_features(sample_events()).set_index('transaction_id')
    assert f.loc['T4', 'customer_txn_count_10m'] == 0
    assert f.loc['T4', 'customer_amount_sum_1h'] == pytest.approx(0.0)
    assert f.loc['T4', 'customer_unique_merchants_24h'] == 3
    assert f.loc['T4', 'device_seen_before'] == 0
    assert np.isnan(f.loc['T1', 'seconds_since_customer_prev_txn'])
    assert f.loc['T1', 'ip_country_changed_from_prev_txn'] == 0
    assert f.loc['T4', 'ip_country_changed_from_prev_txn'] == 1


def test_shuffled_input_does_not_change_results():
    df = sample_events()
    a = build_online_features(df).set_index('transaction_id').sort_index()
    b = build_online_features(df.sample(frac=1, random_state=144)).set_index('transaction_id').sort_index()
    cols = ['customer_txn_count_10m', 'customer_amount_sum_1h',
            'customer_unique_merchants_24h', 'seconds_since_customer_prev_txn',
            'device_seen_before', 'ip_country_changed_from_prev_txn']
    pd.testing.assert_frame_equal(a[cols], b[cols])
