from __future__ import annotations

import abc
import subprocess
from typing import Any, Union


class classproperty:
    """ @classmethod+@property """
    def __init__(self, f):
        self.f = classmethod(f)

    def __get__(self, *args):
        return self.f.__get__(*args)()


class Feature(abc.ABC):
    @abc.abstractmethod
    def of(self, value: Any) -> Any:
        pass

    @classproperty
    def ItemImage(cls) -> ItemImage:
        from domain.model.feature.impl import ItemImage

        return ItemImage(300, 300)

    @classproperty
    def ItemName(cls) -> ItemName:
        from hocho.tokenizer.impl import MeCabTokenizer
        from domain.model.feature.impl import ItemName

        dicdir = subprocess.getoutput("mecab-config --dicdir")
        return ItemName(MeCabTokenizer(f"{dicdir}/mecab-ipadic-neologd"))
