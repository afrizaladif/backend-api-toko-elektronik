
from flask import Blueprint
from controllers import kategori_controller

kategori_bp = Blueprint("kategori", __name__)


@kategori_bp.route("/api/kategori", methods=["GET"])
def get_all():
    return kategori_controller.get_all()


@kategori_bp.route("/api/kategori/<string:id_kategori>", methods=["GET"])
def get_by_id(id_kategori):
    return kategori_controller.get_by_id(id_kategori)


@kategori_bp.route("/api/kategori", methods=["POST"])
def create():
    return kategori_controller.create()


@kategori_bp.route("/api/kategori/<string:id_kategori>", methods=["PUT"])
def update(id_kategori):
    return kategori_controller.update(id_kategori, partial=False)


@kategori_bp.route("/api/kategori/<string:id_kategori>", methods=["PATCH"])
def patch(id_kategori):
    return kategori_controller.update(id_kategori, partial=True)


@kategori_bp.route("/api/kategori/<string:id_kategori>", methods=["DELETE"])
def delete(id_kategori):
    return kategori_controller.delete(id_kategori)
