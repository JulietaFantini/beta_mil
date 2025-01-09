import streamlit as st
import re

TEMPLATE_BASE = {
    "inicio": "Imagina una imagen de una",
    "representar": "que represente",
    "proposito": "creada para",
    "estilo": "con un estilo que se inspire en",
    "iluminacion": "La iluminación debe ser",
    "plano": "capturada desde un",
    "composicion": "siguiendo una composición de",
    "paleta": "La imagen debe tener una paleta de colores",
    "textura": "y texturas",
    "resolucion": "Finalmente, la resolución debe ser",
    "aspecto": "con una relación de aspecto de"
}

FRASES_OTRO = {
    "tipo_imagen": "Imagina un tipo de imagen inspirado en",
    "idea_inicial": "Concebido como una idea inicial basada en",
    "proposito": "Diseñada para un propósito que evoque",
    "estilo_artistico": "Con un estilo que se inspire en"
}

def validar_parametros(params):
    errores = []
    if params.get("tipo_de_imagen") == "Otro" and not params.get("tipo_de_imagen_personalizado"):
        errores.append("El campo 'Tipo de Imagen' está vacío. Por favor, describe el tipo.")
    if params.get("estilo_artístico") == "Otro" and not params.get("estilo_artístico_personalizado"):
        errores.append("El campo 'Estilo Artístico' está vacío. Por favor, describe el estilo.")
    return errores

def generar_prompt(params):
    prompt_parts = []

    # Tipo de Imagen
    if params.get("tipo_de_imagen"):
        if params["tipo_de_imagen"] == "Otro":
            tipo = params.get("tipo_de_imagen_personalizado", "")
            prompt_parts.append(f"{FRASES_OTRO['tipo_imagen']}: {tipo}")
        else:
            prompt_parts.append(f"{TEMPLATE_BASE['inicio']} {params['tipo_de_imagen'].lower()}")

    # Idea Inicial
    if params.get("idea_inicial"):
        prompt_parts.append(f"{TEMPLATE_BASE['representar']} {params['idea_inicial']}")

    # Propósito
    if params.get("proposito_categoria"):
        proposito = f"{TEMPLATE_BASE['proposito']} {params['proposito_categoria'].lower()}"
        if params.get("subpropósito"):
            proposito += f", orientada hacia {params['subpropósito'].lower()}"
        prompt_parts.append(proposito)

    # Estilo Artístico
    if params.get("estilo_artístico"):
        if params["estilo_artístico"] == "Otro":
            estilo = params.get("estilo_artístico_personalizado", "")
            prompt_parts.append(f"{FRASES_OTRO['estilo_artistico']}: {estilo}")
        else:
            prompt_parts.append(f"{TEMPLATE_BASE['estilo']} {params['estilo_artístico'].lower()}")

    # Opcionales
    opcionales = {
        'iluminación': TEMPLATE_BASE['iluminacion'],
        'plano_fotográfico': TEMPLATE_BASE['plano'],
        'composicion': TEMPLATE_BASE['composicion'],
        'paleta_de_colores': TEMPLATE_BASE['paleta'],
        'textura': TEMPLATE_BASE['textura'],
        'resolucion': TEMPLATE_BASE['resolucion'],
        'aspecto': TEMPLATE_BASE['aspecto']
    }
    for campo, frase in opcionales.items():
        if params.get(campo) and params[campo] != "Seleccioná una opción...":
            prompt_parts.append(f"{frase} {params[campo].lower()}")

    # Combinar partes
    return ". ".join(filter(None, prompt_parts)).capitalize() + "."

def mostrar_prompt(prompt):
    st.subheader("Tu descripción detallada está lista")

    # Versión editable (con etiquetas)
    prompt_editable = st.text_area(
        "Versión con referencias - Podés editar el texto:",
        value=prompt,
        height=300
    )

    # Versión limpia
    prompt_limpio = re.sub(r'\s*\([^)]*\)', '', prompt_editable).strip()
    prompt_limpio = re.sub(r'\s+', ' ', prompt_limpio)

    st.subheader("Versión final para copiar")
    st.code(prompt_limpio, language="")

    return prompt_limpio

def configurar_pantalla2():
    st.title("Generador de Prompts para DALL·E")

    if "params" not in st.session_state:
        st.warning("Completá primero los datos básicos")
        if st.button("Volver a Pantalla 1"):
            st.session_state.mostrar_pantalla2 = False
        return

    errores = validar_parametros(st.session_state.params)
    if errores:
        for error in errores:
            st.error(error)
        return

    prompt_inicial = generar_prompt(st.session_state.params)
    prompt_final = mostrar_prompt(prompt_inicial)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Modificar parámetros"):
            st.session_state.mostrar_pantalla2 = False
    with col2:
        google_translate_url = f"https://translate.google.com/?sl=es&tl=en&text={re.sub(r'\s+', '%20', prompt_final)}"
        st.markdown(f"[Abrir en Google Translate]({google_translate_url})", unsafe_allow_html=True)

if __name__ == "__main__":
    configurar_pantalla2()
