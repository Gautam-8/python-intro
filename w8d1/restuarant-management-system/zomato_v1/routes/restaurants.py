# FastAPI routes for Restaurant CRUD and search endpoints
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from database import get_db
from crud import (
    create_restaurant, get_restaurant, list_restaurants, update_restaurant,
    delete_restaurant, search_by_cuisine, list_active_restaurants,
    get_menu_for_restaurant, get_restaurant_reviews, calculate_restaurant_rating,
    get_restaurant_orders, get_average_menu_price, get_restaurant_with_menu
)
from schemas import (
    RestaurantCreate, RestaurantUpdate, RestaurantOut,
    MenuItemOut, ReviewOut, OrderOut
)

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

# Create new restaurant
@router.post("/", response_model=RestaurantOut, status_code=status.HTTP_201_CREATED)
async def create_new_restaurant(
    restaurant: RestaurantCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new restaurant."""
    return await create_restaurant(db, restaurant)

# Get restaurant by ID
@router.get("/{restaurant_id}", response_model=RestaurantOut)
async def get_restaurant_by_id(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    """Get details of a specific restaurant."""
    restaurant = await get_restaurant(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant

# List all restaurants with pagination
@router.get("/", response_model=List[RestaurantOut])
async def list_all_restaurants(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """List all restaurants with pagination."""
    return await list_restaurants(db, skip=skip, limit=limit)

# Update restaurant
@router.put("/{restaurant_id}", response_model=RestaurantOut)
async def update_restaurant_by_id(
    restaurant_id: int,
    restaurant: RestaurantUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an existing restaurant's details."""
    updated = await update_restaurant(db, restaurant_id, restaurant)
    if not updated:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return updated

# Delete restaurant
@router.delete("/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_restaurant_by_id(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a restaurant."""
    success = await delete_restaurant(db, restaurant_id)
    if not success:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return None

# Search restaurants by cuisine
@router.get("/search/cuisine/{cuisine_type}", response_model=List[RestaurantOut])
async def search_restaurants_by_cuisine(
    cuisine_type: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Search restaurants by cuisine type."""
    return await search_by_cuisine(db, cuisine_type, skip=skip, limit=limit)

# List active restaurants
@router.get("/active/", response_model=List[RestaurantOut])
async def get_active_restaurants(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """List only active restaurants."""
    return await list_active_restaurants(db, skip=skip, limit=limit)

# Get restaurant menu
@router.get("/{restaurant_id}/menu", response_model=List[MenuItemOut])
async def get_restaurant_menu(
    restaurant_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get the menu for a specific restaurant."""
    menu = await get_menu_for_restaurant(db, restaurant_id, skip=skip, limit=limit)
    if not menu and not await get_restaurant(db, restaurant_id):
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return menu

# Get restaurant reviews
@router.get("/{restaurant_id}/reviews", response_model=List[ReviewOut])
async def get_reviews_for_restaurant(
    restaurant_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get all reviews for a specific restaurant."""
    if not await get_restaurant(db, restaurant_id):
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return await get_restaurant_reviews(db, restaurant_id, skip=skip, limit=limit)

# Get restaurant rating
@router.get("/{restaurant_id}/rating", response_model=float)
async def get_restaurant_avg_rating(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    """Get the average rating for a restaurant."""
    if not await get_restaurant(db, restaurant_id):
        raise HTTPException(status_code=404, detail="Restaurant not found")
    rating = await calculate_restaurant_rating(db, restaurant_id)
    return rating if rating is not None else 0.0

# Get restaurant orders
@router.get("/{restaurant_id}/orders", response_model=List[OrderOut])
async def get_orders_for_restaurant(
    restaurant_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get all orders for a specific restaurant."""
    if not await get_restaurant(db, restaurant_id):
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return await get_restaurant_orders(db, restaurant_id, skip=skip, limit=limit)

# Get average menu price
@router.get("/{restaurant_id}/average-price", response_model=float)
async def get_menu_average_price(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    """Calculate and return the average menu item price for a restaurant."""
    if not await get_restaurant(db, restaurant_id):
        raise HTTPException(status_code=404, detail="Restaurant not found")
    avg_price = await get_average_menu_price(db, restaurant_id)
    return avg_price if avg_price is not None else 0.0

# Get restaurant with full menu
@router.get("/{restaurant_id}/full-details", response_model=RestaurantOut)
async def get_restaurant_full_details(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    """Get restaurant details including its complete menu."""
    restaurant = await get_restaurant_with_menu(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant

from crud import (
    create_menu_item, get_menu_item, list_menu_items, update_menu_item, delete_menu_item,
    get_menu_for_restaurant, get_menu_item_with_restaurant, get_restaurant_with_menu,
    search_menu_items, get_average_menu_price
)
from schemas import (
    RestaurantCreate, RestaurantUpdate, RestaurantOut, RestaurantWithMenu,
    MenuItemCreate, MenuItemUpdate, MenuItemOut, MenuItemWithRestaurant
)

# --- Restaurant Router ---
router = APIRouter(prefix="/restaurants", tags=["restaurants"])

# Create new restaurant
@router.post("/", response_model=RestaurantOut, status_code=status.HTTP_201_CREATED)
async def create_restaurant_view(restaurant: RestaurantCreate, db: AsyncSession = Depends(get_db)):
    return await create_restaurant(db, restaurant)

# List all restaurants (with pagination)
@router.get("/", response_model=List[RestaurantOut])
async def list_restaurants_view(
    skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), db: AsyncSession = Depends(get_db)
):
    return await list_restaurants(db, skip=skip, limit=limit)

# Get specific restaurant by ID
@router.get("/{restaurant_id}", response_model=RestaurantOut)
async def get_restaurant_view(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    restaurant = await get_restaurant(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant

# Update restaurant by ID
@router.put("/{restaurant_id}", response_model=RestaurantOut)
async def update_restaurant_view(
    restaurant_id: int, restaurant: RestaurantUpdate, db: AsyncSession = Depends(get_db)
):
    updated = await update_restaurant(db, restaurant_id, restaurant)
    if not updated:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return updated

# Delete restaurant by ID
@router.delete("/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_restaurant_view(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await delete_restaurant(db, restaurant_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return None

# Search by cuisine type
@router.get("/search", response_model=List[RestaurantOut])
async def search_by_cuisine_view(
    cuisine: str, skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), db: AsyncSession = Depends(get_db)
):
    return await search_by_cuisine(db, cuisine, skip=skip, limit=limit)

# List only active restaurants
@router.get("/active", response_model=List[RestaurantOut])
async def list_active_restaurants_view(
    skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), db: AsyncSession = Depends(get_db)
):
    return await list_active_restaurants(db, skip=skip, limit=limit)

# --- Menu Item Endpoints under /restaurants ---

# Add menu item to restaurant
@router.post("/{restaurant_id}/menu-items/", response_model=MenuItemOut, status_code=status.HTTP_201_CREATED)
async def add_menu_item(restaurant_id: int, item: MenuItemCreate, db: AsyncSession = Depends(get_db)):
    return await create_menu_item(db, restaurant_id, item)

# Get all menu items for a restaurant
@router.get("/{restaurant_id}/menu", response_model=List[MenuItemOut])
async def get_menu(restaurant_id: int, skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), db: AsyncSession = Depends(get_db)):
    return await get_menu_for_restaurant(db, restaurant_id, skip=skip, limit=limit)

# Get restaurant with all menu items
@router.get("/{restaurant_id}/with-menu", response_model=RestaurantWithMenu)
async def get_restaurant_menu(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    restaurant = await get_restaurant_with_menu(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant

# Get average menu price per restaurant
@router.get("/{restaurant_id}/menu/average-price", response_model=float)
async def average_menu_price(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    avg = await get_average_menu_price(db, restaurant_id)
    if avg is None:
        raise HTTPException(status_code=404, detail="No menu items found for this restaurant")
    return avg

# --- Standalone Menu Item Router ---
menu_router = APIRouter(prefix="/menu-items", tags=["menu-items"])

# List all menu items
@menu_router.get("/", response_model=List[MenuItemOut])
async def list_menu_items_view(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), db: AsyncSession = Depends(get_db)):
    return await list_menu_items(db, skip=skip, limit=limit)

# Get specific menu item
@menu_router.get("/{item_id}", response_model=MenuItemOut)
async def get_menu_item_view(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await get_menu_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item

# Get menu item with restaurant details
@menu_router.get("/{item_id}/with-restaurant", response_model=MenuItemWithRestaurant)
async def get_menu_item_with_restaurant_view(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await get_menu_item_with_restaurant(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item

# Update menu item
@menu_router.put("/{item_id}", response_model=MenuItemOut)
async def update_menu_item_view(item_id: int, item: MenuItemUpdate, db: AsyncSession = Depends(get_db)):
    updated = await update_menu_item(db, item_id, item)
    if not updated:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return updated

# Delete menu item
@menu_router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_menu_item_view(item_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await delete_menu_item(db, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return None

# Search menu items by category and vegetarian
@menu_router.get("/search", response_model=List[MenuItemOut])
async def search_menu_items_view(
    category: Optional[str] = None,
    vegetarian: Optional[bool] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    return await search_menu_items(db, category, vegetarian, skip=skip, limit=limit)
