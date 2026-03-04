from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.user_router import router as user_router
from app.routers.product_router import router as product_router
from app.routers.order_router import router as order_router
from app.routers.auth_router import router as auth_router

app = FastAPI(
    title="FootyConnects API",
    description="Production-ready e-commerce backend for FootyConnects",
    version="1.0.0",
)

# ── CORS ────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ─────────────────────────────────────────────────────────
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(product_router)
app.include_router(order_router)


@app.get("/")
def home():
    return {"message": "Welcome to FootyConnects API"}


@app.get("/health")
def health():
    return {"status": "ok"}