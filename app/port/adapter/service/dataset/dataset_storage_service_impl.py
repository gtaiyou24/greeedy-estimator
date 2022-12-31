from pathlib import Path
from typing import Union

import numpy as np
import pandas as pd
from injector import inject

from domain.model.dataset import DatasetStorageService
from port.adapter.service.dataset.adapter import DatasetStorageAdapter


class DatasetStorageServiceImpl(DatasetStorageService):
    @inject
    def __init__(self, adapter: DatasetStorageAdapter):
        self.__adapter = adapter

    def load(self, full_path: Path) -> Union[pd.DataFrame, np.ndarray]:
        return self.__adapter.load(full_path)
