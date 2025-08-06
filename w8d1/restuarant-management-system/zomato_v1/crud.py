
# CRUD operations for Restaurant and MenuItem models using async SQLAlchemy
import asyncio
from time import time
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from models import Restaurant, MenuItem, Review, Order, OrderItem, Customer
from schemas import (
    RestaurantCreate, RestaurantUpdate,
    MenuItemCreate, MenuItemUpdate,
    ReviewCreate, ReviewUpdate,
    OrderCreate, OrderUpdate,
    OrderItemCreate, OrderItemUpdate,
    CustomerCreate, CustomerUpdate
)
from typing import List, Optional
from fastapi import HTTPException, status
from fastapi_cache.decorator import cache

# Create a new restaurant
async def create_restaurant(db: AsyncSession, restaurant: RestaurantCreate) -> Restaurant:
    # Create a new Restaurant instance
    db_restaurant = Restaurant(**restaurant.dict())
    db.add(db_restaurant)
    try:
        await db.commit()  # Commit transaction
        await db.refresh(db_restaurant)  # Refresh instance with DB data
        return db_restaurant
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Restaurant name already exists.")


# --- MENU ITEM CRUD ---

# Add menu item to restaurant
async def create_menu_item(db: AsyncSession, restaurant_id: int, item: MenuItemCreate) -> MenuItem:
    # Ensure restaurant exists
    restaurant = await get_restaurant(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    db_item = MenuItem(**item.dict(), restaurant_id=restaurant_id)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

# Get menu item by ID
async def get_menu_item(db: AsyncSession, item_id: int) -> Optional[MenuItem]:
    result = await db.execute(select(MenuItem).where(MenuItem.id == item_id))
    return result.scalar_one_or_none()

# List all menu items
async def list_menu_items(db: AsyncSession, skip: int = 0, limit: int = 10) -> List[MenuItem]:
    result = await db.execute(select(MenuItem).offset(skip).limit(limit))
    return result.scalars().all()

# Update menu item
async def update_menu_item(db: AsyncSession, item_id: int, item: MenuItemUpdate) -> Optional[MenuItem]:
    db_item = await get_menu_item(db, item_id)
    if not db_item:
        return None
    for key, value in item.dict(exclude_unset=True).items():
        setattr(db_item, key, value)
    await db.commit()
    await db.refresh(db_item)
    return db_item

# Delete menu item
async def delete_menu_item(db: AsyncSession, item_id: int) -> bool:
    db_item = await get_menu_item(db, item_id)
    if not db_item:
        return False
    await db.delete(db_item)
    await db.commit()
    return True

# Get all menu items for a restaurant
async def get_menu_for_restaurant(db: AsyncSession, restaurant_id: int, skip: int = 0, limit: int = 10) -> List[MenuItem]:
    result = await db.execute(
        select(MenuItem).where(MenuItem.restaurant_id == restaurant_id).offset(skip).limit(limit)
    )
    return result.scalars().all()

# Get menu item with restaurant details
async def get_menu_item_with_restaurant(db: AsyncSession, item_id: int) -> Optional[MenuItem]:
    result = await db.execute(
        select(MenuItem).options(selectinload(MenuItem.restaurant)).where(MenuItem.id == item_id)
    )
    return result.scalar_one_or_none()

# Get restaurant with all menu items
async def get_restaurant_with_menu(db: AsyncSession, restaurant_id: int) -> Optional[Restaurant]:
    result = await db.execute(
        select(Restaurant).options(selectinload(Restaurant.menu_items)).where(Restaurant.id == restaurant_id)
    )
    return result.scalar_one_or_none()

# Search menu items by category and dietary preference
async def search_menu_items(db: AsyncSession, category: Optional[str] = None, vegetarian: Optional[bool] = None, skip: int = 0, limit: int = 10) -> List[MenuItem]:
    query = select(MenuItem)
    if category:
        query = query.where(MenuItem.category.ilike(f"%{category}%"))
    if vegetarian is not None:
        query = query.where(MenuItem.is_vegetarian == vegetarian)
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()

# Calculate average menu price per restaurant
async def get_average_menu_price(db: AsyncSession, restaurant_id: int) -> Optional[float]:
    result = await db.execute(
        select(func.avg(MenuItem.price)).where(MenuItem.restaurant_id == restaurant_id)
    )
    avg_price = result.scalar()
    return float(avg_price) if avg_price is not None else None

# Get a restaurant by ID
@cache(expire=1000, key_builder=lambda restaurant_id: f"restaurant_{restaurant_id}")
async def get_restaurant(db: AsyncSession, restaurant_id: int) -> Optional[Restaurant]:
    result = await db.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
    return result.scalar_one_or_none()

# List all restaurants with pagination
@cache(expire=300, key_builder=lambda *args, **kwargs: f"restaurants_list_{kwargs.get('skip', 0)}_{kwargs.get('limit', 10)}")
async def list_restaurants(db: AsyncSession, skip: int = 0, limit: int = 10) -> List[Restaurant]:
    result = await db.execute(select(Restaurant).offset(skip).limit(limit))
    asyncio.sleep(4)
    return result.scalars().all()

# Update a restaurant by ID
async def update_restaurant(db: AsyncSession, restaurant_id: int, restaurant: RestaurantUpdate) -> Optional[Restaurant]:
    db_restaurant = await get_restaurant(db, restaurant_id)
    if not db_restaurant:
        return None
    for key, value in restaurant.dict(exclude_unset=True).items():
        setattr(db_restaurant, key, value)
    try:
        await db.commit()
        await db.refresh(db_restaurant)
        return db_restaurant
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Restaurant name already exists.")

# Delete a restaurant by ID
async def delete_restaurant(db: AsyncSession, restaurant_id: int) -> bool:
    db_restaurant = await get_restaurant(db, restaurant_id)
    if not db_restaurant:
        return False
    await db.delete(db_restaurant)
    await db.commit()
    return True

# Search restaurants by cuisine type
async def search_by_cuisine(db: AsyncSession, cuisine_type: str, skip: int = 0, limit: int = 10) -> List[Restaurant]:
    result = await db.execute(
        select(Restaurant).where(Restaurant.cuisine_type.ilike(f"%{cuisine_type}%")).offset(skip).limit(limit)
    )
    return result.scalars().all()

# List only active restaurants
async def list_active_restaurants(db: AsyncSession, skip: int = 0, limit: int = 10) -> List[Restaurant]:
    result = await db.execute(
        select(Restaurant).where(Restaurant.is_active == True).offset(skip).limit(limit)
    )
    return result.scalars().all()

# --- REVIEW CRUD OPERATIONS ---

# Create a new review
async def create_review(db: AsyncSession, order_id: int, review: ReviewCreate) -> Review:
    db_review = Review(**review.dict(), order_id=order_id)
    db.add(db_review)
    try:
        await db.commit()
        await db.refresh(db_review)
        return db_review
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Review already exists for this order")

# Get a specific review
async def get_review(db: AsyncSession, review_id: int) -> Optional[Review]:
    result = await db.execute(select(Review).where(Review.id == review_id))
    return result.scalar_one_or_none()

# List all reviews with pagination
async def list_reviews(db: AsyncSession, skip: int = 0, limit: int = 10) -> List[Review]:
    result = await db.execute(select(Review).offset(skip).limit(limit))
    return result.scalars().all()

# Update a review
async def update_review(db: AsyncSession, review_id: int, review: ReviewUpdate) -> Optional[Review]:
    db_review = await get_review(db, review_id)
    if not db_review:
        return None
    
    for key, value in review.dict(exclude_unset=True).items():
        setattr(db_review, key, value)
    
    await db.commit()
    await db.refresh(db_review)
    return db_review

# Delete a review
async def delete_review(db: AsyncSession, review_id: int) -> bool:
    db_review = await get_review(db, review_id)
    if not db_review:
        return False
    await db.delete(db_review)
    await db.commit()
    return True

# Get reviews for a restaurant
async def get_restaurant_reviews(db: AsyncSession, restaurant_id: int, skip: int = 0, limit: int = 10) -> List[Review]:
    result = await db.execute(
        select(Review)
        .join(Order)
        .where(Order.restaurant_id == restaurant_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

# Get reviews by a customer
async def get_customer_reviews(db: AsyncSession, customer_id: int, skip: int = 0, limit: int = 10) -> List[Review]:
    result = await db.execute(
        select(Review)
        .join(Order)
        .where(Order.customer_id == customer_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

# Get review for a specific order
async def get_order_review(db: AsyncSession, order_id: int) -> Optional[Review]:
    result = await db.execute(
        select(Review).where(Review.order_id == order_id)
    )
    return result.scalar_one_or_none()

# Calculate restaurant rating
async def calculate_restaurant_rating(db: AsyncSession, restaurant_id: int) -> Optional[float]:
    result = await db.execute(
        select(func.avg(Review.rating))
        .join(Order)
        .where(Order.restaurant_id == restaurant_id)
    )
    avg_rating = result.scalar()
    return float(avg_rating) if avg_rating is not None else None

# --- ORDER CRUD OPERATIONS ---

# Create a new order
async def create_order(db: AsyncSession, order: OrderCreate) -> Order:
    db_order = Order(**order.dict())
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    return db_order

# Get order by ID
async def get_order(db: AsyncSession, order_id: int) -> Optional[Order]:
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.id == order_id)
    )
    return result.scalar_one_or_none()

# List all orders with pagination
async def list_orders(db: AsyncSession, skip: int = 0, limit: int = 10) -> List[Order]:
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items))
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

# Update order status
async def update_order_status(db: AsyncSession, order_id: int, order: OrderUpdate) -> Optional[Order]:
    db_order = await get_order(db, order_id)
    if not db_order:
        return None
    
    for key, value in order.dict(exclude_unset=True).items():
        setattr(db_order, key, value)
    
    await db.commit()
    await db.refresh(db_order)
    return db_order

# Get orders for a customer
async def get_customer_orders(db: AsyncSession, customer_id: int, skip: int = 0, limit: int = 10) -> List[Order]:
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.customer_id == customer_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

# Get orders for a restaurant
async def get_restaurant_orders(db: AsyncSession, restaurant_id: int, skip: int = 0, limit: int = 10) -> List[Order]:
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.restaurant_id == restaurant_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

# Calculate order total
async def calculate_order_total(db: AsyncSession, order_id: int) -> Optional[float]:
    result = await db.execute(
        select(func.sum(MenuItem.price * OrderItem.quantity))
        .join(OrderItem, OrderItem.menu_item_id == MenuItem.id)
        .where(OrderItem.order_id == order_id)
    )
    total = result.scalar()
    return float(total) if total is not None else None

# Add item to order
async def add_order_item(db: AsyncSession, order_id: int, item: OrderItemCreate) -> OrderItem:
    db_item = OrderItem(**item.dict(), order_id=order_id)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

# Remove item from order
async def remove_order_item(db: AsyncSession, order_id: int, item_id: int) -> bool:
    db_item = await db.execute(
        select(OrderItem)
        .where(OrderItem.order_id == order_id, OrderItem.id == item_id)
    )
    db_item = db_item.scalar_one_or_none()
    if not db_item:
        return False
    await db.delete(db_item)
    await db.commit()
    return True

# Get order items
async def get_order_items(db: AsyncSession, order_id: int) -> List[OrderItem]:
    result = await db.execute(
        select(OrderItem)
        .options(selectinload(OrderItem.menu_item))
        .where(OrderItem.order_id == order_id)
    )
    return result.scalars().all()

# --- CUSTOMER CRUD OPERATIONS ---

# Create a new customer
async def create_customer(db: AsyncSession, customer: CustomerCreate) -> Customer:
    db_customer = Customer(**customer.dict())
    db.add(db_customer)
    try:
        await db.commit()
        await db.refresh(db_customer)
        return db_customer
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")

# Get customer by ID
async def get_customer(db: AsyncSession, customer_id: int) -> Optional[Customer]:
    result = await db.execute(
        select(Customer).where(Customer.id == customer_id)
    )
    return result.scalar_one_or_none()

# Get customer by email
async def get_customer_by_email(db: AsyncSession, email: str) -> Optional[Customer]:
    result = await db.execute(
        select(Customer).where(Customer.email == email)
    )
    return result.scalar_one_or_none()

# List all customers with pagination
async def list_customers(db: AsyncSession, skip: int = 0, limit: int = 10) -> List[Customer]:
    result = await db.execute(
        select(Customer).offset(skip).limit(limit)
    )
    return result.scalars().all()

# Update customer
async def update_customer(db: AsyncSession, customer_id: int, customer: CustomerUpdate) -> Optional[Customer]:
    db_customer = await get_customer(db, customer_id)
    if not db_customer:
        return None
    
    # If email is being updated, check if new email already exists
    if customer.email and customer.email != db_customer.email:
        existing = await get_customer_by_email(db, customer.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    for key, value in customer.dict(exclude_unset=True).items():
        setattr(db_customer, key, value)
    
    try:
        await db.commit()
        await db.refresh(db_customer)
        return db_customer
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")

# Delete customer
async def delete_customer(db: AsyncSession, customer_id: int) -> bool:
    db_customer = await get_customer(db, customer_id)
    if not db_customer:
        return False
    await db.delete(db_customer)
    await db.commit()
    return True
