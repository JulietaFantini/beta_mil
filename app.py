import os
os.environ["WATCHDOG_OBSERVERS"] = "polling"

import streamlit as st
from pantalla1 import configurar_pantalla1
from pantalla2 import configurar_pantalla2

def inyectar_css_personalizado():
    """
    Hack de CSS para personalizar estilos de títulos, subtítulos, texto y campos de entrada,
    mapeando lo definido en [title_style], [subheader_style], [text_style] e [input_style].
    """
    st.markdown(
        """
        <style>
        /* ====== TÍTULOS (h1) ====== */
        h1 {
          font-size: 1.7rem !important;   /* [title_style] fontSize */
          font-weight: 700 !important;    /* [title_style] fontWeight */
          color: #6B46C1 !important;      /* [title_style] color */
        }

        /* ====== SUBTÍTULOS (h2) ====== */
        h2 {
          font-size: 1.3rem !important;   /* [subheader_style] fontSize */
          font-weight: 600 !important;    /* [subheader_style] fontWeight */
          color: #805AD5 !important;      /* [subheader_style] color */
        }

        /* ====== TEXTO NORMAL (p) ====== */
        [data-testid="stMarkdownContainer"] p {
          font-size: 1rem !important;     /* [text_style] fontSize */
          font-weight: 400 !important;    /* [text_style] fontWeight */
          color: #4A5568 !important;      /* [text_style] color */
        }

        /* ====== LABELS DE CAMPOS DE ENTRADA ====== */
        .stTextArea label, .stTextInput label {
          font-family: sans-serif !important;   /* [input_style] font */
          font-size: 0.9rem !important;         /* [input_style] fontSize */
          font-weight: 500 !important;          /* [input_style] fontWeight */
          color: #333333 !important;            /* [input_style] color */
        }

        /* ====== CAMPOS DE TEXTO ENTRADA (textarea / input) ====== */
        .stTextArea textarea, .stTextInput input {
          background-color: #E2DFFA !important; /* [input_style] backgroundColor */
          border: 1px solid #6B46C1 !important; /* [input_style] borderColor */
          color: #333333 !important;            /* [input_style] color */
          font-family: sans-serif !important;   /* [input_style] font */
          font-size: 0.9rem !important;         /* [input_style] fontSize */
          font-weight: 500 !important;          /* [input_style] fontWeight */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    """
    Punto de entrada principal de la aplicación Streamlit.
    Maneja la navegación entre Pantalla 1 y Pantalla 2.
    """

    # Configuración de la página (se recomienda llamar set_page_config en lo más alto posible)
    st.set_page_config(
        page_title="Creador de imágenes con IA",
        page_icon=":art:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Inyectamos el CSS personalizado
    inyectar_css_personalizado()

    # Inicializar variables en session_state si no existen
    if "mostrar_pantalla2" not in st.session_state:
        st.session_state.mostrar_pantalla2 = False
    if "params" not in st.session_state:
        st.session_state.params = {}

    # Navegar entre Pantalla 1 y Pantalla 2 según el estado
    if st.session_state.mostrar_pantalla2:
        configurar_pantalla2()
    else:
        configurar_pantalla1()

if __name__ == "__main__":
    main()
