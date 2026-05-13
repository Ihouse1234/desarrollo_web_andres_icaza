from flask import Flask, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = "mi_clave_secreta"

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+pymysql://cc5002:programacionweb@localhost:3306/Tarea_2/datos'
)

app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)

@app.route("/templates/registro")
def registro():
    return render_template(
        "registro.html",
        regiones=[],
        comunas=[],
        form_data={},
        errors={}
    )

@app.route("/templates/miembros")
def miembros():
    return render_template("miembros.html",
                           miembros = [],
                           pagination = None
                           )

@app.route("/templates/miembro_detalle")
def miembro_detalle():
    return render_template("miembro_detalle.html",
                           miembro = None,
                           )

@app.route("/")
def index():
    flash("Bienvenidos a ComuniRed", "success")
    return render_template("base.html")

@app.route("/test-db")
def test_db():
    regiones = Region.query.all()
    return str(regiones)

if __name__ == "__main__":
    app.run(debug=True)