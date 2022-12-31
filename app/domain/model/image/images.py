from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from domain.model.image import Image


@dataclass(init=False, unsafe_hash=True, frozen=True)
class Images:
    rgb_arr: np.ndarray

    def __init__(self, rgb_arr: np.ndarray):
        assert len(rgb_arr.shape) == 4, 'shapeが(n, height, width, channels)となるようにnumpy.arrayを指定してください。'
        super().__setattr__('rgb_arr', rgb_arr)

    def add(self, image: Image) -> Images:
        return Images(np.append(self.rgb_arr, image.rgb, axis=0))

    def add_other(self, images: Images) -> Images:
        return Images(np.append(self.rgb_arr, images.rgb_arr, axis=0))
