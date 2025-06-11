from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify
from flask_cors import cross_origin
from database import db
from utils.validations import validate_form
from utils.validations_comentario import validate_posteo, validate_texto, validate_nombre_comentario
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import hashlib
import filetype
from sqlalchemy import func, case
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
            "termino": actividad.dia_hora_termino if actividad.dia_hora_termino else "No especificada",
            "comuna": actividad.comuna.nombre,
            "sector": actividad.sector if actividad.sector else "No especificado",
            "tema": temas_actividad,
            "path_foto": path_foto
        })
    session.close()
    return render_template("portada.html", data=data)

@app.route('/estadisticas', methods=["GET"])
def estadisticas():
    return render_template("estadisticas.html")

@app.route("/get-estadisticas-data", methods=["GET"])
@cross_origin(origin="127.0.0.1", supports_credentials=True)
def gets_estadisticas_data():
    session = db.SessionLocal()
    actividades_por_dia = session.query(
        func.date(db.Actividad.dia_hora_inicio).label('fecha'),
        func.count(db.Actividad.id).label('cantidad')
    ).group_by(func.date(db.Actividad.dia_hora_inicio)).order_by(func.date(db.Actividad.dia_hora_inicio)).all()

    fechas = []
    cantidades = []
    for row in actividades_por_dia:
        fechas.append(row.fecha.strftime('%d-%m-%Y'))
        cantidades.append(row.cantidad)
    
    session.close()
    return jsonify({
        'categories': fechas,
        'data': cantidades
    })

@app.route("/get-estadisticas-data-torta", methods=["GET"])
@cross_origin(origin="127.0.0.1", supports_credentials=True)
def get_estadisticas_data_torta():
    session = db.SessionLocal()
    actividades_por_tipo = session.query(
        db.Actividad_tema.tema,
        func.count(db.Actividad_tema.id).label('cantidad')
    ).group_by(db.Actividad_tema.tema).all()

    data_para_grafico = []
    for tema, cantidad in actividades_por_tipo:
        data_para_grafico.append({
            "name": tema.capitalize(),
            "y": cantidad
        })

    session.close()
    return jsonify({"data": data_para_grafico})

@app.route("/get-estadisticas-data-3", methods=["GET"])
@cross_origin(origin="127.0.0.1", supports_credentials=True)
def get_estadisticas_data_tres():
    session = db.SessionLocal()
    franja_horaria_case = case(
        (func.hour(db.Actividad.dia_hora_inicio) < 12, 'Mañana'),
        (func.hour(db.Actividad.dia_hora_inicio) < 18, 'Mediodía'),
        else_='Tarde'
    ).label('franja')

    actividad_por_hora_mes = session.query(
        func.month(db.Actividad.dia_hora_inicio).label('mes'),
        franja_horaria_case,
        func.count(db.Actividad.id).label('cantidad')
    ).group_by(func.month(db.Actividad.dia_hora_inicio),
               franja_horaria_case
    ).order_by(func.month(db.Actividad.dia_hora_inicio),
               franja_horaria_case).all()

    datos_por_franja = {
        'Mañana': [0,0,0,0,0,0,0,0,0,0,0,0],
        'Mediodía': [0,0,0,0,0,0,0,0,0,0,0,0],
        'Tarde': [0,0,0,0,0,0,0,0,0,0,0,0]
    }

    for row in actividad_por_hora_mes:
        mes_numero = row.mes
        franja = row.franja
        cantidad = row.cantidad
        datos_por_franja[franja][mes_numero - 1] = cantidad
    
    series_para_grafico = []
    for nombre_franja, data_puntos in datos_por_franja.items():
        series_para_grafico.append({
            "name": nombre_franja,
            "data": data_puntos
        })

    session.close()
    return jsonify({'series': series_para_grafico})

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
            "id": actividad.id,
            "inicio": actividad.dia_hora_inicio,
            "termino": actividad.dia_hora_termino if actividad.dia_hora_termino else "No especificada",
            "comuna": actividad.comuna.nombre,
            "sector": actividad.sector if actividad.sector else "No especificado",
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
                dt_termino = None

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

            return redirect(url_for('enviado'))
        else:
            return render_template("formulario.html")
    else:
        return render_template("formulario.html")

@app.route('/enviado_éxito', methods=['GET'])
def enviado():
    return render_template("enviado.html")

@app.route('/actividad/<int:actividad_id>', methods=['GET'])
def actividad(actividad_id):
    session = db.SessionLocal()
    actividad = session.query(db.Actividad).filter_by(id=actividad_id).first()

    temas_detalle = []
    for act_tema in actividad.actividad_tema:
        if act_tema.tema == "otro" and act_tema.glosa_otro:
            temas_detalle.append(act_tema.glosa_otro)
        else:
            temas_detalle.append(act_tema.tema)

    contactos_detalle = []
    if actividad.contactar_por:
        for contacto in actividad.contactar_por:
            tipo_contacto = contacto.nombre
            contactos_detalle.append(f"{tipo_contacto}: {contacto.identificador}")
    
    lista_fotos = []
    for foto in actividad.foto:
        img_filename = f"uploads/{foto.nombre_archivo}"
        lista_fotos.append(url_for('static', filename=img_filename))

    data = {
        "id": actividad.id,
        "nombre_organizador": actividad.nombre,
        "email": actividad.email,
        "celular": actividad.celular if actividad.celular else "No especificado",
        "dia_hora_inicio": actividad.dia_hora_inicio.strftime('%d de %B de %Y a las %H:%M hrs'),
        "dia_hora_termino": actividad.dia_hora_termino.strftime('%d de %B de %Y a las %H:%M hrs') if actividad.dia_hora_termino else "No especificada",
        "descripcion": actividad.descripcion if actividad.descripcion else "Sin descripción.",
        "sector": actividad.sector if actividad.sector else "No especificado",
        "comuna": actividad.comuna.nombre,
        "region": actividad.comuna.region.nombre,
        "temas": temas_detalle,
        "contactos": contactos_detalle if contactos_detalle else ["No especificado"],
        "fotos": lista_fotos
    }
    
    session.close()

    return render_template("actividad_elegida.html", data=data)

@app.route('/comentario', methods=['POST'])
@cross_origin(origin="127.0.0.1", supports_credentials=True)
def comentario():
    data = request.form
    nombre = data.get("nombre")
    comentario_texto = data.get("comentario")
    actividad_id = int(data.get("actividad_id"))

    if not validate_posteo(nombre, comentario_texto):
        return jsonify({
            "status": "error",
            "message": "Datos inválidos. El nombre debe tener entre 3 y 80 caracteres, y el comentario al menos 5."
        }), 400

    session = db.SessionLocal()
    nuevo_comentario = db.Comentario(nombre=nombre, texto=comentario_texto, actividad_id=actividad_id)
    session.add(nuevo_comentario)
    session.commit()
    comentario_creado = {
        'id': nuevo_comentario.id,
        'nombre': nuevo_comentario.nombre,
        'texto': nuevo_comentario.texto,
        'fecha': nuevo_comentario.fecha.strftime('%d de %B de %Y a las %H:%M hrs')
    }

    session.close()

    return jsonify({"status": "ok", "comentario": comentario_creado})

@app.route('/actividad/<int:actividad_id>/comentarios', methods=['GET'])
@cross_origin(origin="127.0.0.1", supports_credentials=True)
def get_comentarios(actividad_id):
    session = db.SessionLocal()
    comentarios = session.query(db.Comentario).filter_by(actividad_id=actividad_id).order_by(db.Comentario.fecha.desc()).all()
    comentarios_list = []
    for com in comentarios:
        comentarios_list.append({
            'id': com.id,
            'nombre': com.nombre,
            'texto': com.texto,
            'fecha': com.fecha.strftime('%d de %B de %Y a las %H:%M hrs')
        })
    session.close()
    return jsonify(comentarios_list)

if __name__ == "__main__":
    app.run(debug=True)