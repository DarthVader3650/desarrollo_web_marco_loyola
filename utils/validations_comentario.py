def validate_nombre_comentario(nombre):
    return nombre and (3 <= len(nombre) <= 80)

def validate_texto(texto):
    return texto and (len(texto) >= 5 and len(texto) <= 300)

def validate_posteo(nombre, texto):
    return validate_nombre_comentario(nombre) and validate_texto(texto)