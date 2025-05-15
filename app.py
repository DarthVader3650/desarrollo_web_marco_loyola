from flask import Flask, request, render_template, redirect, url_for, session
from database import db
from utils.validations import validate_form
from datetime import datetime
UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)

app.secret_key = "DartH_VadER34"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=["GET"])
def index():
    data = []
    for actividad in db.get_actividades(page_size=5):
        path_foto = None
        if actividad.foto and len(actividad.foto) > 0:
            primera_foto = actividad.foto[0]
            img_filename = f"uploads/{primera_foto.nombre_archivo}"
            path_foto = url_for('static', filename=img_filename)
        
        temas_actividad = []
        for tema in actividad.actividad_tema:
            temas_actividad.append(tema)

        data.append({
            "inicio": actividad.dia_hora_inicio,
            "termino": actividad.dia_hora_termino,
            "comuna": actividad.comuna,
            "sector": actividad.sector,
            "tema": temas_actividad,
            "path_foto": path_foto
        })

    return render_template("portada.html", data=data)

@app.route('/estadisticas', methods=["GET"])
def estadisticas():
    return render_template("estadisticas.html")

@app.route('/listado_actividades', methods=["GET"])
def listado():
    return render_template("lista_actividades.html")

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
            None
        
        fotos_adjuntas = files_form.getlist("foto")
        otra_foto_adjunta = files_form.get("otra-foto")

        contactos_seleccionados = []
        posibles_contactos_check = ['whatsapp', 'instagram', 'telegram', 'tiktok', 'X', 'otra']
        for tipo_contacto in posibles_contactos_check:
            if tipo_contacto in data_form:
                id_key = f"{tipo_contacto}_id"
                id_valor = data_form.get(id_key)
                if id_valor:
                    contactos_seleccionados.append({
                        "contacto": tipo_contacto,
                        "id": id_valor
                })

        if validate_form(nombre, email, telefono, sector, dia_hora_inicio, dia_hora_termino, region, comuna, tema_nombre, fotos_adjuntas):
            dt_inicio = datetime.fromisoformat(dia_hora_inicio)
            if dia_hora_termino:
                dt_termino = datetime.fromisoformat(dia_hora_termino)
            else:
                None

            _comuna_ = db.get_comuna_by_name(comuna)

            actividad_nueva = db.crear_actividad(
                comuna_id=int(_comuna_.id),
                sector=sector,
                nombre=nombre,
                email=email,
                celular=telefono,
                inicio=dt_inicio,
                termino=dt_termino,
                descripcion=descripcion
            )

            actividad_id_creada = actividad_nueva.id

            # Guardar Contactos en BD
            for contacto_info in contactos_seleccionados:
                db.crear_contacto(
                    nombre=contacto_info["contacto"], # ej: "whatsapp"
                    identificador=contacto_info["id"],
                    actividad_id=actividad_id_creada
                )
            
            # Guardar Tema en BD
            db.crear_tema_actividad(
                tema=tema_nombre, # ej: "música" o "otro"
                otro=otro_tema, # Será None si tema_nombre no es "otro"
                actividad_id=actividad_id_creada
            )

            return redirect(url_for('index')) # O a una página de confirmación
    else:
        return render_template("formulario.html")



if __name__ == "__main__":
    app.run(debug=True)