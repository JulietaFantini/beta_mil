import pytest
from validaciones import validar_errores

def test_validar_errores():
    # Caso de prueba con parámetros completos
    params_validos = {
        "tipo_de_imagen": "Fotografía",
        "idea_inicial": "Una ciudad flotante al amanecer",
        "estilo_artístico": "Arte Digital",
        "proposito_categoria": "Comercial y Marketing"
    }
    errores = validar_errores(params_validos)
    assert len(errores) == 0  # No debería haber errores

    # Caso de prueba con parámetros faltantes
    params_invalidos = {
        "tipo_de_imagen": "",
        "idea_inicial": "",
        "estilo_artístico": "Arte Digital",
        "proposito_categoria": ""
    }
    errores = validar_errores(params_invalidos)
    assert len(errores) > 0  # Debería haber errores debido a los campos vacíos

