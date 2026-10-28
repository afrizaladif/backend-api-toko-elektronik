
from flask import Blueprint
from controllers import detail_pembelian_controller

detail_pembelian_bp = Blueprint("detail_pembelian", __name__)


@detail_pembelian_bp.route("/api/detail_pembelian", methods=["GET"])
def get_all():
    return detail_pembelian_controller.get_all()


@detail_pembelian_bp.route(
    "/api/detail_pembelian/<string:id_detail_pembelian>",
    methods=["GET"]
)
def get_by_id(id_detail_pembelian):
    return detail_pembelian_controller.get_by_id(id_detail_pembelian)


@detail_pembelian_bp.route("/api/detail_pembelian", methods=["POST"])
def create():
    return detail_pembelian_controller.create()


@detail_pembelian_bp.route(
    "/api/detail_pembelian/<string:id_detail_pembelian>",
    methods=["PUT"]
)
def update(id_detail_pembelian):
    return detail_pembelian_controller.update(
        id_detail_pembelian, partial=False
    )


@detail_pembelian_bp.route(
    "/api/detail_pembelian/<string:id_detail_pembelian>",
    methods=["PATCH"]
)
def patch(id_detail_pembelian):
    return detail_pembelian_controller.update(
        id_detail_pembelian, partial=True
    )


@detail_pembelian_bp.route(
    "/api/detail_pembelian/<string:id_detail_pembelian>",
    methods=["DELETE"]
)
def delete(id_detail_pembelian):
    return detail_pembelian_controller.delete(id_detail_pembelian)
