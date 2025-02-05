from fastapi import FastAPI
from app.routers import customers, orders, analytics
from app.database import engine, Base

app = FastAPI()

# Include routers
app.include_router(analytics.router)
app.include_router(customers.router)
app.include_router(orders.router)
