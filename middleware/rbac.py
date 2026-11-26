
from functools import wraps
from flask import jsonify, g


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        # Mengambil payload user dari JWT
        current_user = getattr(g, "current_user", None)

        if not isinstance(current_user, dict):
            return jsonify({
                "status": "error",
                "message": "User tidak terautentikasi"
            }), 401

        # Mengambil role dari payload JWT
        user_role = current_user.get("role")

        # Memastikan hanya admin yang dapat mengakses
        if not user_role or user_role.lower() != "admin":
            return jsonify({
                "status": "error",
                "message": "Akses ditolak: hanya admin yang diizinkan"
            }), 403

        return f(*args, **kwargs)

    return decorated
