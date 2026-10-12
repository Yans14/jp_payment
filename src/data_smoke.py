"""Read-only sanity checks; pass without implementing the interview."""
from pathlib import Path
import pandas as pd
import joblib

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / 'data'


def main():
    tx = pd.read_csv(D / 'transactions_live.csv')
    labels = pd.read_csv(D / 'labels_live.csv')
    merchants = pd.read_csv(D / 'merchants.csv')
    routes = pd.read_csv(D / 'acquirer_reference.csv')
    messages = pd.read_csv(D / 'payment_exception_messages.csv')
    emb = pd.read_csv(D / 'payment_exception_embeddings.csv')
    assert tx['transaction_id'].nunique() == len(labels)
    assert len(merchants) > 0 and len(routes) > 0
    assert messages['message_id'].is_unique and emb['message_id'].is_unique
    assert messages['message_id'].sort_values().reset_index(drop=True).equals(
        emb['message_id'].sort_values().reset_index(drop=True))
    assert len([x for x in emb.columns if x.startswith('emb_')]) == 32
    encoder = joblib.load(ROOT / 'artifacts' / 'text_embedding_pipeline.joblib')
    assert encoder.transform(['Payment held for sanctions screening']).shape == (1, 32)
    print(f'PASS: {len(tx):,} gateway events, {len(labels):,} labels, '
          f'{len(messages):,} English exception messages and 32-dimensional text embeddings.')


if __name__ == '__main__':
    main()
