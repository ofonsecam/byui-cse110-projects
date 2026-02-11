"""
Author: Oscar Fonseca
Project W05
Program that generates a receipt by reading products and an order from CSV files.

This program exceeds the base requirements by including dynamic discount logic
for specific products: a "Buy one, get the second at half price" promotion is
applied to product D083, and the receipt shows how much the customer saved.

Tested with:
1. Standard order: Validated subtotal, tax, and total calculations.
2. Discount Logic: Verified 50% discount on the second unit of D083.
3. Error Handling: Successfully caught FileNotFoundError and KeyError (invalid product ID).
"""

import csv
import time

# Column indices in products.csv: 0=Product #, 1=Name, 2=Price
KEY_COLUMN_INDEX = 0
NAME_INDEX = 1
PRICE_INDEX = 2

# Sales tax rate (6%)
SALES_TAX_RATE = 0.06

# Promotion: "Buy one, get second at half price" for this product ID
PROMO_PRODUCT_ID = "D083"
PROMO_HALF_PRICE_RATE = 0.5  # Second unit (and every second unit) at 50% off


def read_dictionary(filename, key_column_index):
    """
    Read a CSV file and return a dictionary where the key is the value
    of the column specified by key_column_index (e.g. product ID).

    Args:
        filename: Path to the CSV file (e.g. products.csv)
        key_column_index: Index of the column to use as key (0 = first column)

    Returns:
        dict: Dictionary {key: list of row values}

    Raises:
        FileNotFoundError: If the file does not exist
    """
    dictionary = {}

    with open(filename, "rt", encoding="utf-8") as file:
        reader = csv.reader(file)
        # Skip the header row
        next(reader)
        for row in reader:
            if len(row) > 0:
                key = row[key_column_index]
                dictionary[key] = row

    return dictionary


def main():
    """Main function: load products, process the order, and print the receipt."""
    try:
        # 1. Call read_dictionary using products.csv and column 0 as key
        products_dict = read_dictionary("products.csv", KEY_COLUMN_INDEX)

        # 2. Process request.csv: skip header, collect items and compute totals
        items = []
        number_of_items = 0
        subtotal = 0.0
        total_promo_saved = 0.0  # Total amount saved by "BOGO half price" promotion

        with open("request.csv", "rt", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header "Product #,Quantity"
            for row in reader:
                if len(row) < 2:
                    continue
                product_id = row[0]
                quantity = int(row[1])
                # Look up product; KeyError propagates to outer except
                product_row = products_dict[product_id]
                name = product_row[NAME_INDEX]
                price = float(product_row[PRICE_INDEX])

                # Apply "buy one, get second at half price" for promo product
                if product_id == PROMO_PRODUCT_ID:
                    full_price_units = quantity - quantity // 2  # 1st, 3rd, 5th... at full price
                    half_price_units = quantity // 2              # 2nd, 4th, 6th... at 50% off
                    line_total = price * full_price_units + (price * PROMO_HALF_PRICE_RATE) * half_price_units
                    total_promo_saved += (quantity * price) - line_total
                else:
                    line_total = quantity * price

                items.append((name, quantity, price))
                number_of_items += quantity
                subtotal += line_total

        # 3. Print receipt
        print("Fons Emporium\n")
        for name, quantity, price in items:
            print(f"{name}: {quantity} @ ${price:.2f}")
        print()
        sales_tax = subtotal * SALES_TAX_RATE
        total = subtotal + sales_tax
        print(f"Number of Items: {number_of_items}")
        print(f"Subtotal: ${subtotal:.2f}")
        if total_promo_saved > 0:
            print(f"Promotion savings (BOGO 50% off {PROMO_PRODUCT_ID}): ${total_promo_saved:.2f} saved")
        print(f"Sales Tax: ${sales_tax:.2f}")
        print(f"Total: ${total:.2f}")
        print()
        print("Thank you for shopping at the Fons Emporium.")
        print(time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()))

    except FileNotFoundError as e:
        print(f"Error: missing file\n{e}")

    except KeyError as e:
        print(f"Error: unknown product ID in the request.csv file\n{e}")


if __name__ == "__main__":
    main()
