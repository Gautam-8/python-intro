# Import and include all routers here for main.py
from .restaurants import router as restaurant_router
from .menu_items import router as menu_item_router
from .customers import router as customer_router
from .orders import router as order_router
from .reviews import router as review_router
