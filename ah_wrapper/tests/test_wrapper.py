"""
Tests for the Albert Heijn API Wrapper.

This module contains comprehensive tests for all functionality provided by the
AH wrapper.
"""

import pytest

from ..wrapper import AH, SearchProductsSortType


class TestAHWrapper:
    @pytest.fixture(scope="class")
    def ah_wrapper(self):
        return AH()

    def test_authentication(self, ah_wrapper):
        assert ah_wrapper.access_token is not None
        assert len(ah_wrapper.access_token) > 0

    def test_basic_product_search(self, ah_wrapper):
        results = ah_wrapper.search_products("milk")

        assert "products" in results
        assert isinstance(results["products"], list)
        assert len(results["products"]) > 0

    def test_get_product_details(self, ah_wrapper):
        results = ah_wrapper.search_products("bread")
        products = results.get("products", [])

        if products:
            product_id = products[0]["id"]
            product = ah_wrapper.get_product(product_id)

            assert product is not None
            assert "title" in product
            assert "id" in product

    def test_price_filtering(self, ah_wrapper):
        results = ah_wrapper.search_products_by_price("pizza", 5.00, tolerance=2.00)

        assert "products" in results
        assert isinstance(results["products"], list)

    def test_get_product_price(self, ah_wrapper):
        results = ah_wrapper.search_products("milk")
        products = results.get("products", [])

        if products:
            price = ah_wrapper._get_product_price(products[0])
            assert price is None or isinstance(price, (int, float))

    def test_search_products_with_options(self, ah_wrapper):
        options = {"page": {"size": 5}}
        results = ah_wrapper.search_products("bread", options)

        assert "products" in results
        assert isinstance(results["products"], list)


class TestSearchProductsSortType:
    def test_sort_types(self):
        assert SearchProductsSortType.RELEVANCE == "RELEVANCE"
        assert SearchProductsSortType.PRICE_LOW_HIGH == "PRICE_LOW_HIGH"
        assert SearchProductsSortType.PRICE_HIGH_LOW == "PRICE_HIGH_LOW"
        assert SearchProductsSortType.NAME_A_Z == "NAME_A_Z"
        assert SearchProductsSortType.NAME_Z_A == "NAME_Z_A"
