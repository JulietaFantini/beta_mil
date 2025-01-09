import streamlit as st

# Constantes para conectores y frases base
VERBOS_BASE = {
    'representar': 'que represente',
    'proposito': 'diseñada para',
    'estilo': 'con',
    'iluminacion': 'bañada en luz',
    'plano': 'mostrando detalles capturados desde un plano',
    'composicion': 'siguiendo una composición basada en',
}

FRASES_OTRO = {
    'tipo_imagen': 'inspirada en',
    'idea_inicial': 'basada en',
    'proposito': 'orientada hacia',
    'estilo': 'con',
}

# Validación de datos
def validar_datos(params):
    """
    Valida los datos proporcionados para asegurar coherencia y evitar errores.
    """
    errores = []
    if not params.get("idea_inicial"):
        errores.append("La 'Idea Inicial' no puede estar vacía.")
    if params.get("tipo_de_imagen") == "Otro" and not params.get("tipo_de_imagen_personalizado"):
        errores.append("Si seleccionaste 'Otro' en 'Tipo de Imagen', completa su descripción.")
    if params.get("estilo_artístico") == "Otro" and not params.get("estilo_artístico_personalizado"):
        errores.append("Si seleccionaste 'Otro' en 'Estilo Artístico', completa su descripción.")
    return errores

# Generación del prompt
def generar_prompt(params):
    """
    Genera un texto narrativo fluido a partir de los parámetros predefinidos.
    """
    partes_prompt = ["Imagina"]

    # Idea inicial
    if params.get("idea_inicial"):
        partes_prompt.append(params["idea_inicial"].lower())

    # Tipo de Imagen
    if params.get("tipo_de_imagen") == "Otro":
        partes_prompt.append(f"{FRASES_OTRO['tipo_imagen']} {params.get('tipo_de_imagen_personalizado', '').lower()}")
    else:
        partes_prompt.append(f"representada en una {params['tipo_de_imagen'].lower()}")

    # Propósito
    if params.get("proposito_categoria"):
        texto_proposito = f"{VERBOS_BASE['proposito']} {params['proposito_categoria'].lower()}"
        if params.get("subpropósito"):
            texto_proposito += f", {FRASES_OTRO['proposito']} {params['subpropósito'].lower()}"
        partes_prompt.append(texto_proposito)

    # Estilo Artístico
    if params.get("estilo_artístico") == "Otro":
        partes_prompt.append(f"{FRASES_OTRO['estilo']} {params.get('estilo_artístico_personalizado', '').lower()} como estilo")
    else:
        partes_prompt.append(f"{VERBOS_BASE['estilo']} {params['estilo_artístico'].lower()} como estilo")

    # Opcionales
    opcionales = {
        'iluminación': VERBOS_BASE['iluminacion'],
        'plano_fotográfico': VERBOS_BASE['plano'],
        'composicion': VERBOS_BASE['composicion'],
        'paleta_de_colores': 'utilizando una paleta de colores',
        'textura': 'destacando texturas',
        'resolucion': 'en una resolución de',
        'aspecto': 'con una relación de aspecto de',
    }
    for campo, verbo in opcionales.items():
        if params.get(campo) and params[campo] != "Seleccioná una opción...":
            partes_prompt.append(f"{verbo} {params[campo].lower()}")

    # Combinar partes con narrativa consolidada
    return ", ".join(partes_prompt).capitalize() + "."

# Configuración de Pantalla 2
def configurar_pantalla2():
    """
    Configura Pantalla 2 para generar y mostrar el prompt.
    """
    # Verifica que los parámetros existan
    if "params" not in st.session_state or not st.session_state.params:
        st.warning("No se han proporcionado datos de la Pantalla 1. Regresa y completa los campos obligatorios.")
        if st.button("Volver a Pantalla 1"):
            st.session_state.mostrar_pantalla2 = False
        return

    # Obtiene los parámetros
    params = st.session_state.params

    # Validaciones
    errores = validar_datos(params)
    if errores:
        st.error("Errores detectados:")
        for error in errores:
            st.markdown(f"- {error}")
        return

    # Genera el prompt
    prompt = generar_prompt(params)

    # Layout de la pantalla
    st.title("Tu prompt está listo")
    st.markdown(
        """
        Este texto combina todos los parámetros que seleccionaste en un formato optimizado para IA. Revísalo y ajústalo si lo necesitas.
        """
    )

    # Muestra el prompt generado
    st.subheader("Texto generado - Edita y personaliza si es necesario.")
    texto_editable = st.text_area("Edita tu prompt aquí:", value=prompt, height=200)

    # Opciones de interacción
    st.subheader("Opciones")
    st.code(texto_editable, language="")  # Botón de copia nativo
    if st.button("Copiar código"):
        st.success("Prompt copiado correctamente al portapapeles.")

    if st.button("Abrir en Google Translate"):
        google_translate_url = f"https://translate.google.com/?sl=es&tl=en&text={texto_editable.replace(' ', '%20')}"
        st.markdown(f"[Abrir en Google Translate]({google_translate_url})", unsafe_allow_html=True)

    if st.button("Ajustar parámetros"):
        st.session_state.mostrar_pantalla2 = False
        st.markdown("Regresa a la pantalla anterior para ajustar los parámetros y generar un nuevo prompt.")

    # Herramientas recomendadas
    st.subheader("Herramientas recomendadas")
    st.markdown(
        """
        - **DALL-E**: Ideal para realismo y precisión.  
        - **Midjourney**: Excelente para resultados artísticos.  
        - **Stable Diffusion**: Perfecto para personalización detallada.  
        - **Canva**: Integra IA con diseño gráfico.  
        - **Adobe Firefly**: Herramienta profesional con IA.
        """
    )

# Ejecuta Pantalla 2
if __name__ == "__main__":
    configurar_pantalla2()
