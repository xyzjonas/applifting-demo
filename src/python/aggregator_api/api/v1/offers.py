from uuid import UUID

from fastapi import APIRouter
from fastapi_pagination import Page, add_pagination

from aggregator_api.api.v1.common.dependencies import ProductsDependency, OffersDependency
from aggregator_common.schemas import Product, Offer

router = APIRouter(tags=['Offers'])


@router.get('')
async def get_offers(offers: OffersDependency, product_id: UUID = None) -> Page[Offer]:
    return await offers.get_all(use_paginate=True)


@router.get('/{offer_id}')
async def get_product(offers: ProductsDependency, offer_id: UUID) -> Product:
    return await offers.get_by_id(offer_id)


add_pagination(router)
