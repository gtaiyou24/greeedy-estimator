from dataclasses import dataclass

from sklearn.feature_extraction.text import CountVectorizer

from domain.model.estimator import Estimator


@dataclass(unsafe_hash=True, frozen=True)
class LoadEstimatorDpo:
    estimator: Estimator
    vectorizer: CountVectorizer
