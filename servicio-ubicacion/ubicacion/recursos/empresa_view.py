from flask import jsonify, request, g
from ..database import Empresa
from flask_classy import route
import peewee
from .base_view import BaseView
from ..excepciones import EmpresaError, CamposInvalidosError
from .validaciones.validaciones import ValidacionEmpresa, union_de_errores


class EmpresasView(BaseView):

    def index(self):
        with self.conexion.atomic():
            try:
                resultado = Empresa.select()\
                            .where(Empresa.usuario == g.usuario)
                res = [obj.as_dict_without("usuario") for obj in resultado]
                return jsonify(res)
            except peewee.IntegrityError:
                return EmpresaError("Problemas")

    @route('/mi_empresa', methods=["GET"])
    def mi_empresa(self):
        with self.conexion.atomic():
            try:
                resultado = Empresa.get(Empresa.usuario == g.usuario)
                return jsonify(resultado.as_dict_without("usuario"))
            except Empresa.DoesNotExist:
                raise EmpresaError("Empresa no existe", status=404)

    def post(self):
        with self.conexion.atomic():
            try:
                datos = request.json
                form = ValidacionEmpresa.from_json(datos)
                if not form.validate():
                    errors = union_de_errores(form.errors)
                    raise CamposInvalidosError(errors)
                empresa = Empresa.create(
                    rif=datos.get("rif"),
                    nombre=datos.get("nombre").upper(),
                    telefono=datos.get("telefono"),
                    ciudad=datos.get("ciudad").upper(),
                    usuario=g.usuario,
                    direccion=datos.get("direccion").upper())
                return jsonify(empresa.as_dict_without("usuario")), 201
            except peewee.IntegrityError as e:
                raise EmpresaError("Error al registrar empresa")

    @route('/', methods=["PUT"])
    def modificar(self):
        with self.conexion.atomic():
            try:
                empresa = Empresa.get(Empresa.usuario == g.usuario)
                datos = request.json
                form = ValidacionEmpresa.from_json(datos)
                if not form.validate():
                    errors = union_de_errores(form.errors)
                    raise CamposInvalidosError(errors)
                parametos = {
                    "rif": datos.get("rif"),
                    "nombre": datos.get("nombre").upper(),
                    "telefono": datos.get("telefono"),
                    "ciudad": datos.get("ciudad").upper(),
                    "direccion": datos.get("direccion").upper()
                }
                for key in parametos.keys():
                    getattr(empresa, key)
                    setattr(empresa, key, parametos[key])
                if empresa.save() > 0:
                    return jsonify(empresa.as_dict_without("usuario"))
            except Empresa.DoesNotExist:
                raise EmpresaError("Empresa no existe", status=404)
            except peewee.IntegrityError as e:
                raise EmpresaError("Error al modificar empresa")
