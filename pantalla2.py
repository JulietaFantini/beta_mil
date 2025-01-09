import streamlit as st

def configurar_pantalla2():
    """
    Pantalla 2: Generación del Prompt a partir de los datos ingresados.
    """
    # Validar si los parámetros están disponibles
    if "params" not in st.session_state or not st.session_state.params:
        st.warning("No se han proporcionado datos de la Pantalla 1. Regresa y completa los campos obligatorios.")
        if st.button("Volver a Pantalla 1"):
            st.session_state.mostrar_pantalla2 = False
        return

    params = st.session_state.params

    # Encabezado y texto de introducción
    st.title("Tu descripción detallada está lista")
    st.markdown(
        """
        A continuación encontrarás el texto generado a partir de tus selecciones.  
        Este texto está optimizado para herramientas de generación de imágenes con IA.  
        Podés copiarlo o editarlo según tus necesidades.
        """
    )

    # Generar el prompt
    prompt = generar_prompt(params)

    # Mostrar el prompt en un cuadro editable
    st.text_area(
        label="Texto generado - Editá y personalizá si es necesario:",
        value=prompt,
        height=300,
        key="texto_editable"
    )

    # Botón nativo para copiar texto
    st.download_button(
        label="Descargar descripción como archivo .txt",
        data=prompt,
        file_name="descripcion_generada.txt",
        mime="text/plain"
    )

    # Botón para modificar parámetros
    if st.button("Modificar Parámetros"):
        st.session_state.mostrar_pantalla2 = False

    # Mensaje final
    st.markdown(
        """
        ### Llevá tu visión a la realidad  
        Copiá tu descripción personalizada o hacé clic en "Modificar Parámetros" para realizar ajustes adicionales.  
        ¡Usá este texto en herramientas de IA para crear imágenes increíbles!
        """
    )

def generar_prompt(params):
    """
    Genera un texto narrativo a partir de los parámetros ingresados.
    """
    prompt_parts = []

    if params.get("idea_inicial"):
        idea = params["idea_inicial"].capitalize()
        prompt_parts.append(f"Imagina {idea}")

    if params.get("tipo_de_imagen"):
        tipo = params["tipo_de_imagen"]
        prompt_parts.append(f", representada como una {tipo.lower()}.")

    if params.get("proposito_categoria"):
        subproposito = params.get("subpropósito", "").lower()
        proposito_text = f"diseñada para {params['proposito_categoria'].lower()}"
        if subproposito:
            proposito_text += f", con enfoque en {subproposito}"
        prompt_parts.append(f"{proposito_text}.")

    if params.get("estilo_artístico"):
        estilo = params["estilo_artístico"]
        prompt_parts.append(f"Inspirada en un estilo {estilo.lower()}.")

    if params.get("iluminación"):
        iluminacion_text = params["iluminación"]
        prompt_parts.append(f"Iluminada con {iluminacion_text.lower()}.")

    if params.get("plano_fotográfico"):
        prompt_parts.append(f"Capturada desde un {params['plano_fotográfico'].lower()}.")

    if params.get("composición"):
        composicion_text = params["composición"]
        prompt_parts.append(f"Siguiendo una composición basada en la {composicion_text.lower()}.")

    if params.get("paleta_de_colores"):
        color_text = params["paleta_de_colores"]
        prompt_parts.append(f"Utiliza una paleta de colores {color_text.lower()}.")

    if params.get("textura"):
        textura_text = params["textura"]
        prompt_parts.append(f"Destaca por sus texturas {textura_text.lower()}.")

    if params.get("resolucion"):
        prompt_parts.append(f"Resolución {params['resolucion']}.")

    if params.get("aspecto"):
        aspect_ratio = params["aspecto"]
        prompt_parts.append(f"Con relación de aspecto {aspect_ratio.lower()}.")

    return " ".join(prompt_parts)
