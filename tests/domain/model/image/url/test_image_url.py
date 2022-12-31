from typing import NoReturn

from domain.model.image.url import ImageUrl


class TestImageUrl:
    class Test_生成について:
        def test_文字列の画像URL指定で生成できる(self) -> NoReturn:
            ImageUrl('https://www.test.com/item/1/images/1.png')
