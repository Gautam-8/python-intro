# Main FastAPI app entry point
from fastapi import FastAPI
from models import Base
from database import engine
from routes import router as restaurant_router, menu_router
import asyncio

app = FastAPI(title="Zomato V1 - Restaurant Management System", description="API for managing restaurants and menu items.")

# Include the restaurant and menu item routes
app.include_router(restaurant_router)
app.include_router(menu_router)

# Create database tables on startup
@app.on_event("startup")
async def on_startup():
    # Create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
