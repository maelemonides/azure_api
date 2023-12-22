from fastapi import FastAPI, HTTPException
from models import Product, ProductCreate
from db import products_collection
from bson import ObjectId
from typing import List
import random


app = FastAPI()

# Function to seed initial products
def seed_initial_products():
    products = [
        {"name": "Laptop", "price": 1000},
        {"name": "Smartphone", "price": 500},
        {"name": "Headphones", "price": 200},
        {"name": "Tablet", "price": 300},
        {"name": "Camera", "price": 700}
    ]
    for product in products:
        products_collection.insert_one(product)

# Seed initial products when the application starts
seed_initial_products()

@app.get("/products/random", response_model=Product)
async def get_random_product():
    # Clear all products
    products_collection.delete_many({})
    # Seed initial products
    seed_initial_products()
    # Fetch a random product
    count = products_collection.count_documents({})
    if count == 0:
        raise HTTPException(status_code=404, detail="No products found")
    random_index = random.randint(0, count - 1)
    product = products_collection.find().limit(1).skip(random_index).next()
    # Convert the '_id' field from ObjectId to string
    product['_id'] = str(product['_id'])
    return Product(**product)
    
@app.delete("/products/clear")
async def clear_all_products():
    """Clear all products."""
    result = products_collection.delete_many({})
    return {"message": f"Deleted {result.deleted_count} products"}

@app.get("/products/", response_model=List[Product])
async def get_all_products():
    """Return all products."""
    products = list(products_collection.find({}))
    for product in products:
        product['_id'] = str(product['_id'])  # Convert ObjectId to string
    return products


@app.post("/products/", response_model=Product)
async def create_product(product: ProductCreate):
    """Create a new product."""
    new_product = product.dict()
    
    # Insert the new product into the database
    inserted_product_id = products_collection.insert_one(new_product).inserted_id
    
    # Convert the ObjectId to its string representation
    inserted_product_id_str = str(inserted_product_id)
    
    # Fetch the newly inserted product from the database using the string ID
    created_product = products_collection.find_one({"_id": ObjectId(inserted_product_id_str)})
    
    if created_product:
        # Manually update the '_id' field with its string representation
        created_product['_id'] = inserted_product_id_str
        
        return Product(**created_product)
    else:
        raise HTTPException(status_code=400, detail="Failed to create product")
