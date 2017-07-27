import wtforms_json
from wtforms import Form, StringField, IntegerField, DateTimeField, validators
wtforms_json.init()

requerido = "es requerido"
monto_invalido = "formato invalido, ejemplo 123 o 123.0 o 123.0001"


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


class ValidacionProveedor(Form):
    nombre = StringField("nombre", [
        validators.InputRequired(message=requerido),
        validators.Length(max=30, message="caracteres maximo 30")])

    rif = StringField("rif", [
        validators.InputRequired(message=requerido),
        validators.Regexp(r'^[VEPCJ]-\d{8}-\d{1}$', message="formato de rif invalido, ejemplo V-12345678-1")])  # noqa E501

    correo = StringField("correo", [
        validators.InputRequired(message=requerido),
        validators.Regexp(r'^[_a-z0-9-]+(.[_a-z0-9-]+)*@[a-z0-9-]+(.[a-z0-9-]+)*(.[a-z]{2,4})$', message="email invalido")  # noqa E501
        ])

    telefono = StringField("telefono", [
        validators.InputRequired(message=requerido),
        validators.Regexp(r'^\d{3}\-\d{7}?$', message="telefono invalido, formato 123-1234567")])  # noqa E501

    descripcion = StringField("descripcion", [
        validators.InputRequired(message=requerido)])


class ValidacionCompra(Form):
    factura = StringField("factura", [
        validators.InputRequired(message=requerido),
        validators.Length(max=15, message="caracteres maximo 15")])

    proveedor = IntegerField("proveedor", [
        validators.InputRequired(message=requerido)])

    fecha = DateTimeField('fecha', [
        validators.InputRequired(message=requerido)], format='%d/%m/%Y')


class ValidacionDetalleCompra(Form):
    costo = StringField("costo", [
        validators.InputRequired(message=requerido),
        validators.Regexp(r'^\d{1,16}(\.\d{1,4})?$', message=monto_invalido)])

    cantidad = IntegerField("cantidad", [
        validators.InputRequired(message=requerido)])

    producto = IntegerField("producto", [
        validators.InputRequired(message=requerido)])
