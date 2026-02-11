def main():
    # Obtener el valor del odometro inicial
    start_miles = float (input("Enter the starting odometer reading (miles): "))

    # Obetener otro valor del odometro
    end_miles = float(input("Enter the ending odometer reading (miles): "))

    #Obtener galones de gasolina usados
    amount_gallons = float(input("Enter the amount of fuel used (gallons): "))

    #calcular millas por galon el resultado es una vairable llamada mpg
    mpg = miles_per_gallon(start_miles, end_miles, amount_gallons)

    #llamamos lp100k_from_mpg para convertir mpg a l/100km y almacenamos el resultado en lp100k
    lp100k = lp100k_from_mpg(mpg)

    #mostrar los resultados
    print(f'{mpg:.1f} miles per gallon')
    print(f'{lp100k:.2f} liters per 100 km')

def miles_per_gallon(start_miles, end_miles, amount_gallons):
    """
    eEl proposito es vonveritr de millas y galones a millas por galon
    parameters:
        start_miles: An odometer value in miles.
        end_miles: Another odometer value in miles.
        amount_gallons: The amount of fuel used in gallons.
    Return: Fuel efficiency in miles per gallon.
    """
    mpg = (end_miles - start_miles) / amount_gallons
    return mpg

def lp100k_from_mpg(mpg):
    """
    Purpose: Convert miles per gallon to liters per 100 kilometers.
    Parameter:
        mpg: Fuel efficiency in miles per gallon.
    Return: Fuel efficiency in liters per 100 kilometers.
    """
    lp100k = 235.215 / mpg
    return lp100k

# llamamos la funcion main para iniciar el programa
main()
