from typing import List

from pydantic import BaseModel, Field


class InvocationsRequest(BaseModel):
    item_name: str = Field(title='アイテム名', default='', description='画像から指定したアイテムのカラーを推定します。')
    image_urls: List[str] = Field(title='アイテムの画像URL', default=[],
                                      description='この画像ごとに対象アイテムのカラーを推定します。')
    option_colors: List[str] = Field(title='カラー候補一覧', default=[],
                                     description='カラー候補一覧が指定されている場合、カラー候補一覧からカラーを推定します。')
