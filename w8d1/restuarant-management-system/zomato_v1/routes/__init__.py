"""
Routes package for the restaurant management system.
Contains all the API route handlers for different entities.
"""

from .restaurants import router as restaurant_router
from .menu_items import router as menu_router
from .orders import router as order_router
from .customers import router as customer_router
from .reviews import router as review_router

__all__ = [
    'restaurant_router',
    'menu_router',
    'order_router',
    'customer_router',
    'review_router'
]
