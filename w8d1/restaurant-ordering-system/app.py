from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator, root_validator
from typing import List, Optional
from enum import Enum
from decimal import Decimal
import re

# FoodCategory enum
class FoodCategory(str, Enum):
    APPETIZER = "appetizer"
    MAIN_COURSE = "main_course"
    DESSERT = "dessert"
    BEVERAGE = "beverage"
    SALAD = "salad"

# FoodItem Pydantic model
class FoodItem(BaseModel):
    id: int
    name: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=10, max_length=500)
    category: FoodCategory
    price: Decimal = Field(..., gt=0, max_digits=5, decimal_places=2)
    is_available: bool = True
    preparation_time: int = Field(..., ge=1, le=120)
    ingredients: List[str] = Field(..., min_items=1)
    calories: Optional[int] = Field(None, gt=0)
    is_vegetarian: bool = False
    is_spicy: bool = False

    @validator("name")
    def name_must_be_letters_and_spaces(cls, v):
        if not re.fullmatch(r"[A-Za-z ]+", v):
            raise ValueError("Name must contain only letters and spaces.")
        return v

    @validator("price")
    def price_range(cls, v):
        if v < Decimal("1.00") or v > Decimal("100.00"):
            raise ValueError("Price must be between $1.00 and $100.00.")
        if v.quantize(Decimal('0.01')) != v:
            raise ValueError("Price must have at most 2 decimal places.")
        return v

    @validator("preparation_time")
    def beverage_prep_time(cls, v, values):
        if values.get("category") == FoodCategory.BEVERAGE and v > 10:
            raise ValueError("Preparation time for beverages must be ≤ 10 minutes.")
        return v

    @validator("is_spicy")
    def dessert_beverage_not_spicy(cls, v, values):
        if v and values.get("category") in [FoodCategory.DESSERT, FoodCategory.BEVERAGE]:
            raise ValueError("Desserts and beverages cannot be marked as spicy.")
        return v

    @validator("ingredients")
    def must_have_ingredients(cls, v):
        if not v or not isinstance(v, list) or len(v) == 0:
            raise ValueError("At least one ingredient is required.")
        return v

    @root_validator
    def vegetarian_calories_limit(cls, values):
        if values.get("is_vegetarian") and values.get("calories") is not None:
            if values["calories"] >= 800:
                raise ValueError("Vegetarian items must have calories < 800.")
        return values

    @property
    def price_category(self):
        if self.price < Decimal("10.00"):
            return "Budget"
        elif self.price <= Decimal("25.00"):
            return "Mid-range"
        else:
            return "Premium"

    @property
    def dietary_info(self):
        info = []
        if self.is_vegetarian:
            info.append("Vegetarian")
        if self.is_spicy:
            info.append("Spicy")
        return info

# In-memory database
menu_db = {}
app = FastAPI()

# Helper for auto-incrementing IDs
def get_next_id():
    if menu_db:
        return max(menu_db.keys()) + 1
    return 1

# GET /menu - Get all menu items
@app.get("/menu", response_model=List[FoodItem])
def get_menu():
    return list(menu_db.values())

# GET /menu/{item_id} - Get specific menu item
@app.get("/menu/{item_id}", response_model=FoodItem)
def get_menu_item(item_id: int):
    item = menu_db.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item

# POST /menu - Add new menu item (staff only)
@app.post("/menu", response_model=FoodItem, status_code=201)
def add_menu_item(item: FoodItem):
    if item.id in menu_db:
        raise HTTPException(status_code=400, detail="ID already exists")
    # Auto-generate ID if not provided or 0
    if not item.id or item.id in menu_db:
        item.id = get_next_id()
    menu_db[item.id] = item
    return item

# PUT /menu/{item_id} - Update existing menu item
@app.put("/menu/{item_id}", response_model=FoodItem)
def update_menu_item(item_id: int, item: FoodItem):
    if item_id not in menu_db:
        raise HTTPException(status_code=404, detail="Menu item not found")
    if item.id != item_id:
        raise HTTPException(status_code=400, detail="ID in path and body must match")
    menu_db[item_id] = item
    return item

# DELETE /menu/{item_id} - Remove menu item from menu
@app.delete("/menu/{item_id}", status_code=204)
def delete_menu_item(item_id: int):
    if item_id not in menu_db:
        raise HTTPException(status_code=404, detail="Menu item not found")
    del menu_db[item_id]

# GET /menu/category/{category} - Get items by category
@app.get("/menu/category/{category}", response_model=List[FoodItem])
def get_menu_by_category(category: FoodCategory):
    return [item for item in menu_db.values() if item.category == category]
