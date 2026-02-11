#importthe standart math module so that math.p can be used
import math

def main():
    # call the cone volume function to calculate the volume of a cone
    ex_radius = 2.8
    ex_height = 3.2
    ex_vol = cone_volume(ex_radius, ex_height)

    #print several lines that describe this program
    print("This program computes the volume of a right circular cone.")
    print(f'For example, if the radius of ca one is {ex_radius} and')
    print(f'the height is {ex_height}, then the volume is {ex_vol:.2f}.')
    print()

    #get the radios and height from the user
    radius = float(input('Please enter the radius of the cone: '))
    height = float(input('Please enter the height of the cone: '))

    #call the cone volume function to calculate the volume
    volume = cone_volume(radius, height)

    #print the radius, height and volume
    print(f'Radio: {radius}')
    print(f'Height: {height}')
    print(f'Volume: {volume:.1f}')

def cone_volume(radius, height):
    """calculate and return the volume of a right circular cone"""
    volume = math.pi * radius**2 * height / 3
    return volume

#start the program by calling the main function
main()
