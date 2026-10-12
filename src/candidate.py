"""VP Payments interview starter — implement incrementally.

From the repository root, run:
    python src/data_smoke.py
    pytest -q tests/test_public_data.py
    pytest -q tests/test_public_features.py  # fails until Stage 2 is implemented

See docs/ for exact contracts. AI assistance is permitted; validate its results.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / 'data'


def load_data():
    """Load gateway, label, merchant and acquirer data."""
    transactions = pd.read_csv(DATA_DIR / 'transactions_live.csv', parse_dates=['created_at'])
    labels = pd.read_csv(DATA_DIR / 'labels_live.csv', parse_dates=['chargeback_reported_at'])
    merchants = pd.read_csv(DATA_DIR / 'merchants.csv')
    acquirers = pd.read_csv(DATA_DIR / 'acquirer_reference.csv')
    return transactions, labels, merchants, acquirers


def audit_data(transactions: pd.DataFrame, labels: pd.DataFrame) -> dict:
    """Stage 1: return a useful, auditable overview. Explain choices orally."""
    raise NotImplementedError('Stage 1')


def build_online_features(transactions: pd.DataFrame) -> pd.DataFrame:
    """Stage 2: strictly earlier, deduplicated, time-windowed customer features.

    Requirements and equal-timestamp semantics are in docs/02_ONLINE_FEATURES.md.
    """
    raise NotImplementedError('Stage 2')


def split_by_time(frame: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Stage 3: train/validation/test split."""
    raise NotImplementedError('Stage 3')


def train_chargeback_baseline(features_and_labels: pd.DataFrame):
    """Stage 3: risk baseline, with metrics."""
    raise NotImplementedError('Stage 3')


def choose_actions(probabilities: np.ndarray, amounts: np.ndarray,
                   max_review_rate: float = 0.015) -> np.ndarray:
    """Stage 4: choose APPROVE, REVIEW, or BLOCK under a review-capacity bound."""
    raise NotImplementedError('Stage 4')


def train_text_baselines(messages: pd.DataFrame, embeddings: pd.DataFrame):
    """Stage 5: sparse TF-IDF and dense-embedding classifiers and comparison."""
    raise NotImplementedError('Stage 5')


def classify_with_abstention(model, X, threshold: float):
    """Stage 5: class / confidence / human-fallback output."""
    raise NotImplementedError('Stage 5')


def retrieve_similar(query_vector: np.ndarray, index_vectors: np.ndarray,
                     index_ids: list[str], k: int = 3):
    """Stage 5: k most similar indexed examples."""
    raise NotImplementedError('Stage 5')


def choose_acquirer(transaction: dict, acquirer_reference: pd.DataFrame) -> str:
    """Stage 6: pick an acquirer for a new payment."""
    raise NotImplementedError('Stage 6')


if __name__ == '__main__':
    tx, labels, merchants, acquirers = load_data()
    print(f'Starter loaded {len(tx):,} raw gateway events and {len(labels):,} label rows.')
    print('Choose a stage from docs/ and implement the relevant functions.')
