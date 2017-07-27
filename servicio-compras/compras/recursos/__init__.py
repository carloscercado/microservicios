from flask import request, jsonify, g, debughelpers
from flask.json import JSONEncoder
import compras
from flask_cors import CORS
from decimal import Decimal
import datetime
from .proveedor_view import ProveedoresView
from .compra_view import ComprasView
import jwt
from ..excepciones import BaseError, AuthError


class AllMightyJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime.time):
                return obj.strftime("%H:%M")
            if isinstance(obj, datetime.date):
                return obj.strftime("%Y-%m-%d")
            if isinstance(obj, datetime.datetime):
                return obj.strftime("%Y-%m-%d %H:%M:%S")
            if isinstance(obj, compras.database.ModeloBase):
                return obj.as_dict()
            if isinstance(obj, Decimal):
                return str(obj)
        except TypeError:
            pass
        return JSONEncoder.default(self, obj)


def cargar_recursos(app):
    ProveedoresView.build(app)
    ComprasView.build(app)
    CORS(app)
    app.json_encoder = AllMightyJSONEncoder

    @app.before_request
    def interceptar_consulta():
        if request.method == 'OPTIONS':
            return
        cabecera = request.headers.get('Authorization')
        if not cabecera:
            raise AuthError("Credenciales son necesarias")
        json_web_token = cabecera.split(" ")[1]
        if not json_web_token:
            raise AuthError("Credenciales invalidas")
        resultado = descifrar_jwt(json_web_token)
        g.empresa = resultado.get("empresa")
        g.usuario = resultado.get("sub")

    def descifrar_jwt(json_web_token):
        try:
            return jwt.decode(json_web_token, "secret")
        except jwt.exceptions.DecodeError as e:
            raise AuthError("firma invalida", status=500)

    @app.errorhandler(BaseError)
    def manejador_de_excepciones(e):
        response = jsonify(e.getJSON())
        return response, e.status

    @app.errorhandler(debughelpers.FormDataRoutingRedirect)
    def excepcion_post(e):
        response = jsonify({"mensaje": "falta / al final del recurso",
                            "codigo": "0000"})
        return response, 400
