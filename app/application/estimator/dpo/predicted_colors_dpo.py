from dataclasses import dataclass

from domain.model.color import Color
from domain.model.image.url import ImageUrl


@dataclass(unsafe_hash=True, frozen=True)
class PredictedColorsDpo:
    @dataclass(unsafe_hash=True, frozen=True)
    class Predicted:
        image_url: ImageUrl
        color: Color

    predicted_list: list[Predicted]
