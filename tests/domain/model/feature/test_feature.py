from typing import NoReturn

from domain.model.feature import Feature


class TestFeature:
    def test_ItemImageを生成できる(self) -> NoReturn:
        Feature.ItemImage.of('https://www.dzimg.com/Dahong/202212/1532168_21713446_k3.gif')

    def test_ItemNameを生成できる(self) -> NoReturn:
        Feature.ItemName.of('ウェーブ長袖ニット・p477418')
