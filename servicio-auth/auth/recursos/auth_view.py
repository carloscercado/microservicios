from .base_view import BaseView
from ..database import Usuario, Conexion
from ..excepciones import CamposInvalidosError, AuthError, RefreshTokenError
import peewee
from flask_classy import route
import datetime
from .validaciones.validaciones import ValidacionLogin, ValidacionRefresh, union_de_errores  # noqa E501
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
                conexion = Conexion.create(
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
                username = datos.get("username").upper()
                usuario = Usuario.get(Usuario.usuario == username,
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
            except:
                pass

    def get_claims_jwt(self, usuario):
        return  {
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
            "iss": "refresh token"
        }
