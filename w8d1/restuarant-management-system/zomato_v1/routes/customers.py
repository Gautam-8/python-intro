# Customer endpoints router (CRUD, analytics)
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from database import get_db
from crud import (
    create_customer, get_customer, list_customers, update_customer, delete_customer,
    get_customer_orders, get_customer_reviews
)
from schemas import CustomerCreate, CustomerUpdate, CustomerOut, OrderOut, ReviewOut

router = APIRouter(prefix="/customers", tags=["customers"])

# Create new customer
@router.post("/", response_model=CustomerOut, status_code=status.HTTP_201_CREATED)
async def create_new_customer(
    customer: CustomerCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new customer account."""
    return await create_customer(db, customer)

# Get customer by ID
@router.get("/{customer_id}", response_model=CustomerOut)
async def get_customer_by_id(customer_id: int, db: AsyncSession = Depends(get_db)):
    """Get details of a specific customer."""
    customer = await get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

# List all customers with pagination
@router.get("/", response_model=List[CustomerOut])
async def list_all_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """List all customers with pagination."""
    return await list_customers(db, skip=skip, limit=limit)

# Update customer
@router.put("/{customer_id}", response_model=CustomerOut)
async def update_customer_by_id(
    customer_id: int,
    customer: CustomerUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an existing customer's details."""
    updated = await update_customer(db, customer_id, customer)
    if not updated:
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated

# Delete customer
@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer_by_id(customer_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a customer account."""
    success = await delete_customer(db, customer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Customer not found")
    return None

# Get customer's orders
@router.get("/{customer_id}/orders", response_model=List[OrderOut])
async def get_customer_order_history(
    customer_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get order history for a customer."""
    return await get_customer_orders(db, customer_id, skip=skip, limit=limit)

# Get customer's reviews
@router.get("/{customer_id}/reviews", response_model=List[ReviewOut])
async def get_customer_review_history(
    customer_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get review history for a customer."""
    return await get_customer_reviews(db, customer_id, skip=skip, limit=limit)
