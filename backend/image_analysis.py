import cv2
import numpy as np


def analyze_room(image_bytes, product):
    image_array = np.frombuffer(image_bytes, np.uint8)

    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image is None:
        return None

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Brightness
    brightness = int(np.mean(gray))

    # Edge density
    edges = cv2.Canny(gray, 100, 200)
    edge_density = float(np.mean(edges > 0))

    # Dominant room color
    avg_color = np.mean(image.reshape(-1, 3), axis=0)

    blue, green, red = avg_color

    if red > green and red > blue:
        room_tone = "Warm"
    elif blue > red and blue > green:
        room_tone = "Cool"
    else:
        room_tone = "Neutral"

    # Calculate fit score from image properties
    fit_score = 65

    if brightness > 170:
        fit_score += 10
    elif brightness < 90:
        fit_score -= 8

    if edge_density < 0.08:
        fit_score += 12
    elif edge_density > 0.18:
        fit_score -= 10

    fit_score = max(40, min(98, fit_score))

    style_match = fit_score - 4

    space_utilization = min(85, int(edge_density * 250))

    return {
        "fit_score": fit_score,
        "style_match": style_match,
        "space_utilization": space_utilization,
        "brightness": brightness,
        "room_tone": room_tone,
        "recommendation": (
            f"{product['name']} is a better match for a "
            f"{room_tone.lower()} room with this lighting."
        ),
    }