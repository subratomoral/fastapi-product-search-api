# Day 11: FastAPI Product Search API

A beginner-friendly FastAPI project built while learning how to use **Path parameters**, **required Query parameters**, **optional Query parameters**, and validation in a practical product-search API.

## What I learned

- Creating request models with Pydantic `BaseModel` and `Field`
- Validating request data, including string length, positive values, and rating limits
- Using a Path parameter to select a product category
- Using a required Query parameter to select a brand
- Adding optional Query parameters for minimum price, maximum price, and minimum rating
- Applying business validation: `min_price` may equal `max_price`, but cannot be greater than it
- Returning meaningful HTTP errors for duplicate IDs, missing search results, and unknown products
- Deleting a product only when it actually exists

## Features

- Add a product with input validation
- List all products
- Search by category and brand, with optional price and rating filters
- Prevent duplicate product IDs
- Delete a product by ID with a correct `404 Not Found` response when it does not exist

## API endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/products` | Create a product |
| `GET` | `/products` | Get all products |
| `GET` | `/products/{category}/search` | Search products using Path and Query parameters |
| `DELETE` | `/products/{product_id}` | Delete one product by ID |

### Search example

```text
GET /products/Phone/search?brand=Apple&min_price=50000&max_price=100000&min_rating=8
```

Parameter roles:

- `Phone` is the **Path parameter** (`category`).
- `brand` is a **required Query parameter**.
- `min_price`, `max_price`, and `min_rating` are **optional Query parameters**.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open the interactive API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Example request body

```json
{
  "product_id": 69,
  "name": "iPhone",
  "category": "Phone",
  "brand": "Apple",
  "price": 85940.9,
  "rating": 8.5
}
```

## Note

This project stores data in memory, so products are reset when the server restarts. That keeps the focus on FastAPI request handling and validation.
