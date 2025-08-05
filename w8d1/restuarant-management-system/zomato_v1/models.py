
# Import necessary modules from SQLAlchemy and other libraries
from sqlalchemy import Column, Integer, String, Float, Boolean, Time, DateTime, func, ForeignKey, Numeric
from sqlalchemy.orm import relationship, declarative_base

# Create a base class for declarative class definitions
Base = declarative_base()

# Define the Restaurant model/table
class Restaurant(Base):
    __tablename__ = "restaurants"  # Table name in the database

    id = Column(Integer, primary_key=True, index=True)  # Primary key, auto-incremented
    name = Column(String(100), unique=True, nullable=False)  # Restaurant name, required, unique, 3-100 chars
    description = Column(String, nullable=True)  # Optional description
    cuisine_type = Column(String(50), nullable=False)  # Cuisine type, required
    address = Column(String(255), nullable=False)  # Address, required
    phone_number = Column(String(20), nullable=False)  # Phone number, required, validated in schema
    rating = Column(Float, default=0.0)  # Rating, float, 0.0-5.0, default 0.0
    is_active = Column(Boolean, default=True)  # Is the restaurant active? Default True
    opening_time = Column(Time, nullable=False)  # Opening time, required
    closing_time = Column(Time, nullable=False)  # Closing time, required
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Timestamp of creation
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())  # Timestamp of last update

    # Relationship: One restaurant has many menu items
    menu_items = relationship(
        "MenuItem",
        back_populates="restaurant",
        cascade="all, delete-orphan"
    )

# Define the MenuItem model/table
class MenuItem(Base):
    __tablename__ = "menu_items"  # Table name in the database

    id = Column(Integer, primary_key=True, index=True)  # Primary key
    name = Column(String(100), nullable=False)  # Menu item name, required, 3-100 chars
    description = Column(String, nullable=True)  # Optional description
    price = Column(Numeric(10, 2), nullable=False)  # Price, required, decimal with 2 places
    category = Column(String(50), nullable=False)  # Category, required
    is_vegetarian = Column(Boolean, default=False)  # Is vegetarian? Default False
    is_vegan = Column(Boolean, default=False)  # Is vegan? Default False
    is_available = Column(Boolean, default=True)  # Is available? Default True
    preparation_time = Column(Integer, nullable=True)  # Preparation time in minutes
    restaurant_id = Column(Integer, ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False)  # FK to Restaurant
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Timestamp of creation
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())  # Timestamp of last update

    # Relationship: Each menu item belongs to a restaurant
    restaurant = relationship("Restaurant", back_populates="menu_items")

# --- Customer Model ---
class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone_number = Column(String(20), nullable=False)
    address = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    orders = relationship("Order", back_populates="customer", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="customer", cascade="all, delete-orphan")

# --- Order Model ---
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False)
    order_status = Column(String(30), nullable=False, default="placed")
    total_amount = Column(Numeric(10, 2), nullable=False)
    delivery_address = Column(String(255), nullable=False)
    special_instructions = Column(String, nullable=True)
    order_date = Column(DateTime(timezone=True), server_default=func.now())
    delivery_time = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    customer = relationship("Customer", back_populates="orders")
    restaurant = relationship("Restaurant")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    review = relationship("Review", back_populates="order", uselist=False)

# --- OrderItem Model (Association Table) ---
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False)
    item_price = Column(Numeric(10, 2), nullable=False)
    special_requests = Column(String, nullable=True)

    # Relationships
    order = relationship("Order", back_populates="order_items")
    menu_item = relationship("MenuItem")

# --- Review Model ---
class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Float, nullable=False)
    comment = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    customer = relationship("Customer", back_populates="reviews")
    restaurant = relationship("Restaurant")
    order = relationship("Order", back_populates="review")
