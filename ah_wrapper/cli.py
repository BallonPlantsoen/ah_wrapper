#!/usr/bin/env python3

import argparse
import json
import sys
from typing import Dict, Any

from .wrapper import AH, SearchProductsSortType


def format_product(product: Dict[str, Any]) -> str:
    title = product.get('title', 'Unknown')
    brand = product.get('brand', 'Unknown')
    
    price_info = "Price not available"
    if product.get('priceV2') and product['priceV2'].get('now'):
        price = product['priceV2']['now'].get('amount')
        formatted = product['priceV2']['now'].get('formattedV2', f"€{price}")
        price_info = formatted
    
    return f"{title} ({brand}) - {price_info}"


def search_products_cmd(args: argparse.Namespace) -> None:
    try:
        ah = AH()
        
        options = {}
        if args.sort:
            options['sort'] = args.sort
        if args.limit:
            options['page'] = {'size': args.limit, 'number': 0}
        
        results = ah.search_products(args.query, options)
        products = results.get('products', [])
        
        if not products:
            print(f"No products found for '{args.query}'")
            return
        
        print(f"Found {len(products)} products for '{args.query}':")
        print("-" * 50)
        
        for i, product in enumerate(products, 1):
            print(f"{i}. {format_product(product)}")
            
        if args.json:
            print("\nJSON output:")
            print(json.dumps(results, indent=2))
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def get_product_cmd(args: argparse.Namespace) -> None:
    try:
        ah = AH()
        product = ah.get_product(args.product_id)
        
        if not product:
            print(f"Product with ID {args.product_id} not found")
            return
        
        if args.json:
            print(json.dumps(product, indent=2))
        else:
            print(f"Product: {product.get('title', 'Unknown')}")
            print(f"Brand: {product.get('brand', 'Unknown')}")
            print(f"Summary: {product.get('summary', 'No summary available')}")
            
            if product.get('priceV2') and product['priceV2'].get('now'):
                price = product['priceV2']['now'].get('amount')
                formatted = product['priceV2']['now'].get('formattedV2', f"€{price}")
                print(f"Price: {formatted}")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def search_by_price_cmd(args: argparse.Namespace) -> None:
    try:
        ah = AH()
        results = ah.search_products_by_price(args.query, args.price, args.tolerance)
        products = results.get('products', [])
        
        if not products:
            print(f"No products found for '{args.query}' around €{args.price}")
            return
        
        print(f"Found {len(products)} products for '{args.query}' around €{args.price}:")
        print("-" * 50)
        
        for i, product in enumerate(products, 1):
            print(f"{i}. {format_product(product)}")
            
        if args.json:
            print("\nJSON output:")
            print(json.dumps(results, indent=2))
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Albert Heijn API wrapper CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search for products")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--limit", type=int, help="Limit number of results")
    search_parser.add_argument("--sort", choices=["relevance", "price-low", "price-high", "name-a-z", "name-z-a"], help="Sort order")
    search_parser.add_argument("--json", action="store_true", help="Output as JSON")
    search_parser.set_defaults(func=search_products_cmd)
    
    # Get product command
    get_parser = subparsers.add_parser("get", help="Get product details")
    get_parser.add_argument("product_id", type=int, help="Product ID")
    get_parser.add_argument("--json", action="store_true", help="Output as JSON")
    get_parser.set_defaults(func=get_product_cmd)
    
    # Price search command
    price_parser = subparsers.add_parser("price", help="Search products by price")
    price_parser.add_argument("query", help="Search query")
    price_parser.add_argument("price", type=float, help="Target price")
    price_parser.add_argument("--tolerance", type=float, default=0.10, help="Price tolerance (default: 0.10)")
    price_parser.add_argument("--json", action="store_true", help="Output as JSON")
    price_parser.set_defaults(func=search_by_price_cmd)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == "__main__":
    main() 