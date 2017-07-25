import wtforms_json
from wtforms import Form, StringField, IntegerField, validators
import re
wtforms_json.init()

requerido = "es requerido"


def union_de_errores(formErrors):
    validation = {}
    for error in formErrors:
        cadena = ', '.join(formErrors[error])
        validation[error] = cadena
    return validation


class ValidacionCategoria(Form):
    nombre = StringField("nombre", [
        validators.InputRequired(message=requerido),
        validators.Length(max=15, message="caracteres maximo 15")])


class ValidacionProducto(Form):
    nombre = StringField("nombre", [
        validators.InputRequired(message=requerido),
        validators.Length(max=30, message="caracteres maximo 30")])

    categoria = IntegerField("categoria", [
        validators.InputRequired(message=requerido)])

    minimo = IntegerField("minimo", [
        validators.InputRequired(message=requerido)])

    medida = StringField("medida", [
        validators.InputRequired(message=requerido),
        validators.Length(max=15, message="caracteres maximo 15")])

    perecedero = StringField("perecedero", [
        validators.Regexp(r'^(true|false)$', re.I,
                          message="debe ser un valor booleano")])
