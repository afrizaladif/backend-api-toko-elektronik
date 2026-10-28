
from flask import Blueprint
from controllers import supply_controller

supply_bp = Blueprint("supply", __name__)


@supply_bp.route("/api/supply", methods=["GET"])
def get_all():
    return supply_controller.get_all()


@supply_bp.route("/api/supply/<string:id_supply>", methods=["GET"])
def get_by_id(id_supply):
    return supply_controller.get_by_id(id_supply)


@supply_bp.route("/api/supply", methods=["POST"])
def create():
    return supply_controller.create()


@supply_bp.route("/api/supply/<string:id_supply>", methods=["PUT"])
def update(id_supply):
    return supply_controller.update(id_supply, partial=False)


@supply_bp.route("/api/supply/<string:id_supply>", methods=["PATCH"])
def patch(id_supply):
    return supply_controller.update(id_supply, partial=True)


@supply_bp.route("/api/supply/<string:id_supply>", methods=["DELETE"])
def delete(id_supply):
    return supply_controller.delete(id_supply)
