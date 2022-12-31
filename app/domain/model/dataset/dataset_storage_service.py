import abc
from pathlib import Path
from typing import Union

import numpy as np
import pandas as pd


class DatasetStorageService(abc.ABC):
    @abc.abstractmethod
    def load(self, full_path: Path) -> Union[pd.DataFrame, np.ndarray]:
        pass
