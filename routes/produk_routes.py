
from flask import Blueprint
from controllers import produk_controller

produk_bp = Blueprint("produk", __name__)


@produk_bp.route("/api/produk", methods=["GET"])
def get_all():
    return produk_controller.get_all()


@produk_bp.route("/api/produk/<string:id_produk>", methods=["GET"])
def get_by_id(id_produk):
    return produk_controller.get_by_id(id_produk)


@produk_bp.route("/api/produk", methods=["POST"])
def create():
    return produk_controller.create()


@produk_bp.route("/api/produk/<string:id_produk>", methods=["PUT"])
def update(id_produk):
    return produk_controller.update(id_produk, partial=False)


@produk_bp.route("/api/produk/<string:id_produk>", methods=["PATCH"])
def patch(id_produk):
    return produk_controller.update(id_produk, partial=True)


@produk_bp.route("/api/produk/<string:id_produk>", methods=["DELETE"])
def delete(id_produk):
    return produk_controller.delete(id_produk)
