
class AggregatorError(Exception):

    msg: str

    def __init__(self, msg, *args: object) -> None:
        self.msg = msg
        super().__init__(*args)


class NotFound(AggregatorError):
    type_: type
    key: str
    value: any

    def __init__(self, type_: type, key: str, value: any, *args: object) -> None:
        self.type_ = type_
        self.key = key
        self.value = value
        super().__init__(
            f"Item of type {type_!r} not found: {self.key!r} = {self.value!r}",
            *args
        )


class Conflict(NotFound):
    type: type
    key: str
    value: str

    def __init__(self, key, value, *args: object) -> None:
        self.key = key
        self.value = value
        super().__init__(
            f"Item of type {type!r} already exists: {self.key!r} = {self.value!r}",
            *args
        )


class RemoteConnectionError(AggregatorError):

    url: str

    def __init__(self, msg, url: str, *args: object) -> None:
        self.url = url
        super().__init__(msg, *args)
        self.msg = f"Failed at url {self.url!r}, {self.msg}"


class TokenError(AggregatorError):
    pass



