import json

from comparison import compare_products


with open(
    "data/products.json",
    "r",
    encoding="utf-8"
) as file:
    products = json.load(file)


result = compare_products(
    products[:2]
)


print(
    json.dumps(
        result,
        indent=2,
        ensure_ascii=False
    )
)