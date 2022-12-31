import abc
from pathlib import Path
from typing import Union

import numpy as np
import pandas as pd


class DatasetStorageAdapter(abc.ABC):
    def load(self, full_path: Path) -> Union[pd.DataFrame, np.ndarray]:
        pass
