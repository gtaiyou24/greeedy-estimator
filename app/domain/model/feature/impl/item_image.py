from dataclasses import dataclass
from typing import Union

import cv2
import numpy as np
import skimage

from domain.model.feature import Feature


@dataclass(init=False, unsafe_hash=True, frozen=True)
class ItemImage(Feature):
    height: int
    width: int

    def __init__(self, height: int, width: int):
        super().__setattr__('height', height)
        super().__setattr__('width', width)

    def of(self, value: Union[str, np.ndarray]) -> np.ndarray:
        if type(value) == str:
            value = skimage.io.imread(value)
        value = cv2.resize(value, dsize=(self.height, self.width))
        if value.shape != (self.height, self.width, 3):
            raise ValueError()
        return value / 255.
