from .base_view import BaseView
from flask import jsonify, g, request
from flask_classy import route
from ..database import Cubiculo, Estante
from ..excepciones import CubiculoError, CamposInvalidosError
from .validaciones.validaciones import ValidacionCubiculo, union_de_errores
import peewee


class CubiculosView (BaseView):

    def index(self):
        with self.conexion.atomic():
            try:
                resultado = Cubiculo.select()\
                            .where(Cubiculo.empresa == g.empresa)
                res = [obj.as_dict_without("estante") for obj in resultado]
                return jsonify(res)
            except peewee.IntegrityError:
                raise CubiculoError("Problemas con Cubiculos")

    def get(self, _id):
        with self.conexion.atomic():
            try:
                resultado = Cubiculo.get(Cubiculo.id == _id,
                                         Cubiculo.empresa == g.empresa)
                return jsonify(resultado.as_dict_without("estante"))
            except Cubiculo.DoesNotExist:
                raise CubiculoError("Cubiculo no existe", status=404)

    def delete(self, _id):
        with self.conexion.atomic():
            try:
                resultado = Cubiculo.get(Cubiculo.id == _id,
                                         Cubiculo.empresa == g.empresa,
                                         Cubiculo.estado)
                resultado.delete_instance()
                return jsonify({})
            except Cubiculo.DoesNotExist:
                raise CubiculoError("Cubiculo no existe", status=404)

    @route('/estante/<int:estante>', methods=["GET"])
    def por_Cubiculo(self, estante):
        with self.conexion.atomic():
            try:
                resultado = Cubiculo.select()\
                            .where(Cubiculo.estante == estante,
                                   Cubiculo.empresa == g.empresa)
                res = [obj.as_dict_without("estante") for obj in resultado]
                return jsonify(res)
            except peewee.IntegrityError:
                raise CubiculoError("Problemas con Cubiculoes", status=404)

    def post(self):
        with self.conexion.atomic():
            try:
                datos = request.json
                form = ValidacionCubiculo.from_json(datos)
                if not form.validate():
                    errors = union_de_errores(form.errors)
                    raise CamposInvalidosError(errors)
                estante = Estante.get(Estante.id == int(datos.get("estante")),
                                      Estante.empresa == g.empresa)
                cubiculo = Cubiculo.create(
                    empresa=g.empresa,
                    estante=estante.id,
                    nombre=datos.get("nombre").upper(),
                    capacidad=datos.get("capacidad"),
                    capacidad_disponible=datos.get("capacidad"))
                return jsonify(cubiculo.as_dict_without("estante")), 201
            except Estante.DoesNotExist:
                raise CubiculoError("Estante no existe", status=400)
            except peewee.IntegrityError as e:
                raise CubiculoError("Error al registrar Cubiculo")

    def put(self, _id):
        with self.conexion.atomic():
            try:
                datos = request.json
                form = ValidacionCubiculo.from_json(datos)
                if not form.validate():
                    errors = union_de_errores(form.errors)
                    raise CamposInvalidosError(errors)
                cubiculo = Cubiculo.get(Cubiculo.id == _id,
                                        Cubiculo.empresa == g.empresa)
                parametos = {
                    "nombre": datos.get("nombre").upper(),
                    "capacidad": datos.get("capacidad")
                }
                for key in parametos.keys():
                    getattr(cubiculo, key)
                    setattr(cubiculo, key, parametos[key])
                if Cubiculo.save() > 0:
                    return jsonify(Cubiculo.as_dict_without("estante"))
            except Cubiculo.DoesNotExist:
                raise CubiculoError("Cubiculo no existe", status=404)
            except peewee.IntegrityError as e:
                raise CubiculoError("Error al modificar empresa")
