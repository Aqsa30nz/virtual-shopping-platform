from fastapi import FastAPI, File, UploadFile, Form
from image_analysis import analyze_room
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
    

@app.post("/api/visualize")
async def visualize(
    room_image: UploadFile = File(...),
    product_id: str = Form(...),
):
    # Validate image type
    if not room_image.content_type or not room_image.content_type.startswith("image/"):
        return {
            "success": False,
            "message": "Please upload a valid image."
        }

    # Find selected product
    products = load_products()

    product = next(
        (item for item in products if item["id"] == product_id),
        None
    )

    if product is None:
        return {
            "success": False,
            "message": "Product not found."
        }

    # Read uploaded image
    image_bytes = await room_image.read()

    # Basic validation
    if len(image_bytes) == 0:
        return {
            "success": False,
            "message": "Uploaded image is empty."
        }
        
    analysis = analyze_room(image_bytes, product)

    if analysis is None:
        return {
            "success": False,
            "message": "Unable to process image."
        }

    return {
        "success": True,
        "message": "Room analyzed successfully.",
        "product": product,
        "analysis": analysis
    }