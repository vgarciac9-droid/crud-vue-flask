from decimal import Decimal, InvalidOperation

from flask import jsonify, request

from ..errors import error, required
from ..extensions import db
from ..models import Producto
from . import api_bp


def producto_data(data):
    missing = required(data, ["nombre", "precio", "stock"])
    if missing:
        return None, error("Faltan campos obligatorios", details=missing)
    try:
        precio = Decimal(str(data["precio"]))
        stock = int(data["stock"])
    except (InvalidOperation, TypeError, ValueError):
        return None, error("Precio o stock no válidos")
    if not precio.is_finite() or precio < 0 or stock < 0:
        return None, error("Precio y stock deben ser mayores o iguales a cero")
    if precio >= Decimal("100000000"):
        return None, error("El precio es demasiado alto")
    nombre = str(data["nombre"]).strip()
    descripcion = str(data.get("descripcion") or "").strip()
    if not nombre or len(nombre) > 120:
        return None, error("El nombre es obligatorio (máximo 120 caracteres)")
    if len(descripcion) > 300:
        return None, error("La descripción admite máximo 300 caracteres")
    activo = data.get("activo", True)
    if not isinstance(activo, bool):
        return None, error("El campo activo debe ser verdadero o falso")
    return {
        "nombre": nombre,
        "descripcion": descripcion,
        "precio": precio.quantize(Decimal("0.01")),
        "stock": stock,
        "activo": activo,
    }, None


@api_bp.get("/productos")
def listar_productos():
    productos = Producto.query.order_by(Producto.id.desc()).all()
    return jsonify([p.to_dict() for p in productos])


@api_bp.get("/productos/<int:producto_id>")
def obtener_producto(producto_id):
    return jsonify(db.get_or_404(Producto, producto_id).to_dict())


@api_bp.post("/productos")
def crear_producto():
    data, response = producto_data(request.get_json(silent=True) or {})
    if response:
        return response
    producto = Producto(**data)
    db.session.add(producto)
    db.session.commit()
    return jsonify(producto.to_dict()), 201


@api_bp.put("/productos/<int:producto_id>")
def actualizar_producto(producto_id):
    producto = db.get_or_404(Producto, producto_id)
    data, response = producto_data(request.get_json(silent=True) or {})
    if response:
        return response
    for key, value in data.items():
        setattr(producto, key, value)
    db.session.commit()
    return jsonify(producto.to_dict())


@api_bp.delete("/productos/<int:producto_id>")
def eliminar_producto(producto_id):
    producto = db.get_or_404(Producto, producto_id)
    if producto.pedidos:
        return error("No se puede eliminar un producto con pedidos", 409)
    db.session.delete(producto)
    db.session.commit()
    return "", 204
