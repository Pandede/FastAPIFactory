from typing import Any, Type

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette_exporter import PrometheusMiddleware, handle_metrics


def set_prometheus_exporter(app: FastAPI):
    """
    Expose the metrics endpoint to Prometheus.

    Args:
        app (FastAPI): The FastAPI application.
    """
    app.add_middleware(PrometheusMiddleware)
    app.add_route('/metrics', handle_metrics)


def set_shared_object(app: FastAPI, obj: Any, name: str):
    """
    Set an shared instance across the application.

    The instance can be accessed in endpoints or middlewares with attribute `request`.

    Args:
        app (FastAPI): The FastAPI application.
        obj (Any): The instance want to be shared.
        name (str): The unique name of the instance.
    """
    app.state.__setattr__(name, obj)


def get_shared_object(request: Request, name: str) -> Any:
    """
    Get the shared instance from attribute `request`.

    Args:
        request (Request): The request contains the shared instance.
        name (str): The unique name of the instance.

    Returns:
        Any: The specified instance.
    """
    return request.app.state.__getattr__(name)


def set_exception_status(app: FastAPI, exception: Type[Exception], status_code: int):
    """
    Catch the exception with status code.

    Args:
        app (FastAPI): The FastAPI application.
        exception (Type[Exception]): The expected exception to be caught.
        status_code (int): The corresponding status code to be returned when the exception is caught.
    """
    async def handler(_, exc: Exception):
        return JSONResponse({'detail': str(exc)}, status_code=status_code)

    app.add_exception_handler(exception, handler)


def set_home(app: FastAPI):
    """
    Set a simple homepage to show the title and version of application.

    Args:
        app (FastAPI): The FastAPI application.
    """
    async def home():
        return {'message': f'Hello from {app.title} {app.version}!'}

    app.get('/')(home)
