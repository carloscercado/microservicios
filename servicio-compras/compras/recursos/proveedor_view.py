from .base_view import BaseView
from ..database import Proveedor, Producto
from ..excepciones import ProveedorError, CamposInvalidosError
import peewee
#from .validaciones.validaciones import ValidacionProveedor, union_de_errores
from flask import jsonify, g, request


class ProveedoresView(BaseView):

    def index(self):
        with self.conexion.atomic():
            try:
                resultado = Proveedor.select()\
                            .where(Proveedor.empresa == g.empresa)
                res = [obj.as_dict() for obj in resultado]
                return jsonify(res)
            except peewee.IntegrityError:
                raise ProveedorError("Problemas al consultar Proveedores")

    def get(self, _id):
        with self.conexion.atomic():
            try:
                resultado = Proveedor.get(Proveedor.id == _id,
                                          Proveedor.empresa == g.empresa)
                return jsonify(resultado.as_dict())
            except Proveedor.DoesNotExist:
                raise ProveedorError("Proveedor no existe", status=404)

    def delete(self, _id):
        with self.conexion.atomic():
            try:
                resultado = Proveedor.get(Proveedor.id == _id,
                                          Proveedor.empresa == g.empresa)
                if len(Compra.select().where(Compra.proveedor == resultado.id)) > 0:  # noqa E501
                    raise ProveedorError("No puede ser eliminada, existen comrpas a este proveedor")  # noqa E501
                resultado.delete_instance()
                return jsonify({})
            except Proveedor.DoesNotExist:
                raise ProveedorError("Proveedor no existe", status=404)

    """
    def post(self):
        with self.conexion.atomic():
            try:
                datos = request.json
                form = ValidacionProveedor.from_json(datos)
                if not form.validate():
                    errors = union_de_errores(form.errors)
                    raise CamposInvalidosError(errors)

                Proveedor = Proveedor.create(
                    empresa=g.empresa,
                    nombre=datos.get("nombre").upper())
                return jsonify(Proveedor.as_dict()), 201
            except peewee.IntegrityError as e:
                raise ProveedorError("Error al registrar Proveedor")

    def put(self, _id):
        with self.conexion.atomic():
            try:
                datos = request.json
                form = ValidacionProveedor.from_json(datos)
                if not form.validate():
                    errors = union_de_errores(form.errors)
                    raise CamposInvalidosError(errors)
                Proveedor = Proveedor.get(Proveedor.id == _id,
                                          Proveedor.empresa == g.empresa)
                parametos = {
                    "nombre": datos.get("nombre").upper()
                }
                for key in parametos.keys():
                    getattr(Proveedor, key)
                    setattr(Proveedor, key, parametos[key])
                if Proveedor.save() > 0:
                    return jsonify(Proveedor.as_dict())
            except Proveedor.DoesNotExist:
                raise ProveedorError("Proveedor no existe", status=404)
            except peewee.IntegrityError as e:
                raise ProveedorError("Error al modificar Proveedor")
    """