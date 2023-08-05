import uuid
from uuid import UUID

from fastapi import APIRouter
from fastapi_pagination import Page, add_pagination
from starlette.responses import Response

from aggregator_api.api.v1.common.dependencies import ProductsDependency, OffersDependency, \
    RemoteClientDependency
from aggregator_api.api.v1.common.schemas import ProductCreate, ProductUpdate
from aggregator_common.schemas import Product, Offer

router = APIRouter(tags=['Products'])


@router.get('')
async def get_products(products: ProductsDependency) -> Page[Product]:
    return await products.get_all(use_paginate=True)


@router.get('/{product_id}')
async def get_product(products: ProductsDependency, product_id: UUID) -> Product:
    return await products.get_by_id(product_id)


@router.get('/{product_id}/offers')
async def get_product_offers(offers: OffersDependency, product_id: UUID) -> Page[Offer]:
    return await offers.get_by_product(product_id=product_id, use_paginate=True)


@router.post('')
async def create_product(
        response: Response,
        products: ProductsDependency,
        client: RemoteClientDependency,
        product_data: ProductCreate,
) -> Product:
    product_id = uuid.uuid4()
    await client.register_product(
        Product(id=product_id, **product_data.model_dump())
    )

    product = await products.create(product_data, own_id=product_id)
    response.status_code = 201
    return product


@router.put('/{product_id}')
async def update_product(
        products: ProductsDependency,
        product_data: ProductUpdate,
        product_id: UUID,
) -> Product:
    return await products.update(product_id, product_data)


@router.delete('/{product_id}')
async def create_product(products: ProductsDependency, product_id: UUID):
    return await products.delete(product_id)


add_pagination(router)
