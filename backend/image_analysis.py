import cv2
import numpy as np


def analyze_room(image_bytes, product):
    image_array = np.frombuffer(image_bytes, np.uint8)

    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image is None:
        return None

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 1. Brightness
    brightness = int(np.mean(gray))

    # 2. Edge density
    edges = cv2.Canny(gray, 100, 200)
    edge_density = float(np.mean(edges > 0))

    # 3. Room tone
    avg_color = np.mean(image.reshape(-1, 3), axis=0)

    blue, green, red = avg_color

    if red > green and red > blue:
        room_tone = "Warm"
    elif blue > red and blue > green:
        room_tone = "Cool"
    else:
        room_tone = "Neutral"

    # 4. Estimate available space
    if edge_density < 0.08:
        space_level = "Open"
    elif edge_density < 0.18:
        space_level = "Moderate"
    else:
        space_level = "Crowded"

    # 5. Product size factor
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

    # 6. Base compatibility score
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
    fit_score = max(40, min(98, fit_score))

    # Style match
    style_match = max(40, min(98, fit_score - 4))

    # Relative space utilization
    space_utilization = min(
        85,
        int(edge_density * 250) + max(0, product_area // 5000)
    )

    # Recommendation
    if space_level == "Crowded":
        recommendation = (
            f"{product['name']} may feel large in this crowded space. "
            f"Consider a smaller {product['category'].lower()}."
        )
    elif space_level == "Open":
        recommendation = (
            f"{product['name']} has a good amount of surrounding space "
            f"based on the uploaded image."
        )
    else:
        recommendation = (
            f"{product['name']} appears reasonably suitable for this "
            f"space based on its visual characteristics."
        )

    return {
        "fit_score": fit_score,
        "style_match": style_match,
        "space_utilization": space_utilization,
        "brightness": brightness,
        "room_tone": room_tone,
        "space_level": space_level,
        "recommendation": recommendation,
    }