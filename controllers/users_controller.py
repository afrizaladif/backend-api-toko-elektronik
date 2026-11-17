
from flask import request
from models import users


# =====================================
# FIELD YANG BOLEH DIKIRIM PENGGUNA
# =====================================

FIELDS = {
    "nama_user": 100,
    "email": 100,
    "password": 255,
    "no_telepon": 20
}


# =====================================
# GET ALL USERS
# =====================================

def get_all():
    try:
        data = users.get_all()

        return {
            "message": "Data user berhasil diambil",
            "data": data
        }, 200

    except Exception as e:
        print("ERROR GET ALL USERS:", repr(e))
        return {"message": "Terjadi kesalahan pada server"}, 500


# =====================================
# GET USER BY ID
# =====================================

def get_by_id(id_user):
    try:
        data = users.get_by_id(id_user)

        if data is None:
            return {"message": "User tidak ditemukan"}, 404

        return {
            "message": "Data user berhasil diambil",
            "data": data
        }, 200

    except Exception as e:
        print("ERROR GET USER:", repr(e))
        return {"message": "Terjadi kesalahan pada server"}, 500


# =====================================
# VALIDASI DATA
# =====================================

def validate(data, required_fields):

    if not isinstance(data, dict):
        return "Body harus berupa JSON"

    # Menolak field yang tidak dikenal
    unknown = set(data.keys()) - set(FIELDS.keys())

    if unknown:
        return "Field tidak dikenal: " + ", ".join(sorted(unknown))

    # Memeriksa field wajib
    for field in required_fields:

        value = data.get(field)

        if not isinstance(value, str) or not value.strip():
            return f"{field} wajib diisi dan harus berupa teks"

        if len(value) > FIELDS[field]:
            return f"{field} maksimal {FIELDS[field]} karakter"

    # Validasi format email sederhana
    if "email" in data:
        email = data["email"].strip()

        if "@" not in email or "." not in email.split("@")[-1]:
            return "Format email tidak valid"

    return None


# =====================================
# CREATE USER (POST)
# =====================================

def create():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {"message": "Body harus berupa JSON"}, 400

    # Semua field wajib saat registrasi
    error = validate(data, list(FIELDS.keys()))

    if error:
        return {"message": error}, 400

    try:

        # ID dibuat otomatis oleh model
        # Role otomatis customer
        id_user = users.create({
            field: data[field] for field in FIELDS
        })

        return {
            "message": "User berhasil ditambahkan",
            "data": {
                "id_user": id_user,
                "nama_user": data["nama_user"],
                "email": data["email"],
                "no_telepon": data["no_telepon"],
                "role": "customer"
            }
        }, 201

    except ValueError as e:
        return {"message": str(e)}, 400

    except Exception as e:

        print("ERROR CREATE USER:", repr(e))

        # MySQL duplicate entry
        if getattr(e, "errno", None) == 1062:
            return {"message": "Email sudah digunakan"}, 409

        return {"message": "Gagal menambahkan user"}, 500


# =====================================
# UPDATE USER (PUT & PATCH)
# =====================================

def update(id_user, partial=False):

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {"message": "Body harus berupa JSON"}, 400

    if not data:
        return {"message": "Kirim data yang ingin diperbarui"}, 400

    # PUT wajib mengirim semua field
    # PATCH hanya memvalidasi field yang dikirim
    required_fields = list(data.keys()) if partial else list(FIELDS.keys())

    error = validate(data, required_fields)

    if error:
        return {"message": error}, 400

    try:

        # Memeriksa keberadaan user
        existing = users.get_by_id(id_user)

        if existing is None:
            return {"message": "User tidak ditemukan"}, 404

        if partial:

            # PATCH memperbarui sebagian data
            users.patch(id_user, data)

            result = {
                "id_user": id_user,
                "nama_user": data.get(
                    "nama_user", existing["nama_user"]
                ),
                "email": data.get(
                    "email", existing["email"]
                ),
                "no_telepon": data.get(
                    "no_telepon", existing["no_telepon"]
                )
            }

        else:

            # PUT memperbarui seluruh data
            users.update(id_user, data)

            result = {
                "id_user": id_user,
                "nama_user": data["nama_user"],
                "email": data["email"],
                "no_telepon": data["no_telepon"]
            }

        return {
            "message": "Data user berhasil diperbarui",
            "data": result
        }, 200

    except ValueError as e:
        return {"message": str(e)}, 400

    except Exception as e:

        print("ERROR UPDATE USER:", repr(e))

        if getattr(e, "errno", None) == 1062:
            return {"message": "Email sudah digunakan"}, 409

        return {"message": "Gagal memperbarui data user"}, 500


# =====================================
# DELETE USER
# =====================================

def delete(id_user):

    try:

        existing = users.get_by_id(id_user)

        if existing is None:
            return {"message": "User tidak ditemukan"}, 404

        users.delete(id_user)

        return {
            "message": "User berhasil dihapus"
        }, 200

    except Exception as e:

        print("ERROR DELETE USER:", repr(e))

        if getattr(e, "errno", None) == 1451:
            return {
                "message": "User tidak dapat dihapus karena masih memiliki data terkait"
            }, 409

        return {
            "message": "Terjadi kesalahan saat menghapus user"
        }, 500
