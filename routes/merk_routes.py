
from flask import Blueprint
from controllers import merk_controller

merk_bp = Blueprint(
    "merk",
    __name__,
    url_prefix="/api/merk"
)


# GET: Mengambil semua data merk
@merk_bp.route("", methods=["GET"])
@merk_bp.route("/", methods=["GET"])
def get_all_merk():
    return merk_controller.get_all()


# GET: Mengambil merk berdasarkan ID
@merk_bp.route("/<string:id_merk>", methods=["GET"])
def get_merk_by_id(id_merk):
    return merk_controller.get_by_id(id_merk)


# POST: Menambahkan merk
@merk_bp.route("", methods=["POST"])
@merk_bp.route("/", methods=["POST"])
def create_merk():
    return merk_controller.create()


# PUT: Mengubah data merk
@merk_bp.route("/<string:id_merk>", methods=["PUT"])
def update_merk(id_merk):
    return merk_controller.update(id_merk)


# PATCH: Mengubah sebagian data merk
@merk_bp.route("/<string:id_merk>", methods=["PATCH"])
def patch_merk(id_merk):
    return merk_controller.patch(id_merk)


# DELETE: Menghapus merk
@merk_bp.route("/<string:id_merk>", methods=["DELETE"])
def delete_merk(id_merk):
    return merk_controller.delete(id_merk)
