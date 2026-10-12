"""Reproducible, label-free text-derived representations.

These 32-dimensional *SVD text embeddings* are not neural sentence embeddings.
The tokenizer, vocabulary, IDF and SVD are fit on training-period text only.
For a production semantic model replace this pipeline with a vetted encoder.
"""
from pathlib import Path
import argparse
import joblib
import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Normalizer

TRAIN_END = pd.Timestamp('2026-07-01T00:00:00Z')


def create_encoder(train_texts):
    encoder = Pipeline([
        ('tfidf', TfidfVectorizer(analyzer='char_wb', ngram_range=(3, 5),
                                  min_df=3, max_features=12000,
                                  sublinear_tf=True, dtype=np.float32)),
        ('svd', TruncatedSVD(n_components=32, n_iter=3, random_state=42)),
        ('norm', Normalizer()),
    ])
    encoder.fit(train_texts.fillna('').astype(str))
    return encoder


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--data-dir', type=Path, default=Path(__file__).resolve().parents[1] / 'data')
    p.add_argument('--artifact-dir', type=Path, default=Path(__file__).resolve().parents[1] / 'artifacts')
    args = p.parse_args()
    messages = pd.read_csv(args.data_dir / 'payment_exception_messages.csv', parse_dates=['created_at'])
    train = messages['created_at'] < TRAIN_END
    encoder = create_encoder(messages.loc[train, 'exception_text'])
    vector = encoder.transform(messages['exception_text'].fillna('').astype(str))
    out = pd.DataFrame(vector, columns=[f'emb_{i:02d}' for i in range(vector.shape[1])])
    out.insert(0, 'message_id', messages['message_id'])
    out.to_csv(args.data_dir / 'payment_exception_embeddings.csv', index=False)
    args.artifact_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(encoder, args.artifact_dir / 'text_embedding_pipeline.joblib', compress=3)
    print(f'Generated {len(out)} embeddings, fitted on {int(train.sum())} training messages.')


if __name__ == '__main__':
    main()
