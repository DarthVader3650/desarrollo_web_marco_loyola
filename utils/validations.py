import re
import filetype

def validate_nombre(nombre):
    return nombre and (4 <= len(nombre) <= 200)

def validate_email(email):
    regex_email = r"^[\w.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$"
    return bool(re.fullmatch(regex_email, email)) and (15 <= len(email) <= 100)

def validate_phone(numero):
    regex_numero = r"^(\+56)?(\s?)((2|3|4|5|6|7|8|9)(\s?)\d{8})$"
    valid_len = (8 <= len(numero))
    if numero is not None:
        return bool(re.fullmatch(regex_numero, numero)) and valid_len
    else:
        return True
    
def validate_sector(sector):
    return (0 <= len(sector) <= 100)

def validate_inicio(inicio):
    regex_time = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$"
    if inicio:
        return bool(re.fullmatch(regex_time, inicio))
    else:
        return False
    
def validate_termino(termino): #ARREGLAR ESTO
    if termino is None:
        return True
    else:
        return True

def validate_region(region):
    if region is not None:
        return True
    else:
        return False

def validate_comuna(comuna):
    if comuna is not None:
        return True
    else:
        return False
    
def validate_tema(tema):
    if tema is not None:
        return True
    else:
        return False
    
def validate_foto(foto):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    ALLOWED_MIMETYPES = {"image/jpeg", "image/png", "image/gif"}

    if foto is None:
        return False
    
    if foto.filename == "":
        return False
    
    ftype_guess = filetype.guess(foto)
    if ftype_guess.extension not in ALLOWED_EXTENSIONS:
        return False
    
    if ftype_guess.mime not in ALLOWED_MIMETYPES:
        return False
    return True

# Falta validar las otras fotos, la info de contacto y el valor de "otro".

def validate_form(nombre, email, numero, sector, inicio, termino, region, comuna, tema, foto):
    return validate_nombre(nombre) and validate_email(email) and validate_phone(numero) and validate_sector(sector) and validate_inicio(inicio) and validate_termino(termino) and validate_region(region) and validate_comuna(comuna) and validate_tema(tema) and validate_foto(foto)