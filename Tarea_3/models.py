from app import db

class Region(db.Model):
    __tablename__ = 'region'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    comunas = db.relationship('Comuna', backref='region')

class Comuna(db.Model):
    __tablename__ = 'comuna'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))

class Miembro(db.Model):
    __tablename__ = 'miembro'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    fecha_registro = db.Column(db.DateTime, nullable=False)
    comuna_id = db.Column(db.Integer, db.ForeignKey('comuna.id'))
    actividades = db.relationship('Actividad', backref='miembro')

class Actividad(db.Model):
    __tablename__ = 'actividad'
    id = db.Column(db.Integer, primary_key=True)
    miembro_id = db.Column(db.Integer, db.ForeignKey('miembro.id'))
    dia = db.Column(db.Enum('lunes','martes','miércoles','jueves',
                            'viernes','sábado','domingo'))
    hora_inicio = db.Column(db.String(5))
    duracion = db.Column(db.String(5))
    tipo = db.Column(db.Enum('arte','deporte','tecnología',
                             'social','recreación','otra'))
    nombre = db.Column(db.String(45))
    descripcion = db.Column(db.Text)
    fotos = db.relationship('Foto', backref='actividad')

class Foto(db.Model):
    __tablename__ = 'foto'
    id = db.Column(db.Integer, primary_key=True)
    ruta_archivo = db.Column(db.String(300))
    nombre_archivo = db.Column(db.String(300))
    actividad_id = db.Column(db.Integer, db.ForeignKey('actividad.id'))