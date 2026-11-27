
from flask import jsonify

from models import activity_log


# ==========================================
# MENGAMBIL SEMUA ACTIVITY LOG
# ==========================================

def get_all():
    try:
        data = activity_log.get_all()

        return jsonify({
            "status": "success",
            "pesan": "Data activity log berhasil diambil",
            "jumlah": len(data),
            "data": data
        }), 200

    except Exception:
        return jsonify({
            "status": "error",
            "pesan": "Gagal mengambil data activity log"
        }), 500


# ==========================================
# MENGAMBIL ACTIVITY LOG BERDASARKAN USER
# ==========================================

def get_by_user(id_user):
    try:
        data = activity_log.get_by_user(id_user)

        return jsonify({
            "status": "success",
            "pesan": "Data activity log pengguna berhasil diambil",
            "jumlah": len(data),
            "data": data
        }), 200

    except Exception:
        return jsonify({
            "status": "error",
            "pesan": "Gagal mengambil activity log pengguna"
        }), 500
