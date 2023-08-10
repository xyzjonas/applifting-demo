from pydantic import BaseModel

from aggregator_common.exceptions import AggregatorAuthError


class User(BaseModel):
    username: str
    password: str


# ad-hoc PoC users 'database'
allowed_users = {
    "applifting-demo": User(
        username="applifting-demo",
        password="applifting",
    )
}


def authorize_user(username: str, password: str) -> User:
    user = allowed_users.get(username)
    if not user or user.password != password:
        raise AggregatorAuthError("Incorrect username or password")
    return user


def generate_token(user: User) -> str:
    # todo: JWT
    return f"token:{user.username}"


def decode_token(token: str) -> User:
    # todo: JWT
    try:
        tok, username = token.split(":")
        if tok != "token":
            raise AggregatorAuthError("Wrong token: invalid format!")
        if user := allowed_users.get(username):
            return user
        raise AggregatorAuthError("Wrong token: invalid user!")

    except Exception:
        raise AggregatorAuthError("Error while decoding token.") from Exception


def login(username: str, password: str) -> str:
    return generate_token(user=authorize_user(username, password))
