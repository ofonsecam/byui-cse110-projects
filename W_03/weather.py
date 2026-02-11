# weather.py
def cels_from_fahr(fahr):
    """Convert a temperature from fahrenheit to celsius."""
    cels = (fahr - 32) * 5 / 9
    return cels