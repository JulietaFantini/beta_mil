import streamlit as st
import re

# --------------------------------------------------------------------------------
# 1. Función para validar parámetros
# --------------------------------------------------------------------------------
def validar_parametros(params):
    """
    Verifica si en 'Otro' no se dejó vacío el campo personalizado.
    Retorna una lista de strings con errores si algo falta.
    """
    errores = []
    if params.get("tipo_de_imagen") == "Otro" and not params.get("tipo_de_imagen_personalizado"):
        errores.append("Seleccionaste 'Otro' como tipo de imagen, pero no lo describiste.")
    if params.get("estilo_artístico") == "Otro" and not params.get("estilo_artístico_personalizado"):
        errores.append("Seleccionaste 'Otro' como estilo artístico, pero no lo describiste.")
    return errores

# --------------------------------------------------------------------------------
# 2. Función para generar el prompt (versión mejorada)
# --------------------------------------------------------------------------------
def generar_prompt_mejorado(params):
    """
    Toma los parámetros en 'params' y construye un texto (prompt) con lógica:
    - Idea inicial
    - Tipo de imagen
    - Propósito
    - Estilo artístico
    - Aspectos técnicos (iluminación, plano, composición)
    - Aspectos visuales (paleta, texturas)
    - Resolución y relación de aspecto
    Agrega limpieza y capitalización final.
    """
    prompt_parts = []

    # Idea inicial
    if params.get("idea_inicial"):
        prompt_parts.append(f"Imagina {params['idea_inicial']} representada en una")

    # Tipo de imagen
    if params.get("tipo_de_imagen"):
        if params["tipo_de_imagen"] == "Otro":
            tipo_pers = params.get("tipo_de_imagen_personalizado", "")
            if prompt_parts:
                prompt_parts[-1] = f"Imagina un concepto inspirado en {tipo_pers}"
            else:
                prompt_parts.append(f"Imagina un concepto inspirado en {tipo_pers}")
        else:
            if prompt_parts:
                prompt_parts[-1] += f" {params['tipo_de_imagen'].lower()}"
            else:
                prompt_parts.append(f"Imagina {params['tipo_de_imagen'].lower()}")

    # Propósito
    if params.get("proposito_categoria"):
        proposito_text = f"diseñada para {params['proposito_categoria'].lower()}"
        if params.get("subpropósito"):
            proposito_text += f", orientada hacia {params['subpropósito'].lower()}"
        prompt_parts.append(proposito_text)

    # Estilo artístico
    if params["estilo_artístico"] == "Otro":
    ...
