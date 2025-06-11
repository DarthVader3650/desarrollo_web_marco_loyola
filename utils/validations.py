import re
import filetype
from datetime import datetime

def validate_nombre(nombre):
    return nombre and (4 <= len(nombre) <= 200)

def validate_email(email):
    regex_email = r"^[\w.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$"
    return bool(re.fullmatch(regex_email, email)) and (15 <= len(email) <= 100)

def validate_phone(numero):
    if numero is None or numero.strip() == "":
        return True
    else:
        regex_numero = r"^(\+56)?(\s?)((2|3|4|5|6|7|8|9)(\s?)\d{8})$"
        valid_len = (8 <= len(numero))
        return bool(re.fullmatch(regex_numero, numero)) and valid_len
    
def validate_sector(sector):
    return (0 <= len(sector) <= 100)

def validate_inicio(inicio):
    regex_time = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$"
    if inicio:
        return bool(re.fullmatch(regex_time, inicio))
    else:
        return False
    
def validate_termino(termino, inicio):
    if not termino:
        return True
    if not inicio:
        return False 
    dt_inicio = datetime.fromisoformat(inicio)
    regex_time = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$"
    if not re.fullmatch(regex_time, termino):
        return False
    dt_termino = datetime.fromisoformat(termino)
    return dt_termino > dt_inicio

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
    
def validate_otro_tema(glosa_otro):
    return glosa_otro and (3 <= len(glosa_otro) <= 15)

ALLOWED_CONTACT_NAMES = {'whatsapp', 'telegram', 'X', 'instagram', 'tiktok', 'otra'}
def validate_info_contacto(contactos_seleccionados):
    if not contactos_seleccionados:
        return True
    if len(contactos_seleccionados) > 5:
        return False

    for contacto in contactos_seleccionados:
        tipo = contacto.get("contacto")
        identificador = contacto.get("id")
        if tipo not in ALLOWED_CONTACT_NAMES:
            return False
        if not identificador or not (4 <= len(identificador) <= 50):
            return False

    return True

def validate_foto(foto):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    ALLOWED_MIMETYPES = {"image/jpeg", "image/png", "image/gif"}

    if not foto or foto.filename == "":
        return False
    
    ftype_guess = filetype.guess(foto)
    if ftype_guess.extension not in ALLOWED_EXTENSIONS:
        return False
    if ftype_guess.mime not in ALLOWED_MIMETYPES:
        return False
    return True

def validate_form(nombre, email, numero, sector, inicio, termino, region, comuna, tema, glosa_otro, contactos, fotos_adjuntas, otra_foto_adjunta):
    if not fotos_adjuntas:
        return False
    else:
        if len(fotos_adjuntas) > 5:
            return False
        else:
            for i, foto_file in enumerate(fotos_adjuntas):
                valid_foto = validate_foto(foto_file)
                if not valid_foto:
                    return False

    if otra_foto_adjunta and otra_foto_adjunta.filename != '':
        valid_otra_foto = validate_foto(otra_foto_adjunta)
        if not valid_otra_foto:
            return False

    return validate_nombre(nombre) and validate_email(email) and validate_phone(numero) and validate_sector(sector) and validate_inicio(inicio) and validate_termino(termino, inicio) and validate_region(region) and validate_comuna(comuna) and validate_tema(tema) and validate_otro_tema(glosa_otro) and validate_info_contacto(contactos)