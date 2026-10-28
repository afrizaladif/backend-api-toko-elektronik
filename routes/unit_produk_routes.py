
from flask import Blueprint
from controllers import unit_produk_controller

unit_produk_bp = Blueprint("unit_produk", __name__)


@unit_produk_bp.route("/api/unit_produk", methods=["GET"])
def get_all():
    return unit_produk_controller.get_all()


@unit_produk_bp.route(
    "/api/unit_produk/<string:kode_serial>",
    methods=["GET"]
)
def get_by_id(kode_serial):
    return unit_produk_controller.get_by_id(kode_serial)


@unit_produk_bp.route("/api/unit_produk", methods=["POST"])
def create():
    return unit_produk_controller.create()


@unit_produk_bp.route(
    "/api/unit_produk/<string:kode_serial>",
    methods=["PUT"]
)
def update(kode_serial):
    return unit_produk_controller.update(
        kode_serial, partial=False
    )


@unit_produk_bp.route(
    "/api/unit_produk/<string:kode_serial>",
    methods=["PATCH"]
)
def patch(kode_serial):
    return unit_produk_controller.update(
        kode_serial, partial=True
    )


@unit_produk_bp.route(
    "/api/unit_produk/<string:kode_serial>",
    methods=["DELETE"]
)
def delete(kode_serial):
    return unit_produk_controller.delete(kode_serial)
