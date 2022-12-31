from pathlib import Path
from typing import NoReturn

from injector import singleton


@singleton
class MakeDatasetApplicationService:
    def make(self, dataset_path: Path) -> NoReturn:
        pass
