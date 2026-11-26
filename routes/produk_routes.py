
from flask import Blueprint

from controllers import produk_controller
from middleware.jwt_auth import jwt_required
from middleware.rbac import admin_required


produk_bp = Blueprint("produk", __name__)


# GET semua produk
# Admin dan Customer: JWT
@produk_bp.route("/api/produk", methods=["GET"])
@jwt_required
def get_all():
    return produk_controller.get_all()


# GET produk berdasarkan ID
# Admin dan Customer: JWT
@produk_bp.route("/api/produk/<string:id_produk>", methods=["GET"])
@jwt_required
def get_by_id(id_produk):
    return produk_controller.get_by_id(id_produk)


# POST tambah produk
# Admin: JWT + Role Admin
@produk_bp.route("/api/produk", methods=["POST"])
@jwt_required
@admin_required
def create():
    return produk_controller.create()


# PUT update produk
# Admin: JWT + Role Admin
@produk_bp.route("/api/produk/<string:id_produk>", methods=["PUT"])
@jwt_required
@admin_required
def update(id_produk):
    return produk_controller.update(
        id_produk,
        partial=False
    )


# PATCH update sebagian produk
# Admin: JWT + Role Admin
@produk_bp.route("/api/produk/<string:id_produk>", methods=["PATCH"])
@jwt_required
@admin_required
def patch(id_produk):
    return produk_controller.update(
        id_produk,
        partial=True
    )


# DELETE produk
# Admin: JWT + Role Admin
@produk_bp.route("/api/produk/<string:id_produk>", methods=["DELETE"])
@jwt_required
@admin_required
def delete(id_produk):
    return produk_controller.delete(id_produk)
