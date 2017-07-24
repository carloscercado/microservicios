import wtforms_json
from wtforms import Form, StringField, IntegerField, validators, DateTimeField
wtforms_json.init()

requerido = "es requerido"
password_mensaje = "Minimo 8 caracteres, Maximo 15, Al menos una letra mayúscula, Al menos una letra minucula, Al menos un dígito, No espacios en blanco, Al menos 1 caracter especial"  # noqa E501


def union_de_errores(formErrors):
    validation = {}
    for error in formErrors:
        cadena = ', '.join(formErrors[error])
        validation[error] = cadena
    return validation


class ValidacionLogin(Form):
    username = StringField("username", [
        validators.InputRequired(message=requerido),
        validators.Length(min=6, max=20, message="caracteres minimo 6")])

    password = StringField("password", [
        validators.InputRequired(message=requerido)])
    #  validators.Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{6,15}', message=password_mensaje)


class ValidacionRefresh(Form):
    refresh_token = StringField("refresh_token", [
        validators.InputRequired(message=requerido)])


class ValidacionRegistro(Form):
    nombre = StringField("nombre", [
        validators.InputRequired(message=requerido)])

    apellido = StringField("apellido", [
        validators.InputRequired(message=requerido)])

    usuario = StringField("usuario", [
        validators.InputRequired(message=requerido),
        validators.Length(min=6, max=15, message="caracteres entre 5 a 15")])
    clave = StringField("clave", [
        validators.InputRequired(message=requerido),
        validators.Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{6,15}', message=password_mensaje)])  # noqa E501

    email = StringField("email", [
        validators.Regexp(r'^[_a-z0-9-]+(.[_a-z0-9-]+)*@[a-z0-9-]+(.[a-z0-9-]+)*(.[a-z]{2,4})$', message="email invalido")  # noqa E501
        ])

    pregunta = StringField("pregunta", [
        validators.InputRequired(message=requerido)])

    respuesta = StringField("respuesta", [
        validators.InputRequired(message=requerido)])

    nacimiento = DateTimeField('nacimiento', [
        validators.InputRequired(message="es requerida y formato debe ser d/m/y")],  # noqa E501
        format='%d/%m/%Y')
