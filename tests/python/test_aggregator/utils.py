import json

from aiohttp import ClientResponseError
from httpx import Response
from mock.mock import MagicMock


def assert_response(response: Response):
    try:
        response.raise_for_status()
    except Exception as exc:
        raise AssertionError(response.text, exc)
    return response


class MockResponse:

    response_data: dict
    status: int

    def __init__(self, response_data: dict, status: int):
        self.response_data = response_data
        self.status = status

    async def text(self):
        return json.dumps(self.response_data)

    def raise_for_status(self):
        if self.status > 300:
            raise ClientResponseError(MagicMock(), MagicMock(), message="mocker error")

    async def json(self) -> dict:
        return self.response_data

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self
