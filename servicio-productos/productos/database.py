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
        return model_to_dict(self, exclude=(Categoria.empresa,
                                            Producto.empresa, ))

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


class Usuario(ModeloBase):
    nombre = peewee.CharField(max_length=30)
    usuario = peewee.CharField(unique=True, max_length=15)
    clave = peewee.CharField(max_length=32)


class Empresa(ModeloBase):
    rif = peewee.CharField(max_length=20, unique=True)
    nombre = peewee.CharField(max_length=40)
    telefono = peewee.CharField(max_length=15, null=True)
    ciudad = peewee.CharField(max_length=15)
    direccion = peewee.CharField(max_length=60)
    usuario = peewee.ForeignKeyField(Usuario)


class Categoria(ModeloBase):
    nombre = peewee.CharField(max_length=15)
    empresa = peewee.ForeignKeyField(Empresa)


class Producto(ModeloBase):
    nombre = peewee.CharField(max_length=30)
    categoria = peewee.ForeignKeyField(Categoria)
    empresa = peewee.IntegerField()
    cantidad = peewee.IntegerField(default=0)
    minimo = peewee.IntegerField(default=0)
    medida = peewee.CharField(max_length=15)
    perecedero = peewee.BooleanField(default=False)


def get_modelos():
    return [Categoria, Producto]


def crear_tablas():
    conexion.create_tables(get_modelos(), safe=True)


def borrar_tablas():
    conexion.drop_tables(get_modelos(), cascade=True)


def verificar_exisencia_modelo():
    for modelo in get_modelos():
        if not modelo.table_exists():
            raise Exception("FALTAN TABLAS EN LA BASE DE DATOS")
