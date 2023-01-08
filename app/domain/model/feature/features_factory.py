from typing import Any, Dict, Tuple, List

import numpy as np
import pandas as pd

from domain.model.feature import Feature


class FeaturesFactory:
    def __init__(self, feature_dict: Dict[str, Feature]):
        self.__columns = list(feature_dict.keys())
        self.__feature_dict = feature_dict

    def make(self, dataset: pd.DataFrame) -> Tuple[np.ndarray, List[int]]:
        index: list[int] = []
        features: list[list[Any]] = []
        for i, arr in enumerate(dataset[self.__columns].values):
            try:
                features.append([self.__feature_of(j, value) for j, value in enumerate(arr)])
                index.append(i)
            except Exception:
                continue

        return np.array(features, dtype=object), index

    def __feature_of(self, j: int, value: Any) -> Any:
        column_name = self.__columns[j]
        return self.__feature_dict[column_name].of(value)
