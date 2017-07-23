from .base_view import BaseView
from flask import jsonify, g, request
from ..database import Almacen, Estante
from ..excepciones import AlmacenError, CamposInvalidosError
from .validaciones.validaciones import ValidacionAlmacen, union_de_errores
import peewee


class AlmacenesView (BaseView):

    def index(self):
        with self.conexion.atomic():
            try:
                resultado = Almacen.select()\
                        .where(Almacen.empresa == g.empresa)
                res = [obj.as_dict_without("empresa") for obj in resultado]
                return jsonify(res)
            except peewee.IntegrityError:
                raise AlmacenError("Problemas con Almacenes")

    def get(self, _id):
        with self.conexion.atomic():
            try:
                resultado = Almacen.get(Almacen.id == _id,
                                        Almacen.empresa == g.empresa)
                return jsonify(resultado.as_dict_without("empresa"))
            except Almacen.DoesNotExist:
                raise AlmacenError("Almacen no existe", status=404)

    def delete(self, _id):
        with self.conexion.atomic():
            try:
                resultado = Almacen.get(Almacen.id == _id,
                                        Almacen.empresa == g.empresa)
                if len(Estante.select().where(Estante.almacen == resultado.id)) > 0:  # noqa E501
                    raise AlmacenError("No puede ser eliminado, aun existen estantes registrados dentro de este almacen")  # noqa E501
                resultado.delete_instance()
                return jsonify({})
            except Almacen.DoesNotExist:
                raise AlmacenError("Almacen no existe", status=404)

    def post(self):
        with self.conexion.atomic():
            try:
                datos = request.json
                form = ValidacionAlmacen.from_json(datos)
                if not form.validate():
                    errors = union_de_errores(form.errors)
                    raise CamposInvalidosError(errors)
                almacen = Almacen.create(
                    empresa=g.empresa,
                    nombre=datos.get("nombre").upper(),
                    capacidad=datos.get("capacidad"),
                    capacidad_disponible=datos.get("capacidad"))
                return jsonify(almacen.as_dict_without("empresa")), 201
            except peewee.IntegrityError as e:
                raise AlmacenError("Error al registrar almacen")

    def put(self, _id):
        with self.conexion.atomic():
            try:
                almacen = Almacen.get(Almacen.id == _id,
                                      Almacen.empresa == g.empresa)
                datos = request.json
                form = ValidacionAlmacen.from_json(datos)
                if not form.validate():
                    errors = union_de_errores(form.errors)
                    raise CamposInvalidosError(errors)
                parametos = {
                    "nombre": datos.get("nombre").upper(),
                    "capacidad": datos.get("capacidad")
                }
                for key in parametos.keys():
                    getattr(almacen, key)
                    setattr(almacen, key, parametos[key])
                if almacen.save() > 0:
                    return jsonify(almacen.as_dict_without("empresa"))
            except Almacen.DoesNotExist:
                raise AlmacenError("Almacen no existe", status=404)
            except peewee.IntegrityError:
                raise AlmacenError("Error al modificar empresa")
