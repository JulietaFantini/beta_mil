import streamlit as st
import re

# --------------------------------------------------------------------------------
# 1. Función para validar parámetros
# --------------------------------------------------------------------------------
def validar_parametros(params):
    """
    Verifica si en 'Otro' no se dejó vacío el campo personalizado.
    Retorna una lista de strings con errores si algo falta.
    """
    errores = []
    if params.get("tipo_de_imagen") == "Otro" and not params.get("tipo_de_imagen_personalizado"):
        errores.append("Seleccionaste 'Otro' como tipo de imagen, pero no lo describiste.")
    if params.get("estilo_artístico") == "Otro" and not params.get("estilo_artístico_personalizado"):
        errores.append("Seleccionaste 'Otro' como estilo artístico, pero no lo describiste.")
    return errores

# --------------------------------------------------------------------------------
# 2. Función para generar el prompt (versión mejorada)
# --------------------------------------------------------------------------------
def generar_prompt_mejorado(params):
    """
    Toma los parámetros en 'params' y construye un texto (prompt) con lógica:
    - Idea inicial
    - Tipo de imagen
    - Propósito
    - Estilo artístico
    - Aspectos técnicos (iluminación, plano, composición)
    - Aspectos visuales (paleta, texturas)
    - Resolución y relación de aspecto
    Agrega limpieza y capitalización final.
    """
    prompt_parts = []

    # Idea inicial
    if params.get("idea_inicial"):
        prompt_parts.append(f"Imagina {params['idea_inicial']} representada en una")

    # Tipo de imagen
    if params.get("tipo_de_imagen"):
        if params["tipo_de_imagen"] == "Otro":
            tipo_pers = params.get("tipo_de_imagen_personalizado", "")
            if prompt_parts:
                prompt_parts[-1] = f"Imagina un concepto inspirado en {tipo_pers}"
            else:
                prompt_parts.append(f"Imagina un concepto inspirado en {tipo_pers}")
        else:
            if prompt_parts:
                prompt_parts[-1] += f" {params['tipo_de_imagen'].lower()}"
            else:
                prompt_parts.append(f"Imagina {params['tipo_de_imagen'].lower()}")

    # Propósito
    if params.get("proposito_categoria"):
        proposito_text = f"diseñada para {params['proposito_categoria'].lower()}"
        if params.get("subpropósito"):
            proposito_text += f", orientada hacia {params['subpropósito'].lower()}"
        prompt_parts.append(proposito_text)

    # Estilo artístico
    if params.get("estilo_artístico"):
        if params["estilo_artístico"] == "Otro":
            estilo_pers = params.get("estilo_artístico_personalizado", "")
            prompt_parts.append(f"con un estilo artístico que recuerde a {estilo_pers}")
        else:
            prompt_parts.append(f"con el estilo visual del {params['estilo_artístico'].lower()}")

    # Aspectos técnicos
    aspectos_tecnicos = []
    if params.get("iluminación"):
        aspectos_tecnicos.append(f"iluminada con {params['iluminación'].lower()}")
    if params.get("plano_fotográfico"):
        aspectos_tecnicos.append(f"capturada desde un {params['plano_fotográfico'].lower()}")
    if params.get("composicion"):
        aspectos_tecnicos.append(f"siguiendo una composición de {params['composicion'].lower()}")
    if aspectos_tecnicos:
        prompt_parts.append(", ".join(aspectos_tecnicos))

    # Aspectos visuales
    aspectos_visuales = []
    if params.get("paleta_de_colores"):
        aspectos_visuales.append(f"una paleta de colores {params['paleta_de_colores'].lower()}")
    if params.get("textura"):
        aspectos_visuales.append(f"texturas {params['textura'].lower()}")
    if aspectos_visuales:
        prompt_parts.append(", ".join(aspectos_visuales))

    # Resolución y aspecto
    final_part = []
    if params.get("resolucion"):
        final_part.append(f"resolución {params['resolucion']}")
    if params.get("aspecto"):
        final_part.append(f"con relación de aspecto {params['aspecto'].lower()}")
    if final_part:
        prompt_parts.append(", ".join(final_part))

    # Unión final y limpieza
    fragments = [fragment.strip() for fragment in prompt_parts if fragment]

    # Capitalizar cada fragmento (primera letra)
    fragments = [
        frag[0].upper() + frag[1:] if len(frag) > 1 else frag.upper()
        for frag in fragments
    ]

    prompt = ". ".join(fragments)
    # Reemplazar secuencias de puntos
    prompt = re.sub(r"\.\.+", ".", prompt)

    # Asegurar que termine en punto
    if not prompt.endswith("."):
        prompt += "."

    # Quitar espacios múltiples
    prompt = re.sub(r"\s+", " ", prompt).strip()

    return prompt

# --------------------------------------------------------------------------------
# 3. Pantalla 2
# --------------------------------------------------------------------------------
def configurar_pantalla2():
    """
    Muestra la pantalla 2:
    - Genera prompt con la función anterior
    - Permite edición y copia con st.code
    - Ofrece traducir a inglés (Google Translate)
    - Lista herramientas recomendadas con enlaces
    - Botón para reiniciar y volver a Pantalla 1
    - Mensaje final de contacto
    """

    # Verificar si existen params
    if "params" not in st.session_state or not st.session_state.params:
        st.warning("No se han proporcionado datos de la Pantalla 1. Volvé y completá los campos obligatorios.")
        if st.button("Volver a Pantalla 1"):
            st.session_state.mostrar_pantalla2 = False
        return

    # Validar parámetros
    errores = validar_parametros(st.session_state.params)
    if errores:
        for error in errores:
            st.error(error)
        return

    # Generar prompt
    prompt_generado = generar_prompt_mejorado(st.session_state.params)

    # Encabezado
    st.title("Tu prompt está listo")
    st.subheader(
        "Este texto combina todos los parámetros que seleccionaste en un formato optimizado para IA. "
        "Podés editarlo y copiarlo, o traducirlo si lo necesitás en inglés."
    )

    # Área Editable
    st.write(
        "Acá podés ajustar libremente los detalles que quieras. No es necesario presionar Ctrl+Enter; "
        "los cambios se guardan en cuanto hacés clic fuera del cuadro."
    )
    texto_editable = st.text_area(
        label="Editar Prompt",
        value=prompt_generado,
        height=200
    )

    # Recurso Nativo para Copiar
    st.subheader("Copiá tu prompt final")
    st.write("Podés hacer clic en el **icono de copiar** (arriba a la derecha del recuadro) para guardarlo en tu portapapeles.")
    st.code(texto_editable, language="")  # Muestra el recuadro con el ícono de copiar

    # Traducción al inglés
    st.subheader("¿Preferís usarlo en inglés?")
    st.write(
        "Algunas herramientas de IA funcionan mejor con descripciones en inglés. "
        "Para traducir, hacé clic en este enlace y pegá tu texto:"
    )
    google_translate_url = f"https://translate.google.com/?sl=es&tl=en&text={texto_editable.replace(' ', '%20')}"
    st.markdown(f"[Abrir Google Translate →]({google_translate_url})")

    # Herramientas Recomendadas
    st.subheader("Herramientas recomendadas")
    st.markdown("""
Estas plataformas te permiten **pegar tu prompt** y generar imágenes basadas en él.  
Después, **podés volver a esta pantalla** para seguir refinando o crear un nuevo prompt.

- [**DALL-E**](https://labs.openai.com/)  
  :arrow_right: Herramienta de OpenAI para dibujar imágenes con inteligencia artificial.  
  Permite creaciones artísticas y composiciones realistas. Usa GPT como base para generar conceptos.

- [**MidJourney**](https://www.midjourney.com/)  
  :arrow_right: Reconocida por su **calidad artística** y estética muy cuidada en las imágenes generadas.

- [**Stable Diffusion**](https://stability.ai/)  
  :arrow_right: Ideal para **personalización** y modificaciones detalladas de tu prompt. 
""")

    # Botón para generar un nuevo prompt
    if st.button("Generá un nuevo prompt"):
        st.session_state.mostrar_pantalla2 = False

    # Mensaje final
    st.markdown("""
---
**Trabajo final de un curso de IA.**  
Para cualquier feedback o consulta, escribí a **julietafantini@gmail.com**.
    """)

# --------------------------------------------------------------------------------
# 4. Ejecución local
# --------------------------------------------------------------------------------
if __name__ == "__main__":
    # Si querés probar este módulo individualmente
    if "params" not in st.session_state:
        st.session_state.params = {
            "idea_inicial": "un bosque mágico con criaturas fantásticas",
            "tipo_de_imagen": "Ilustración",
            "proposito_categoria": "promoción",
            "subpropósito": "campaña de marketing",
            "estilo_artístico": "Otro",
            "estilo_artístico_personalizado": "estilo acuarela",
            "iluminación": "luz suave en atardecer",
            "plano_fotográfico": "plano general",
            "composicion": "regla de los tercios",
            "paleta_de_colores": "pastel",
            "textura": "suave",
            "resolucion": "4K",
            "aspecto": "16:9"
        }
    configurar_pantalla2()
