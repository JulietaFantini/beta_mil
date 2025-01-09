import streamlit as st
import textwrap

# Constantes para verbos y frases de "Otro"
VERBOS_BASE = {
    'representar': 'que represente',
    'proposito': 'diseñada para',
    'estilo': 'inspirada en un estilo',
    'iluminacion': 'iluminada con',
    'plano': 'capturada desde',
    'composicion': 'siguiendo una composición basada en',
}

FRASES_OTRO = {
    'tipo_imagen': 'un tipo de imagen inspirado en',
    'idea_inicial': 'una idea inicial basada en',
    'proposito': 'un propósito que evoque',
    'estilo': 'un estilo artístico que recuerde a',
}

def generar_prompt(params):
    """
    Genera un texto narrativo a partir de los parámetros ingresados.
    """
    prompt_parts = []

    # 1. Inicio obligatorio con "Imagina"
    prompt_parts.append("Imagina")

    # 2. Tipo de imagen
    if params.get("tipo_de_imagen"):
        if params["tipo_de_imagen"] == "Otro" and params.get("tipo_de_imagen_personalizado"):
            valor = params['tipo_de_imagen_personalizado'].lower()
            prompt_parts.append(f"{FRASES_OTRO['tipo_imagen']} {valor}")
        else:
            prompt_parts.append(f"{params['tipo_de_imagen'].lower()} (tipo de imagen)")

    # 3. Idea inicial
    if params.get("idea_inicial"):
        if params["idea_inicial"] == "Otro" and params.get("idea_inicial_personalizado"):
            valor = params['idea_inicial_personalizado'].lower()
            prompt_parts.append(f"{FRASES_OTRO['idea_inicial']} {valor}")
        else:
            prompt_parts.append(f"{VERBOS_BASE['representar']} {params['idea_inicial'].lower()} (idea inicial)")

    # 4. Propósito y subpropósito
    if params.get("proposito_categoria"):
        if params["proposito_categoria"] == "Otro" and params.get("proposito_personalizado"):
            valor = params['proposito_personalizado'].lower()
            prompt_parts.append(f"{FRASES_OTRO['proposito']} {valor}")
        else:
            proposito_text = f"{VERBOS_BASE['proposito']} {params['proposito_categoria'].lower()} (propósito)"
            if params.get("subpropósito"):
                proposito_text += f", con un enfoque en {params['subpropósito'].lower()} (subpropósito)"
            prompt_parts.append(proposito_text)

    # 5. Estilo artístico
    if params.get("estilo_artístico"):
        if params["estilo_artístico"] == "Otro" and params.get("estilo_artístico_personalizado"):
            valor = params['estilo_artístico_personalizado'].lower()
            prompt_parts.append(f"{FRASES_OTRO['estilo']} {valor}")
        else:
            prompt_parts.append(f"{VERBOS_BASE['estilo']} {params['estilo_artístico'].lower()} (estilo artístico)")

    # Opcionales (iluminación, plano, etc.)
    opcionales = {
        'iluminación': VERBOS_BASE['iluminacion'],
        'plano_fotográfico': VERBOS_BASE['plano'],
        'composición': VERBOS_BASE['composicion'],
        'paleta_de_colores': 'utilizando una paleta de colores',
        'textura': 'destacando por sus texturas',
        'resolucion': 'diseñada en una resolución de',
        'aspecto': 'con una relación de aspecto de',
    }

    for campo, verbo in opcionales.items():
        if params.get(campo):
            valor = params[campo].split(" ")[0].lower() if campo in ['resolucion', 'aspecto'] else params[campo].lower()
            prompt_parts.append(f"{verbo} {valor} ({campo})")

    # Formato final
    prompt = ". ".join(filter(None, prompt_parts)) + "."
    return textwrap.fill(prompt, width=80)

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

    # Encabezado y texto de introducción dentro de un contenedor para evitar desplazamientos
    with st.container():
        st.title("Tu descripción detallada está lista")
        st.markdown(
            """
            A continuación encontrarás el texto generado a partir de tus selecciones.  
            Este texto está optimizado para herramientas de generación de imágenes con IA.  
            Podés copiarlo, traducirlo o ajustarlo según tus necesidades.
            """
        )

    params = st.session_state.params

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
