import jwt
from ..excepciones import AuthError
from flask import request, g


def validar_jwt(func):
    def validar(*args, **kwargs):
        cabecera = request.headers.get("Authorization")
        if not cabecera:
            raise AuthError("Credenciales son necesarias")
        json_web_token = cabecera.split(" ")[1]
        if not json_web_token:
            raise AuthError("Credenciales invalidas")
        try:
            resultado = jwt.decode(json_web_token, "secret")
            g.empresa = resultado.get("empresa")
            g.usuario = resultado.get("sub")
            return func(*args, **kwargs)
        except jwt.exceptions.DecodeError as e:
            raise AuthError("firma invalida", status=500)
    return validar
