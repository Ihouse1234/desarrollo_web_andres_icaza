import os                       # crear carpetas y armar rutas de archivos
import re                       # expresiones regulares (validar email, teléfono, hora)
import uuid                     # generar nombres únicos para las fotos
from datetime import datetime   # fecha/hora de registro de miembros y comentarios

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename 
from sqlalchemy import func                   # funciones SQL: count(), date() (para estadísticas)

app = Flask(__name__)
app.secret_key = "mi_clave_secreta"   # necesaria para flash() (mensajes temporales)

# Conexión a MySQL. El ?charset=utf8mb4 es para que las tildes y la ñ se guarden y lean correctamente.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+pymysql://cc5002:programacionweb@localhost:3306/tarea2?charset=utf8mb4'
)

app.config['UPLOAD_FOLDER'] = 'static/uploads'                    
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'webp'}

db = SQLAlchemy(app)  


class Region(db.Model):
    __tablename__ = 'region'
    id      = db.Column(db.Integer, primary_key=True)
    nombre  = db.Column(db.String(200), nullable=False)
    # back_populates conecta esta relación con Comuna.region (bidireccional)
    comunas = db.relationship('Comuna', back_populates='region')

class Comuna(db.Model):
    __tablename__ = 'comuna'
    id        = db.Column(db.Integer, primary_key=True)
    nombre    = db.Column(db.String(200), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))  # FK -> region
    # Estas relaciones permiten hacer comuna.region y comuna.miembros en el código
    region    = db.relationship('Region', back_populates='comunas')
    miembros  = db.relationship('Miembro', back_populates='comuna')

class Miembro(db.Model):
    __tablename__ = 'miembro'
    id             = db.Column(db.Integer, primary_key=True)
    nombre         = db.Column(db.String(255), nullable=False)
    email          = db.Column(db.String(80),  nullable=False)
    telefono       = db.Column(db.String(15),  nullable=False)
    fecha_registro = db.Column(db.DateTime,    nullable=False)  # se llena con datetime.now()
    comuna_id      = db.Column(db.Integer, db.ForeignKey('comuna.id'))  # FK -> comuna
    comuna         = db.relationship('Comuna', back_populates='miembros')
    # backref crea automáticamente actividad.miembro en el otro lado
    actividades    = db.relationship('Actividad', backref='miembro')

class Actividad(db.Model):
    __tablename__ = 'actividad'
    id          = db.Column(db.Integer, primary_key=True)
    miembro_id  = db.Column(db.Integer, db.ForeignKey('miembro.id'))
    # ENUM: la columna solo acepta exactamente estos valores (tildes incluidas)
    dia         = db.Column(db.Enum('lunes','martes','miércoles','jueves',
                                    'viernes','sábado','domingo'))
    hora_inicio = db.Column(db.String(5))   # "HH:MM"
    duracion    = db.Column(db.String(5))   # "HH:MM"
    tipo        = db.Column(db.Enum('arte','deporte','tecnología',
                                    'social','recreación','otra'))
    nombre      = db.Column(db.String(45))
    descripcion = db.Column(db.Text)
    fotos       = db.relationship('Foto', backref='actividad')

class Foto(db.Model):
    __tablename__ = 'foto'
    id             = db.Column(db.Integer, primary_key=True)
    ruta_archivo   = db.Column(db.String(300))  # ruta completa en el servidor
    nombre_archivo = db.Column(db.String(300))  # nombre único del archivo guardado
    actividad_id   = db.Column(db.Integer, db.ForeignKey('actividad.id'))

class Comentario(db.Model):
    __tablename__ = 'comentario'
    id            = db.Column(db.Integer, primary_key=True)
    actividad_id  = db.Column(db.Integer, db.ForeignKey('actividad.id'), nullable=False)
    nombre        = db.Column(db.String(80), nullable=False)  # nombre del comentarista
    texto         = db.Column(db.Text, nullable=False)
    fecha         = db.Column(db.DateTime, nullable=False)

DIAS_VALIDOS  = {'lunes','martes','miércoles','jueves','viernes','sábado','domingo'}
TIPOS_VALIDOS = {'arte','deporte','tecnología','social','recreación','otra'}

RE_HORA  = re.compile(r'^\d{2}:\d{2}$')              # formato "HH:MM"
RE_EMAIL = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$') # email básico
RE_TEL   = re.compile(r'^\+?[0-9]{7,15}$')           # teléfono, + opcional al inicio

def allowed_file(filename):
    # True si el archivo tiene una extensión de imagen permitida.
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
    )

def save_file(file):
    """Guarda una foto con nombre único (uuid) y retorna (ruta, nombre_archivo)."""
    ext      = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"   # nombre único: evita colisiones
    ruta     = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(ruta)
    return ruta, filename

def validar_miembro(nombre, email, telefono, region_id, comuna_id):
    # Valida los datos del miembro en el SERVIDOR, retorna un dict de errores (vacío = todo válido).
    errors = {}
    if not nombre or len(nombre.strip()) < 2:
        errors['nombre'] = 'El nombre debe tener al menos 2 caracteres.'
    if not email or not RE_EMAIL.match(email.strip()):
        errors['email'] = 'Ingrese un correo electrónico válido.'
    if not telefono or not RE_TEL.match(telefono.strip()):
        errors['telefono'] = 'Teléfono inválido. Ejemplo: +56912345678'
    if not region_id:
        errors['region_id'] = 'Seleccione una región.'
    if not comuna_id:
        errors['comuna_id'] = 'Seleccione una comuna.'
    else:
        # Verifica que la comuna exista y pertenezca a la región elegida
        comuna = db.session.get(Comuna, int(comuna_id))
        if not comuna:
            errors['comuna_id'] = 'Comuna no encontrada.'
        elif region_id and str(comuna.region_id) != str(region_id):
            errors['comuna_id'] = 'La comuna no corresponde a la región.'
    return errors

@app.route('/')
def index():
    # Últimos 5 miembros (ordenados por fecha descendente)
    ultimos_miembros  = Miembro.query.order_by(Miembro.fecha_registro.desc()).limit(5).all()
    # Contadores para las cajas de estadísticas de la portada
    total_miembros    = Miembro.query.count()
    total_actividades = Actividad.query.count()
    total_fotos       = Foto.query.count()
    total_comunas     = Comuna.query.count()
    return render_template(
        'index.html',
        ultimos_miembros=ultimos_miembros,
        total_miembros=total_miembros,
        total_actividades=total_actividades,
        total_fotos=total_fotos,
        total_comunas=total_comunas,
    )

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    # Se necesitan en GET (mostrar el form) y en POST (repoblar si hay error)
    regiones = Region.query.order_by(Region.nombre).all()
    comunas  = Comuna.query.order_by(Comuna.nombre).all()

    # GET: mostrar el formulario vacío
    if request.method == 'GET':
        return render_template('registro.html',
                               regiones=regiones,
                               comunas=comunas,
                               form_data=None,
                               errors=None)

    # POST: procesar el formulario enviado
    # request.form.get() para campos simples
    nombre    = request.form.get('nombre', '').strip()
    email     = request.form.get('email', '').strip()
    telefono  = request.form.get('telefono', '').strip()
    region_id = request.form.get('region_id', '').strip()
    comuna_id = request.form.get('comuna_id', '').strip()

    # request.form.getlist() para los campos repetidos (varias actividades)
    act_nombres      = request.form.getlist('act_nombre[]')
    act_tipos        = request.form.getlist('act_tipo[]')
    act_dias         = request.form.getlist('act_dia[]')
    act_horas        = request.form.getlist('act_hora[]')
    act_duraciones   = request.form.getlist('act_duracion[]')
    act_descripciones = request.form.getlist('act_descripcion[]')

    # Validación en el servidor (no confiar solo en el JS del navegador)
    errors = validar_miembro(nombre, email, telefono, region_id, comuna_id)

    if not act_nombres or all(n.strip() == '' for n in act_nombres):
        errors['actividades'] = 'Debe agregar al menos una actividad.'

    # Si hay errores: devolver el form con los datos ya escritos.
    if errors:
        form_data = {
            'nombre': nombre, 'email': email, 'telefono': telefono,
            'region_id': region_id, 'comuna_id': comuna_id,
            'actividades': [
                {
                    'nombre':      act_nombres[i],
                    'tipo':        act_tipos[i]        if i < len(act_tipos)        else '',
                    'dia':         act_dias[i]         if i < len(act_dias)         else '',
                    'hora':        act_horas[i]        if i < len(act_horas)        else '',
                    'duracion':    act_duraciones[i]   if i < len(act_duraciones)   else '',
                    'descripcion': act_descripciones[i] if i < len(act_descripciones) else '',
                }
                for i in range(len(act_nombres))
            ]
        }
        return render_template('registro.html',
                               regiones=regiones, comunas=comunas,
                               errors=errors, form_data=form_data)

    # Sin errores: insertar el miembro
    nuevo_miembro = Miembro(
        nombre=nombre, email=email, telefono=telefono,
        fecha_registro=datetime.now(), comuna_id=int(comuna_id),
    )
    db.session.add(nuevo_miembro)
    db.session.flush()   # flush() asigna el id sin cerrar la transacción.

    # Insertar cada actividad y sus fotos asociadas
    for i, act_nombre in enumerate(act_nombres):
        nueva_actividad = Actividad(
            miembro_id  = nuevo_miembro.id,
            nombre      = act_nombre.strip(),
            tipo        = act_tipos[i],
            dia         = act_dias[i],
            hora_inicio = act_horas[i],
            duracion    = act_duraciones[i],
            descripcion = act_descripciones[i].strip() if i < len(act_descripciones) else None,
        )
        db.session.add(nueva_actividad)
        db.session.flush()   # obtener el id de la actividad para asociar sus fotos

        # Las fotos de la actividad i llegan en el campo act_fotos_i[]
        fotos = request.files.getlist(f'act_fotos_{i}[]')
        for foto in fotos:
            if foto and foto.filename and allowed_file(foto.filename):
                ruta, nombre_archivo = save_file(foto)
                db.session.add(Foto(
                    ruta_archivo=ruta,
                    nombre_archivo=nombre_archivo,
                    actividad_id=nueva_actividad.id,
                ))

    db.session.commit()   # confirma TODAS las inserciones juntas
    flash(f'Miembro "{nombre}" registrado exitosamente.', 'success')
    return redirect(url_for('index'))   # vuelve a la portada con mensaje de éxito

@app.route('/miembros')
def miembros():
    page       = request.args.get('page', 1, type=int)   # ?page=N en la URL
    # paginate() divide los resultados en páginas de 10
    pagination = Miembro.query.order_by(Miembro.fecha_registro.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('miembros.html',
                           miembros=pagination.items,   # solo los de esta página
                           pagination=pagination)        # info de paginación

@app.route('/miembros/<int:id>')
def miembro_detalle(id):
    miembro = db.session.get(Miembro, id)   # busca por id
    if miembro is None:
        flash('Miembro no encontrado.', 'error')
        return redirect(url_for('miembros'))
    return render_template('miembro_detalle.html', miembro=miembro)

@app.route('/estadisticas')
def estadisticas():
    # Solo renderiza el HTML; los datos los pide el JS con fetch a las APIs de abajo
    return render_template('estadisticas.html')


@app.route('/api/miembros-por-dia')
def api_miembros_por_dia():
    # Agrupa por fecha y cuenta cuántos miembros se registraron cada día
    resultados = (
        db.session.query(
            func.date(Miembro.fecha_registro).label('dia'),  # solo la fecha (sin hora)
            func.count(Miembro.id).label('total')
        )
        .group_by(func.date(Miembro.fecha_registro))
        .order_by(func.date(Miembro.fecha_registro))
        .all()
    )
    data = [
        {
            'dia':   str(r.dia),   # formato 'YYYY-MM-DD'
            'total': r.total
        }
        for r in resultados
    ]
    return jsonify(data)


@app.route('/api/actividades-por-tipo')
def api_actividades_por_tipo():
    # Cuenta cuántas actividades hay de cada tipo
    resultados = (
        db.session.query(
            Actividad.tipo.label('tipo'),
            func.count(Actividad.id).label('total')
        )
        .group_by(Actividad.tipo)
        .order_by(func.count(Actividad.id).desc())
        .all()
    )
    data = [
        {
            'tipo':  r.tipo,
            'total': r.total
        }
        for r in resultados
    ]
    return jsonify(data)


# ── API: Actividades por comuna (gráfico de barras) ────────────
@app.route('/api/actividades-por-comuna')
def api_actividades_por_comuna():
    # JOIN comuna -> miembro -> actividad para contar actividades por comuna
    resultados = (
        db.session.query(
            Comuna.nombre.label('comuna'),
            func.count(Actividad.id).label('total')
        )
        .join(Miembro, Miembro.comuna_id == Comuna.id)
        .join(Actividad, Actividad.miembro_id == Miembro.id)
        .group_by(Comuna.nombre)
        .order_by(func.count(Actividad.id).desc())
        .all()
    )
    data = [
        {
            'comuna': r.comuna,
            'total':  r.total
        }
        for r in resultados
    ]
    return jsonify(data)


@app.route('/api/comentarios/<int:actividad_id>', methods=['GET'])
def api_get_comentarios(actividad_id):
    # Verificar que la actividad existe
    actividad = db.session.get(Actividad, actividad_id)
    if actividad is None:
        return jsonify({'error': 'Actividad no encontrada'}), 404

    # Trae los comentarios de esa actividad, más antiguos primero
    comentarios = (
        Comentario.query
        .filter_by(actividad_id=actividad_id)
        .order_by(Comentario.fecha.asc())
        .all()
    )
    data = [
        {
            'id':     c.id,
            'nombre': c.nombre,
            'texto':  c.texto,
            'fecha':  c.fecha.strftime('%d/%m/%Y %H:%M')   
        }
        for c in comentarios
    ]
    return jsonify(data)

@app.route('/api/comentarios/<int:actividad_id>', methods=['POST'])
def api_post_comentario(actividad_id):
    # Verificar que la actividad existe
    actividad = db.session.get(Actividad, actividad_id)
    if actividad is None:
        return jsonify({'ok': False, 'error': 'Actividad no encontrada'}), 404

    datos = request.get_json()   # el cuerpo llega como JSON.
    if not datos:
        return jsonify({'ok': False, 'error': 'JSON inválido'}), 400

    nombre = datos.get('nombre', '').strip()
    texto  = datos.get('texto', '').strip()

    # Validación en el servidor según las reglas del enunciado
    errors = {}
    if len(nombre) < 3 or len(nombre) > 80:
        errors['nombre'] = 'El nombre debe tener entre 3 y 80 caracteres.'
    if len(texto) < 5:
        errors['texto'] = 'El comentario debe tener al menos 5 caracteres.'

    if errors:
        return jsonify({'ok': False, 'errors': errors}), 400

    # Insertar el comentario
    nuevo = Comentario(
        actividad_id = actividad_id,
        nombre       = nombre,
        texto        = texto,
        fecha        = datetime.now(),
    )
    db.session.add(nuevo)
    db.session.commit()

    # Devolver el comentario creado para que el JS lo muestre sin recargar la página
    return jsonify({
        'ok':     True,
        'id':     nuevo.id,
        'nombre': nuevo.nombre,
        'texto':  nuevo.texto,
        'fecha':  nuevo.fecha.strftime('%d/%m/%Y %H:%M')
    }), 201

if __name__ == '__main__':
    app.run(debug=True)  