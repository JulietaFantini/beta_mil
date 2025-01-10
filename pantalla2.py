import streamlit as st
import re

# Estructura para plantillas de frases
TEMPLATE_BASE = {
    "inicio": "Imagina",
    "representar": "que represente",
    "proposito": "creada para",
    "estilo": "con el estilo visual del",
    "iluminacion": "La imagen debe iluminarse con",
    "plano": "capturada desde un",
    "composicion": "siguiendo una composición de",
    "paleta": "Debe tener una paleta de colores",
    "textura": "y una textura",
    "resolucion": "Finalmente, la resolución debe ser",
    "aspecto": "con una relación de aspecto de"
}

# Frases adicionales para "Otro"
FRASES_OTRO = {
    "idea_inicial": "Concebido como una idea inicial basada en",
    "proposito": "Diseñada para un propósito que evoque",
    "estilo_artistico": "Con un estilo artístico que recuerde a"
}

# Validar parámetros

def validar_parametros(params):
    errores = []
    if params.get("tipo_de_imagen") == "Otro" and not params.get("tipo_de_imagen_personalizado"):
        errores.append("Seleccionaste 'Otro' como tipo de imagen, pero no lo describiste.")
    if params.get("estilo_artístico") == "Otro" and not params.get("estilo_artístico_personalizado"):
        errores.append("Seleccionaste 'Otro' como estilo artístico, pero no lo describiste.")
    return errores

# Generar prompt con ajustes

def generar_prompt(params):
    prompt_parts = []

    if params.get("idea_inicial"):
        prompt_parts.append(f"Imagina {params['idea_inicial']} representada en una")

    if params.get("tipo_de_imagen"):
        if params["tipo_de_imagen"] == "Otro":
            tipo = params.get("tipo_de_imagen_personalizado", "")
            prompt_parts[-1] = f"Imagina un concepto inspirado en {tipo}"
        else:
            prompt_parts[-1] += f" {params['tipo_de_imagen'].lower()}"

    if params.get("proposito_categoria"):
        proposito = f"{TEMPLATE_BASE['proposito']} {params['proposito_categoria'].lower()}"
        if params.get("subpropósito"):
            proposito += f", orientada hacia {params['subpropósito'].lower()}"
        prompt_parts.append(proposito)

    if params.get("estilo_artístico"):
        if params["estilo_artístico"] == "Otro":
            estilo = params.get("estilo_artístico_personalizado", "")
            prompt_parts.append(f"{FRASES_OTRO['estilo_artistico']}: {estilo}")
        else:
            prompt_parts.append(f"{TEMPLATE_BASE['estilo']} {params['estilo_artístico'].lower()}")

    aspectos_tecnicos = []
    if params.get("iluminación"):
        aspectos_tecnicos.append(f"{TEMPLATE_BASE['iluminacion']} {params['iluminación'].lower()}")
    if params.get("plano_fotográfico"):
        aspectos_tecnicos.append(f"{TEMPLATE_BASE['plano']} {params['plano_fotográfico'].lower()}")
    if params.get("composicion"):
        aspectos_tecnicos.append(f"{TEMPLATE_BASE['composicion']} {params['composicion'].lower()}")
    if aspectos_tecnicos:
        prompt_parts.append(". " + ", ".join(aspectos_tecnicos))

    aspectos_visuales = []
    if params.get("paleta_de_colores"):
        aspectos_visuales.append(f"{TEMPLATE_BASE['paleta']} {params['paleta_de_colores'].lower()}")
    if params.get("textura"):
        aspectos_visuales.append(f"{TEMPLATE_BASE['textura']} {params['textura'].lower()}")
    if aspectos_visuales:
        prompt_parts.append(", " + ", ".join(aspectos_visuales))

    if params.get("resolucion") and params.get("aspecto"):
        prompt_parts.append(f". {TEMPLATE_BASE['resolucion']} {params['resolucion']}, {TEMPLATE_BASE['aspecto']} {params['aspecto'].lower()}")

    prompt = " ".join(filter(None, prompt_parts)).strip()
    prompt = re.sub(r'\s+', ' ', prompt)
    prompt = re.sub(r',\s*', ', ', prompt)
    sentences = re.split(r'(?<=\.)\s+', prompt)
    prompt = '. '.join(sentence[:1].upper() + sentence[1:] for sentence in sentences)
    prompt = re.sub(r'\.\.+', '.', prompt)
    if not prompt.endswith('.'): 
        prompt += '.'

    return prompt

# Mostrar prompt

def mostrar_prompt(prompt):
    st.subheader("Descripción Detallada")

    st.markdown("Podés editar la descripción directamente en el cuadro de texto para personalizarla.")

    prompt_editable = st.text_area(
        "Versión con referencias - Podés editar el texto:",
        value=prompt,
        height=200,
        key="editable_prompt"
    )

    prompt_limpio = re.sub(r'\s*\([^)]*\)', '', prompt_editable).strip()
    prompt_limpio = re.sub(r'\s+', ' ', prompt_limpio)

    st.subheader("Texto Final para Copiar")
    st.code(prompt_limpio, language="")

    return prompt_limpio

# Configurar Pantalla 2

def configurar_pantalla2():
    st.title("Tu prompt está listo")
    st.markdown("Este texto combina todos los parámetros seleccionados en un formato optimizado para IA.")

    st.markdown(
        """
        <script>
            window.scrollTo(0, 0);
        </script>
        """,
        unsafe_allow_html=True
    )

    if "params" not in st.session_state:
        st.warning("Faltan datos importantes. Volvé a la pantalla anterior para completarlos.")
        if st.button("Volver a Pantalla 1"):
            st.session_state.mostrar_pantalla2 = False
            st.experimental_rerun()
        return

    errores = validar_parametros(st.session_state.params)
    if errores:
        for error in errores:
            st.error(error)
        return

    prompt_inicial = generar_prompt(st.session_state.params)
    st.write("**DEBUG: Prompt inicial generado antes de mostrar:**", prompt_inicial)

    prompt_final = mostrar_prompt(prompt_inicial)

    if st.button("Modificar parámetros"):
        st.session_state.mostrar_pantalla2 = False

if __name__ == "__main__":
    configurar_pantalla2()
