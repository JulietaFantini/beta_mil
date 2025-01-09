import streamlit as st

def validar_errores(params):
    """
    Valida los campos obligatorios ingresados en Pantalla 1.
    Si algún campo obligatorio está vacío o con el valor predeterminado 'Seleccioná una opción...', 
    genera un error correspondiente para ese campo.
    """
    campos_obligatorios = {
        "tipo_de_imagen": "Selecciona un tipo de imagen.",
        "idea_inicial": "Describe tu idea inicial.",
        "estilo_artístico": "Selecciona un estilo artístico.",
        "proposito_categoria": "Indica el propósito de la imagen."
    }
    
    errores = [
        mensaje for campo, mensaje in campos_obligatorios.items()
        if not params.get(campo) or params.get(campo) == "Seleccioná una opción..."
    ]
    
    return errores


def validar_advertencias(params):
    """
    Genera advertencias para los campos opcionales.
    Si algún campo opcional está vacío o tiene el valor predeterminado 'Seleccioná una opción...',
    devuelve una lista de advertencias indicando qué campo podría afectar los resultados de generación de imagen.
    """
    advertencias = [
        f"El campo '{campo.replace('_', ' ').capitalize()}' no está completo, lo cual puede afectar los resultados. Se recomienda completarlo para obtener mejores resultados."
        for campo in ["iluminación", "plano_fotográfico", "composición", "paleta_de_colores", "textura", "resolucion", "aspecto"]
        if not params.get(campo) or params.get(campo) == "Seleccioná una opción..."
    ]
    
    return advertencias
