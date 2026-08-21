from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.image_analysis import analyze_room
from ai.comparison import compare_products

import json
import base64

from pathlib import Path


# ---------------------------------------------------------
# Comparison request model
# ---------------------------------------------------------

class CompareRequest(BaseModel):
    product_ids: list[str]


# ---------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------

app = FastAPI(
    title="VirtualShop AI API"
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Products
# ---------------------------------------------------------

PRODUCTS_FILE = (
    Path(__file__).parent.parent
    / "data"
    / "products.json"
)


def load_products():

    with open(
        PRODUCTS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ---------------------------------------------------------
# Root
# ---------------------------------------------------------

@app.get("/")
def root():

    return {
        "message": "VirtualShop AI API is running"
    }


# ---------------------------------------------------------
# Health
# ---------------------------------------------------------

@app.get("/api/health")
def health():

    return {
        "status": "ok"
    }


# ---------------------------------------------------------
# Products API
# ---------------------------------------------------------

@app.get("/api/products")
def get_products():

    return load_products()


# ---------------------------------------------------------
# AI Product Comparison
# ---------------------------------------------------------

@app.post("/api/compare")
async def compare(
    request: CompareRequest
):

    # -----------------------------------------------------
    # 1. Get product IDs
    # -----------------------------------------------------

    product_ids = request.product_ids


    # -----------------------------------------------------
    # 2. Validate selection
    # -----------------------------------------------------

    if len(product_ids) < 2:

        return {
            "success": False,
            "message": (
                "Select at least two products "
                "to compare."
            )
        }


    # -----------------------------------------------------
    # 3. Load products
    # -----------------------------------------------------

    products = load_products()


    # -----------------------------------------------------
    # 4. Find selected products
    # -----------------------------------------------------

    selected_products = [
        product
        for product in products
        if product["id"] in product_ids
    ]


    # -----------------------------------------------------
    # 5. Validate products
    # -----------------------------------------------------

    if len(selected_products) != len(product_ids):

        return {
            "success": False,
            "message": (
                "One or more selected products "
                "were not found."
            )
        }


    # -----------------------------------------------------
    # 6. Run Gemini comparison
    # -----------------------------------------------------

    try:

        comparison = compare_products(
            selected_products
        )

    except Exception as error:

        print(
            "AI comparison error:",
            error
        )

        return {
            "success": False,
            "message": (
                "Unable to generate "
                "AI comparison."
            )
        }


    # -----------------------------------------------------
    # 7. Return comparison
    # -----------------------------------------------------

    return {

        "success": True,

        "products": selected_products,

        "comparison": comparison
    }


# ---------------------------------------------------------
# AI Room Visualization
# ---------------------------------------------------------

@app.post("/api/visualize")
async def visualize(
    room_image: UploadFile = File(...),
    product_id: str = Form(...),
):

    # -----------------------------------------------------
    # 1. Validate image type
    # -----------------------------------------------------

    if (
        not room_image.content_type
        or not room_image.content_type.startswith(
            "image/"
        )
    ):

        return {
            "success": False,
            "message": (
                "Please upload a valid image."
            )
        }


    # -----------------------------------------------------
    # 2. Find selected product
    # -----------------------------------------------------

    products = load_products()

    product = next(
        (
            item
            for item in products
            if item["id"] == product_id
        ),
        None
    )


    if product is None:

        return {
            "success": False,
            "message": "Product not found."
        }


    # -----------------------------------------------------
    # 3. Read uploaded image
    # -----------------------------------------------------

    image_bytes = await room_image.read()


    # -----------------------------------------------------
    # 4. Validate uploaded image
    # -----------------------------------------------------

    if len(image_bytes) == 0:

        return {
            "success": False,
            "message": (
                "Uploaded image is empty."
            )
        }


    # -----------------------------------------------------
    # 5. Analyze room
    # -----------------------------------------------------

    try:

        analysis = analyze_room(
            image_bytes,
            product
        )

    except Exception as error:

        print(
            "Room visualization error:",
            error
        )

        return {
            "success": False,
            "message": (
                "Unable to process "
                "the room image."
            )
        }


    if analysis is None:

        return {
            "success": False,
            "message": (
                "Unable to process image."
            )
        }


    # -----------------------------------------------------
    # 6. Get visualization
    # -----------------------------------------------------

    visualization = analysis.get(
        "visualization"
    )


    if visualization is None:

        return {
            "success": False,
            "message": (
                "Visualization was not generated."
            )
        }


    # -----------------------------------------------------
    # 7. Convert visualization to Base64
    # -----------------------------------------------------

    visualization_base64 = base64.b64encode(
        visualization
    ).decode("utf-8")


    # -----------------------------------------------------
    # 8. Remove binary visualization
    # -----------------------------------------------------

    analysis.pop(
        "visualization",
        None
    )


    # -----------------------------------------------------
    # 9. Return response
    # -----------------------------------------------------

    return {

        "success": True,

        "message": (
            "Room analyzed successfully."
        ),

        "product": product,

        "analysis": analysis,

        "visualization": (
            "data:image/jpeg;base64,"
            + visualization_base64
        )
    }