def generar_prompt(params):
    """
    Genera un texto narrativo a partir de los parámetros ingresados.
    """
    prompt_parts = []

    # 1. Inicio obligatorio con "Imagina"
    prompt_parts.append("Imagina")

    # 2. Idea inicial (primero)
    if params.get("idea_inicial"):
        if params["idea_inicial"] == "Otro" and params.get("idea_inicial_personalizado"):
            valor = params['idea_inicial_personalizado'].lower()
            prompt_parts.append(f"que represente {valor} (idea inicial)")
        else:
            prompt_parts.append(f"que represente {params['idea_inicial'].lower()} (idea inicial)")

    # 3. Tipo de imagen (segundo)
    if params.get("tipo_de_imagen"):
        if params["tipo_de_imagen"] == "Otro" and params.get("tipo_de_imagen_personalizado"):
            valor = params['tipo_de_imagen_personalizado'].lower()
            prompt_parts.append(f"{valor}")
        else:
            prompt_parts.append(f"{params['tipo_de_imagen'].lower()} (tipo de imagen)")

    # 4. Propósito y subpropósito
    if params.get("proposito_categoria"):
        if params["proposito_categoria"] == "Otro" and params.get("proposito_personalizado"):
            valor = params['proposito_personalizado'].lower()
            prompt_parts.append(f"diseñada para un propósito que evoque {valor}")
        else:
            proposito_text = f"diseñada para {params['proposito_categoria'].lower()} (propósito)"
            if params.get("subpropósito"):
                proposito_text += f" con un enfoque en {params['subpropósito'].lower()} (subpropósito)"
            prompt_parts.append(proposito_text)

    # 5. Estilo artístico
    if params.get("estilo_artístico"):
        if params["estilo_artístico"] == "Otro" and params.get("estilo_artístico_personalizado"):
            valor = params['estilo_artístico_personalizado'].lower()
            prompt_parts.append(f"inspirada en {valor}")
        else:
            prompt_parts.append(f"inspirada en un estilo {params['estilo_artístico'].lower()} (estilo artístico)")

    # Opcionales (iluminación, plano, etc.)
    opcionales = {
        'iluminación': 'iluminada con',
        'plano_fotográfico': 'capturada desde',
        'composición': 'siguiendo una composición basada en',
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
    prompt = ". ".join(filter(None, prompt_parts)).replace(". ", ", ", prompt_parts.count('.') - 1) + "."
    return textwrap.fill(prompt, width=80)
