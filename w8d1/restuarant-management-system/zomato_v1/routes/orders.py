# Order endpoints router (place order, status, history, analytics)
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime

from database import get_db
from crud import (
    create_order, get_order, list_orders, update_order_status,
    get_customer_orders, get_restaurant_orders, calculate_order_total,
    add_order_item, remove_order_item, get_order_items
)
from schemas import OrderCreate, OrderUpdate, OrderOut, OrderItemCreate, OrderItemOut
from models import Order

router = APIRouter(prefix="/orders", tags=["orders"])

# Create a new order
@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create_new_order(
    order: OrderCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new order for a customer."""
    return await create_order(db, order)

# Get order by ID
@router.get("/{order_id}", response_model=OrderOut)
async def get_order_by_id(order_id: int, db: AsyncSession = Depends(get_db)):
    """Get details of a specific order."""
    order = await get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# List all orders with pagination
@router.get("/", response_model=List[OrderOut])
async def list_all_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """List all orders with pagination."""
    return await list_orders(db, skip=skip, limit=limit)

# Update order status
@router.put("/{order_id}/status", response_model=OrderOut)
async def update_status(
    order_id: int,
    order: OrderUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update the status of an order."""
    updated = await update_order_status(db, order_id, order)
    if not updated:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated

# Get orders for a customer
@router.get("/customer/{customer_id}", response_model=List[OrderOut])
async def get_orders_by_customer(
    customer_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get all orders for a specific customer."""
    return await get_customer_orders(db, customer_id, skip=skip, limit=limit)

# Get orders for a restaurant
@router.get("/restaurant/{restaurant_id}", response_model=List[OrderOut])
async def get_orders_by_restaurant(
    restaurant_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get all orders for a specific restaurant."""
    return await get_restaurant_orders(db, restaurant_id, skip=skip, limit=limit)

# Calculate order total
@router.get("/{order_id}/total", response_model=float)
async def get_order_total(order_id: int, db: AsyncSession = Depends(get_db)):
    """Calculate and return the total amount for an order."""
    total = await calculate_order_total(db, order_id)
    if total is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return total

# Add item to order
@router.post("/{order_id}/items", response_model=OrderItemOut)
async def add_item_to_order(
    order_id: int,
    item: OrderItemCreate,
    db: AsyncSession = Depends(get_db)
):
    """Add a new item to an existing order."""
    return await add_order_item(db, order_id, item)

# Remove item from order
@router.delete("/{order_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_item_from_order(
    order_id: int,
    item_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Remove an item from an order."""
    success = await remove_order_item(db, order_id, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order item not found")
    return None

# Get order items
@router.get("/{order_id}/items", response_model=List[OrderItemOut])
async def list_order_items(
    order_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all items in an order."""
    items = await get_order_items(db, order_id)
    if not items:
        raise HTTPException(status_code=404, detail="Order not found or has no items")
    return items
