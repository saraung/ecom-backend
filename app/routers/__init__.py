from fastapi import APIRouter
from app.routers.auth_router import router as auth_router
from app.routers.user_router import router as user_router
from app.routers.product_router import router as product_router
from app.routers.order_router import router as order_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(product_router)
api_router.include_router(order_router)