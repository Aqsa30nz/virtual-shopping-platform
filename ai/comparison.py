import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


# ---------------------------------------------------------
# Environment
# ---------------------------------------------------------

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY not found in .env"
    )


# ---------------------------------------------------------
# Gemini client
# ---------------------------------------------------------

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ---------------------------------------------------------
# AI Product Comparison
# ---------------------------------------------------------

def compare_products(products):
    """
    Compare furniture products using Gemini.

    Product specifications remain the source of truth.
    Gemini interprets the supplied data and produces
    a structured shopping recommendation.
    """

    if len(products) < 2:
        raise ValueError(
            "At least two products are required for comparison."
        )

    # -----------------------------------------------------
    # Prepare product data
    # -----------------------------------------------------

    product_data = []

    for product in products:
        product_data.append({
            "name": product["name"],
            "category": product["category"],
            "price": product["price"],
            "dimensions": product["dimensions"],
            "material": product["material"],
            "color": product["color"],
            "style": product["style"],
        })

    products_json = json.dumps(
        product_data,
        indent=2,
        ensure_ascii=False
    )

    # -----------------------------------------------------
    # Prompt
    # -----------------------------------------------------

    prompt = f"""
You are an AI shopping assistant for a virtual furniture
shopping platform.

Compare the following furniture products.

PRODUCT DATA:
{products_json}

Use ONLY the supplied product data.

Analyze:

1. Price and value
2. Dimensions and space requirements
3. Material
4. Color
5. Style
6. Category and intended use
7. Advantages of each product
8. Trade-offs of each product

Determine:

- best value
- best for smaller spaces
- best style match
- overall recommendation
- reasoning behind the recommendation

Important rules:

- Do NOT invent specifications.
- Do NOT invent customer reviews.
- Do NOT invent comfort claims.
- Do NOT invent durability claims.
- Do NOT invent measurements.
- Do NOT claim features that are not present in the data.
- Base every conclusion only on the supplied information.

Return ONLY valid JSON.

The JSON MUST have exactly this structure:

{{
    "summary": "Short comparison summary",
    "best_value": "Exact product name",
    "best_for_small_spaces": "Exact product name",
    "best_style_match": "Exact product name",
    "recommendation": "Exact product name",
    "reasoning": "Clear explanation of the overall recommendation",
    "tradeoffs": [
        {{
            "product": "Exact product name",
            "advantages": [
                "advantage based on supplied data",
                "advantage based on supplied data"
            ],
            "tradeoffs": [
                "trade-off based on supplied data",
                "trade-off based on supplied data"
            ]
        }}
    ]
}}
"""

    # -----------------------------------------------------
    # Gemini request
    # -----------------------------------------------------

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
        ),
    )

    # -----------------------------------------------------
    # Validate response
    # -----------------------------------------------------

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    try:
        comparison = json.loads(
            response.text
        )

    except json.JSONDecodeError as error:
        raise RuntimeError(
            "Gemini returned invalid JSON."
        ) from error

    return comparison