from flask import Blueprint

from controllers.auth.admin_auth_controller import (
    admin_login,
    create_admin
)

from middleware.api_key import api_key_required


# ==========================================
# BLUEPRINT ADMIN AUTHENTICATION
# ==========================================

admin_auth_bp = Blueprint(
    "admin_auth",
    __name__
)


# ==========================================
# REGISTRASI ADMIN
# ==========================================
# Endpoint:
# POST /api/admin/register
#
# Registrasi admin dilindungi API Key.
# Tidak membutuhkan JWT karena admin belum login.

@admin_auth_bp.route(
    "/api/admin/register",
    methods=["POST"]
)
@api_key_required
def register_admin():
    return create_admin()


# ==========================================
# LOGIN ADMIN
# ==========================================
# Endpoint:
# POST /api/admin/login

@admin_auth_bp.route(
    "/api/admin/login",
    methods=["POST"]
)
def login_admin():
    return admin_login()