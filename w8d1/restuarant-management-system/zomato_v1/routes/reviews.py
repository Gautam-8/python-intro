# Review endpoints router (add review, get reviews, analytics)
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime
from database import get_db
from crud import (
    create_review, get_review, list_reviews, update_review, delete_review,
    get_restaurant_reviews, get_customer_reviews, get_order_review,
    calculate_restaurant_rating
)
from schemas import ReviewCreate, ReviewUpdate, ReviewOut
from models import Review

router = APIRouter(prefix="/reviews", tags=["reviews"])

# Create a new review for an order
@router.post("/orders/{order_id}", response_model=ReviewOut, status_code=status.HTTP_201_CREATED)
async def create_order_review(
    order_id: int,
    review: ReviewCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a review for a completed order."""
    return await create_review(db, order_id, review)

# Get a specific review
@router.get("/{review_id}", response_model=ReviewOut)
async def get_review_by_id(review_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific review by its ID."""
    review = await get_review(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

# List all reviews with pagination
@router.get("/", response_model=List[ReviewOut])
async def list_all_reviews(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """List all reviews with pagination."""
    return await list_reviews(db, skip=skip, limit=limit)

# Update a review
@router.put("/{review_id}", response_model=ReviewOut)
async def update_review_by_id(
    review_id: int,
    review: ReviewUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an existing review."""
    updated = await update_review(db, review_id, review)
    if not updated:
        raise HTTPException(status_code=404, detail="Review not found")
    return updated

# Delete a review
@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review_by_id(review_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a review."""
    deleted = await delete_review(db, review_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Review not found")
    return None

# Get reviews for a restaurant
@router.get("/restaurants/{restaurant_id}", response_model=List[ReviewOut])
async def get_restaurant_reviews_view(
    restaurant_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get all reviews for a specific restaurant."""
    return await get_restaurant_reviews(db, restaurant_id, skip=skip, limit=limit)

# Get reviews by a customer
@router.get("/customers/{customer_id}", response_model=List[ReviewOut])
async def get_customer_reviews_view(
    customer_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get all reviews by a specific customer."""
    return await get_customer_reviews(db, customer_id, skip=skip, limit=limit)

# Get review for a specific order
@router.get("/orders/{order_id}", response_model=Optional[ReviewOut])
async def get_order_review_view(order_id: int, db: AsyncSession = Depends(get_db)):
    """Get the review for a specific order if it exists."""
    review = await get_order_review(db, order_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found for this order")
    return review

# Get restaurant rating analytics
@router.get("/restaurants/{restaurant_id}/rating", response_model=float)
async def get_restaurant_rating(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    """Calculate and return the average rating for a restaurant."""
    rating = await calculate_restaurant_rating(db, restaurant_id)
    if rating is None:
        raise HTTPException(status_code=404, detail="No reviews found for this restaurant")
    return rating
