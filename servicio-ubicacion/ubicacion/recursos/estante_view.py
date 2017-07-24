from .base_view import BaseView
from flask import jsonify, g, request
from flask_classy import route
from ..database import Estante, Almacen, Cubiculo
from ..excepciones import EstanteError, CamposInvalidosError
from .validaciones.validaciones import ValidacionEstante, union_de_errores
import peewee


class EstantesView (BaseView):

    def index(self):
        with self.conexion.atomic():
            try:
                resultado = Estante.select()\
                            .where(Estante.empresa == g.empresa)
                res = [obj.as_dict_without("almacen") for obj in resultado]
                return jsonify(res)
            except peewee.IntegrityError:
                raise EstanteError("Problemas con Estantees")

    def get(self, _id):
        with self.conexion.atomic():
            try:
                resultado = Estante.get(Estante.id == _id,
                                        Estante.empresa == g.empresa)
                return jsonify(resultado.as_dict_without("almacen"))
            except Estante.DoesNotExist:
                raise EstanteError("Estante no existe", status=404)

    def delete(self, _id):
        with self.conexion.atomic():
            try:
                resultado = Estante.get(Estante.id == _id,
                                        Estante.empresa == g.empresa)
                if len(Cubiculo.select().where(Cubiculo.estante == resultado.id)) > 0:  # noqa E501
                    raise EstanteError("No puede ser eliminado, aun existen cubiculos registrados dentro de este almacen")  # noqa E501
                resultado.delete_instance()
                return jsonify({})
            except Estante.DoesNotExist:
                raise EstanteError("Estante no existe", status=404)

    @route('/almacen/<int:almacen>', methods=["GET"])
    def por_estante(self, almacen):
        with self.conexion.atomic():
            try:
                resultado = Estante.select()\
                .where(Estante.almacen == almacen, Estante.empresa == g.empresa)  # noqa E501
                res = [obj.as_dict_without("almacen") for obj in resultado]
                return jsonify(res)
            except peewee.IntegrityError:
                raise EstanteError("Problemas con Estantees", status=404)

    def post(self):
        with self.conexion.atomic():
            try:
                datos = request.json
                form = ValidacionEstante.from_json(datos)
                if not form.validate():
                    errors = union_de_errores(form.errors)
                    raise CamposInvalidosError(errors)
                almacen = Almacen.get(Almacen.id == int(datos.get("almacen")),
                                      Almacen.empresa == g.empresa)
                estante = Estante.create(
                    empresa=g.empresa,
                    almacen=almacen.id,
                    nombre=datos.get("nombre").upper(),
                    capacidad=datos.get("capacidad"),
                    capacidad_disponible=datos.get("capacidad"))
                return jsonify(estante.as_dict_without("almacen")), 201
            except Almacen.DoesNotExist:
                raise EstanteError("Almacen no existe", status=400)
            except peewee.IntegrityError as e:
                raise EstanteError("Error al registrar Estante")

    def put(self, _id):
        with self.conexion.atomic():
            try:
                estante = Estante.get(Estante.id == _id,
                                      Estante.empresa == g.empresa)
                datos = request.json
                form = ValidacionEstante.from_json(datos)
                if not form.validate():
                    errors = union_de_errores(form.errors)
                    raise CamposInvalidosError(errors)
                parametos = {
                    "nombre": datos.get("nombre").upper(),
                    "capacidad": datos.get("capacidad")
                }
                for key in parametos.keys():
                    getattr(estante, key)
                    setattr(estante, key, parametos[key])
                if Estante.save() > 0:
                    return jsonify(estante.as_dict_without("almacen"))
            except Estante.DoesNotExist:
                raise EstanteError("Estante no existe", status=404)
            except peewee.IntegrityError as e:
                raise EstanteError("Error al modificar empresa")
