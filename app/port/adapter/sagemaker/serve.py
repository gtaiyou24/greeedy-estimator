from typing import NoReturn

import uvicorn
from fastapi import FastAPI

from config import ServeEventHandler, AppConfig
from port.adapter.resource.invocation import invocation_resource
from port.adapter.resource.ping import ping_resource


def run(host: str, port: int) -> NoReturn:
    app = FastAPI(title="Greeedy Estimator")

    handler = ServeEventHandler(app)
    app.add_event_handler('startup', handler.startup)
    app.add_event_handler('shutdown', handler.shutdown)

    app.include_router(invocation_resource.router)
    app.include_router(ping_resource.router)

    uvicorn.run(app, host=host, port=port, reload=AppConfig.instance().is_local())
