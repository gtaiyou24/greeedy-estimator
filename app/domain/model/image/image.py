from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np

from domain.model.image.url import ImageUrl


@dataclass(init=False, unsafe_hash=True, frozen=True)
class Image:
    url: ImageUrl
    rgb: np.ndarray

    def __init__(self, url: ImageUrl, rgb: np.ndarray):
        super().__setattr__('url', url)
        super().__setattr__('rgb', rgb)

    def resize(self, height: int, width: int) -> Image:
        rgb = cv2.resize(self.rgb, dsize=(height, width))
        return Image(self.url, rgb)
