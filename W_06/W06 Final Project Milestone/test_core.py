# Inventory tests for core.py — W06 Final Project Milestone

import pytest
from core import (
    load_inventory,
    update_stock,
    add_product,
    delete_product,
    get_out_of_stock_requested,
)


# --- test_update_stock ---


def test_update_stock_success():
    """update_stock: success case — adds or subtracts quantity correctly."""
    inv = {"P001": ["Arroz", 50]}
    update_stock(inv, "P001", 10)
    assert inv["P001"] == ["Arroz", 60]
    update_stock(inv, "P001", -20)
    assert inv["P001"] == ["Arroz", 40]


def test_update_stock_insufficient_stock():
    """update_stock: raises ValueError('Insufficient stock') when result would be negative."""
    inv = {"P001": ["Arroz", 50], "P002": ["Leche", 45]}
    with pytest.raises(ValueError, match="Insufficient stock"):
        update_stock(inv, "P001", -60)
    with pytest.raises(ValueError, match="Insufficient stock"):
        update_stock(inv, "P002", -50)


# --- test_get_out_of_stock_requested ---


def test_get_out_of_stock_requested_returns_requested_and_zero():
    """get_out_of_stock_requested: returns names of products that are out of stock and requested."""
    inv = {"P001": ["Arroz", 50], "P002": ["Leche", 45], "P004": ["Sal", 0]}
    result1 = get_out_of_stock_requested(inv, ["P004"])
    assert result1 == ["Sal"]
    result2 = get_out_of_stock_requested(inv, ["P001", "P004"])
    assert result2 == ["Sal"]


def test_get_out_of_stock_requested_ignores_in_stock():
    """get_out_of_stock_requested: only products with quantity 0 are returned."""
    inv = {"P001": ["Arroz", 50], "P004": ["Sal", 0]}
    result1 = get_out_of_stock_requested(inv, ["P001", "P004"])
    assert result1 == ["Sal"]
    result2 = get_out_of_stock_requested(inv, ["P004"])
    assert result2 == ["Sal"]


# --- test_load_inventory ---


def test_load_inventory():
    """load_inventory: builds dict from CSV with product_id as key and [name, quantity] as value."""
    result1 = load_inventory("inventory.csv")
    result2 = load_inventory("inventory.csv")
    expected = {
        "P001": ["Arroz", 50],
        "P002": ["Leche", 45],
        "P003": ["Milo", 25],
        "P004": ["Sal", 0],
        "P005": ["Pan", 10],
    }
    assert result1 == expected
    assert result2 == expected


# --- test_add_product ---


def test_add_product():
    """add_product: new product is added to dict; duplicate product_id raises ValueError."""
    inv = {}
    add_product(inv, "P001", "Arroz", 50)
    assert inv["P001"] == ["Arroz", 50]
    add_product(inv, "P002", "Leche", 45)
    assert inv["P002"] == ["Leche", 45]
    assert len(inv) == 2
    with pytest.raises(ValueError, match="Product ID already exists"):
        add_product(inv, "P001", "Otro", 10)


# --- test_delete_product ---


def test_delete_product():
    """delete_product: product is removed from dict; missing product_id raises KeyError."""
    inv = {"P001": ["Arroz", 50], "P002": ["Leche", 45], "P003": ["Milo", 25]}
    delete_product(inv, "P001")
    assert "P001" not in inv
    delete_product(inv, "P002")
    assert "P002" not in inv
    assert inv["P003"] == ["Milo", 25]
    with pytest.raises(KeyError, match="Product not found"):
        delete_product(inv, "P999")
