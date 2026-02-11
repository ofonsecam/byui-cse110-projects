"""Business logic - inventory and CSV handling."""

import csv

HEADERS = ("product_id", "product_name", "quantity")


def load_inventory(filename):
    """
    Read a CSV file and return a dictionary where the key is product_id
    and the value is a list [product_name, quantity] with quantity as integer.

    Args:
        filename: Path to the CSV file.

    Returns:
        Dictionary mapping product_id to [product_name, quantity].
        Returns empty dict if file is empty or on read error.
    """
    inventory = {}
    try:
        with open(filename, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                product_id = row.get("product_id", "").strip()
                if not product_id:
                    continue
                name = row.get("product_name", "").strip()
                try:
                    qty = int(row.get("quantity", 0))
                except (ValueError, TypeError):
                    qty = 0
                inventory[product_id] = [name, qty]
    except (FileNotFoundError, OSError):
        return {}
    return inventory


def update_stock(inventory_dict, product_id, change_amount):
    """
    Update product stock by adding change_amount. Raises ValueError if stock would go negative.

    Args:
        inventory_dict: Dictionary mapping product_id to [product_name, quantity].
        product_id: The product to update.
        change_amount: Amount to add (positive) or subtract (negative).

    Raises:
        KeyError: If product_id is not in inventory.
        ValueError: If resulting stock would be less than 0 ('Insufficient stock').
    """
    if product_id not in inventory_dict:
        raise KeyError(f"Product not found: {product_id}")
    name, current_qty = inventory_dict[product_id]
    new_qty = current_qty + change_amount
    if new_qty < 0:
        raise ValueError("Insufficient stock")
    inventory_dict[product_id] = [name, new_qty]


def add_product(inventory_dict, product_id, name, quantity):
    """
    Add a new product to the inventory. Raises ValueError if product_id already exists.

    Args:
        inventory_dict: Dictionary mapping product_id to [product_name, quantity].
        product_id: The new product ID.
        name: The product name.
        quantity: Initial quantity (integer).

    Raises:
        ValueError: If product_id already exists ("Product ID already exists").
    """
    if product_id in inventory_dict:
        raise ValueError("Product ID already exists")
    inventory_dict[product_id] = [name, int(quantity)]


def delete_product(inventory_dict, product_id):
    """
    Remove a product from the inventory. Raises KeyError if product_id does not exist.

    Args:
        inventory_dict: Dictionary mapping product_id to [product_name, quantity].
        product_id: The product ID to remove.

    Raises:
        KeyError: If product_id is not in inventory.
    """
    if product_id not in inventory_dict:
        raise KeyError(f"Product not found: {product_id}")
    del inventory_dict[product_id]


def save_inventory(filename, inventory_dict):
    """
    Write the inventory dictionary back to a CSV file with original headers.

    Args:
        filename: Path to the CSV file to write.
        inventory_dict: Dictionary mapping product_id to [product_name, quantity].
    """
    if not inventory_dict:
        return
    try:
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(HEADERS)
            for product_id, (product_name, quantity) in inventory_dict.items():
                writer.writerow([product_id, product_name, quantity])
    except OSError as e:
        raise OSError(f"Failed to save inventory: {e}") from e


def get_out_of_stock_requested(inventory_dict, requested_list):
    """
    Return names of products that are out of stock (quantity 0) and were requested by customers.

    Args:
        inventory_dict: Dictionary mapping product_id to [product_name, quantity].
        requested_list: List of product IDs that customers have asked about.

    Returns:
        List of product names that are out of stock and in requested_list (urgent to purchase).
    """
    result = []
    for product_id in requested_list:
        if product_id not in inventory_dict:
            continue
        name, quantity = inventory_dict[product_id]
        if quantity == 0:
            result.append(name)
    return result


def get_high_rotation_products(sales_data_list, threshold):
    """
    Return product IDs that have been sold more times than the threshold.

    Args:
        sales_data_list: List of product IDs (one per sale event).
        threshold: Minimum number of sales; products with strictly more sales are returned.

    Returns:
        List of product IDs whose sale count is greater than threshold.
    """
    counts = {}
    for product_id in sales_data_list:
        counts[product_id] = counts.get(product_id, 0) + 1
    return [pid for pid, count in counts.items() if count > threshold]
