
from flask import Blueprint
from controllers import detail_supply_controller

detail_supply_bp = Blueprint(
    "detail_supply",
    __name__,
    url_prefix="/api/detail-supply"
)


@detail_supply_bp.route("/", methods=["GET"])
def get_all_detail_supply():
    return detail_supply_controller.get_all()


@detail_supply_bp.route("/<string:id_detail_supply>", methods=["GET"])
def get_detail_supply_by_id(id_detail_supply):
    return detail_supply_controller.get_by_id(id_detail_supply)


@detail_supply_bp.route("/", methods=["POST"])
def create_detail_supply():
    return detail_supply_controller.create()


@detail_supply_bp.route("/<string:id_detail_supply>", methods=["PUT"])
def update_detail_supply(id_detail_supply):
    return detail_supply_controller.update(id_detail_supply)


@detail_supply_bp.route("/<string:id_detail_supply>", methods=["PATCH"])
def patch_detail_supply(id_detail_supply):
    return detail_supply_controller.patch(id_detail_supply)


@detail_supply_bp.route("/<string:id_detail_supply>", methods=["DELETE"])
def delete_detail_supply(id_detail_supply):
    return detail_supply_controller.delete(id_detail_supply)
