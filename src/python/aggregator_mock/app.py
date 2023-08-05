import datetime
import random
import uuid
from uuid import UUID

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import Response

from aggregator_common.schemas import Product, Offer


app = FastAPI()


class RegisterProductResponse(BaseModel):
    id: UUID


class TokenResposne(BaseModel):
    access_token: str


offer = Offer(id=uuid.uuid4(), price=10, items_in_stock=1)


@app.post("/api/v1/auth")
def auth(response: Response) -> TokenResposne:
    response.status_code = 201
    return TokenResposne(
        access_token=f"TOKEN-{datetime.datetime.timestamp(datetime.datetime.utcnow())}"
    )


@app.post("/api/v1/products/register")
def register_product(product: Product, response: Response) -> RegisterProductResponse:
    response.status_code = 201
    return RegisterProductResponse(id=product.id)


@app.get("/api/v1/products/{product_id}/offers")
def get_offers() -> list[Offer]:
    offer.price = random.randint(1, 1000)
    offer.items_in_stock = random.randint(1, 30)
    offers = [offer]
    for index in range(random.randint(0, 20)):
        offers.append(
            Offer(
                id=uuid.uuid4(),
                price=random.randint(10, 1000),
                items_in_stock=random.randint(1, 30)
            )
        )
    return offers


def serve():
    import uvicorn
    uvicorn.run(app, port=9000)


if __name__ == '__main__':
    serve()
