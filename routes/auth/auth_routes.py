from flask import Blueprint
from controllers.auth.auth_controller import login
from middleware.api_key import api_key_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
@api_key_required
def login_route():
    return login()