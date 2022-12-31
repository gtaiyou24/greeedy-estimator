from pathlib import Path
from typing import NoReturn

from di import DIContainer

from application.estimator import EstimatorApplicationService
from config import EventHandler


def run(dataset_path: Path, artifact_path: Path) -> NoReturn:
    handler = EventHandler()
    handler.startup()

    application_service = DIContainer.instance().resolve(EstimatorApplicationService)
    application_service.train(dataset_path, artifact_path)

    handler.shutdown()
