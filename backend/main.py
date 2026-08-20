from fastapi import FastAPI
import json
from pathlib import Path

app = FastAPI(title="VirtualShop AI API")

PRODUCTS_FILE = Path(__file__).parent.parent / "data" / "products.json"


def load_products():
    with open(PRODUCTS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


@app.get("/")
def root():
    return {"message": "VirtualShop AI API is running"}


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/products")
def get_products():
    return load_products()