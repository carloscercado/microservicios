from .base_view import BaseView
from ..database import Producto, Categoria
from ..excepciones import ProductoError, CamposInvalidosError
import peewee
from .validaciones.validaciones import ValidacionProducto, union_de_errores
from flask import jsonify, g, request


class ProductosView(BaseView):

    def index(self):
        with self.conexion.atomic():
            try:
                resultado = Producto.select()\
                            .where(Producto.empresa == g.empresa)
                res = [obj.as_dict() for obj in resultado]
                return jsonify(res)
            except peewee.IntegrityError:
                raise ProductoError("Problemas al consultar Productos")

    def get(self, _id):
        with self.conexion.atomic():
            try:
                resultado = Producto.get(Producto.id == _id,
                                         Producto.empresa == g.empresa)
                return jsonify(resultado.as_dict())
            except Producto.DoesNotExist:
                raise ProductoError("Producto no existe", status=404)

    def delete(self, _id):
        with self.conexion.atomic():
            try:
                resultado = Producto.get(Producto.id == _id,
                                         Producto.empresa == g.empresa)
                if len(Producto.select().where(Producto.cantidad != 0)) > 0:
                    raise ProductoError("No puede ser eliminada")
                resultado.delete_instance()
                return jsonify({})
            except Producto.DoesNotExist:
                raise ProductoError("Producto no existe", status=404)

    def post(self):
        with self.conexion.atomic():
            try:
                datos = request.json
                form = ValidacionProducto.from_json(datos)
                if not form.validate():
                    errors = union_de_errores(form.errors)
                    raise CamposInvalidosError(errors)
                categoria = Categoria.get(Categoria.id == datos.get("categoria"),  # noqa E501
                                          Categoria.empresa == g.empresa)
                perecedero = False if datos.get("perecedero").lower()=="false" else True  # noqa E501
                producto = Producto.create(
                    empresa=g.empresa,
                    medida=datos.get("medida").upper(),
                    categoria=categoria.id,
                    perecedero=perecedero,
                    minimo=datos.get("minimo"),
                    nombre=datos.get("nombre").upper())
                return jsonify(producto.as_dict()), 201
            except Categoria.DoesNotExist:
                raise ProductoError("Categoria no existe", status=400)
            except peewee.IntegrityError as e:
                print(e)
                raise ProductoError("Error al registrar Producto")

    def put(self, _id):
        with self.conexion.atomic():
            try:
                producto = Producto.get(Producto.id == _id,
                                        Producto.empresa == g.empresa)
                datos = request.json
                form = ValidacionProducto.from_json(datos)
                if not form.validate():
                    errors = union_de_errores(form.errors)
                    raise CamposInvalidosError(errors)
                categoria = Categoria.get(Categoria.id == datos.get("categoria"),  # noqa E501
                                          Categoria.empresa == g.empresa)
                perecedero = False if datos.get("perecedero").lower()=="false" else True  # noqa E501
                parametos = {
                    "nombre": datos.get("nombre").upper(),
                    "medida": datos.get("medida").upper(),
                    "categoria": categoria.id,
                    "perecedero": perecedero,
                    "minimo": datos.get("minimo")
                }
                for key in parametos.keys():
                    getattr(producto, key)
                    setattr(producto, key, parametos[key])
                if Producto.save() > 0:
                    return jsonify(producto.as_dict())
            except Producto.DoesNotExist:
                raise ProductoError("Producto no existe", status=404)
            except peewee.IntegrityError as e:
                raise ProductoError("Error al modificar Producto")
