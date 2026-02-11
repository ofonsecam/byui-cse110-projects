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
    inv = {"P001": ["Widget A", 50]}
    update_stock(inv, "P001", 10)
    assert inv["P001"] == ["Widget A", 60]
    update_stock(inv, "P001", -20)
    assert inv["P001"] == ["Widget A", 40]


def test_update_stock_insufficient_stock():
    """update_stock: raises ValueError('Insufficient stock') when result would be negative."""
    inv = {"P001": ["Widget A", 5]}
    with pytest.raises(ValueError, match="Insufficient stock"):
        update_stock(inv, "P001", -10)


# --- test_get_out_of_stock_requested ---


def test_get_out_of_stock_requested_returns_requested_and_zero():
    """get_out_of_stock_requested: returns names of products that are out of stock and requested."""
    inv = {"P001": ["Widget A", 0], "P002": ["Widget B", 10]}
    requested = ["P001", "P003"]
    result = get_out_of_stock_requested(inv, requested)
    assert result == ["Widget A"]


def test_get_out_of_stock_requested_ignores_in_stock():
    """get_out_of_stock_requested: only products with quantity 0 are returned."""
    inv = {"P001": ["Widget A", 5], "P002": ["Widget B", 0]}
    result = get_out_of_stock_requested(inv, ["P001", "P002"])
    assert result == ["Widget B"]


# --- test_load_inventory ---


def test_load_inventory():
    """load_inventory: builds dict from CSV with product_id as key and [name, quantity] as value."""
    result = load_inventory("inventory.csv")
    
    # Check the IDs exist
    assert "P001" in result
    assert "P002" in result
    assert "P003" in result
    assert "P004" in result 

    assert result["P001"] == ["Arroz", 50]
    assert result["P002"] == ["Leche", 30]
    assert result["P003"] == ["Milo", 25]
    assert result["P004"] == ["Sal", 0]


# --- test_add_product ---


def test_add_product():
    """add_product: new product is added to dict; duplicate product_id raises ValueError."""
    inv = {}
    add_product(inv, "P001", "Arroz", 50)
    assert inv["P001"] == ["Arroz", 50]
    assert len(inv) == 1
    # No duplicates allowed.
    with pytest.raises(ValueError, match="Product ID already exists"):
        add_product(inv, "P001", "Otro", 10)


# --- test_delete_product ---


def test_delete_product():
    """delete_product: product is removed from dict; missing product_id raises KeyError."""
    inv = {"P001": ["Arroz", 50], "P002": ["Leche", 30]}
    delete_product(inv, "P002")
    assert "P002" not in inv
    assert inv["P001"] == ["Arroz", 50]
    # Error when ID does not exist.
    with pytest.raises(KeyError, match="Product not found"):
        delete_product(inv, "P999")
