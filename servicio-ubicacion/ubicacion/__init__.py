from flask import Flask
from . import recursos, database


def iniciar_aplicacion(test=False):
    app = Flask(__name__)
    if not test:
        database.conexion.connect()
        database.verificar_exisencia_modelo()
    recursos.cargar_recursos(app)
    return app
