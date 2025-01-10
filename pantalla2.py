import streamlit as st
import re

# --------------------------------------------------------------------------------
# 1. Función opcional para validar parámetros
# --------------------------------------------------------------------------------
def validar_parametros(params):
    errores = []
    # Ejemplo: Si "tipo_de_imagen" == "Otro" pero no se llenó el campo personalizado
    if params.get("tipo_de_imagen") == "Otro" and not params.get("tipo_de_imagen_personalizado"):
        errores.append("Seleccionaste 'Otro' como tipo de imagen, pero no lo describiste.")
    # Si "estilo_artístico" == "Otro" y no se completó el campo personalizado
    if params.get("estilo_artístico") == "Otro" and not params.get("estilo_artístico_personalizado"):
        errores.append("Seleccionaste 'Otro' como estilo artístico, pero no lo describiste.")
    return errores

# --------------------------------------------------------------------------------
# 2. Función mejorada para generar el prompt
# --------------------------------------------------------------------------------
def generar_prompt_mejorado(params):
    """
    Genera un texto (prompt) a partir de los parámetros ingresados,
    con validaciones y mejoras en la concatenación de frases.
    """
    prompt_parts = []

    # -------------------------------------------
    # Ejemplo de inserción de idea_inicial
    # -------------------------------------------
    if params.get("idea_inicial"):
        prompt_parts.append(f"Imagina {params['idea_inicial']} representada en una")

    # -------------------------------------------
    # Manejo de "tipo_de_imagen"
    # -------------------------------------------
    if params.get("tipo_de_imagen"):
        if params["tipo_de_imagen"] == "Otro":
            tipo_pers = params.get("tipo_de_imagen_personalizado", "")
            # Verificar que prompt_parts tenga algo antes de cambiar la última posición
            if prompt_parts:
                # Sobrescribimos la última frase para evitar duplicar palabras
                prompt_parts[-1] = f"Imagina un concepto inspirado en {tipo_pers}"
            else:
                # Si no existe nada, simplemente añadimos una nueva frase
                prompt_parts.append(f"Imagina un concepto inspirado en {tipo_pers}")
        else:
            if prompt_parts:
                prompt_parts[-1] += f" {params['tipo_de_imagen'].lower()}"
            else:
                prompt_parts.append(f"Imagina {params['tipo_de_imagen'].lower()}")

    # -------------------------------------------
    # Manejo de propósito
    # -------------------------------------------
    if params.get("proposito_categoria"):
        proposito_text = f"diseñada para {params['proposito_categoria'].lower()}"
        if params.get("subpropósito"):
            proposito_text += f", orientada hacia {params['subpropósito'].lower()}"
        prompt_parts.append(proposito_text)

    # -------------------------------------------
    # Manejo de estilo artístico
    # -------------------------------------------
    if params.get("estilo_artístico"):
        if params["estilo_artístico"] == "Otro":
            estilo_pers = params.get("estilo_artístico_personalizado", "")
            prompt_parts.append(f"con un estilo artístico que recuerde a {estilo_pers}")
        else:
            prompt_parts.append(f"con el estilo visual del {params['estilo_artístico'].lower()}")

    # -------------------------------------------
    # Asignar aspectos técnicos
    # -------------------------------------------
    aspectos_tecnicos = []
    if params.get("iluminación"):
        aspectos_tecnicos.append(f"iluminada con {params['iluminación'].lower()}")
    if params.get("plano_fotográfico"):
        aspectos_tecnicos.append(f"capturada desde un {params['plano_fotográfico'].lower()}")
    if params.get("composicion"):
        aspectos_tecnicos.append(f"siguiendo una composición de {params['composicion'].lower()}")
    if aspectos_tecnicos:
        prompt_parts.append(", ".join(aspectos_tecnicos))

    # -------------------------------------------
    # Asignar aspectos visuales
    # -------------------------------------------
    aspectos_visuales = []
    if params.get("paleta_de_colores"):
        aspectos_visuales.append(f"una paleta de colores {params['paleta_de_colores'].lower()}")
    if params.get("textura"):
        aspectos_visuales.append(f"texturas {params['textura'].lower()}")
    if aspectos_visuales:
        prompt_parts.append(", ".join(aspectos_visuales))

    # -------------------------------------------
    # Resolución y relación de aspecto
    # -------------------------------------------
    final_part = []
    if params.get("resolucion"):
        final_part.append(f"resolución {params['resolucion']}")
    if params.get("aspecto"):
        final_part.append(f"con relación de aspecto {params['aspecto'].lower()}")
    if final_part:
        prompt_parts.append(", ".join(final_part))

    # -------------------------------------------
    # Unión y limpieza del texto final
    # -------------------------------------------
    # 1) Limpiamos fragmentos vacíos y posibles espacios sobrantes
    fragments = [fragment.strip() for fragment in prompt_parts if fragment]

    # 2) Capitalizar cada fragmento (opcional, pero sugerido)
    fragments = [
        frag[0].upper() + frag[1:] if len(frag) > 1 else frag.upper()
        for frag in fragments
    ]

    # 3) Unimos los fragmentos con punto y espacio
    prompt = ". ".join(fragments)

    # 4) Evitamos secuencias de puntos repetidas
    prompt = re.sub(r"\.\.+", ".", prompt)

    # 5) Si no termina en punto, lo agregamos
    if not prompt.endswith("."):
        prompt += "."

    # 6) Reemplazamos espacios múltiples por uno solo
    prompt = re.sub(r"\s+", " ", prompt).strip()

    return prompt

# --------------------------------------------------------------------------------
# 3. Función principal: Pantalla 2
# --------------------------------------------------------------------------------
def configurar_pantalla2():
    """
    Muestra la pantalla 2 con:
    - Validaciones y generación de prompt
    - Texto editable
    - Botón para copiar
    - Enlace a Google Translate
    - Herramientas recomendadas
    - Botón para volver a Pantalla 1
    """

    # Verificamos si existen los parámetros guardados en la sesión
    if "params" not in st.session_state or not st.session_state.params:
        st.warning("No se han proporcionado datos de la Pantalla 1. Volvé y completá los campos obligatorios.")
        if st.button("Volver a Pantalla 1"):
            st.session_state.mostrar_pantalla2 = False
        return

    # Validar parámetros si es necesario
    errores = validar_parametros(st.session_state.params)
    if errores:
        for error in errores:
            st.error(error)
        return  # No generamos prompt si hay errores

    # Generamos el prompt
    prompt_generado = generar_prompt_mejorado(st.session_state.params)

    # --------------------------------------------------------------------------------
    # Encabezado
    # --------------------------------------------------------------------------------
    st.title("Tu prompt está listo")
    st.subheader(
        "Este texto combina todos los parámetros que seleccionaste en un formato optimizado para IA. "
        "Podés editarlo, copiarlo o traducirlo según tus necesidades."
    )

    # --------------------------------------------------------------------------------
    # Cuadro Editable
    # --------------------------------------------------------------------------------
    st.write(
        "Podés editar este texto directamente en el cuadro para ajustarlo. "
        "Si querés copiarlo, seleccioná manualmente el texto o usá el botón a continuación."
    )
    texto_editable = st.text_area(
        label="Editar Prompt",
        value=prompt_generado,
        height=200
    )

    # --------------------------------------------------------------------------------
    # Botón para Copiar (JavaScript embebido)
    # --------------------------------------------------------------------------------
    if st.button("Copiar Prompt"):
        st.code(
            f"""
<script>
    navigator.clipboard.writeText({repr(texto_editable)}).then(() => {{
        console.log('Texto copiado con éxito');
    }});
</script>
            """,
            language="html"
        )
        st.success("¡Texto copiado al portapapeles con éxito!")

    st.markdown("_Hacé clic para copiar automáticamente el texto al portapapeles. "
                "Si no funciona, podés copiarlo manualmente._")

    # --------------------------------------------------------------------------------
    # Enlace a Google Translate
    # --------------------------------------------------------------------------------
    st.write("¿Necesitás este texto en inglés? Traducilo fácilmente con Google Translate.")
    google_translate_url = f"https://translate.google.com/?sl=es&tl=en&text={texto_editable.replace(' ', '%20')}"
    st.markdown(f"[Traducir mi texto con Google Translate →]({google_translate_url})")

    # --------------------------------------------------------------------------------
    # Herramientas Recomendadas
    # --------------------------------------------------------------------------------
    st.subheader("Herramientas Recomendadas")
    st.markdown("""
**Grok de Twitter**  
:arrow_right: Conectá tus imágenes con las tendencias más actuales en redes sociales.

**Claude**  
:arrow_right: Ideal para analizar y mejorar prompts complejos.

**Copilot**  
:arrow_right: Soporte creativo para generación rápida y versátil.

**DALL-E**  
:arrow_right: Ideal para realismo y precisión.

**MidJourney**  
:arrow_right: Excelente para resultados artísticos.

**Stable Diffusion**  
:arrow_right: Perfecto para personalización detallada.
    """)

    # --------------------------------------------------------------------------------
    # Botón para volver (Modificar Parámetros)
    # --------------------------------------------------------------------------------
    if st.button("Modificar Parámetros"):
        st.session_state.mostrar_pantalla2 = False

    # --------------------------------------------------------------------------------
    # Mensaje final
    # --------------------------------------------------------------------------------
    st.markdown("""
---
Con tu descripción personalizada, estás listo para generar imágenes asombrosas usando herramientas de inteligencia artificial. 
Copiá el texto generado y pegalo en la herramienta de tu elección. 
¡Dejá volar tu creatividad y comenzá a crear imágenes únicas!
    """)

# --------------------------------------------------------------------------------
# Ejecución local: Si querés probar este archivo en solitario con "streamlit run"
# --------------------------------------------------------------------------------
if __name__ == "__main__":
    # Simulamos que la Pantalla 1 ya guardó datos en session_state
    if "params" not in st.session_state:
        st.session_state["params"] = {
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
