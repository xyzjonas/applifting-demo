from fastapi import APIRouter

from aggregator_api.api.v1.offers import router as offers_router
from aggregator_api.api.v1.products import router as products_router

router = APIRouter(prefix='/v1')
router.include_router(products_router, prefix="/products")
router.include_router(offers_router, prefix="/offers")
