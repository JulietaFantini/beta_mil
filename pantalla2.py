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
        Podés copiarlo, traducirlo o ajustarlo según tus necesidades.
        """
    )

    # Generar el prompt
    prompt = generar_prompt(params)

    # Área editable para personalizar el texto generado
    st.subheader("Descripción detallada - Editá y personalizá si es necesario")
    texto_editable = st.text_area(
        label="Podés editar tu descripción aquí:",
        value=prompt,
        height=300
    )

    # Mostrar el prompt con el botón de copia nativo
    st.subheader("Texto para copiar:")
    st.code(texto_editable, language="")  # Botón nativo de copiar dentro del cuadro de código

    # Opción para traducir al inglés
    st.subheader("Traducción al inglés:")
    st.markdown(
        """
        **¿Por qué traducir?**  
        Muchas herramientas de IA están optimizadas para procesar descripciones en inglés.  
        Usá el botón para traducir el texto en Google Translate.
        """
    )
    if st.button("Abrir en Google Translate"):
        google_translate_url = f"https://translate.google.com/?sl=es&tl=en&text={texto_editable.replace(' ', '%20')}"
        st.markdown(f"[Abrir en Google Translate]({google_translate_url})", unsafe_allow_html=True)

    # Herramientas recomendadas
    st.subheader("Herramientas recomendadas:")
    st.markdown(
        """
        - [**DALL-E**](https://openai.com/dall-e): Ideal para realismo y precisión.  
        - [**Midjourney**](https://www.midjourney.com/): Excelente para resultados artísticos.  
        - [**Stable Diffusion**](https://stability.ai/): Perfecto para personalización detallada.  
        - [**Canva**](https://www.canva.com/): Integra IA con diseño gráfico.  
        - [**Adobe Firefly**](https://www.adobe.com/sensei/generative-ai/adobe-firefly.html): Herramienta profesional con IA.  
        """
    )

    # Botón para modificar parámetros
    if st.button("Modificar parámetros"):
        st.session_state.mostrar_pantalla2 = False

    # Mensaje final
    st.markdown(
        """
        ### Llevá tu visión a la realidad  
        Copiá tu descripción personalizada, traducila al inglés o hacé clic en "Modificar parámetros"  
        para realizar ajustes adicionales. ¡Usá este texto en herramientas de IA para crear imágenes únicas!
        """
    )

def generar_prompt(params):
    """
    Genera un texto narrativo a partir de los parámetros ingresados.
    """
    prompt_parts = []

    # 1. Inicio obligatorio
    prompt_parts.append("Imagina")

    # 2. Tipo de Imagen
    if params.get("tipo_de_imagen"):
        if params["tipo_de_imagen"] == "Otro" and params.get("tipo_de_imagen_personalizado"):
            prompt_parts.append(f"{params['tipo_de_imagen_personalizado']}")
        else:
            prompt_parts.append(f"una {params['tipo_de_imagen'].lower()} (tipo de imagen)")

    # 3. Idea Inicial
    if params.get("idea_inicial"):
        if params["idea_inicial"] == "Otro" and params.get("idea_inicial_personalizado"):
            prompt_parts.append(f"que represente {params['idea_inicial_personalizado']}")
        else:
            prompt_parts.append(f"que represente {params['idea_inicial']} (idea inicial)")

    # 4. Propósito y Subpropósito
    if params.get("proposito_categoria"):
        if params["proposito_categoria"] == "Otro" and params.get("proposito_personalizado"):
            prompt_parts.append(f"diseñada para un propósito que evoque {params['proposito_personalizado']}")
        else:
            proposito_text = f"diseñada para {params['proposito_categoria'].lower()} (propósito)"
            if params.get("subpropósito"):
                proposito_text += f", con un enfoque en {params['subpropósito'].lower()} (subpropósito)"
            prompt_parts.append(proposito_text)

    # 5. Estilo Artístico
    if params.get("estilo_artístico"):
        if params["estilo_artístico"] == "Otro" and params.get("estilo_artístico_personalizado"):
            prompt_parts.append(f"inspirada en {params['estilo_artístico_personalizado']}")
        else:
            prompt_parts.append(f"inspirada en un estilo {params['estilo_artístico'].lower()} (estilo artístico)")

    # Opcionales
    if params.get("iluminación"):
        prompt_parts.append(f"iluminada con {params['iluminación'].lower()} (iluminación)")
    if params.get("plano_fotográfico"):
        prompt_parts.append(f"capturada desde un {params['plano_fotográfico'].lower()} (plano fotográfico)")
    if params.get("composición"):
        prompt_parts.append(f"siguiendo una composición basada en la {params['composición'].lower()} (composición)")
    if params.get("paleta_de_colores"):
        prompt_parts.append(f"utilizando una paleta de colores {params['paleta_de_colores'].lower()} (paleta de colores)")
    if params.get("textura"):
        prompt_parts.append(f"destacando por sus texturas {params['textura'].lower()} (textura)")
    if params.get("resolucion"):
        prompt_parts.append(f"diseñada en una resolución de {params['resolucion']} (resolución)")
    if params.get("aspecto"):
        prompt_parts.append(f"con una relación de aspecto de {params['aspecto']} (relación de aspecto)")

    # Combinar todo
    return ", ".join(prompt_parts) + "."
