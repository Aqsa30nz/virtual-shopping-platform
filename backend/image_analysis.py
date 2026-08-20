import cv2
import numpy as np
from pathlib import Path


PRODUCT_IMAGES_DIR = (
    Path(__file__).parent / "product_images"
)


def overlay_product(
    room_image,
    product_image,
    placement_area
):
    """
    Overlay the transparent product image
    onto the room image.
    """

    room = room_image.copy()
    product = product_image.copy()

    # ---------------------------------------------------------
    # 1. Get room dimensions
    # ---------------------------------------------------------

    room_height, room_width = room.shape[:2]


    # ---------------------------------------------------------
    # 2. Resize product
    # ---------------------------------------------------------

    target_width = int(
        room_width * 0.35
    )

    product_height, product_width = (
        product.shape[:2]
    )

    scale = (
        target_width / product_width
    )

    target_height = int(
        product_height * scale
    )

    product = cv2.resize(
        product,
        (
            target_width,
            target_height
        ),
        interpolation=cv2.INTER_AREA
    )


    # ---------------------------------------------------------
    # 3. Determine horizontal position
    # ---------------------------------------------------------

    if placement_area == "Left":

        x_position = int(
            room_width * 0.08
        )

    elif placement_area == "Right":

        x_position = int(
            room_width * 0.57
        )

    else:

        x_position = int(
            (room_width - target_width) / 2
        )


    # ---------------------------------------------------------
    # 4. Determine vertical position
    # ---------------------------------------------------------

    y_position = int(
        room_height * 0.55
    )


    # ---------------------------------------------------------
    # 5. Keep product inside room boundaries
    # ---------------------------------------------------------

    x_position = max(
        0,
        min(
            x_position,
            room_width - target_width
        )
    )

    y_position = max(
        0,
        min(
            y_position,
            room_height - target_height
        )
    )


    # ---------------------------------------------------------
    # 6. Extract alpha channel
    # ---------------------------------------------------------

    alpha = (
        product[:, :, 3]
        / 255.0
    )

    product_rgb = (
        product[:, :, :3]
    )


    # ---------------------------------------------------------
    # 7. Select room region where product goes
    # ---------------------------------------------------------

    roi = room[
        y_position:
        y_position + target_height,

        x_position:
        x_position + target_width
    ]


    # ---------------------------------------------------------
    # 8. Alpha blending
    # ---------------------------------------------------------

    for channel in range(3):

        roi[:, :, channel] = (
            alpha * product_rgb[:, :, channel]
            +
            (1 - alpha)
            * roi[:, :, channel]
        )


    # ---------------------------------------------------------
    # 9. Put blended region back into room
    # ---------------------------------------------------------

    room[
        y_position:
        y_position + target_height,

        x_position:
        x_position + target_width
    ] = roi


    return room


def analyze_room(
    image_bytes,
    product
):

    # ---------------------------------------------------------
    # 1. Decode uploaded room image
    # ---------------------------------------------------------

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


    # ---------------------------------------------------------
    # 2. Load transparent product image
    # ---------------------------------------------------------

    product_image_path = (
        PRODUCT_IMAGES_DIR
        / "modern-grey-sofa.png"
    )

    product_image = cv2.imread(
        str(product_image_path),
        cv2.IMREAD_UNCHANGED
    )

    if product_image is None:
        return None


    # Make sure product has an alpha channel
    if product_image.shape[2] != 4:
        return None


    # ---------------------------------------------------------
    # 3. Convert room image to grayscale
    # ---------------------------------------------------------

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )


    # ---------------------------------------------------------
    # 4. Calculate brightness
    # ---------------------------------------------------------

    brightness = int(
        np.mean(gray)
    )


    # ---------------------------------------------------------
    # 5. Calculate overall edge density
    # ---------------------------------------------------------

    edges = cv2.Canny(
        gray,
        100,
        200
    )

    edge_density = float(
        np.mean(edges > 0)
    )


    # ---------------------------------------------------------
    # 6. Analyze lower region of room
    # ---------------------------------------------------------

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


    # ---------------------------------------------------------
    # 7. Divide lower region into 3 areas
    # ---------------------------------------------------------

    lower_height, lower_width = (
        lower_region.shape
    )

    left_region = lower_region[
        :,
        :lower_width // 3
    ]

    center_region = lower_region[
        :,
        lower_width // 3:
        2 * lower_width // 3
    ]

    right_region = lower_region[
        :,
        2 * lower_width // 3:
    ]


    # ---------------------------------------------------------
    # 8. Calculate edge density for each area
    # ---------------------------------------------------------

    left_edges = cv2.Canny(
        left_region,
        100,
        200
    )

    center_edges = cv2.Canny(
        center_region,
        100,
        200
    )

    right_edges = cv2.Canny(
        right_region,
        100,
        200
    )


    left_density = float(
        np.mean(left_edges > 0)
    )

    center_density = float(
        np.mean(center_edges > 0)
    )

    right_density = float(
        np.mean(right_edges > 0)
    )


    # ---------------------------------------------------------
    # 9. Select area with least visual obstruction
    # ---------------------------------------------------------

    placement_scores = {
        "Left": left_density,
        "Center": center_density,
        "Right": right_density,
    }

    placement_area = min(
        placement_scores,
        key=placement_scores.get
    )


    # ---------------------------------------------------------
    # 10. Generate furniture visualization
    # ---------------------------------------------------------

    visualization = overlay_product(
        image,
        product_image,
        placement_area
    )


    # ---------------------------------------------------------
    # 11. Analyze room tone
    # ---------------------------------------------------------

    avg_color = np.mean(
        image.reshape(-1, 3),
        axis=0
    )

    blue, green, red = avg_color


    if red > green and red > blue:

        room_tone = "Warm"

    elif blue > red and blue > green:

        room_tone = "Cool"

    else:

        room_tone = "Neutral"


    # ---------------------------------------------------------
    # 12. Estimate available space
    # ---------------------------------------------------------

    if edge_density < 0.08:

        space_level = "Open"

    elif edge_density < 0.18:

        space_level = "Moderate"

    else:

        space_level = "Crowded"


    # ---------------------------------------------------------
    # 13. Calculate product size factor
    # ---------------------------------------------------------

    width = product["dimensions"]["width"]

    depth = product["dimensions"]["depth"]

    product_area = (
        width * depth
    )


    if product_area <= 5000:

        size_factor = 10

    elif product_area <= 10000:

        size_factor = 5

    elif product_area <= 20000:

        size_factor = 0

    else:

        size_factor = -8


    # ---------------------------------------------------------
    # 14. Calculate base compatibility score
    # ---------------------------------------------------------

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


    # Keep score within sensible range
    fit_score = max(
        40,
        min(
            98,
            fit_score
        )
    )


    # ---------------------------------------------------------
    # 15. Calculate style match
    # ---------------------------------------------------------

    style_match = max(
        40,
        min(
            98,
            fit_score - 4
        )
    )


    # ---------------------------------------------------------
    # 16. Calculate space utilization
    # ---------------------------------------------------------

    space_utilization = min(
        85,
        int(
            edge_density * 250
        )
        +
        max(
            0,
            product_area // 5000
        )
    )


    # ---------------------------------------------------------
    # 17. Generate recommendation
    # ---------------------------------------------------------

    if space_level == "Crowded":

        recommendation = (
            f"{product['name']} may feel large "
            f"in this crowded space. "
            f"Consider a smaller "
            f"{product['category'].lower()}."
        )

    elif space_level == "Open":

        recommendation = (
            f"{product['name']} has a good amount "
            f"of surrounding space based on "
            f"the uploaded image."
        )

    else:

        recommendation = (
            f"{product['name']} appears reasonably "
            f"suitable for this space based on "
            f"its visual characteristics."
        )


    # ---------------------------------------------------------
    # 18. Encode visualization as JPEG
    # ---------------------------------------------------------

    success, encoded_image = cv2.imencode(
        ".jpg",
        visualization
    )

    if not success:
        return None


    visualization_bytes = (
        encoded_image.tobytes()
    )


    # ---------------------------------------------------------
    # 19. Return analysis + visualization
    # ---------------------------------------------------------

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