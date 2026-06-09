import os
import re
import uuid
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "mi_clave_secreta"

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+pymysql://cc5002:programacionweb@localhost:3306/tarea2?charset=utf8mb4'
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'webp'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

class Region(db.Model):
    __tablename__ = 'region'
    id      = db.Column(db.Integer, primary_key=True)
    nombre  = db.Column(db.String(200), nullable=False)
    comunas = db.relationship('Comuna', back_populates='region')  # ← back_populates

class Comuna(db.Model):
    __tablename__ = 'comuna'
    id        = db.Column(db.Integer, primary_key=True)
    nombre    = db.Column(db.String(200), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))
    region    = db.relationship('Region', back_populates='comunas')  # ← back_populates
    miembros  = db.relationship('Miembro', back_populates='comuna')  # ← agregar

class Miembro(db.Model):
    __tablename__ = 'miembro'
    id             = db.Column(db.Integer, primary_key=True)
    nombre         = db.Column(db.String(255), nullable=False)
    email          = db.Column(db.String(80),  nullable=False)
    telefono       = db.Column(db.String(15),  nullable=False)
    fecha_registro = db.Column(db.DateTime,    nullable=False)
    comuna_id      = db.Column(db.Integer, db.ForeignKey('comuna.id'))
    comuna         = db.relationship('Comuna', back_populates='miembros')  # ← agregar
    actividades    = db.relationship('Actividad', backref='miembro')

class Actividad(db.Model):
    __tablename__ = 'actividad'
    id          = db.Column(db.Integer, primary_key=True)
    miembro_id  = db.Column(db.Integer, db.ForeignKey('miembro.id'))
    dia         = db.Column(db.Enum('lunes','martes','miércoles','jueves',
                                    'viernes','sábado','domingo'))
    hora_inicio = db.Column(db.String(5))
    duracion    = db.Column(db.String(5))
    tipo        = db.Column(db.Enum('arte','deporte','tecnología',
                                    'social','recreación','otra'))
    nombre      = db.Column(db.String(45))
    descripcion = db.Column(db.Text)
    fotos       = db.relationship('Foto', backref='actividad')

class Foto(db.Model):
    __tablename__ = 'foto'
    id             = db.Column(db.Integer, primary_key=True)
    ruta_archivo   = db.Column(db.String(300))
    nombre_archivo = db.Column(db.String(300))
    actividad_id   = db.Column(db.Integer, db.ForeignKey('actividad.id'))

DIAS_VALIDOS  = {'lunes','martes','miércoles','jueves','viernes','sábado','domingo'}
TIPOS_VALIDOS = {'arte','deporte','tecnología','social','recreación','otra'}
RE_HORA  = re.compile(r'^\d{2}:\d{2}$')
RE_EMAIL = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')
RE_TEL   = re.compile(r'^\+?[0-9]{7,15}$')

def allowed_file(filename):
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
    )

def save_file(file):
    ext      = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    ruta     = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(ruta)
    return ruta, filename

def validar_miembro(nombre, email, telefono, region_id, comuna_id):
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
        comuna = db.session.get(Comuna, int(comuna_id))
        if not comuna:
            errors['comuna_id'] = 'Comuna no encontrada.'
        elif region_id and str(comuna.region_id) != str(region_id):
            errors['comuna_id'] = 'La comuna no corresponde a la región.'
    return errors


@app.route('/')
def index():
    ultimos_miembros  = Miembro.query.order_by(Miembro.fecha_registro.desc()).limit(5).all()
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
    regiones = Region.query.order_by(Region.nombre).all()
    comunas  = Comuna.query.order_by(Comuna.nombre).all()

    if request.method == 'GET':
        return render_template('registro.html',
                               regiones=regiones,
                               comunas=comunas,
                               form_data=None,
                               errors=None)

    # POST: recoger datos
    nombre    = request.form.get('nombre', '').strip()
    email     = request.form.get('email', '').strip()
    telefono  = request.form.get('telefono', '').strip()
    region_id = request.form.get('region_id', '').strip()
    comuna_id = request.form.get('comuna_id', '').strip()

    act_nombres      = request.form.getlist('act_nombre[]')
    act_tipos        = request.form.getlist('act_tipo[]')
    act_dias         = request.form.getlist('act_dia[]')
    act_horas        = request.form.getlist('act_hora[]')
    act_duraciones   = request.form.getlist('act_duracion[]')
    act_descripciones = request.form.getlist('act_descripcion[]')

    errors = validar_miembro(nombre, email, telefono, region_id, comuna_id)

    if not act_nombres or all(n.strip() == '' for n in act_nombres):
        errors['actividades'] = 'Debe agregar al menos una actividad.'

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

    # Sin errores: insertar
    nuevo_miembro = Miembro(
        nombre=nombre, email=email, telefono=telefono,
        fecha_registro=datetime.now(), comuna_id=int(comuna_id),
    )
    db.session.add(nuevo_miembro)
    db.session.flush()

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
        db.session.flush()

        fotos = request.files.getlist(f'act_fotos_{i}[]')
        for foto in fotos:
            if foto and foto.filename and allowed_file(foto.filename):
                ruta, nombre_archivo = save_file(foto)
                db.session.add(Foto(
                    ruta_archivo=ruta,
                    nombre_archivo=nombre_archivo,
                    actividad_id=nueva_actividad.id,
                ))

    db.session.commit()
    flash(f'Miembro "{nombre}" registrado exitosamente.', 'success')
    return redirect(url_for('index'))

@app.route('/miembros')
def miembros():
    page       = request.args.get('page', 1, type=int)
    pagination = Miembro.query.order_by(Miembro.fecha_registro.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('miembros.html',
                           miembros=pagination.items,
                           pagination=pagination)

@app.route('/miembros/<int:id>')
def miembro_detalle(id):
    miembro = db.session.get(Miembro, id)
    if miembro is None:
        flash('Miembro no encontrado.', 'error')
        return redirect(url_for('miembros'))
    return render_template('miembro_detalle.html', miembro=miembro)

if __name__ == '__main__':
    app.run(debug=True)