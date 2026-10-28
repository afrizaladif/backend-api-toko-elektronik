
from flask import Blueprint
from controllers import customer_controller

customer_bp = Blueprint("customer", __name__)


@customer_bp.route("/api/customer", methods=["GET"])
def get_all():
    return customer_controller.get_all()


@customer_bp.route("/api/customer/<string:id_customer>", methods=["GET"])
def get_by_id(id_customer):
    return customer_controller.get_by_id(id_customer)


@customer_bp.route("/api/customer", methods=["POST"])
def create():
    return customer_controller.create()


@customer_bp.route("/api/customer/<string:id_customer>", methods=["PUT"])
def update(id_customer):
    return customer_controller.update(id_customer, partial=False)


@customer_bp.route("/api/customer/<string:id_customer>", methods=["PATCH"])
def patch(id_customer):
    return customer_controller.update(id_customer, partial=True)


@customer_bp.route("/api/customer/<string:id_customer>", methods=["DELETE"])
def delete(id_customer):
    return customer_controller.delete(id_customer)
