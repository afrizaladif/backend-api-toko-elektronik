from functools import wraps
from flask import jsonify, g

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_user = getattr(g, "current_user", None)

        # Pastikan pengguna sudah terautentikasi
        if not current_user:
            return jsonify({
                "status": "error",
                "pesan": "Silakan login terlebih dahulu"
            }), 401

        # Ambil role dari payload JWT
        role = current_user.get("role")

        # Pastikan hanya admin yang boleh mengakses
        if role != "admin":
            return jsonify({
                "status": "error",
                "pesan": "Akses ditolak. Hanya admin yang boleh mengakses"
            }), 403

        return func(*args, **kwargs)

    return wrapper