
# CRUD operations for Restaurant and MenuItem models using async SQLAlchemy
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from models import Restaurant, MenuItem
from schemas import RestaurantCreate, RestaurantUpdate, MenuItemCreate, MenuItemUpdate
from typing import List, Optional
from fastapi import HTTPException, status

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
async def get_restaurant(db: AsyncSession, restaurant_id: int) -> Optional[Restaurant]:
    result = await db.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
    return result.scalar_one_or_none()

# List all restaurants with pagination
async def list_restaurants(db: AsyncSession, skip: int = 0, limit: int = 10) -> List[Restaurant]:
    result = await db.execute(select(Restaurant).offset(skip).limit(limit))
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
