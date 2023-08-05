from httpx import Response


def assert_response(response: Response):
    try:
        response.raise_for_status()
    except Exception as exc:
        raise AssertionError(response.text, exc)
    return response
