import streamlit as st

def generar_dropdown(parametro, descripcion, opciones, params):
    st.subheader(parametro)
    st.markdown(descripcion)
    # Etiqueta vacía para evitar repetir el título
    params[parametro.lower().replace(" ", "_")] = st.selectbox(
        label="",
        options=opciones
    )
    return params

def parametros_obligatorios(params):
    st.header("Parámetros Clave")
    st.caption("Campos obligatorios para generar el prompt")

    # Tipo de Imagen
    params = generar_dropdown(
        "Tipo de imagen",
        "Fotografía para realismo, ilustración para libertad creativa, render 3D para productos, arte conceptual para ideas abstractas.",
        ["Seleccioná una opción...", "Fotografía", "Ilustración", "Render 3D", "Pintura digital", 
         "Arte conceptual", "Collage surrealista", "Dibujo técnico", "Fotografía conceptual", "Otro"],
        params
    )
    if params["tipo_de_imagen"].lower() == "otro":
        params["tipo_de_imagen_personalizado"] = st.text_input(
            "Describe el tipo de imagen aquí (ej.: 'Collage surrealista'):"
        )

    # Idea Inicial
    st.subheader("Idea inicial")
    st.markdown(
        "Describe los elementos principales y el ambiente deseado. Ejemplo: 'Ciudad futurista al amanecer con rascacielos de cristal.'"
    )
    params["idea_inicial"] = st.text_input(
        "Idea Inicial",
        placeholder="Ej.: 'Una ciudad flotante al amanecer'"
    )

    # Estilo Artístico
    params = generar_dropdown(
        "Estilo artístico",
        "Digital para efectos modernos, clásico para elegancia tradicional, minimalista para simpleza, surrealista para combinaciones oníricas.",
        ["Seleccioná una opción...", "Arte Digital", "Arte Clásico", "Minimalismo", 
         "Futurismo", "Cubismo", "Impresionismo", "Surrealismo", "Otro"],
        params
    )
    if params["estilo_artístico"].lower() == "otro":
        params["estilo_artístico_personalizado"] = st.text_input(
            "Describí tu estilo artístico personalizado (ej.: 'realismo fotográfico con elementos surrealistas'):"
        )

    # Propósito de la Imagen
    st.subheader("Propósito de la imagen")
    st.markdown("Marketing requiere claridad, arte permite experimentación. El propósito influye en la composición y el enfoque final.")
    usos_data = {
        "Comercial y Marketing": ["Publicidad", "Branding Visual", "Campañas Digitales"],
        "Arte y Decoración": ["Arte Conceptual", "Diseño Ambiental", "Arte Personalizado"],
        "Innovación y Experimentación": ["Proyectos Futuristas", "Exploraciones Técnicas"],
        "Técnico y Educativo": ["Infografías STEM", "Material Educativo", "Diagramas Técnicos"],
        "Entretenimiento Digital": ["Storyboarding", "Diseño de Personajes", "Arte Conceptual"]
    }
    uso_categoria = st.selectbox(
        label="Seleccioná una categoría de propósito:",
        options=["Seleccioná una opción..."] + list(usos_data.keys())
    )
    if uso_categoria != "Seleccioná una opción...":
        params["proposito_categoria"] = uso_categoria
        params["subpropósito"] = st.selectbox(
            label="Seleccioná un subpropósito:",
            options=usos_data[uso_categoria]
        )

    return params

def parametros_opcionales(params):
    st.header("Detalles Adicionales")
    st.caption("Opcionales - Ajustá estos detalles si lo deseás")
    st.markdown("Si no encontrás exactamente lo que buscás, podrás personalizar el prompt más adelante.")

    params = generar_dropdown(
        "Iluminación",
        "Natural para realismo, artificial para control creativo. Las sombras dramáticas añaden profundidad.",
        ["Seleccioná una opción...", "Luz Natural", "Luz Artificial", "Efectos Especiales", 
         "Luz Ambiental", "Contraluz", "Sombras Dramáticas"],
        params
    )

    params = generar_dropdown(
        "Plano Fotográfico",
        "Primer plano destaca detalles, plano general muestra contexto, cenital ofrece vista superior.",
        ["Seleccioná una opción...", "Primer Plano", "Plano General", "Cenital", 
         "Detalle", "Plano Medio", "Plano Americano", "Plano Picado"],
        params
    )

    params = generar_dropdown(
        "Composición",
        "Simetría para equilibrio, regla de tercios para dinamismo, líneas dominantes guían la mirada.",
        ["Seleccioná una opción...", "Simetría", "Regla de los Tercios", "Líneas Dominantes", 
         "Profundidad", "Encuadre Diagonal", "Perspectiva Lineal", "Composición en Espiral"],
        params
    )

    params = generar_dropdown(
        "Paleta de Colores",
        "Monocromático para elegancia, complementarios para contraste, análogos para armonía.",
        ["Seleccioná una opción...", "Monocromático", "Complementario", "Análogo", 
         "Triádico", "Tetrádico", "Pasteles", "Cálidos", "Saturados"],
        params
    )

    params = generar_dropdown(
        "Textura",
        "Suave para delicadeza, rugosa para carácter, metálica para modernidad.",
        ["Seleccioná una opción...", "Suave", "Rugosa", "Natural", "Sintética", 
         "Metálica", "Vidriosa", "Textura Orgánica"],
        params
    )

    st.subheader("Resolución y formato")
    st.markdown(
        "Mayor resolución permite más detalle. Formato cuadrado para balance, panorámico para paisajes, vertical para móvil."
    )
    params["resolucion"] = st.selectbox(
        label="Seleccioná una resolución:",
        options=["Seleccioná una opción...", "300x300 px (Miniaturas más grandes o pequeños íconos)", 
                 "800x800 px (Imágenes de productos para e-commerce)", "1200x628 px (Facebook, enlaces o anuncios)", 
                 "1280x720 px (HD, contenido general y banners)", "1920x1080 px (Full HD, imágenes de fondo o encabezados)", 
                 "2560x1440 px (Resolución mayor, ideal para fondos y pantallas grandes)"]
    )
    params["aspecto"] = st.selectbox(
        label="Seleccioná una proporción:",
        options=["Seleccioná una opción...", "1:1 (Cuadrado)", "4:3 (Estándar)", 
                 "16:9 (Pantalla ancha)", "3:2 (Fotografía)", "5:4 (Casi cuadrado)", 
                 "2:1 (Panorámica)", "9:16 (Vertical)"]
    )

    return params

def validar_errores(params):
    campos_obligatorios = {
        "tipo_de_imagen": "Selecciona un tipo de imagen.",
        "idea_inicial": "Describe tu idea inicial.",
        "estilo_artístico": "Selecciona un estilo artístico.",
        "proposito_categoria": "Indica el propósito de la imagen."
    }
    errores = [
        mensaje for campo, mensaje in campos_obligatorios.items()
        if not params.get(campo) or params.get(campo) == "Seleccioná una opción..."
    ]
    return errores

def configurar_pantalla1():
    if "params" not in st.session_state:
        st.session_state.params = {}

    params = st.session_state.params

    st.title("Creador de imágenes con IA")
    st.markdown(
        "Herramienta para diseñar imágenes únicas y generar descripciones efectivas para IA. Comienza completando los campos obligatorios."
    )

    params = parametros_obligatorios(params)

    if st.button("Validar y continuar"):
        errores = validar_errores(params)
        if errores:
            st.error("\n".join(errores))
        else:
            st.session_state.mostrar_pantalla2 = True

if __name__ == "__main__":
    configurar_pantalla1()
