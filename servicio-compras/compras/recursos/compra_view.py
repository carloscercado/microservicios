from .base_view import BaseView
from ..database import Compra, DetalleCompra, Proveedor, Producto
from ..excepciones import CompraError, CamposInvalidosError
import peewee
from .validaciones.validaciones import ValidacionCompra, ValidacionDetalleCompra,  union_de_errores  # noqa E501
from flask import jsonify, g, request
from datetime import datetime
import decimal


class ComprasView(BaseView):

    def index(self):
        with self.conexion.atomic():
            try:
                resultado = Compra.select()\
                            .where(Compra.empresa == g.empresa)\
                            .order_by(Compra.fecha)
                res = [obj.as_dict() for obj in resultado]
                return jsonify(res)
            except peewee.IntegrityError:
                raise CompraError("Problemas al consultar Compras")

    def get(self, _id):
        with self.conexion.atomic():
            try:
                resultado = Compra.get(Compra.id == _id,
                                       Compra.empresa == g.empresa)
                detalles = DetalleCompra.select()\
                                        .where(DetalleCompra.compra ==
                                               resultado.id)
                resultado = resultado.as_dict()
                resultado["detalles"] = [obj.as_dict() for obj in detalles]
                return jsonify(resultado)
            except Compra.DoesNotExist:
                raise CompraError("Compra no existe", status=404)

    def delete(self, _id):
        with self.conexion.atomic():
            try:
                resultado = Compra.get(Compra.id == _id,
                                       Compra.empresa == g.empresa)
                if len(DetalleCompra.select().where(DetalleCompra.compra == resultado.id)) > 0:  # noqa E501
                    raise CompraError("No puede ser eliminada, existen DetalleCompras usando esta Compra")  # noqa E501
                resultado.delete_instance()
                return jsonify({})
            except Compra.DoesNotExist:
                raise CompraError("Compra no existe", status=404)

    def post(self):
        with self.conexion.atomic():
            try:
                datos = request.json
                form = ValidacionCompra.from_json(datos)
                if not form.validate():
                    errors = union_de_errores(form.errors)
                    raise CamposInvalidosError(errors)

                if type(datos.get("detalles")) != list:
                    raise CompraError("Son necesarios los articulos comprados")  # noqa E501

                detalles = self.validar_detalles(datos.get("detalles"))
                proveedor = Proveedor.get(Proveedor.id ==
                                          datos.get("proveedor"))
                compra = Compra.create(
                    empresa=g.empresa,
                    factura=datos.get("factura").upper(),
                    proveedor=proveedor.id,
                    fecha=datos.get("fecha")
                )
                detalles, total, productos = self.registrar_detalles(detalles, compra.id)  # noqa E501
                compra.total = total
                compra.productos = productos
                compra.save()
                compra = compra.as_dict()
                compra["detalles"] = detalles
                return jsonify(compra), 201
            except Proveedor.DoesNotExist:
                raise CompraError("Proveedor no existe", status=400)
            except Producto.DoesNotExist:
                raise CompraError("producto no existe", status=400)
            except peewee.IntegrityError as e:
                raise CompraError("Error al registrar Compra")
            except KeyError:
                raise CompraError("Hay campos adicionales en los detalles")

    def validar_detalles(self, detalles):
        for detalle in detalles:
            form = ValidacionDetalleCompra.from_json(detalle)
            if not form.validate():
                errors = union_de_errores(form.errors)
                raise CamposInvalidosError(errors)
            producto = Producto.get(Producto.id == detalle.get("producto"))
            cantidad = decimal.Decimal(detalle.get("cantidad"))
            costo = decimal.Decimal(detalle.get("costo"))
            detalle["total"] = (cantidad * costo)
        return detalles

    def registrar_detalles(self, detalles, compra):
        salida = list()
        suma = 0
        productos = 0
        for detalle in detalles:
            detalle["compra"] = compra
            res = DetalleCompra.create(**detalle)
            suma = suma + detalle["total"]
            productos = productos + detalle["cantidad"]
            salida.append(res.as_dict())
        return salida, suma, productos

    """
    def put(self, _id):
        with self.conexion.atomic():
            try:
                datos = request.json
                form = ValidacionCompra.from_json(datos)
                if not form.validate():
                    errors = union_de_errores(form.errors)
                    raise CamposInvalidosError(errors)
                Compra = Compra.get(Compra.id == _id,
                                          Compra.empresa == g.empresa)
                parametos = {
                    "nombre": datos.get("nombre").upper()
                }
                for key in parametos.keys():
                    getattr(Compra, key)
                    setattr(Compra, key, parametos[key])
                if Compra.save() > 0:
                    return jsonify(Compra.as_dict())
            except Compra.DoesNotExist:
                raise CompraError("Compra no existe", status=404)
            except peewee.IntegrityError as e:
                raise CompraError("Error al modificar Compra")
    """
