def get_postive_value(prompt):
    """ Purpose: Prompt the user to enter a positive value.
        Return: A positive float value.
    """
    # este es el pront par el valpr
    value = float(input(prompt))

    #Aca verificamos que sea positivo
    while value <= 0:
        print("Error: value must be positive.")
        value = float(input(prompt))

    #aca regresanis el valor
    return value

length = get_postive_value("What is the length of the rectangle? ")
width = get_postive_value("What is the width of the rectangle? ")

area = length * width

print(f"The area is {area}")


