import streamlit as st
from pantalla1 import configurar_pantalla1
from pantalla2 import configurar_pantalla2

def main():
    """
    Punto de entrada principal de la aplicación Streamlit.
    Maneja la navegación entre Pantalla 1 y Pantalla 2.
    """
    # Inicializar variables en session_state si no existen
    if "mostrar_pantalla2" not in st.session_state:
        st.session_state.mostrar_pantalla2 = False
    if "params" not in st.session_state:
        st.session_state.params = {}

    # Configuración de la página
    st.set_page_config(
        page_title="Creador de imágenes con IA",
        page_icon=":art:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Navegar entre Pantalla 1 y Pantalla 2 según el estado
    if st.session_state.mostrar_pantalla2:
        configurar_pantalla2()
    else:
        configurar_pantalla1()

if __name__ == "__main__":
    main()
