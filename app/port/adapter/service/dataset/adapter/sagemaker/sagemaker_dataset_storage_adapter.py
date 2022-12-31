from pathlib import Path
from typing import Union

import numpy as np
import pandas as pd

from port.adapter.service.dataset.adapter import DatasetStorageAdapter


class SagemakerDatasetStorageAdapter(DatasetStorageAdapter):
    def load(self, path: Path) -> Union[pd.DataFrame, np.ndarray]:
        pass
