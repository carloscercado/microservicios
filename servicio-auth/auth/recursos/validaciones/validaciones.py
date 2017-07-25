import wtforms_json
from wtforms import Form, StringField, validators, DateTimeField
wtforms_json.init()

requerido = "es requerido"
password_mensaje = "clave invalida, minimo 6 caracteres, maximo 15, al menos una letra mayúscula, al menos un dígito, sin espacios en blanco y al menos 1 caracter especial"  # noqa E501


def union_de_errores(formErrors):
    validation = {}
    for error in formErrors:
        cadena = ', '.join(formErrors[error])
        validation[error] = cadena
    return validation


class ValidacionLogin(Form):
    email = StringField("email", [
        validators.Regexp(r'^[_a-z0-9-]+(.[_a-z0-9-]+)*@[a-z0-9-]+(.[a-z0-9-]+)*(.[a-z]{2,4})$', message="email invalido")  # noqa E501
        ])

    password = StringField("password", [
        validators.InputRequired(message=requerido)])


class ValidacionRefresh(Form):
    refresh_token = StringField("refresh_token", [
        validators.InputRequired(message=requerido)])


class ValidacionEmpresa(Form):
    empresa = StringField("empresa", [
        validators.InputRequired(message=requerido)])

    rif = StringField("rif", [
        validators.InputRequired(message=requerido),
        validators.Regexp(r'^[VEPCJ]-\d{8}-\d{1}$', message="formato de rif invalido, ejemplo V-12345678-1")])  # noqa E501

    telefono = StringField("telefono", [
        validators.InputRequired(message=requerido),
        validators.Regexp(r'^\d{3}\-\d{7}?$', message="telefono invalido, formato 123-1234567")])  # noqa E501

    ciudad = StringField("ciudad", [
        validators.InputRequired(message=requerido)])

    direccion = StringField("direccion", [
        validators.InputRequired(message=requerido)])


class ValidacionRegistro(Form):
    nombre = StringField("nombre", [
        validators.InputRequired(message=requerido)])

    apellido = StringField("apellido", [
        validators.InputRequired(message=requerido)])

    clave = StringField("clave", [
        validators.InputRequired(message=requerido),
        validators.Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[.()$@$!%*?&])[A-Za-z\d$@$!%*?&]{6,15}', message=password_mensaje)])  # noqa E501

    email = StringField("email", [
        validators.InputRequired(message=requerido),
        validators.Regexp(r'^[_a-z0-9-]+(.[_a-z0-9-]+)*@[a-z0-9-]+(.[a-z0-9-]+)*(.[a-z]{2,4})$', message="email invalido")  # noqa E501
        ])

    pregunta = StringField("pregunta", [
        validators.InputRequired(message=requerido)])

    respuesta = StringField("respuesta", [
        validators.InputRequired(message=requerido)])

    nacimiento = DateTimeField('nacimiento', [
        validators.InputRequired(message="es requerida y formato debe ser d/m/y")],  # noqa E501
        format='%d/%m/%Y')
