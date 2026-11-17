
from flask import Blueprint
from controllers import users_controller

users_bp = Blueprint("users", __name__)


# =====================================
# GET ALL USERS
# =====================================

@users_bp.route("/api/users", methods=["GET"])
def get_all():
    return users_controller.get_all()


# =====================================
# GET USER BY ID
# =====================================

@users_bp.route("/api/users/<string:id_user>", methods=["GET"])
def get_by_id(id_user):
    return users_controller.get_by_id(id_user)


# =====================================
# CREATE USER (POST)
# =====================================

@users_bp.route("/api/users", methods=["POST"])
def create():
    return users_controller.create()


# =====================================
# UPDATE USER (PUT)
# =====================================

@users_bp.route("/api/users/<string:id_user>", methods=["PUT"])
def update(id_user):
    return users_controller.update(id_user, partial=False)


# =====================================
# PATCH USER
# =====================================

@users_bp.route("/api/users/<string:id_user>", methods=["PATCH"])
def patch(id_user):
    return users_controller.update(id_user, partial=True)


# =====================================
# DELETE USER
# =====================================

@users_bp.route("/api/users/<string:id_user>", methods=["DELETE"])
def delete(id_user):
    return users_controller.delete(id_user)
