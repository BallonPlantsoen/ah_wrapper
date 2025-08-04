#!/usr/bin/env python3

from .wrapper import AH


def basic_search():
    print("=== Basic Search ===")
    ah = AH()

    results = ah.search_products("milk")
    products = results.get("products", [])

    print(f"Found {len(products)} milk products")

    for i, product in enumerate(products[:3]):
        print(f"{i + 1}. {product['title']}")
        if product.get("priceV2", {}).get("now", {}).get("amount"):
            print(f"   Price: €{product['priceV2']['now']['amount']}")


def product_details():
    print("\n=== Product Details ===")
    ah = AH()

    results = ah.search_products("bread")
    products = results.get("products", [])

    if products:
        product_id = products[0]["id"]
        product = ah.get_product(product_id)

        if product:
            print(f"Product: {product['title']}")
            print(f"Brand: {product.get('brand', 'Unknown')}")
            print(f"Summary: {product.get('summary', 'No summary')}")


def price_filtering():
    print("\n=== Price Filtering ===")
    ah = AH()

    results = ah.search_products_by_price("pizza", 5.00, tolerance=1.00)
    products = results.get("products", [])

    print(f"Found {len(products)} pizza products around €5.00")

    for product in products[:3]:
        price = ah._get_product_price(product)
        print(f"- {product['title']}: €{price}")


def main():
    print("AH Wrapper Examples")
    print("=" * 20)

    try:
        basic_search()
        product_details()
        price_filtering()
        print("\nAll examples completed!")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
