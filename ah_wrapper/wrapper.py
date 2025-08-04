from typing import Dict, Optional

import requests


class SearchProductsSortType:
    RELEVANCE = "RELEVANCE"
    PRICE_LOW_HIGH = "PRICE_LOW_HIGH"
    PRICE_HIGH_LOW = "PRICE_HIGH_LOW"
    NAME_A_Z = "NAME_A_Z"
    NAME_Z_A = "NAME_Z_A"


class AH:
    def __init__(self):
        self.api_url = "https://api.ah.nl"
        self.session = requests.Session()
        self.access_token = None
        self._authenticate()

    def _authenticate(self):
        auth_url = f"{self.api_url}/mobile-auth/v1/auth/token/anonymous"
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            ),
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        payload = {"clientId": "appie", "clientSecret": "appie"}

        response = self.session.post(auth_url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        self.access_token = data.get("access_token")

        if not self.access_token:
            raise Exception("No access token received")

        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            }
        )

    def graphql(self, query: str, variables: Dict = None) -> Dict:
        if not self.access_token:
            raise Exception("Not authenticated")

        url = f"{self.api_url}/graphql"
        payload = {"query": query, "variables": variables or {}}

        response = self.session.post(url, json=payload)
        response.raise_for_status()
        result = response.json()

        if "errors" in result:
            error_msg = "; ".join(
                [error.get("message", "Unknown error") for error in result["errors"]]
            )
            raise Exception(f"GraphQL errors: {error_msg}")

        return result

    def search_products(self, query: str, options: Dict = None) -> Dict:
        search_input = {"query": query}
        if options:
            search_input.update(options)

        search_query = """
        query SearchProducts($input: SearchProductsInput!) {
            searchProducts(input: $input) {
                totalFound
                products {
                    id
                    title
                    brand
                    priceV2 {
                        now {
                            amount
                            formattedV2
                        }
                        was {
                            amount
                            formattedV2
                        }
                    }
                    listPrice {
                        amount
                        currency
                    }
                    images {
                        url
                    }
                }
            }
        }
        """

        try:
            result = self.graphql(search_query, {"input": search_input})
            search_result = result.get("data", {}).get("searchProducts", {})

            if not search_result:
                search_result = {"products": [], "totalFound": 0}

            if "totalFound" in search_result:
                search_result["totalCount"] = search_result["totalFound"]

            return search_result
        except Exception as e:
            return {"products": [], "totalCount": 0, "error": str(e)}

    def get_product(self, product_id: int) -> Dict:
        product_query = """
        query Product($id: Int!) {
            product(id: $id) {
                id
                title
                brand
                summary
                priceV2 {
                    now {
                        amount
                        formattedV2
                    }
                    was {
                        amount
                        formattedV2
                    }
                }
                listPrice {
                    amount
                    currency
                }
                images {
                    url
                }
            }
        }
        """

        try:
            result = self.graphql(product_query, {"id": product_id})
            return result.get("data", {}).get("product")
        except Exception:
            return None

    def search_products_by_price(
        self, query: str, target_price: float, tolerance: float = 0.10
    ) -> Dict:
        results = self.search_products(query)
        products = results.get("products", [])

        filtered_products = []
        for product in products:
            price = self._get_product_price(product)
            if price is not None:
                price_diff = abs(price - target_price)
                if price_diff <= tolerance:
                    filtered_products.append(product)

        return {
            "products": filtered_products,
            "totalCount": len(filtered_products),
            "originalQuery": query,
            "targetPrice": target_price,
            "tolerance": tolerance,
        }

    def _get_product_price(self, product: Dict) -> Optional[float]:
        if (
            product.get("priceV2")
            and product["priceV2"].get("now")
            and product["priceV2"]["now"].get("amount")
        ):
            return product["priceV2"]["now"]["amount"]

        if product.get("listPrice") and product["listPrice"].get("amount"):
            return product["listPrice"]["amount"]

        return None
