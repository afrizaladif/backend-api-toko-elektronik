
from flask import Blueprint
from controllers import supplier_controller

supplier_bp = Blueprint("supplier", __name__)


@supplier_bp.route("/api/supplier", methods=["GET"])
def get_all():
    return supplier_controller.get_all()


@supplier_bp.route("/api/supplier/<string:id_supplier>", methods=["GET"])
def get_by_id(id_supplier):
    return supplier_controller.get_by_id(id_supplier)


@supplier_bp.route("/api/supplier", methods=["POST"])
def create():
    return supplier_controller.create()


@supplier_bp.route("/api/supplier/<string:id_supplier>", methods=["PUT"])
def update(id_supplier):
    return supplier_controller.update(id_supplier, partial=False)


@supplier_bp.route("/api/supplier/<string:id_supplier>", methods=["PATCH"])
def patch(id_supplier):
    return supplier_controller.update(id_supplier, partial=True)


@supplier_bp.route("/api/supplier/<string:id_supplier>", methods=["DELETE"])
def delete(id_supplier):
    return supplier_controller.delete(id_supplier)
