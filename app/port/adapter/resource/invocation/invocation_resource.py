import fastapi
from di import DIContainer
from fastapi import APIRouter

from application.estimator import EstimatorApplicationService
from application.estimator.command import PredictCommand
from port.adapter.resource.invocation.request import InvocationsRequest
from port.adapter.resource.invocation.response.invocations_json import InvocationsJson

router = APIRouter(
    prefix='/invocations',
    tags=['推論']
)


@router.post('', name='推論用エンドポイント', response_model=InvocationsJson)
def invocations(invocations_request: InvocationsRequest, request: fastapi.Request) -> InvocationsJson:
    application_service: EstimatorApplicationService = DIContainer\
        .instance()\
        .resolve(EstimatorApplicationService)

    command = PredictCommand(
        [PredictCommand.Item(invocations_request.item_name, image_url) for image_url in invocations_request.image_urls],
        set(invocations_request.option_colors),
        request.app.state.estimator,
        request.app.state.vectorizer
    )

    dpo = application_service.predict(command)

    return InvocationsJson.of(dpo)
