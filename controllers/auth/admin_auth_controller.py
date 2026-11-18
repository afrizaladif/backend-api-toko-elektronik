
from flask import jsonify, request
from models import users


def admin_login():
    return jsonify({
        "status": "success",
        "message": "Autentikasi admin berhasil",
        "role": "admin"
    }), 200

def create_admin():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "status": "error",
            "message": "Request harus berupa JSON"
        }), 400

    required_fields = [
        "nama_user",
        "email",
        "password",
        "no_telepon"
    ]

    if not all(data.get(field) for field in required_fields):
        return jsonify({
            "status": "error",
            "message": "Semua field wajib diisi"
        }), 400

    try:
        admin_id = users.create_admin(data)

        return jsonify({
            "status": "success",
            "message": "Data admin berhasil ditambahkan",
            "id_user": admin_id
        }), 201

    except ValueError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400
