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
        Debajo encontrarás el texto generado a partir de tus selecciones. Reúne todos los detalles en una descripción efectiva lista para usar en herramientas de IA.
        Revisá el texto y realizá los ajustes necesarios para obtener los mejores resultados en la generación de imágenes.
        """
    )

    # Generar el prompt
    prompt = generar_prompt(params)

    # Cuadro Editable para el Prompt
    st.subheader("Descripción detallada - Editá y personalizá si es necesario")
    texto_editable = st.text_area(
        label="Editá tu descripción aquí:",
        value=prompt,
        height=300,  # Altura ajustada para mayor legibilidad
        key="texto_editable"
    )

    # Cuadro de Copia con el Texto Actualizado
    st.subheader("Texto para copiar")
    st.code(texto_editable, language="")  # Botón nativo de copiar funcional

    # Sección: Traducción al Inglés
    st.subheader("Traducción al inglés")
    st.markdown(
        """
        **¿Por qué traducir?**  
        Muchas herramientas de IA están optimizadas para procesar descripciones en inglés. Usa el botón de traducción para llevar tu descripción a Google Translate.
        """
    )
    if st.button("Abrir en Google Translate"):
        google_translate_url = f"https://translate.google.com/?sl=es&tl=en&text={texto_editable.replace(' ', '%20')}"
        st.markdown(f"[Abrir en Google Translate]({google_translate_url})", unsafe_allow_html=True)

    # Sección: Herramientas Recomendadas
    st.subheader("Herramientas recomendadas")
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
    if st.button("Modificar Parámetros"):
        st.session_state.mostrar_pantalla2 = False

    # Mensaje final
    st.subheader("Llevá tu visión a la realidad")
    st.markdown(
        """
        Con tu descripción personalizada, estás listo para generar imágenes asombrosas usando herramientas de inteligencia artificial. 
        Copiá el texto generado y pegalo en la herramienta de tu elección. ¡Dejá volar tu creatividad y comenzá a crear imágenes únicas!
        """
    )

def generar_prompt(params):
    """
    Genera un texto narrativo a partir de los parámetros ingresados, optimizando la coherencia y fluidez.
    """
    prompt_parts = []

    if params.get("idea_inicial"):
        idea = params["idea_inicial"].capitalize()
        prompt_parts.append(f"Imagina {idea}")

    if params.get("tipo_de_imagen"):
        tipo = params["tipo_de_imagen"]
        prompt_parts.append(f", representada como una {tipo.lower()}.")

    if params.get("proposito_categoria"):
        subproposito = params.get("subproposito", "").lower()
        proposito_text = f"diseñada para {params['proposito_categoria'].lower()}"
        if subproposito:
            proposito_text += f", con enfoque en {subproposito}"
        prompt_parts.append(f"{proposito_text}.")

    if params.get("estilo_artístico"):
        prompt_parts.append(f"Inspirada en un estilo {params['estilo_artístico'].lower()}.")

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
