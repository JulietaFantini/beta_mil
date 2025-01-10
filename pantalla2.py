import streamlit as st
import re

# Función para validar valores
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

def es_valor_valido(valor):
    return valor and isinstance(valor, str) and valor.strip()

def generar_prompt(params):
    if not params:
        return ""

    prompt_parts = []

    if es_valor_valido(params.get("idea_inicial")):
        prompt_parts.append(f"Imagina {params['idea_inicial'].lower()} representada en una")

    if es_valor_valido(params.get("tipo_de_imagen")):
        if params["tipo_de_imagen"] == "Otro":
            if es_valor_valido(params.get("tipo_de_imagen_personalizado")):
                prompt_parts[-1] = f"Imagina un concepto inspirado en {params['tipo_de_imagen_personalizado'].lower()}"
        else:
            prompt_parts[-1] += f" {params['tipo_de_imagen'].lower()}"

    if es_valor_valido(params.get("proposito_categoria")):
        if params["proposito_categoria"] == "Otro":
            if es_valor_valido(params.get("proposito_categoria_personalizado")):
                proposito = f"creada para {params['proposito_categoria_personalizado'].lower()}"
                prompt_parts.append(proposito)
        else:
            proposito = f"creada para {params['proposito_categoria'].lower()}"
            if es_valor_valido(params.get("subpropósito")):
                proposito += f", orientada hacia {params['subpropósito'].lower()}"
            prompt_parts.append(proposito)

    if es_valor_valido(params.get("estilo_artístico")):
        if params["estilo_artístico"] == "Otro":
            if es_valor_valido(params.get("estilo_artístico_personalizado")):
                estilo = params.get("estilo_artístico_personalizado", "")
                prompt_parts.append(f"con un estilo artístico que recuerde a {estilo.lower()}")
        else:
            prompt_parts.append(f"con el estilo visual del {params['estilo_artístico'].lower()}")

    aspectos_tecnicos = []
    if es_valor_valido(params.get("iluminación")):
        aspectos_tecnicos.append(f"la imagen debe iluminarse con {params['iluminación'].lower()}")
    if es_valor_valido(params.get("plano_fotográfico")):
        aspectos_tecnicos.append(f"capturada desde un {params['plano_fotográfico'].lower()}")
    if es_valor_valido(params.get("composicion")):
        aspectos_tecnicos.append(f"siguiendo una composición de {params['composicion'].lower()}")
    if aspectos_tecnicos:
        prompt_parts.append(". " + ", ".join(aspectos_tecnicos))

    aspectos_visuales = []
    if es_valor_valido(params.get("paleta_de_colores")):
        aspectos_visuales.append(f"debe tener una paleta de colores {params['paleta_de_colores'].lower()}")
    if es_valor_valido(params.get("textura")):
        aspectos_visuales.append(f"y una textura {params['textura'].lower()}")
    if aspectos_visuales:
        prompt_parts.append(", " + ", ".join(aspectos_visuales))

    if es_valor_valido(params.get("resolucion")) and es_valor_valido(params.get("aspecto")):
        prompt_parts.append(f". finalmente, la resolución debe ser {params['resolucion']}, con una relación de aspecto de {params['aspecto'].lower()}")

    prompt = " ".join(filter(None, prompt_parts)).strip()
    prompt = re.sub(r'\s+', ' ', prompt)
    prompt = prompt.capitalize()
    if not prompt.endswith('.'):
        prompt += '.'

    return prompt

def configurar_pantalla2():
    st.title("Tu prompt está listo")
    st.markdown("Este texto combina todos los parámetros que seleccionaste en un formato optimizado para IA. Revisalo, editalo si es necesario y copialo fácilmente.")

    if "params" not in st.session_state:
        st.warning("Faltan algunos datos importantes. Por favor, volvé a la pantalla anterior y completá los campos obligatorios.")
        if st.button("Volver a la Pantalla Anterior"):
            st.session_state.mostrar_pantalla2 = False
        return

    prompt_inicial = generar_prompt(st.session_state.params)
    if not prompt_inicial:
        st.error("No se pudo generar el prompt. Por favor, completá al menos los campos obligatorios.")
        if st.button("Volver"):
            st.session_state.mostrar_pantalla2 = False
        return

    st.subheader("Descripción Detallada")
    prompt_editable = st.text_area(
        "Podés editar el texto directamente en este cuadro para personalizarlo aún más:",
        value=prompt_inicial,
        height=200
    )

    prompt_limpio = re.sub(r'\s*\([^)]*\)', '', prompt_editable).strip()
    prompt_limpio = re.sub(r'\s+', ' ', prompt_limpio)

    st.subheader("Texto Final para Copiar")
    st.markdown("👆 Hacé clic en el botón de la esquina superior derecha para copiar el prompt")
    st.code(prompt_limpio)

    if st.button("Modificar parámetros"):
        st.markdown("Volvé a la pantalla anterior para ajustar los parámetros y generar un nuevo prompt.")
        st.session_state.mostrar_pantalla2 = False

if __name__ == "__main__":
    configurar_pantalla2()
