from __future__ import annotations

from pydantic import BaseModel, Field

from application.estimator.dpo import PredictedColorsDpo


class InvocationsJson(BaseModel):
    class Predicted(BaseModel):
        image_url: str = Field(title='画像URL', default='')
        color: str = Field(title='カラー', default='', description='予測結果のカラー')

    colors: list[InvocationsJson.Predicted] = Field(title='予測カラー一覧', default=[], description='予測されたカラーの一覧')

    @staticmethod
    def of(dpo: PredictedColorsDpo) -> InvocationsJson:
        return InvocationsJson(
            colors=[InvocationsJson.Predicted(image_url=predicted.image_url.resource, color=predicted.color.en_name()) \
                    for predicted in dpo.predicted_list]
        )
