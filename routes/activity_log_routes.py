
from flask import Blueprint

from controllers import activity_log_controller

from middleware.jwt_auth import jwt_required
from middleware.admin_required import admin_required


# ==========================================
# BLUEPRINT ACTIVITY LOG
# ==========================================

activity_log_bp = Blueprint(
    "activity_log",
    __name__,
    url_prefix="/api/activity-logs"
)


# ==========================================
# GET SEMUA ACTIVITY LOG
# HANYA ADMIN
# ==========================================

@activity_log_bp.route("", methods=["GET"])
@jwt_required
@admin_required
def get_all_activity_logs():
    return activity_log_controller.get_all()


# ==========================================
# GET ACTIVITY LOG BERDASARKAN USER
# HANYA ADMIN
# ==========================================

@activity_log_bp.route("/user/<id_user>", methods=["GET"])
@jwt_required
@admin_required
def get_activity_logs_by_user(id_user):
    return activity_log_controller.get_by_user(id_user)
