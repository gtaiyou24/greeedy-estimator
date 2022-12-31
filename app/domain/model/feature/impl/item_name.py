from typing import Union

from hocho.cleaning import clean_text
from hocho.normalization import normalize
from hocho.tokenizer import Tokenizer

from domain.model.feature import Feature


class ItemName(Feature):
    def __init__(self, tokenizer: Tokenizer):
        self.__tokenizer = tokenizer

    def of(self, text: str) -> str:
        text = normalize(text)
        text = clean_text(text)
        return ' '.join(self.__tokenizer.wakati(text))
