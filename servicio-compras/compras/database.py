import peewee as peewee
from playhouse.shortcuts import model_to_dict
import os
import re

base_datos = os.environ.get("DB_NAME", "inventario")
equipo = os.environ.get("DB_HOST", "127.0.0.1")
usuario = os.environ.get("DB_USER", "postgres")
clave = os.environ.get("DB_PASS", "admin")
puerto = int(os.environ.get("DB_PORT",  5432))

conexion = peewee.PostgresqlDatabase(
    base_datos,
    user=usuario,
    password=clave,
    host=equipo,
    port=puerto
)

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def convertir_a_snake_case(name):
    s1 = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', s1).lower()


class ModeloBase(peewee.Model):
    _decimales = 4
    _presicion = 16

    class Meta:
        database = conexion

    def as_dict(self, *args, **kwargs):
        return model_to_dict(self, exclude=(Proveedor.empresa,
                                            Compra.empresa,
                                            Unidad.empresa,
                                            DetalleCompra.compra))

    def as_dict_without(self, *args, **kwargs):
        data = self.as_dict()
        if(len(args) > 0):
            return {c: getattr(self, c) for c in data if c not in args}
        return data

    def as_dict_only_with(self, *args, **kwargs):
        data = self.as_dict()
        if(len(args) > 0):
            return {c: getattr(self, c) for c in data if c in args}
        return data

    def db_table_func(cls):
        return convertir_a_snake_case(cls.__name__)


class Proveedor(ModeloBase):
    rif = peewee.CharField(max_length=20, unique=True)
    nombre = peewee.CharField(max_length=15)
    empresa = peewee.IntegerField()
    telefono = peewee.CharField(max_length=15, null=True)
    correo = peewee.CharField(max_length=30, null=True)
    descripcion = peewee.TextField(null=True)


class Compra(ModeloBase):
    factura = peewee.CharField(max_length=15)
    empresa = peewee.IntegerField()
    proveedor = peewee.ForeignKeyField(Proveedor)
    total = peewee.DecimalField(max_digits=ModeloBase._presicion, decimal_places=ModeloBase._decimales, default=0)  # noqa E501
    fecha = peewee.DateField()
    productos = peewee.IntegerField(default=0)


class Producto(ModeloBase):
    nombre = peewee.CharField(max_length=30)
    medida = peewee.CharField(max_length=15)
    perecedero = peewee.BooleanField(default=False)


class DetalleCompra(ModeloBase):
    compra = peewee.ForeignKeyField(Compra)
    producto = peewee.ForeignKeyField(Producto)
    cantidad = peewee.IntegerField()
    costo = peewee.DecimalField(max_digits=ModeloBase._presicion, decimal_places=ModeloBase._decimales)  # noqa E501
    total = peewee.DecimalField()


class Unidad(ModeloBase):
    detalle = peewee.ForeignKeyField(DetalleCompra)
    cubiculo = peewee.IntegerField()
    codigo = peewee.CharField(max_length=30)
    producto = peewee.IntegerField()
    empresa = peewee.IntegerField()
    cava = peewee.IntegerField()
    status = peewee.BooleanField(default=True)


def get_modelos():
    return [Proveedor, Compra, DetalleCompra, Unidad]


def crear_tablas():
    conexion.create_tables(get_modelos(), safe=True)


def borrar_tablas():
    conexion.drop_tables(get_modelos(), cascade=True)


def verificar_exisencia_modelo():
    for modelo in get_modelos():
        if not modelo.table_exists():
            raise Exception("FALTAN TABLAS EN LA BASE DE DATOS")
