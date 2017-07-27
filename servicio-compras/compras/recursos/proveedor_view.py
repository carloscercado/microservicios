from .base_view import BaseView
from ..database import Proveedor
from ..excepciones import ProveedorError, CamposInvalidosError
import peewee
from .validaciones.validaciones import ValidacionProveedor, union_de_errores
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

    def post(self):
        with self.conexion.atomic():
            try:
                datos = request.json
                form = ValidacionProveedor.from_json(datos)
                if not form.validate():
                    errors = union_de_errores(form.errors)
                    raise CamposInvalidosError(errors)

                resultado = Proveedor.select().where(Proveedor.rif ==
                                                     datos.get("rif"))
                if len(resultado) > 0:
                    raise ProveedorError("Ya existe un proveedor con ese RIF registrado")  # noqa E501

                proveedor = Proveedor.create(
                    rif=datos.get("rif"),
                    correo=datos.get("correo").upper(),
                    telefono=datos.get("telefono"),
                    descripcion=datos.get("descripcion").upper(),
                    empresa=g.empresa,
                    nombre=datos.get("nombre").upper())
                return jsonify(proveedor.as_dict()), 201
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
                proveedor = Proveedor.get(Proveedor.id == _id,
                                          Proveedor.empresa == g.empresa)
                parametos = {
                    "nombre": datos.get("nombre").upper(),
                    "descripcion": datos.get("descripcion").upper(),
                    "telefono": datos.get("telefono"),
                    "correo": datos.get("correo").upper()
                }
                for key in parametos.keys():
                    getattr(proveedor, key)
                    setattr(proveedor, key, parametos[key])
                if proveedor.save() > 0:
                    return jsonify(proveedor.as_dict())
            except Proveedor.DoesNotExist:
                raise ProveedorError("Proveedor no existe", status=404)
            except peewee.IntegrityError as e:
                raise ProveedorError("Error al modificar Proveedor")
