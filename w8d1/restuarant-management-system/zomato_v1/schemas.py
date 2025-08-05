# Import required modules from Pydantic and typing

# Import required modules from Pydantic and typing
from pydantic import BaseModel, Field, validator, condecimal
from typing import Optional, List
from datetime import time, datetime
import re


# Base schema for Restaurant (shared fields)
class RestaurantBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, description="Restaurant name")
    description: Optional[str] = Field(None, description="Description of the restaurant")
    cuisine_type: str = Field(..., min_length=2, max_length=50, description="Cuisine type")
    address: str = Field(..., min_length=3, max_length=255, description="Address")
    phone_number: str = Field(..., description="Phone number")
    rating: float = Field(0.0, ge=0.0, le=5.0, description="Rating between 0.0 and 5.0")
    is_active: Optional[bool] = Field(True, description="Is the restaurant active?")
    opening_time: time = Field(..., description="Opening time")
    closing_time: time = Field(..., description="Closing time")

    # Validate phone number format
    @validator('phone_number')
    def validate_phone(cls, v):
        pattern = r"^\+?\d{10,15}$"  # Accepts international format
        if not re.match(pattern, v):
            raise ValueError("Invalid phone number format")
        return v


# Schema for creating a restaurant
class RestaurantCreate(RestaurantBase):
    pass


# Schema for updating a restaurant (all fields optional)
class RestaurantUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    cuisine_type: Optional[str] = Field(None, min_length=2, max_length=50)
    address: Optional[str] = Field(None, min_length=3, max_length=255)
    phone_number: Optional[str] = None
    rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    is_active: Optional[bool] = None
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None

    @validator('phone_number')
    def validate_phone(cls, v):
        if v is None:
            return v
        pattern = r"^\+?\d{10,15}$"
        if not re.match(pattern, v):
            raise ValueError("Invalid phone number format")
        return v


# --- Menu Item Schemas ---
from decimal import Decimal
class MenuItemBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, description="Menu item name")
    description: Optional[str] = Field(None, description="Description of the menu item")
    price: Decimal = Field(..., gt=0, description="Price, must be positive")
    category: str = Field(..., min_length=2, max_length=50, description="Category")
    is_vegetarian: Optional[bool] = Field(False, description="Is vegetarian?")
    is_vegan: Optional[bool] = Field(False, description="Is vegan?")
    is_available: Optional[bool] = Field(True, description="Is available?")
    preparation_time: Optional[int] = Field(None, ge=0, description="Preparation time in minutes")

    @validator('price')
    def validate_price(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Price must be positive')
        return v

# --- Customer Schemas ---
class CustomerBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., description="Email address")
    phone_number: str = Field(..., description="Phone number")
    address: str = Field(..., min_length=3, max_length=255)
    is_active: Optional[bool] = Field(True)

    @validator('phone_number')
    def validate_phone(cls, v):
        pattern = r"^\+?\d{10,15}$"
        if not re.match(pattern, v):
            raise ValueError("Invalid phone number format")
        return v

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    is_active: Optional[bool] = None

    @validator('phone_number')
    def validate_phone(cls, v):
        if v is None:
            return v
        pattern = r"^\+?\d{10,15}$"
        if not re.match(pattern, v):
            raise ValueError("Invalid phone number format")
        return v

class CustomerOut(CustomerBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    class Config:
        orm_mode = True

# --- Order Item Schemas (Association) ---
class OrderItemBase(BaseModel):
    menu_item_id: int
    quantity: int = Field(..., gt=0)
    item_price: Decimal = Field(..., gt=0)
    special_requests: Optional[str] = None

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(BaseModel):
    quantity: Optional[int] = Field(None, gt=0)
    item_price: Optional[Decimal] = Field(None, gt=0)
    special_requests: Optional[str] = None

class OrderItemOut(OrderItemBase):
    id: int
    menu_item: Optional['MenuItemOut']
    class Config:
        orm_mode = True

# --- Order Schemas ---
class OrderBase(BaseModel):
    restaurant_id: int
    delivery_address: str = Field(..., min_length=3, max_length=255)
    special_instructions: Optional[str] = None

class OrderCreate(OrderBase):
    order_items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    order_status: Optional[str] = None
    delivery_address: Optional[str] = None
    special_instructions: Optional[str] = None

class OrderOut(OrderBase):
    id: int
    customer_id: int
    order_status: str
    total_amount: Decimal
    order_date: datetime
    delivery_time: Optional[datetime]
    order_items: List['OrderItemOut'] = []
    restaurant: Optional['RestaurantOut']
    customer: Optional['CustomerOut']
    class Config:
        orm_mode = True

# --- Review Schemas ---
class ReviewBase(BaseModel):
    rating: float = Field(..., ge=0.0, le=5.0)
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    comment: Optional[str] = None

class ReviewOut(ReviewBase):
    id: int
    customer_id: int
    restaurant_id: int
    order_id: int
    created_at: datetime
    customer: Optional['CustomerOut']
    restaurant: Optional['RestaurantOut']
    order: Optional['OrderOut']
    class Config:
        orm_mode = True

# Schema for creating a menu item
class MenuItemCreate(MenuItemBase):
    pass

# Schema for updating a menu item
class MenuItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=2, max_length=50)
    is_vegetarian: Optional[bool] = None
    is_vegan: Optional[bool] = None
    is_available: Optional[bool] = None
    preparation_time: Optional[int] = Field(None, ge=0)

    @validator('price')
    def validate_price(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Price must be positive')
        return v

# Response schema for MenuItem
class MenuItemOut(MenuItemBase):
    id: int
    restaurant_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

# Nested response: MenuItem with Restaurant details
class MenuItemWithRestaurant(MenuItemOut):
    restaurant: Optional['RestaurantOut']

# Nested response: Restaurant with menu items
class RestaurantWithMenu(RestaurantBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    menu_items: List[MenuItemOut] = []

    class Config:
        orm_mode = True

# Schema for response (includes id, timestamps)
class RestaurantOut(RestaurantBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

# For forward references in nested schemas
MenuItemWithRestaurant.update_forward_refs()
OrderItemOut.update_forward_refs()
OrderOut.update_forward_refs()
ReviewOut.update_forward_refs()
