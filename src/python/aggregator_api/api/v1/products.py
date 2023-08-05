from uuid import UUID

from fastapi import APIRouter
from fastapi_pagination import Page, add_pagination
from starlette.responses import Response

from aggregator_api.api.v1.common.dependencies import ProductsDependency
from aggregator_api.api.v1.common.schemas import ProductRead, ProductCreate, ProductUpdate

router = APIRouter()


@router.get('')
async def get_products(products: ProductsDependency) -> Page[ProductRead]:
    return await products.get_all(use_paginate=True)


@router.get('/{product_id}')
async def get_product(products: ProductsDependency, product_id: UUID) -> ProductRead:
    return await products.get_by_id(product_id)


@router.post('')
async def create_product(
        response: Response, products: ProductsDependency, product_data: ProductCreate
) -> ProductRead:
    product = await products.create(product_data)
    response.status_code = 201
    return product


@router.put('/{product_id}')
async def create_product(
        products: ProductsDependency,
        product_data: ProductUpdate,
        product_id: UUID,
) -> ProductRead:
    return await products.update(product_id, product_data)


@router.delete('/{product_id}')
async def create_product(products: ProductsDependency, product_id: UUID):
    return await products.delete(product_id)


add_pagination(router)
