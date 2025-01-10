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
        errores.append("Faltan algunos datos importantes. Por favor, vuelve a la pantalla anterior y completa los campos obligatorios.")
    if params.get("estilo_artístico") == "Otro" and not params.get("estilo_artístico_personalizado"):
        errores.append("Faltan algunos datos importantes. Por favor, vuelve a la pantalla anterior y completa los campos obligatorios.")
    return errores

def generar_prompt(params):
    # Primera parte del prompt (idea inicial y tipo de imagen)
    primera_parte = []
    if params.get("idea_inicial"):
        primera_parte.append(f"Imagina {params['idea_inicial'].lower()} representada en una")
    if params.get("tipo_de_imagen"):
        if params["tipo_de_imagen"] == "Otro":
            tipo = params.get("tipo_de_imagen_personalizado", "")
            primera_parte[-1] = f"Imagina un concepto inspirado en {tipo}"
        else:
            primera_parte[-1] += f" {params['tipo_de_imagen'].lower()}"

    # Segunda parte (propósito y estilo)
    segunda_parte = []
    if params.get("proposito_categoria"):
        proposito = f"{TEMPLATE_BASE['proposito']} {params['proposito_categoria'].lower()}"
        if params.get("subpropósito"):
            proposito += f", orientada hacia {params['subpropósito'].lower()}"
        segunda_parte.append(proposito)
    
    if params.get("estilo_artístico"):
        if params["estilo_artístico"] == "Otro":
            estilo = params.get("estilo_artístico_personalizado", "")
            segunda_parte.append(f"{FRASES_OTRO['estilo_artistico']}: {estilo}")
        else:
            segunda_parte.append(f"{TEMPLATE_BASE['estilo']} {params['estilo_artístico'].lower()}")

    # Tercera parte (aspectos técnicos)
    tercera_parte = []
    if params.get("iluminación"):
        tercera_parte.append(f"{TEMPLATE_BASE['iluminacion']} {params['iluminación'].lower()}")
    if params.get("plano_fotográfico"):
        tercera_parte.append(f"{TEMPLATE_BASE['plano']} {params['plano_fotográfico'].lower()}")
    if params.get("composicion"):
        tercera_parte.append(f"{TEMPLATE_BASE['composicion']} {params['composicion'].lower()}")
    
    # Cuarta parte (estilo visual)
    cuarta_parte = []
    if params.get("paleta_de_colores"):
        cuarta_parte.append(f"{TEMPLATE_BASE['paleta']} {params['paleta_de_colores'].lower()}")
    if params.get("textura"):
        cuarta_parte.append(f"{TEMPLATE_BASE['textura']} {params['textura'].lower()}")

    # Quinta parte (especificaciones técnicas)
    quinta_parte = []
    if params.get("resolucion") and params.get("aspecto"):
        quinta_parte.append(f"{TEMPLATE_BASE['resolucion']} {params['resolucion']}, {TEMPLATE_BASE['aspecto']} {params['aspecto'].lower()}")

    # Construir el prompt final
    prompt_parts = []
    if primera_parte:
        prompt_parts.append(" ".join(primera_parte))
    if segunda_parte:
        prompt_parts.append(", ".join(segunda_parte))
    if tercera_parte:
        prompt_parts.append(". " + ", ".join(tercera_parte))
    if cuarta_parte:
        prompt_parts.append(", " + ", ".join(cuarta_parte))
    if quinta_parte:
        prompt_parts.append(". " + ", ".join(quinta_parte))

    return " ".join(prompt_parts).capitalize() + "."

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
