from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from pathlib import Path

app = FastAPI(title="VirtualShop AI API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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