from .base_view import BaseView
from ..database import Usuario
from ..excepciones import UsuarioError, CamposInvalidosError
import peewee
from flask_classy import route
from .validaciones.validaciones import ValidacionRegistro, union_de_errores
from flask import jsonify, g, request
from .interceptador import validar_jwt


class UsuariosView(BaseView):

    @validar_jwt
    def index(self):
        with self.conexion.atomic():
            try:
                resultado = Usuario.select()\
                            .where(Usuario.empresa == g.empresa)
                res = [obj.as_dict() for obj in resultado]
                return jsonify(res)
            except peewee.IntegrityError:
                raise UsuarioError("Problemas al consultar Usuarios")

    @validar_jwt
    def get(self, _id):
        with self.conexion.atomic():
            try:
                resultado = Usuario.get(Usuario.id == _id,
                                        Usuario.empresa == g.empresa)
                return jsonify(resultado.as_dict())
            except Usuario.DoesNotExist:
                raise UsuarioError("Usuario no existe", status=404)

    @validar_jwt
    @route("/mi_cuenta")
    def mi_cuenta(self):
        with self.conexion.atomic():
            try:
                resultado = Usuario.get(Usuario.id == g.usuario)
                return jsonify(resultado.as_dict())
            except Usuario.DoesNotExist:
                raise UsuarioError("Usuario no existe", status=404)

    @validar_jwt
    def post(self):
        with self.conexion.atomic():
            try:
                datos = request.json
                form = ValidacionRegistro.from_json(datos)
                if not form.validate():
                    errors = union_de_errores(form.errors)
                    raise CamposInvalidosError(errors)
                res = Usuario.select()\
                             .where(Usuario.email == datos.get("email").upper())  # noqa E501
                if len(res) > 0:
                    raise RegistroError("Ya existe una cuenta usando este email")  # noqa E501

                password = hashlib.md5(datos.get("clave").encode('utf-8')).hexdigest()  # noqa E501
                usuario = Usuario.create(
                    nombre=datos.get("nombre").upper(),
                    apellido=datos.get("apellido").upper(),
                    email=datos.get("email").upper(),
                    clave=password,
                    pregunta=datos.get("pregunta").upper(),
                    respuesta=datos.get("respuesta").upper(),
                    nacimiento=datos.get("nacimiento"),
                    empresa=g.empresa)
                return jsonify(usuario.as_dict()), 201
            except peewee.IntegrityError as e:
                raise UsuarioError("Error al registrar Usuario")

    @validar_jwt
    def put(self, _id):
        with self.conexion.atomic():
            try:
                datos = request.json
                form = ValidacionRegistro.from_json(datos)
                if not form.validate():
                    errors = union_de_errores(form.errors)
                    raise CamposInvalidosError(errors)
                usuario = Usuario.get(Usuario.id == _id,
                                      Usuario.empresa == g.empresa)
                parametos = {
                    "nombre": datos.get("nombre").upper(),
                    "apellido": datos.get("nombre").upper(),
                    "nacimiento": datos.get("nacimiento"),
                    "pregunta": datos.get("pregunta").upper(),
                    "respuesta": datos.get("respuesta").upper()
                }
                for key in parametos.keys():
                    getattr(usuario, key)
                    setattr(usuario, key, parametos[key])
                if usuario.save() > 0:
                    return jsonify(Usuario.as_dict())
            except Usuario.DoesNotExist:
                raise UsuarioError("Usuario no existe", status=404)
            except peewee.IntegrityError as e:
                raise UsuarioError("Error al modificar Usuario")
