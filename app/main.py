from fastapi import FastAPI
from app.routers import customers, orders, analytics
from app.database import engine, Base

app = FastAPI()

# Include routers
app.include_router(customers.router)
app.include_router(orders.router)
app.include_router(analytics.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Pier 2 Imports API"}
