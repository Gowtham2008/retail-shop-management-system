'''
#### learing code###

from fastapi import FastAPI, status,HTTPException,Depends
from pydantic import BaseModel, Field


app = FastAPI()


class ProductCreate(BaseModel):
    name: str =Field(min_length=1,max_length=100)
    price: float = Field(gt=0, description="Price must be greater than zero")
class ProductResponse(BaseModel):
    id:int
    name:str
    price:float


products = [
    {"id": 1, "name": "Apple", "price": 100},
    {"id": 2, "name": "Banana", "price": 60},
    {"id": 3, "name": "Orange", "price": 80}
]


@app.get("/")
def home():
    return {"message": "Welcome to Retail shop"}


# GET - all products
@app.get("/products")
def get_products():
    return products 


# POST - add product
@app.post("/products", status_code=status.HTTP_201_CREATED,response_model=ProductCreate )
def add_product(product: ProductCreate):
    new_id=len(products)+1
    new_product={
        "id": new_id,
        "name": product.name,
        "price": product.price
    }
    products.append(new_product)
    return new_product 

# GET - product by ID (Path Parameter)
@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product

    raise HTTPException(status_code=404,detail="product not found ")



# PUT - update product
@app.put("/products/{product_id}")
def update_product(product_id: int,product: ProductCreate):
    for item in products:
        if item["id"] == product_id:
            item["name"] = product.name
            item["price"] = product.price
            return item

    raise HTTPException(status_code=404,detail="product not found ")
    

# PATCH - update product
#why product_update class becoz in class Product req all values so we create saparate class for patch
class ProductUpdate(BaseModel):
    name: str | None = None
    price: float | None = None

@app.patch("/products/{product_id}")
def patch_product(product_id: int, product: ProductUpdate):
    for item in products:
        if item["id"] == product_id:

            if product.name is not None:
                item["name"] = product.name

            if product.price is not None:
                item["price"] = product.price

            return item


    raise HTTPException(status_code=404,detail="product not found ")
    
#delete product
@app.delete("/products/{product_id}")
def delete_product(product_id:int):
    for product in products:
        if product["id"]==product_id:
            products.remove(product)
            return {"message":"Product deleted successfully"}
    raise HTTPException(status_code=404,detail="Product not found")      

#dependncy injection
def get_shop():
    return {"shop is open 24/7"}

@app.get("/test")
def test(shop=Depends(get_shop)):
    return shop  
  
'''
from fastapi import FastAPI
from database.connection import Base, engine
from database.models import Product
from routers import product,order,customer,category

Base.metadata.create_all(bind=engine)

app = FastAPI()

 


app.include_router(product.router)   
app.include_router(order.router)
app.include_router(customer.router)
app.include_router(category.router)

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/",StaticFiles(directory="frontend", html=True),name="frontend")