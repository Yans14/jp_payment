"""These should pass before the interview; they don't require candidate code."""
from pathlib import Path
import pandas as pd
import numpy as np
import joblib

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / 'data'


def test_data_integrity():
    tx = pd.read_csv(D / 'transactions_live.csv')
    labels = pd.read_csv(D / 'labels_live.csv')
    assert tx.event_id.is_unique
    assert tx.transaction_id.nunique() == len(labels)
    assert labels.transaction_id.is_unique
    assert tx.transaction_id.duplicated().any()  # gateway retries are deliberate
    assert labels.chargeback_flag.isna().any()  # censoring is deliberate


def test_text_and_vectors_match_by_id():
    m = pd.read_csv(D / 'payment_exception_messages.csv')
    v = pd.read_csv(D / 'payment_exception_embeddings.csv')
    assert m.message_id.is_unique and v.message_id.is_unique
    assert set(m.message_id) == set(v.message_id)
    assert len([c for c in v.columns if c.startswith('emb_')]) == 32
    assert m.exception_text.notna().all()
    assert len(m.exception_type.unique()) == 9


def test_encoder_can_embed_new_message():
    encoder = joblib.load(ROOT / 'artifacts' / 'text_embedding_pipeline.joblib')
    z = encoder.transform(['Wire transfer cannot be routed to receiving bank'])
    assert z.shape == (1, 32)
    assert np.isfinite(z).all()
