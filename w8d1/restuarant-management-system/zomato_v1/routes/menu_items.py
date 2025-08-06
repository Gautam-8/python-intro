# Menu items router (CRUD, search, and analytics)
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from database import get_db
from crud import (
    create_menu_item, get_menu_item, list_menu_items, update_menu_item,
    delete_menu_item, get_menu_item_with_restaurant, search_menu_items
)
from schemas import MenuItemCreate, MenuItemUpdate, MenuItemOut

router = APIRouter(prefix="/menu-items", tags=["menu-items"])

# Create new menu item
@router.post("/restaurants/{restaurant_id}", response_model=MenuItemOut, status_code=status.HTTP_201_CREATED)
async def create_new_menu_item(
    restaurant_id: int,
    item: MenuItemCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new menu item for a restaurant."""
    return await create_menu_item(db, restaurant_id, item)

# Get menu item by ID
@router.get("/{item_id}", response_model=MenuItemOut)
async def get_menu_item_by_id(item_id: int, db: AsyncSession = Depends(get_db)):
    """Get details of a specific menu item."""
    item = await get_menu_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item

# List all menu items with pagination
@router.get("/", response_model=List[MenuItemOut])
async def list_all_menu_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """List all menu items with pagination."""
    return await list_menu_items(db, skip=skip, limit=limit)

# Get menu item with restaurant details
@router.get("/{item_id}/with-restaurant", response_model=MenuItemOut)
async def get_menu_item_details(item_id: int, db: AsyncSession = Depends(get_db)):
    """Get menu item details including its restaurant information."""
    item = await get_menu_item_with_restaurant(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item

# Update menu item
@router.put("/{item_id}", response_model=MenuItemOut)
async def update_menu_item_by_id(
    item_id: int,
    item: MenuItemUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an existing menu item."""
    updated = await update_menu_item(db, item_id, item)
    if not updated:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return updated

# Delete menu item
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_menu_item_by_id(item_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a menu item."""
    deleted = await delete_menu_item(db, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return None

# Search menu items
@router.get("/search/", response_model=List[MenuItemOut])
async def search_menu_items_by_filters(
    category: Optional[str] = None,
    vegetarian: Optional[bool] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Search menu items by category and dietary preference."""
    return await search_menu_items(db, category, vegetarian, skip=skip, limit=limit)