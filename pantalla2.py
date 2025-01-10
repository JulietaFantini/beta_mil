import streamlit as st
import re

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

FRASES_OTRO = {
    "idea_inicial": "Concebido como una idea inicial basada en",
    "proposito": "Diseñada para un propósito que evoque",
    "estilo_artistico": "Con un estilo artístico que recuerde a"
}

def validar_parametros(params):
    errores = []
    if params.get("tipo_de_imagen") == "Otro" and not params.get("tipo_de_imagen_personalizado"):
        errores.append("Seleccionaste 'Otro' como tipo de imagen, pero no lo describiste.")
    if params.get("estilo_artístico") == "Otro" and not params.get("estilo_artístico_personalizado"):
        errores.append("Seleccionaste 'Otro' como estilo artístico, pero no lo describiste.")
    return errores

def generar_prompt(params):
    prompt_parts = []

    if params.get("idea_inicial"):
        prompt_parts.append(f"Imagina {params['idea_inicial'].lower()} representada en una")

    if params.get("tipo_de_imagen"):
        if params["tipo_de_imagen"] == "Otro":
            tipo = params.get("tipo_de_imagen_personalizado", "")
            prompt_parts[-1] = f"Imagina un concepto inspirado en {tipo}"
        else:
            prompt_parts[-1] += f" {params['tipo_de_imagen'].lower()}"

    if params.get("proposito_categoria"):
        proposito = f"creada para {params['proposito_categoria'].lower()}"
        if params.get("subpropósito"):
            proposito += f", orientada hacia {params['subpropósito'].lower()}"
        prompt_parts.append(proposito)

    if params.get("estilo_artístico"):
        if params["estilo_artístico"] == "Otro":
            estilo = params.get("estilo_artístico_personalizado", "")
            prompt_parts.append(f"Con un estilo artístico que recuerde a: {estilo}")
        else:
            prompt_parts.append(f"con el estilo visual del {params['estilo_artístico'].lower()}")

    aspectos_tecnicos = []
    if params.get("iluminación"):
        aspectos_tecnicos.append(f"La imagen debe iluminarse con {params['iluminación'].lower()}")
    if params.get("plano_fotográfico"):
        aspectos_tecnicos.append(f"capturada desde un {params['plano_fotográfico'].lower()}")
    if params.get("composicion"):
        aspectos_tecnicos.append(f"siguiendo una composición de {params['composicion'].lower()}")
    if aspectos_tecnicos:
        prompt_parts.append(". " + ", ".join(aspectos_tecnicos))

    aspectos_visuales = []
    if params.get("paleta_de_colores"):
        aspectos_visuales.append(f"Debe tener una paleta de colores {params['paleta_de_colores'].lower()}")
    if params.get("textura"):
        aspectos_visuales.append(f"y una textura {params['textura'].lower()}")
    if aspectos_visuales:
        prompt_parts.append(", " + ", ".join(aspectos_visuales))

    if params.get("resolucion") and params.get("aspecto"):
        prompt_parts.append(f". Finalmente, la resolución debe ser {params['resolucion']}, con una relación de aspecto de {params['aspecto'].lower()}")

    prompt = " ".join(filter(None, prompt_parts)).strip()
    prompt = re.sub(r'\s+', ' ', prompt)  # Corregir espacios múltiples
    prompt = re.sub(r'\s+\.', '.', prompt)  # Eliminar espacios antes de puntos
    prompt = re.sub(r',\s*', ', ', prompt)  # Corregir comas y espacios
    sentences = re.split(r'(?<=\.)\s+', prompt)  # Separar por puntos para capitalizar
    prompt = '. '.join(sentence.capitalize() for sentence in sentences)  # Capitalizar frases
    prompt = re.sub(r'\.\.+', '.', prompt)  # Eliminar puntos duplicados
    if not prompt.endswith('.'):
        prompt += '.'

    return prompt

def mostrar_prompt(prompt):
    st.subheader("Descripción Detallada")

    st.markdown("Puedes editar tu descripción directamente en el cuadro de texto para personalizarla aún más según tus necesidades.")

    prompt_editable = st.text_area(
        "Versión con referencias - Podés editar el texto:",
        value=prompt,
        height=200
    )

    prompt_limpio = re.sub(r'\s*\([^)]*\)', '', prompt_editable).strip()
    prompt_limpio = re.sub(r'\s+', ' ', prompt_limpio)

    st.subheader("Texto Final para Copiar")
    st.markdown("Haz clic en el botón 'Copiar código' para guardar el texto generado en tu portapapeles y usarlo en tu herramienta de IA preferida.")
    st.code(prompt_limpio, language="")

    return prompt_limpio

def configurar_pantalla2():
    st.title("Tu prompt está listo")
    st.markdown("Este texto combina todos los parámetros que seleccionaste en un formato optimizado para IA. Revísalo, edítalo si es necesario y cópialo fácilmente.")

    if "params" not in st.session_state:
        st.warning("Faltan algunos datos importantes. Por favor, vuelve a la pantalla anterior y completa los campos obligatorios.")
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

    if st.button("Modificar parámetros"):
        st.markdown("Regresa a la pantalla anterior para ajustar los parámetros y generar un nuevo prompt.")
        st.session_state.mostrar_pantalla2 = False

    st.subheader("Traducción al Inglés")
    st.markdown("Muchas herramientas de IA están optimizadas para prompts en inglés. Usa el botón de traducción para llevar tu descripción a Google Translate.")

    google_translate_url = f"https://translate.google.com/?sl=es&tl=en&text={re.sub(r'\s+', '%20', prompt_final)}"
    st.markdown(f"[Traducir el texto en Google Translate]({google_translate_url})", unsafe_allow_html=True)

    st.subheader("Herramientas Recomendadas")
    st.markdown("Explora estas herramientas populares para generar imágenes con IA:")
    st.markdown("""
        * **DALL-E:** Realismo y precisión excepcionales.
        * **Midjourney:** Diseños artísticos únicos.
        * **Stable Diffusion:** Perfecto para personalización detallada.
        * **Canva:** Diseño gráfico con IA integrada.
        * **Adobe Firefly:** Resultados profesionales con IA.
    """)

if __name__ == "__main__":
    configurar_pantalla2()
