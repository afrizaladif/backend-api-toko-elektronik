
from flask import Blueprint
from controllers import pembelian_controller

pembelian_bp = Blueprint("pembelian", __name__)


@pembelian_bp.route("/api/pembelian", methods=["GET"])
def get_all():
    return pembelian_controller.get_all()


@pembelian_bp.route("/api/pembelian/<string:id_pembelian>", methods=["GET"])
def get_by_id(id_pembelian):
    return pembelian_controller.get_by_id(id_pembelian)


@pembelian_bp.route("/api/pembelian", methods=["POST"])
def create():
    return pembelian_controller.create()


@pembelian_bp.route("/api/pembelian/<string:id_pembelian>", methods=["PUT"])
def update(id_pembelian):
    return pembelian_controller.update(id_pembelian, partial=False)


@pembelian_bp.route("/api/pembelian/<string:id_pembelian>", methods=["PATCH"])
def patch(id_pembelian):
    return pembelian_controller.update(id_pembelian, partial=True)


@pembelian_bp.route("/api/pembelian/<string:id_pembelian>", methods=["DELETE"])
def delete(id_pembelian):
    return pembelian_controller.delete(id_pembelian)
