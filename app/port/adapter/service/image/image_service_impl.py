from urllib.error import HTTPError

import skimage.io

from domain.model.image import ImageService, Image
from domain.model.image.url import ImageUrl
from exception import SystemException, ErrorCode


class ImageServiceImpl(ImageService):
    def download(self, image_url: ImageUrl) -> Image:
        try:
            rgb = skimage.io.imread(image_url.resource)
        except HTTPError:
            raise SystemException(ErrorCode.IMAGE_NOT_FOUND, f"{image_url.resource}の画像が見つかりませんでした。")
        return Image(image_url, rgb)
