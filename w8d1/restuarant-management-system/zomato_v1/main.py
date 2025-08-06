# Main FastAPI app entry point
from fastapi import FastAPI
from models import Base
from database import engine
from routes import (
    restaurant_router,
    menu_router,
    order_router,
    customer_router,
    review_router
)
import asyncio
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

app = FastAPI(
    title="Zomato V1 - Restaurant Management System",
    description="API for managing restaurants, orders, customers, and reviews.",
    version="1.0.0"
)

# Include all route modules
app.include_router(restaurant_router)
app.include_router(menu_router)
app.include_router(order_router)
app.include_router(customer_router)
app.include_router(review_router)

# Create database tables on startup
@app.on_event("startup")
async def on_startup():
    # Create tables if they don't exist
    redis = aioredis.from_url("redis://localhost:6379")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/cache/stats") 
async def cache_stats():
    """
    Endpoint to get cache statistics.
    """
    redis = FastAPICache.get_backend().redis
    keys = await redis.keys("fastapi-cache:*")
    return {
        "total_keys": len(keys),
        "keys": keys,
        "message": "Cache statistics retrieved successfully."
    }

@app.get("/clear_cache")
async def clear_cache():
    """
    Endpoint to clear the cache.
    """
    redis = FastAPICache.get_backend().redis
    print(redis)
    await redis.flushdb()
    return {
        "message": "Cache cleared successfully."
    }