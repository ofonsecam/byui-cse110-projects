# Author: Oscar Fonseca
#Extra requirements: after printing the volume, ask the user if they want to buy tires with the dimensions they entered. If they respond "yes", prompt them to enter their phone number and append it to the volumes.txt file along with the tire dimensions and volume.
# it prompts for a phone number and stores it in the volumes.txt file.

import math
from datetime import datetime

#step 1: get user input for tire dimensions
width = float(input('Enter the width of the tire in mm (ex 205): '))
aspect_ratio = float(input('Enter the aspect ratio of the tire (ex 60): '))
diameter = float(input('Enter the diameter of the wheel in inches (ex 15): '))

# step 2: calculate the tire volume using the formula
volume = (math.pi * width**2 * aspect_ratio * (width * aspect_ratio + 2540 * diameter)) / 10000000000

#step 3: display the result
print(f"The approximate volume of the tire is {volume:.2f} liters")

#step 4: get current date and time
current_datetime = datetime.now()

#step 5: append the data to volume
with open("volumes.txt", "at") as volumes_file:
    print(f"{current_datetime:%Y-%m-%d}, {width:.0f}, {aspect_ratio:.0f}, {diameter:.0f}, {volume:.2f}", file=volumes_file)

#step 6: ask the user if they want to buy tires
choice = input("Do you want to buy tires with the dimensions you entered? (yes/no): ").lower()

if choice == "yes":
    phone_number = input("Please enter your phone number: ")
    with open("volumes.txt", "at") as volumes_file: 
        print(f"Phone: {phone_number}", file=volumes_file)
        print("Thank you! We will contact you soon.")
