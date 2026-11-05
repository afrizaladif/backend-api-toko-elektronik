
from flask import request
from models import customer


# Field yang dapat dikirim pengguna
FIELDS = {
    "nama_customer": 50,
    "email_customer": 50,
    "password": 50,
    "no_telpon_customer": 50
}


# ==============================
# GET ALL CUSTOMER
# ==============================
def get_all():
    try:
        data = customer.get_all()

        return {
            "message": "Data customer berhasil diambil",
            "data": data
        }, 200

    except Exception as e:
        print("ERROR GET ALL CUSTOMER:", repr(e))
        return {"message": "Terjadi kesalahan pada server"}, 500


# ==============================
# GET CUSTOMER BY ID
# ==============================
def get_by_id(id_customer):
    try:
        data = customer.get_by_id(id_customer)

        if data is None:
            return {"message": "Customer tidak ditemukan"}, 404

        return {
            "message": "Data customer berhasil diambil",
            "data": data
        }, 200

    except Exception as e:
        print("ERROR GET CUSTOMER:", repr(e))
        return {"message": "Terjadi kesalahan pada server"}, 500


# ==============================
# VALIDASI DATA
# ==============================
def validate(data, required_fields):
    if not isinstance(data, dict):
        return "Body harus berupa JSON"

    # Menolak field yang tidak dikenal
    # id_customer dibuat otomatis oleh sistem
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

    return None


# ==============================
# CREATE CUSTOMER (POST)
# ==============================
def create():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {"message": "Body harus berupa JSON"}, 400

    error = validate(data, list(FIELDS))

    if error:
        return {"message": error}, 400

    try:
        # ID dibuat otomatis oleh model
        id_customer = customer.create({
            field: data[field] for field in FIELDS
        })

        return {
            "message": "Customer berhasil ditambahkan",
            "data": {
                "id_customer": id_customer,
                "nama_customer": data["nama_customer"],
                "email_customer": data["email_customer"],
                "no_telpon_customer": data["no_telpon_customer"]
            }
        }, 201

    except ValueError as e:
        return {"message": str(e)}, 400

    except Exception as e:
        print("ERROR CREATE CUSTOMER:", repr(e))
        return {"message": "Gagal menambahkan customer"}, 500


# ==============================
# UPDATE CUSTOMER (PUT & PATCH)
# ==============================
def update(id_customer, partial=False):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {"message": "Body harus berupa JSON"}, 400

    if "id_customer" in data:
        return {"message": "id_customer tidak boleh diubah"}, 400

    if partial and not data:
        return {"message": "Kirim field yang ingin diubah"}, 400

    # PUT wajib mengirim semua field
    # PATCH hanya memvalidasi field yang dikirim
    required_fields = list(data.keys()) if partial else list(FIELDS.keys())

    error = validate(data, required_fields)

    if error:
        return {"message": error}, 400

    try:
        existing = customer.get_by_id(id_customer)

        if existing is None:
            return {"message": "Customer tidak ditemukan"}, 404

        if partial:
            customer.patch(id_customer, data)

            # Menggabungkan data lama dan data baru
            result = {
                "id_customer": id_customer,
                "nama_customer": data.get(
                    "nama_customer", existing["nama_customer"]
                ),
                "email_customer": data.get(
                    "email_customer", existing["email_customer"]
                ),
                "no_telpon_customer": data.get(
                    "no_telpon_customer",
                    existing["no_telpon_customer"]
                )
            }

        else:
            customer.update(id_customer, data)

            result = {
                "id_customer": id_customer,
                "nama_customer": data["nama_customer"],
                "email_customer": data["email_customer"],
                "no_telpon_customer": data["no_telpon_customer"]
            }

        return {
            "message": "Data customer berhasil diperbarui",
            "data": result
        }, 200

    except ValueError as e:
        return {"message": str(e)}, 400

    except Exception as e:
        print("ERROR UPDATE CUSTOMER:", repr(e))
        return {"message": "Gagal memperbarui data customer"}, 500


# ==============================
# DELETE CUSTOMER
# ==============================
def delete(id_customer):
    try:
        existing = customer.get_by_id(id_customer)

        if existing is None:
            return {"message": "Customer tidak ditemukan"}, 404

        customer.delete(id_customer)

        return {
            "message": "Customer berhasil dihapus"
        }, 200

    except Exception as e:
        print("ERROR DELETE CUSTOMER:", repr(e))
        return {
            "message": "Terjadi kesalahan saat menghapus customer"
        }, 500
