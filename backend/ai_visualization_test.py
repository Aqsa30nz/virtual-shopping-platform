import os
from pathlib import Path

import httpx
import replicate
from dotenv import load_dotenv


# ---------------------------------------------------------
# 1. Load environment variables
# ---------------------------------------------------------

load_dotenv()

token = os.getenv("REPLICATE_API_TOKEN")

if not token:
    raise RuntimeError(
        "REPLICATE_API_TOKEN not found in .env"
    )


# ---------------------------------------------------------
# 2. Create Replicate client
# ---------------------------------------------------------
#
# TEMPORARY:
# Your Windows/Python environment currently fails TLS
# certificate verification for api.replicate.com.
#
# We already confirmed that Replicate works with
# certificate verification disabled.
#
# We are injecting the transport because replicate 1.0.7
# supports the `transport` argument.
#

transport = httpx.HTTPTransport(
    verify=False
)

client = replicate.Client(
    api_token=token,
    transport=transport
)


# ---------------------------------------------------------
# 3. Define input files
# ---------------------------------------------------------

BASE_DIR = Path(__file__).parent

room_image = BASE_DIR / "my-room.png"

product_image = (
    BASE_DIR
    / "product_images"
    / "modern-grey-sofa.png"
)


# ---------------------------------------------------------
# 4. Validate files
# ---------------------------------------------------------

if not room_image.exists():
    raise FileNotFoundError(
        f"Room image not found: {room_image}"
    )

if not product_image.exists():
    raise FileNotFoundError(
        f"Product image not found: {product_image}"
    )


print("Room image:", room_image)
print("Product image:", product_image)


# ---------------------------------------------------------
# 5. Run AI image generation
# ---------------------------------------------------------

print()
print("Starting AI visualization...")
print("This may take some time.")


with (
    open(room_image, "rb") as room_file,
    open(product_image, "rb") as product_file
):

    output = client.run(
        "black-forest-labs/flux-kontext-pro",
        input={
            "input_image": room_file,

            "prompt": (
                "Edit this interior room photo by adding "
                "the provided modern grey sofa naturally "
                "into the room. Place the sofa on the "
                "floor in a realistic position appropriate "
                "for the room layout. Preserve the existing "
                "walls, floor, windows, doors, lighting, "
                "architecture and other furniture. "
                "Match the sofa's scale, perspective, "
                "lighting and shadows to the room. "
                "Do not redesign the room. "
                "Do not add extra furniture. "
                "The final image should look like a "
                "real photograph of this room with the "
                "selected sofa."
            ),

            "reference_image": product_file,
        },
    )


# ---------------------------------------------------------
# 6. Save generated image
# ---------------------------------------------------------

print()
print("AI generation completed.")
print("Output:", output)


if isinstance(output, list):
    output = output[0]


output_path = BASE_DIR / "ai_result.png"


with open(output_path, "wb") as file:
    file.write(output.read())


print()
print("Saved AI result to:")
print(output_path)