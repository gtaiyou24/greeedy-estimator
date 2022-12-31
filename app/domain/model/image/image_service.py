import abc

from domain.model.image import Image
from domain.model.image.url import ImageUrl


class ImageService(abc.ABC):
    @abc.abstractmethod
    def download(self, image_url: ImageUrl) -> Image:
        pass
