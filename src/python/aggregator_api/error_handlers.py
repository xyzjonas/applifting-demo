from fastapi import FastAPI
from loguru import logger
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from aggregator_common.exceptions import NotFound, Conflict, AggregatorError, RemoteConnectionError


def generic_500_handler(request: Request, exc: AggregatorError):
    """Return 500, log the trace and pass the exception message."""
    try:
        raise exc
    except type(exc):
        logger.exception('Internal server error.')
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=exc.msg,
    )


def not_found_handler(request: Request, exc: NotFound):
    """Return 404 and just pass the exception message."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=exc.msg,
    )


def conflict_handler(request: Request, exc: Conflict):
    """Return 409 and just pass the exception message."""
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=exc.msg
    )


def remote_error_handler(request: Request, exc: RemoteConnectionError):
    """Return 409 and just pass the exception message."""
    logger.exception("Remote failed.")
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content="Remote server communication failed."
    )


def register_exception_handlers(app: FastAPI):
    """Register exception handling globally here."""
    # app.add_exception_handler(RemoteConnectionError, remote_error_handler)
    app.add_exception_handler(NotFound, not_found_handler)
    app.add_exception_handler(Conflict, conflict_handler)
    app.add_exception_handler(AggregatorError, generic_500_handler)
