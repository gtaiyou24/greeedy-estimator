from pathlib import Path
from typing import Union

import numpy as np
import pandas as pd
from slf4py import set_logger

from port.adapter.service.dataset.adapter import DatasetStorageAdapter


@set_logger
class LocalDatasetStorageAdapter(DatasetStorageAdapter):
    def load(self, full_path: Path) -> Union[pd.DataFrame, np.ndarray]:
        self.log.debug('loading {} ...'.format(full_path))
        return pd.read_csv(full_path)
