from .base_view import BaseView
from ..database import Usuario, Conexion, Empresa
from ..excepciones import CamposInvalidosError, AuthError, RefreshTokenError, RegistroError  # noqa E501
import peewee
from flask_classy import route
import datetime
from .validaciones.validaciones import ValidacionLogin, ValidacionEmpresa, ValidacionRegistro, ValidacionRefresh, union_de_errores  # noqa E501
from flask import jsonify, request
import hashlib
import jwt


class AuthView(BaseView):

    @route("/refresh_token", methods=["POST"])
    def refresh_token(self):
        with self.conexion.atomic():
            try:
                datos = request.json
                form = ValidacionRefresh.from_json(datos)
                if not form.validate():
                    errors = union_de_errores(form.errors)
                    raise CamposInvalidosError(errors)
                refresh_token = datos.get("refresh_token")
                resultado = jwt.decode(refresh_token, self.API_KEY)
                if resultado.get("iss") != "refresh token":
                    raise RefreshTokenError("tipo de token invalido")
                res = Conexion.get(Conexion.usuario == resultado.get("sub"),
                                   Conexion.status,
                                   Conexion.ip == request.remote_addr,
                                   Conexion.refresh_token == refresh_token)
                claims_jwt = self.get_claims_jwt(res.usuario)
                json_web_token = jwt.encode(claims_jwt, self.API_KEY)
                claims_refresh_token = self.get_claims_refresh_token(res.usuario)  # noqa E501
                refresh_token = jwt.encode(claims_refresh_token, self.API_KEY)
                res.status = False
                res.save()
                Conexion.create(
                    usuario=res.usuario.id,
                    user_agent=request.headers.get('User-Agent'),
                    ip=request.remote_addr,
                    refresh_token=refresh_token.decode("utf-8"))
                salida = {
                    "token": json_web_token.decode("utf-8"),
                    "refresh_token": refresh_token.decode("utf-8")
                }
                return jsonify(salida)
            except Conexion.DoesNotExist:
                raise RefreshTokenError("refresh token no existe")
            except jwt.InvalidTokenError:
                raise RefreshTokenError("refresh token invalido")

    def post(self):
        with self.conexion.atomic():
            try:
                datos = request.json
                form = ValidacionLogin.from_json(datos)
                if not form.validate():
                    errors = union_de_errores(form.errors)
                    raise CamposInvalidosError(errors)
                password = hashlib.md5(datos.get("password").encode('utf-8')).hexdigest()  # noqa E501
                username = datos.get("email").upper()
                usuario = Usuario.get(Usuario.email == username,
                                      Usuario.clave == password)

                claims_jwt = self.get_claims_jwt(usuario)
                json_web_token = jwt.encode(claims_jwt, self.API_KEY)
                claims_refresh_token = self.get_claims_refresh_token(usuario)
                refresh_token = jwt.encode(claims_refresh_token, self.API_KEY)
                conexion = Conexion.create(
                    usuario=usuario.id,
                    user_agent=request.headers.get('User-Agent'),
                    ip=request.remote_addr,
                    refresh_token=refresh_token.decode("utf-8"))
                usuario.ultima_conexion = conexion.fecha
                usuario.save()
                salida = {
                    "token": json_web_token.decode("utf-8"),
                    "refresh_token": refresh_token.decode("utf-8")
                }
                return jsonify(salida), 201
            except Usuario.DoesNotExist:
                raise AuthError("Credenciales invalidas")
            except peewee.IntegrityError as e:
                raise AuthError("Error al registrar acceso")

    @route("/registrar", methods=["POST"])
    def registrar(self):
        with self.conexion.atomic():
            try:
                datos = request.json
                form = ValidacionRegistro.from_json(datos)
                if not form.validate():
                    errors = union_de_errores(form.errors)
                    raise CamposInvalidosError(errors)
                form = ValidacionEmpresa.from_json(datos)
                if not form.validate():
                    errors = union_de_errores(form.errors)
                    raise CamposInvalidosError(errors)

                res = Usuario.select()\
                             .where(Usuario.email == datos.get("email").upper())  # noqa E501
                if len(res) > 0:
                    raise RegistroError("Ya existe una cuenta usando este email")  # noqa E501

                res = Empresa.select().where(Empresa.rif == datos.get("rif"))
                if len(res) > 0:
                    raise RegistroError("Ya existe una empresa registrada con este rif")  # noqa E501

                password = hashlib.md5(datos.get("clave").encode('utf-8')).hexdigest()  # noqa E501
                usuario = Usuario.create(
                    nombre=datos.get("nombre").upper(),
                    apellido=datos.get("apellido").upper(),
                    email=datos.get("email").upper(),
                    clave=password,
                    pregunta=datos.get("pregunta").upper(),
                    respuesta=datos.get("respuesta").upper(),
                    nacimiento=datos.get("nacimiento")
                    )
                empresa = Empresa.create(
                    nombre=datos.get("empresa").upper(),
                    ciudad=datos.get("ciudad").upper(),
                    direccion=datos.get("direccion").upper(),
                    rif=datos.get("rif"),
                    usuario=usuario.id,
                    telefono=datos.get("telefono")
                    )
                usuario.empresa = empresa.id
                usuario.save()
                return jsonify(usuario.as_dict_only_with("nombre", "apellido", "email")), 201  # noqa E501
            except peewee.IntegrityError as e:
                print(e)
                raise RegistroError("Problemas al registrar usuario")

    def get_claims_jwt(self, usuario):
        return {
            "exp": (datetime.datetime.utcnow() + datetime.timedelta(minutes=15)),  # noqa E501
            "iss": "inventario",
            "iat": datetime.datetime.utcnow(),
            "empresa": usuario.empresa,
            "sub": usuario.nombre,
            "email": usuario.email,
            "id": usuario.id,
            "pregunta": usuario.pregunta
        }

    def get_claims_refresh_token(self, usuario):
        return {
            "sub": usuario.id,
            "iat": datetime.datetime.utcnow(),
            "iss": "refresh token",
            "email": usuario.email
        }
