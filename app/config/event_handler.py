from typing import NoReturn

from di import DIContainer, DI
from fastapi import FastAPI

from application.estimator import EstimatorApplicationService
from application.estimator.dpo import LoadEstimatorDpo
from config import AppConfig
from domain.model.dataset import DatasetStorageService
from domain.model.image import ImageService
from port.adapter.service.dataset import DatasetStorageServiceImpl
from port.adapter.service.dataset.adapter import DatasetStorageAdapter
from port.adapter.service.dataset.adapter.local import LocalDatasetStorageAdapter
from port.adapter.service.image import ImageServiceImpl


class EventHandler:
    def startup(self) -> NoReturn:
        di_list = [
            DI.of(DatasetStorageAdapter, {}, LocalDatasetStorageAdapter),
            DI.of(DatasetStorageService, {}, DatasetStorageServiceImpl),
            DI.of(ImageService, {}, ImageServiceImpl),
        ]
        [DIContainer.instance().register(di) for di in di_list]

    def shutdown(self) -> NoReturn:
        pass


class ServeEventHandler(EventHandler):
    def __init__(self, app: FastAPI):
        self.__app = app

    def startup(self) -> NoReturn:
        super().startup()
        dpo: LoadEstimatorDpo = DIContainer.instance() \
            .resolve(EstimatorApplicationService) \
            .load(AppConfig.instance().artifact_path())

        self.__app.state.estimator = dpo.estimator
        self.__app.state.vectorizer = dpo.vectorizer

    def shutdown(self) -> NoReturn:
        super().shutdown()
        self.__app.state.estimator = None
        self.__app.state.vectorizer = None
