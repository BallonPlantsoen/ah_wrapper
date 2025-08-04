# AH Wrapper

Simple Python wrapper for Albert Heijn's API to search products and get prices.

## Install

### Using UV (recommended)
```bash
# Install UV if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install the package
uv add ah-wrapper
```

### Using pip
```bash
pip install ah-wrapper
```

## Development

```bash
# Clone and setup with UV
git clone <repository-url>
cd ah-wrapper
uv sync --extra dev

# Run tests
uv run pytest

# Run linting
uv run flake8 ah_wrapper/
uv run black --check ah_wrapper/
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