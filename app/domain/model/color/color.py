from __future__ import annotations

from enum import Enum


class Color(Enum):
    Beige = (1, 'ベージュ', 'beige')
    White = (2, 'ホワイト', 'white')
    Black = (3, 'ブラック', 'black')
    Brown = (4, 'ブラウン', 'brown')
    Pink = (5, 'ピンク', 'pink')
    Gray = (6, 'グレイ', 'gray')
    Green = (7, 'グリーン', 'green')
    Blue = (8, 'ブルー', 'blue')
    Purple = (9, 'パープル', 'purple')
    Yellow = (10, 'イエロー', 'yellow')
    Navy = (11, 'ネイビー', 'navy')
    Red = (12, 'レッド', 'red')
    Orange = (13, 'オレンジ', 'orange')
    Mix = (14, '複数色', 'mix')
    Other = (15, 'その他', 'other')
    Gold = (16, 'ゴールド', 'gold')
    Silver = (17, 'シルバー', 'silver')
    Unknown = (0, '不明', 'unknown')

    def __init__(self, id: int, ja_name: str, en_name: str):
        super().__init__()
        self.__id = id
        self.__ja_name = ja_name
        self.__en_name = en_name

    @staticmethod
    def value_of(id: int) -> Color:
        for color in Color:
            if color.id() == id:
                return color

        raise ValueError(f"カラーIDが {id} は見つかりませんでした。")

    @staticmethod
    def value_of_ja_name(ja_name: str):
        for color in Color:
            if color.ja_name() == ja_name:
                return color
        return Color.Unknown

    @staticmethod
    def value_of_en_name(en_name: str):
        for color in Color:
            if color.en_name() == en_name:
                return color
        return Color.Unknown

    def id(self) -> int:
        return self.__id

    def ja_name(self) -> str:
        return self.__ja_name

    def en_name(self) -> str:
        return self.__en_name
