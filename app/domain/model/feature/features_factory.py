from typing import Any

import numpy as np
import pandas as pd
from tqdm import tqdm

from domain.model.feature import Feature


class FeaturesFactory:
    def __init__(self, feature_dict: dict[str, Feature]):
        self.__columns = list(feature_dict.keys())
        self.__feature_dict = feature_dict

    def make(self, dataset: pd.DataFrame) -> tuple[np.ndarray, list[int]]:
        index: list[int] = []
        features: list[list[Any]] = []
        for i, arr in tqdm(enumerate(dataset[self.__columns].values)):
            try:
                features.append([self.__feature_of(j, value) for j, value in enumerate(arr)])
                index.append(i)
            except Exception:
                continue

        return np.array(features), index

    def __feature_of(self, j: int, value: Any) -> Any:
        column_name = self.__columns[j]
        return self.__feature_dict[column_name].of(value)
