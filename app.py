from flask import Flask, request, render_template, redirect, url_for, session, flash
from database import db
from utils.validations import validate_form
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import hashlib
import filetype
from sqlalchemy import func
from math import ceil

UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)

app.secret_key = "DartH_VadER34"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=["GET"])
def index():
    session = db.SessionLocal()
    actividades = session.query(db.Actividad).order_by(db.Actividad.id.desc()).limit(5).all()
    data = []
    for actividad in actividades:
        path_foto = None
        if actividad.foto and len(actividad.foto) > 0:
            primera_foto = actividad.foto[0]
            img_filename = f"uploads/{primera_foto.nombre_archivo}"
            path_foto = url_for('static', filename=img_filename)
        
        temas_actividad = []
        for act_tema in actividad.actividad_tema:
            if act_tema.tema == "otro" and act_tema.glosa_otro:
                temas_actividad.append(act_tema.glosa_otro)
            else:
                temas_actividad.append(act_tema.tema)

        data.append({
            "inicio": actividad.dia_hora_inicio,
            "termino": actividad.dia_hora_termino,
            "comuna": actividad.comuna.nombre,
            "sector": actividad.sector,
            "tema": temas_actividad,
            "path_foto": path_foto
        })
    session.close()
    return render_template("portada.html", data=data)

@app.route('/estadisticas', methods=["GET"])
def estadisticas():
    return render_template("estadisticas.html")

@app.route('/listado_actividades', methods=["GET"])
def listado():
    session = db.SessionLocal()
    page = request.args.get('page', 1, type=int)
    por_pagina = 5
    actividades = session.query(db.Actividad).order_by(db.Actividad.id.desc())
    actividades_página = actividades.limit(por_pagina).offset((page - 1) * por_pagina).all()
    total_actividades = session.query(func.count(db.Actividad.id)).scalar()
    total_paginas = ceil(total_actividades / por_pagina)
    data = []
    for actividad in actividades_página:
        cantidad_de_fotos = 0
        if actividad.foto and len(actividad.foto) > 0:
            cantidad_de_fotos = len(actividad.foto)
        
        temas_actividad = []
        for act_tema in actividad.actividad_tema:
            if act_tema.tema == "otro" and act_tema.glosa_otro:
                temas_actividad.append(act_tema.glosa_otro)
            else:
                temas_actividad.append(act_tema.tema)

        data.append({
            "inicio": actividad.dia_hora_inicio,
            "termino": actividad.dia_hora_termino,
            "comuna": actividad.comuna.nombre,
            "sector": actividad.sector,
            "tema": temas_actividad,
            "nombre_organizador": actividad.nombre,
            "cantidad_fotos": cantidad_de_fotos
        })
    session.close()

    return render_template("lista_actividades.html", data=data, pagina_actual=page, total_paginas=total_paginas, per_page=por_pagina)

@app.route('/formulario_actividad', methods=["GET", "POST"])
def formulario():
    if request.method == "POST":
        data_form = request.form
        files_form = request.files

        nombre = data_form.get("name")
        email = data_form.get("email")
        telefono = data_form.get("teléfono")
        region = data_form.get("región")
        comuna = data_form.get("comuna")
        sector = data_form.get("sector")
        dia_hora_inicio = data_form.get("inicio")
        dia_hora_termino = data_form.get("término")
        descripcion = data_form.get("descripción")

        tema_nombre = data_form.get("tema")
        if tema_nombre == 'otro':
            otro_tema = data_form.get("otro")
        else:
            otro_tema = "No especifíca"
        
        fotos_adjuntas = files_form.getlist("foto")
        otra_foto_adjunta = files_form.get("otra-foto")

        contactos_seleccionados = []
        posibles_contactos_check = ['whatsapp', 'instagram', 'telegram', 'tiktok', 'X', 'otra']
        for tipo_contacto in posibles_contactos_check:
            if tipo_contacto in data_form:
                id_key = f"{tipo_contacto}-id"
                id_valor = data_form.get(id_key)
                if id_valor:
                    contactos_seleccionados.append({
                        "contacto": tipo_contacto,
                        "id": id_valor
                })

        if validate_form(nombre, email, telefono, sector, dia_hora_inicio, dia_hora_termino, region, comuna, tema_nombre, otro_tema, contactos_seleccionados, fotos_adjuntas, otra_foto_adjunta):
            dt_inicio = datetime.fromisoformat(dia_hora_inicio)
            if dia_hora_termino:
                dt_termino = datetime.fromisoformat(dia_hora_termino)
            else:
                None

            _comuna_ = db.get_comuna_by_name(comuna)
            
            session = db.SessionLocal()
            nueva_actividad = db.Actividad(comuna_id=_comuna_.id, sector=sector, nombre=nombre, email=email, celular=telefono, dia_hora_inicio=dt_inicio, dia_hora_termino=dt_termino, descripcion=descripcion)
            session.add(nueva_actividad)
            session.commit()

            actividad_id_creada = nueva_actividad.id

            archivos_fotos_guardados = []
            
            for foto_file in fotos_adjuntas:
                if foto_file and foto_file.filename != '':
                    filename_foto = hashlib.sha256(secure_filename(foto_file.filename)
                                                   .encode("utf-8")).hexdigest()
                    _extension = filetype.guess(foto_file).extension
                    foto_filename = f"{filename_foto}-{_extension}"
                    foto_file.save(os.path.join(app.config["UPLOAD_FOLDER"], foto_filename))
                    db.crear_foto(ruta_archivo='uploads', nombre_archivo=foto_filename, actividad_id=actividad_id_creada)
                    archivos_fotos_guardados.append(foto_filename)

            if otra_foto_adjunta and otra_foto_adjunta.filename != '':
                filename_otra_foto = hashlib.sha256(secure_filename(otra_foto_adjunta.filename)
                                                .encode("utf-8")).hexdigest()
                _extension_otra = filetype.guess(otra_foto_adjunta).extension
                otra_foto_filename = f"{filename_otra_foto}-{_extension_otra}"
                otra_foto_adjunta.save(os.path.join(app.config["UPLOAD_FOLDER"], otra_foto_filename))
                db.crear_foto(ruta_archivo='uploads', nombre_archivo=otra_foto_filename, actividad_id=actividad_id_creada)
                archivos_fotos_guardados.append(otra_foto_filename)

            for contacto_info in contactos_seleccionados:
                db.crear_contacto(
                    nombre=contacto_info["contacto"],
                    identificador=contacto_info["id"],
                    actividad_id=actividad_id_creada
                )
            
            db.crear_tema_actividad(
                tema=tema_nombre,
                glosa_otro=otro_tema,
                actividad_id=actividad_id_creada
            )

            session.close()

            return redirect(url_for('index'))
    else:
        return render_template("formulario.html")



if __name__ == "__main__":
    app.run(debug=True)