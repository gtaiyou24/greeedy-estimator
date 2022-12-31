from __future__ import annotations

from pathlib import Path
from typing import Optional


class AppConfig:
    __instance: Optional[AppConfig] = None

    def __init__(self, is_local: bool, artifact_path: Path):
        assert artifact_path is not None, 'モデルを格納しているアーティファクトパスが指定されていません。'
        self.__is_local = is_local
        self.__artifact_path = artifact_path

    @classmethod
    def instance(cls, is_local=True, artifact_path=None) -> AppConfig:
        if cls.__instance is None:
            cls.__instance = AppConfig(is_local, artifact_path)
        return cls.__instance

    def is_local(self) -> bool:
        return self.__is_local

    def artifact_path(self) -> Path:
        return self.__artifact_path
