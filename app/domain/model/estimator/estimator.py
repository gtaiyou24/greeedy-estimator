from __future__ import annotations

import abc
from typing import NoReturn

import numpy as np


class Estimator(abc.ABC):
    @abc.abstractmethod
    def name(self) -> str:
        pass

    @abc.abstractmethod
    def version(self) -> float:
        pass

    @abc.abstractmethod
    def fit(self, X, Y) -> NoReturn:
        pass

    @abc.abstractmethod
    def predict(self, X) -> np.ndarray:
        pass
