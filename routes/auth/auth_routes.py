from flask import Blueprint
from controllers.auth.auth_controller import login

auth_bp = Blueprint("auth", __name__)


# Login Customer
@auth_bp.route("/login", methods=["POST"])
def login_route():
    return login()