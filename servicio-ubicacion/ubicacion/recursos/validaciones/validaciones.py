import wtforms_json
from wtforms import Form, StringField, IntegerField, validators

wtforms_json.init()

requerido = "es requerido"


def union_de_errores(formErrors):
    validation = {}
    for error in formErrors:
        cadena = ', '.join(formErrors[error])
        validation[error] = cadena
    return validation


class ValidacionEmpresa(Form):
    rif = StringField("rif", [
        validators.InputRequired(message=requerido),
        validators.Regexp(r'^[VEPCJ]-\d{8}-\d{1}$', message="formato de rif invalido, ejemplo V-12345678-1")])  # noqa E501

    nombre = StringField("nombre", [
        validators.InputRequired(message=requerido),
        validators.Length(min=5, max=40, message="caracteres entres 5 y 40")])

    telefono = StringField("telefono", [
        validators.Regexp(r'^\d{3}\-\d{7}?$', message="Formato invalido, ejemplo: 123-1234567")  # noqa E501
        ])

    ciudad = StringField("ciudad", [
        validators.InputRequired(message=requerido),
        validators.Length(min=5, max=15, message="caracteres entres 5 y 15")])

    direccion = StringField("direccion", [
        validators.InputRequired(message=requerido),
        validators.Length(max=60, message="maximo de caracteres 60")])


class ValidacionAlmacen(Form):
    nombre = StringField("nombre", [
        validators.InputRequired(message=requerido),
        validators.Length(max=30, message="caracteres maximo 40")
        ])

    capacidad = IntegerField("capacidad", [
        validators.InputRequired(message=requerido)
        ])


class ValidacionEstante(Form):
    nombre = StringField("nombre", [
        validators.InputRequired(message=requerido),
        validators.Length(max=30, message="caracteres maximo 40")
        ])

    capacidad = IntegerField("capacidad", [
        validators.InputRequired(message=requerido)
        ])

    almacen = IntegerField("almacen", [
        validators.InputRequired(message=requerido)
        ])


class ValidacionCubiculo(Form):
    nombre = StringField("nombre", [
        validators.InputRequired(message=requerido),
        validators.Length(max=30, message="caracteres maximo 40")
        ])

    capacidad = IntegerField("capacidad", [
        validators.InputRequired(message=requerido)
        ])

    estante = IntegerField("estante", [
        validators.InputRequired(message=requerido)
        ])
