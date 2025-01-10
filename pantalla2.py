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
        errores.append("El campo 'Tipo de Imagen' está vacío. Por favor, describe el tipo.")
    if params.get("estilo_artístico") == "Otro" and not params.get("estilo_artístico_personalizado"):
        errores.append("El campo 'Estilo Artístico' está vacío. Por favor, describe el estilo.")
    return errores

def generar_prompt(params):
    prompt_parts = []

    # Idea Inicial antes de Tipo de Imagen
    if params.get("idea_inicial"):
        prompt_parts.append(f"Imagina {params['idea_inicial'].lower()} representada en una")

    # Tipo de Imagen
    if params.get("tipo_de_imagen"):
        if params["tipo_de_imagen"] == "Otro":
            tipo = params.get("tipo_de_imagen_personalizado", "")
            prompt_parts[-1] = f"Imagina un concepto inspirado en {tipo}"
        else:
            prompt_parts[-1] += f" {params['tipo_de_imagen'].lower()}"

    # Propósito de la Imagen
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
            prompt_parts.append(f"{TEMPLATE_BASE['estilo']} {params['estilo_artístico'].lower()}"
)

    # Iluminación
    if params.get("iluminación"):
        prompt_parts.append(f"{TEMPLATE_BASE['iluminacion']} {params['iluminación'].lower()}"
)

    # Plano Fotográfico
    if params.get("plano_fotográfico"):
        prompt_parts.append(f"{TEMPLATE_BASE['plano']} {params['plano_fotográfico'].lower()}"
)

    # Composición
    if params.get("composicion"):
        prompt_parts.append(f"{TEMPLATE_BASE['composicion']} {params['composicion'].lower()}"
)

    # Paleta de Colores y Textura
    if params.get("paleta_de_colores"):
        prompt_parts.append(f"{TEMPLATE_BASE['paleta']} {params['paleta_de_colores'].lower()}"
)
    if params.get("textura"):
        prompt_parts.append(f"{TEMPLATE_BASE['textura']} {params['textura'].lower()}"
)

    # Resolución y Relación de Aspecto
    if params.get("resolucion") and params.get("aspecto"):
        prompt_parts.append(f"{TEMPLATE_BASE['resolucion']} {params['resolucion']}, {TEMPLATE_BASE['aspecto']} {params['aspecto'].lower()}"
)

    # Combinar partes
    return " ".join(prompt_parts).capitalize() + "."

def mostrar_prompt(prompt):
    st.subheader("Descripción Detallada")

    # Versión editable (con etiquetas)
    prompt_editable = st.text_area(
        "Versión con referencias - Podés editar el texto:",
        value=prompt,
        height=200
    )

    # Versión limpia
    prompt_limpio = re.sub(r'\s*\([^)]*\)', '', prompt_editable).strip()
    prompt_limpio = re.sub(r'\s+', ' ', prompt_limpio)

    st.subheader("Texto Final para Copiar")
    st.markdown(
        """
        **Haz clic en el botón para copiar el texto generado en tu portapapeles y usarlo en tu herramienta de IA preferida.**
        """
    )
    st.code(prompt_limpio, language="")

    return prompt_limpio

def configurar_pantalla2():
    st.title("Tu prompt está listo")
    st.markdown(
    """
    Este texto combina todos los parámetros que seleccionaste en un formato optimizado para IA. Revísalo, edítalo si es necesario y cópialo fácilmente.
    """
)

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
        st.markdown(
            """
            **Regresa a la pantalla anterior para ajustar los parámetros y generar un nuevo prompt.**
            """
        )
        st.session_state.mostrar_pantalla2 = False

    st.subheader("Traducción al Inglés")
    st.markdown(
        """
        Traducí tu descripción al inglés para mejorar la compatibilidad con herramientas de IA.  
        Al hacer clic en el enlace, tu texto se abrirá directamente en Google Translate.
        """
    )
    google_translate_url = f"https://translate.google.com/?sl=es&tl=en&text={re.sub(r'\s+', '%20', prompt_final)}"
    st.markdown(f"[Traducir el texto en Google Translate]({google_translate_url})", unsafe_allow_html=True)

    st.subheader("Explora Herramientas Recomendadas")
    st.markdown(
        """
        Explora estas herramientas populares para generar imágenes con IA:
        - **[DALL-E](https://openai.com/dall-e)**: Realismo y precisión excepcionales.  
        - **[Midjourney](https://www.midjourney.com/)**: Diseños artísticos únicos.  
        - **[Stable Diffusion](https://stability.ai/)**: Perfecto para personalización detallada.  
        - **[Canva](https://www.canva.com/)**: Diseño gráfico con IA integrada.  
        - **[Adobe Firefly](https://www.adobe.com/sensei/generative-ai/adobe-firefly.html)**: Resultados profesionales con IA.
        """
    )

if __name__ == "__main__":
    configurar_pantalla2()
