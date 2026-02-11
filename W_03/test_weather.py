# test_weather.py

from weather import cels_from_fahr                          # Importa la función que quiero probar
from pytest import approx                                   # Importa approx para comparar flotantes
import pytest  #                                              Importa pytest completo
def test_cels_from_fahr():                                  # Nombre DEBE empezar con "test_"
    """Test the cels_from_fahr function by calling it and 
    comparing the values it returns to the expected values.
    Notice this test function uses pytest.approx to compare floating-point numbers. """
    assert cels_from_fahr(-25) == approx(-31.66667)         # Prueba 1: número negativo
    assert cels_from_fahr(0) == approx(-17.77778)           # Prueba 2: cero
    assert cels_from_fahr(32) == approx(0)                  # Prueba 3: punto de congelación
    assert cels_from_fahr(70) == approx(21.1111)            # Prueba 4: temperatura ambiente
# Call the main function that is part of pytest so that the
# computer will execute the test functions in this file.
pytest.main(["-v", "--tb=line", "-rN", __file__])

# `-v`: verbose (muestra más detalles)
# `--tb=line`: muestra errores en una línea
# `-rN`: no muestra resumen extra
# `__file__`: prueba este archivo actual