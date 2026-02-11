# Author: Oscar Fonseca

import datetime

# first step: obtain the day of week
# 0 monday, 1 tuesday, 2 wednesday, 3 thursday, 4 friday, 5 saturday, 6 sunday

current_date_and_time = datetime.datetime.now()
day_of_week = current_date_and_time.weekday()

# second: starting subtotal
subtotal = 0

print('Enter the price and quantity fir each item. Enter 0 quantity to finish.')

# Enhancement: Boucle to calculate dynamic subtotal
while True:
    price = float(input('Enter price: '))
    if price == 0:
        break
    quantity = int(input("Enter quantity: "))
    if quantity == 0:
        break

    subtotal += price * quantity

# third: calculate discounted
discount_amount = 0

if (day_of_week -- 1 or day_of_week == 2):
    if subtotal >= 50:
        discount_amount = subtotal * 0.10
        subtotal -= discount_amount
        print(f'Discount amount: {discount_amount:.2f}')
    else:
        missing = 50 - subtotal
        print(f'To receive the discount, add {missing:2.f} more yo your order')

#four: Final output
sales_tax = subtotal * 0.06
total = subtotal + sales_tax

#five: results
print(f'Sales tax amount: {sales_tax:2f}')
print(f'Total: {total:2f}')