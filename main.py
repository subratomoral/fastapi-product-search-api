from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Path, Query
from typing import Optional

app = FastAPI(
    title="Product Search Api", description="Search product with diff validation"
)


class Product(BaseModel):
    product_id: int = Field(gt=0, description="product id", examples=[69])
    name: str = Field(
        min_length=3, max_length=20, description="enter product", examples=["iphone"]
    )
    category: str = Field(
        min_length=3, max_length=20, description="enter category", examples=["Phone"]
    )
    brand: str = Field(
        min_length=3,
        max_length=20,
        description="enter product brand",
        examples=["Apple"],
    )
    price: float = Field(gt=0, description="enter price", examples=[85940.9])
    rating: float = Field(gt=0, le=10, description="product rating", examples=[8.5])


products_data: list[Product] = []


@app.post("/products", response_model=Product, tags=["Products"])
def post_data(products: Product):
    for data in products_data:
        if data.product_id == products.product_id:
            raise HTTPException(status_code=409, detail="duplicate id")
    products_data.append(products)
    return products


@app.get("/products/getAll", response_model=list[Product], tags=["Product"])
def getAll():
    return products_data


# @app.get("/products/{category}/search", response_model=list[Product], tags=["Product"])
# def getByCategory(
#     category: str = Path(..., min_length=3, max_length=20, examples=["Phone"])
# ):
#     CategoryList: list[Product] = []
#     category = category.strip().lower()
#     for data in products_data:
#         if data.category.strip().lower() == category:
#             CategoryList.append(data)
#     if not CategoryList:
#         raise HTTPException(status_code=404, detail="data not found")
#     return CategoryList


# @app.get("/products/{category}/", response_model=list[Product], tags=["Product"])
# def getByCategoryAndBrand(
#     category: str = Path(..., min_length=3, max_length=20, examples=["Phone"]),
#     brand: str = Query(..., min_length=3, max_length=20, examples=["Apple"]),
# ):
#     CategoryList: list[Product] = []
#     for data in products_data:
#         if (
#             data.category.strip().lower() == category.strip().lower()
#             and data.brand.strip().lower() == brand.lower().strip()
#         ):
#             CategoryList.append(data)
#     if not CategoryList:
#         raise HTTPException(status_code=404, detail="data not found")
#     return CategoryList


@app.get("/products/{category}/", response_model=list[Product], tags=["product"])
def getByCategoryAndBrandAndOptionalMaxPrice(
    category: str = Path(..., min_length=3, max_length=20, examples=["Phone"]),
    brand: str = Query(..., min_length=3, max_length=20, examples=["Apple"]),
    min_price: Optional[float] = Query(default=None, gt=0, examples=[100]),
    max_price: Optional[float] = Query(default=None, gt=0, examples=[10000]),
    min_rating: Optional[float] = Query(default=None, gt=0, le=10, examples=[6.8]),
):
    if min_price is not None and max_price is not None:
        if min_price >= max_price:
            raise HTTPException(
            status_code=400, detail="min_price and max_price can't same"
        )
    CategoryList: list[Product] = []
    for data in products_data:
        if (
            data.category.strip().lower() == category.strip().lower()
            and data.brand.strip().lower() == brand.strip().lower()
            and (min_price is None or min_price <= data.price)
            and (max_price is None or data.price <= max_price)
            and (min_rating is None or data.rating >= min_rating)
        ):
            CategoryList.append(data)
    if not CategoryList:
        raise HTTPException(status_code=404, detail="Data not Found")
    return CategoryList


@app.delete("/products/delete/{id}", tags=["Product"])
def DeleteData(id: int = Path(..., gt=0, examples=[1])):
    for data in products_data:
        if data.product_id == id:
            products_data.remove(data)
            return {"status": "data remove Successfully"}
    raise HTTPException(status_code=404, detail="data not found")
