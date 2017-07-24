from .base_view import BaseView
from ..database import Categoria, Producto
from ..excepciones import CategoriaError, CamposInvalidosError
import peewee
from .validaciones.validaciones import ValidacionCategoria, union_de_errores
from flask import jsonify, g, request


class CategoriasView(BaseView):

    def index(self):
        with self.conexion.atomic():
            try:
                resultado = Categoria.select()\
                            .where(Categoria.empresa == g.empresa)
                res = [obj.as_dict() for obj in resultado]
                return jsonify(res)
            except peewee.IntegrityError:
                raise CategoriaError("Problemas al consultar categorias")

    def get(self, _id):
        with self.conexion.atomic():
            try:
                resultado = Categoria.get(Categoria.id == _id,
                                          Categoria.empresa == g.empresa)
                return jsonify(resultado.as_dict())
            except Categoria.DoesNotExist:
                raise CategoriaError("Categoria no existe", status=404)

    def delete(self, _id):
        with self.conexion.atomic():
            try:
                resultado = Categoria.get(Categoria.id == _id,
                                          Categoria.empresa == g.empresa)
                if len(Producto.select().where(Producto.categoria == resultado.id)) > 0:  # noqa E501
                    raise CategoriaError("No puede ser eliminada, existen productos usando esta categoria")  # noqa E501
                resultado.delete_instance()
                return jsonify({})
            except Categoria.DoesNotExist:
                raise CategoriaError("Categoria no existe", status=404)

    def post(self):
        with self.conexion.atomic():
            try:
                datos = request.json
                form = ValidacionCategoria.from_json(datos)
                if not form.validate():
                    errors = union_de_errores(form.errors)
                    raise CamposInvalidosError(errors)

                categoria = Categoria.create(
                    empresa=g.empresa,
                    nombre=datos.get("nombre").upper())
                return jsonify(categoria.as_dict()), 201
            except peewee.IntegrityError as e:
                raise CategoriaError("Error al registrar Categoria")

    def put(self, _id):
        with self.conexion.atomic():
            try:
                categoria = Categoria.get(Categoria.id == _id,
                                          Categoria.empresa == g.empresa)
                datos = request.json
                form = ValidacionCategoria.from_json(datos)
                if not form.validate():
                    errors = union_de_errores(form.errors)
                    raise CamposInvalidosError(errors)
                parametos = {
                    "nombre": datos.get("nombre").upper()
                }
                for key in parametos.keys():
                    getattr(categoria, key)
                    setattr(categoria, key, parametos[key])
                if categoria.save() > 0:
                    return jsonify(categoria.as_dict())
            except Categoria.DoesNotExist:
                raise CategoriaError("Categoria no existe", status=404)
            except peewee.IntegrityError as e:
                raise CategoriaError("Error al modificar categoria")
