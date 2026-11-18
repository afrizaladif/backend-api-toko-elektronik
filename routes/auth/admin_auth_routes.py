
from flask import Blueprint

from controllers.auth.admin_auth_controller import (
    admin_login,
    create_admin
)

from middleware.api_key import api_key_required


# Membuat Blueprint Admin Authentication
admin_auth_bp = Blueprint("admin_auth", __name__)


# Endpoint Registrasi Admin
@admin_auth_bp.route("/api/admin/register", methods=["POST"])
@api_key_required
def register_admin():
    return create_admin()


# Endpoint Login Admin
@admin_auth_bp.route("/api/admin/login", methods=["POST"])
@api_key_required
def login_admin():
    return admin_login()
