# AH Wrapper

Simple Python wrapper for Albert Heijn's API to search products and get prices.

## Install

```bash
pip install ah-wrapper
```

## Quick Start

```python
from ah_wrapper import AH

ah = AH()

# Search products
results = ah.search_products("milk")
for product in results["products"][:3]:
    print(f"{product['title']}: €{product['priceV2']['now']['amount']}")

# Get product details
product = ah.get_product(12345)
print(f"{product['title']}: {product['summary']}")
```

## CLI

```bash
# Search products
ah-wrapper search "bread"

# Get product details
ah-wrapper get 12345

# Search by price
ah-wrapper price "pizza" 5.00
```

## License

MIT 