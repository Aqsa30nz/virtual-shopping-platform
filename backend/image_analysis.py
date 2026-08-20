import os
from pathlib import Path

import cv2
import numpy as np
import replicate
import httpx
from dotenv import load_dotenv


# ---------------------------------------------------------
# Environment
# ---------------------------------------------------------

load_dotenv()

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

if not REPLICATE_API_TOKEN:
    raise RuntimeError(
        "REPLICATE_API_TOKEN not found in .env"
    )


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).parent

PRODUCT_IMAGES_DIR = (
    BASE_DIR / "product_images"
)

FRONTEND_PRODUCTS_DIR = (
    BASE_DIR.parent
    / "frontend"
    / "public"
    / "products"
)


# ---------------------------------------------------------
# Replicate client
#
# HTTPTransport(verify=False) is intentional because
# this configuration was already verified to work
# in your environment.
# ---------------------------------------------------------

transport = httpx.HTTPTransport(
    verify=False
)

client = replicate.Client(
    api_token=REPLICATE_API_TOKEN,
    transport=transport
)


# ---------------------------------------------------------
# Find product image
# ---------------------------------------------------------

def find_product_image(product):
    """
    Find the local image belonging to the selected product.

    Priority:
    1. backend/product_images/
    2. frontend/public/products/
    """

    image_url = product.get("image")

    if not image_url:
        return None

    filename = Path(image_url).name

    backend_path = (
        PRODUCT_IMAGES_DIR / filename
    )

    if backend_path.exists():
        return backend_path

    frontend_path = (
        FRONTEND_PRODUCTS_DIR / filename
    )

    if frontend_path.exists():
        return frontend_path

    return None


# ---------------------------------------------------------
# Calculate room metrics
# ---------------------------------------------------------

def calculate_room_metrics(image):
    """
    Calculate simple computer-vision metrics used by the
    prototype's room analysis.
    """

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    brightness = int(
        np.mean(gray)
    )

    edges = cv2.Canny(
        gray,
        100,
        200
    )

    edge_density = float(
        np.mean(edges > 0)
    )

    height = gray.shape[0]

    lower_region = gray[
        int(height * 0.4):,
        :
    ]

    lower_edges = cv2.Canny(
        lower_region,
        100,
        200
    )

    lower_edge_density = float(
        np.mean(lower_edges > 0)
    )

    return {
        "brightness": brightness,
        "edge_density": edge_density,
        "lower_edge_density": lower_edge_density,
    }


# ---------------------------------------------------------
# Determine room tone
# ---------------------------------------------------------

def determine_room_tone(image):

    avg_color = np.mean(
        image.reshape(-1, 3),
        axis=0
    )

    blue, green, red = avg_color

    if red > green and red > blue:
        return "Warm"

    if blue > red and blue > green:
        return "Cool"

    return "Neutral"


# ---------------------------------------------------------
# Determine space level
# ---------------------------------------------------------

def determine_space_level(edge_density):

    if edge_density < 0.08:
        return "Open"

    if edge_density < 0.18:
        return "Moderate"

    return "Crowded"


# ---------------------------------------------------------
# Calculate compatibility score
# ---------------------------------------------------------

def calculate_fit_score(
    brightness,
    edge_density,
    product
):

    width = product["dimensions"]["width"]
    depth = product["dimensions"]["depth"]

    product_area = width * depth

    if product_area <= 5000:
        size_factor = 10

    elif product_area <= 10000:
        size_factor = 5

    elif product_area <= 20000:
        size_factor = 0

    else:
        size_factor = -8

    fit_score = 65

    # Lighting contribution
    if brightness > 170:
        fit_score += 10

    elif brightness < 90:
        fit_score -= 8

    # Space contribution
    if edge_density < 0.08:
        fit_score += 12

    elif edge_density > 0.18:
        fit_score -= 10

    # Product size contribution
    fit_score += size_factor

    return max(
        40,
        min(
            98,
            fit_score
        )
    )


# ---------------------------------------------------------
# Generate recommendation
# ---------------------------------------------------------

def generate_recommendation(
    product,
    space_level
):

    if space_level == "Crowded":

        return (
            f"{product['name']} may feel large "
            f"in this crowded space. Consider a "
            f"smaller {product['category'].lower()}."
        )

    if space_level == "Open":

        return (
            f"{product['name']} has a good amount "
            f"of surrounding space based on the "
            f"uploaded image."
        )

    return (
        f"{product['name']} appears reasonably "
        f"suitable for this space based on its "
        f"visual characteristics."
    )


# ---------------------------------------------------------
# AI visualization
# ---------------------------------------------------------

def generate_ai_visualization(
    image_bytes,
    product
):

    product_image_path = find_product_image(
        product
    )

    print()
    print("=" * 60)
    print("Starting Replicate AI visualization...")
    print("Selected product:", product["name"])
    print("Product ID:", product["id"])

    # -----------------------------------------------------
    # Verify selected product image
    # -----------------------------------------------------

    if not product_image_path:

        raise RuntimeError(
            f"Product image not found for "
            f"{product['name']}."
        )

    print(
        "Product reference:",
        product_image_path
    )

    # -----------------------------------------------------
    # Verify image can actually be read
    # -----------------------------------------------------

    product_reference = cv2.imread(
        str(product_image_path),
        cv2.IMREAD_UNCHANGED
    )

    if product_reference is None:

        raise RuntimeError(
            f"Unable to read product image: "
            f"{product_image_path}"
        )

    if (
        len(product_reference.shape) != 3
        or product_reference.shape[2] != 4
    ):

        raise RuntimeError(
            f"Product image must contain "
            f"an alpha channel: "
            f"{product_image_path}"
        )

    print(
        "Reference image verified:",
        product_reference.shape
    )

    # -----------------------------------------------------
    # Create temporary room image file
    # -----------------------------------------------------

    room_path = (
        BASE_DIR / "_temp_room_image.png"
    )

    with open(room_path, "wb") as file:
        file.write(image_bytes)

    try:

        # -------------------------------------------------
        # Build prompt
        # -------------------------------------------------

        prompt = (
            "Edit the uploaded interior room photograph "
            "by placing the selected furniture naturally "
            "inside the room. "

            f"The selected furniture is "
            f"{product['name']}. "

            f"It is a {product['category']} with "
            f"{product['material']} material, "
            f"{product['color']} color and "
            f"{product['style']} style. "

            f"Its real-world dimensions are approximately "
            f"{product['dimensions']['width']} cm wide, "
            f"{product['dimensions']['depth']} cm deep and "
            f"{product['dimensions']['height']} cm high. "

            "Use the provided product reference image "
            "as the visual identity of the furniture. "
            "Preserve its shape, proportions, materials, "
            "colors, design details and overall appearance. "

            "Place exactly this selected product into "
            "the room. "

            "Position it naturally on the floor in a "
            "realistic location appropriate for the "
            "existing room layout. "

            "Match the furniture's scale, perspective, "
            "orientation, lighting, color temperature, "
            "contact shadows and reflections to the room. "

            "The furniture must appear physically present "
            "inside the original photograph. "

            "Preserve the existing walls, floor, ceiling, "
            "windows, doors, architecture and other "
            "furniture. "

            "Do not redesign the room. "
            "Do not remove existing furniture. "
            "Do not add unrelated furniture. "
            "Do not change the camera viewpoint. "

            "The final result should look like a realistic "
            "photograph of the same room after the selected "
            "product has been placed inside it."
        )

        print()
        print("Sending room image + product reference to AI...")

        # -------------------------------------------------
        # Build Replicate input
        # -------------------------------------------------

        room_file = open(
            room_path,
            "rb"
        )

        product_file = open(
            product_image_path,
            "rb"
        )

        replicate_input = {
            "input_image": room_file,
            "reference_image": product_file,
            "prompt": prompt,
        }

        try:

            # ---------------------------------------------
            # Run FLUX Kontext Pro
            # ---------------------------------------------

            output = client.run(
                "black-forest-labs/flux-kontext-pro",
                input=replicate_input
            )

        finally:

            product_file.close()
            room_file.close()

        # -------------------------------------------------
        # Read generated image
        # -------------------------------------------------

        if isinstance(output, list):

            if not output:
                raise RuntimeError(
                    "Replicate returned no images."
                )

            output = output[0]

        generated_bytes = output.read()

        if not generated_bytes:

            raise RuntimeError(
                "Replicate returned an empty image."
            )

        print()
        print("AI visualization generated successfully.")
        print("=" * 60)

        return generated_bytes

    finally:

        if room_path.exists():
            room_path.unlink()


# ---------------------------------------------------------
# Main room analysis function
# ---------------------------------------------------------

def analyze_room(
    image_bytes,
    product
):

    # -----------------------------------------------------
    # Decode uploaded room image
    # -----------------------------------------------------

    image_array = np.frombuffer(
        image_bytes,
        np.uint8
    )

    image = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR
    )

    if image is None:
        return None

    # -----------------------------------------------------
    # Computer vision analysis
    # -----------------------------------------------------

    metrics = calculate_room_metrics(
        image
    )

    brightness = metrics["brightness"]

    edge_density = metrics[
        "edge_density"
    ]

    lower_edge_density = metrics[
        "lower_edge_density"
    ]

    room_tone = determine_room_tone(
        image
    )

    space_level = determine_space_level(
        edge_density
    )

    # -----------------------------------------------------
    # Determine recommended placement area
    # -----------------------------------------------------

    height = image.shape[0]

    lower_region = image[
        int(height * 0.4):,
        :
    ]

    lower_gray = cv2.cvtColor(
        lower_region,
        cv2.COLOR_BGR2GRAY
    )

    lower_height, lower_width = (
        lower_gray.shape
    )

    left_region = lower_gray[
        :,
        :lower_width // 3
    ]

    center_region = lower_gray[
        :,
        lower_width // 3:
        2 * lower_width // 3
    ]

    right_region = lower_gray[
        :,
        2 * lower_width // 3:
    ]

    left_density = float(
        np.mean(
            cv2.Canny(
                left_region,
                100,
                200
            ) > 0
        )
    )

    center_density = float(
        np.mean(
            cv2.Canny(
                center_region,
                100,
                200
            ) > 0
        )
    )

    right_density = float(
        np.mean(
            cv2.Canny(
                right_region,
                100,
                200
            ) > 0
        )
    )

    placement_scores = {
        "Left": left_density,
        "Center": center_density,
        "Right": right_density,
    }

    placement_area = min(
        placement_scores,
        key=placement_scores.get
    )

    # -----------------------------------------------------
    # Compatibility score
    # -----------------------------------------------------

    fit_score = calculate_fit_score(
        brightness,
        edge_density,
        product
    )

    style_match = max(
        40,
        min(
            98,
            fit_score - 4
        )
    )

    width = product["dimensions"]["width"]
    depth = product["dimensions"]["depth"]

    product_area = width * depth

    space_utilization = min(
        85,
        int(edge_density * 250)
        +
        max(
            0,
            product_area // 5000
        )
    )

    recommendation = generate_recommendation(
        product,
        space_level
    )

    # -----------------------------------------------------
    # Generate actual AI visualization
    # -----------------------------------------------------

    visualization_bytes = (
        generate_ai_visualization(
            image_bytes,
            product
        )
    )

    # -----------------------------------------------------
    # Return result
    # -----------------------------------------------------

    return {
        "fit_score": fit_score,
        "style_match": style_match,
        "space_utilization": space_utilization,
        "brightness": brightness,
        "room_tone": room_tone,
        "space_level": space_level,
        "placement_area": placement_area,
        "recommendation": recommendation,
        "visualization": visualization_bytes,
    }