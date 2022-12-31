from dataclasses import dataclass

from sklearn.feature_extraction.text import CountVectorizer

from domain.model.estimator import Estimator


@dataclass(unsafe_hash=True, frozen=True)
class PredictCommand:
    @dataclass(unsafe_hash=True, frozen=True)
    class Item:
        name: str
        image_url: str

    items: list[Item]
    option_colors: set[str]
    estimator: Estimator
    vectorizer: CountVectorizer