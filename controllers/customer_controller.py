
from flask import request
from models import customer


FIELDS = {
    "nama_customer": 50,
    "email_customer": 50,
    "password": 50,
    "no_telpon_customer": 50
}


def get_all():
    return {
        "message": "Data customer berhasil diambil",
        "data": customer.get_all()
    }, 200


def get_by_id(id_customer):
    data = customer.get_by_id(id_customer)

    if data is None:
        return {"message": "Customer tidak ditemukan"}, 404

    return {"data": data}, 200


def validate(data, required_fields):
    if not isinstance(data, dict):
        return "Body harus berupa JSON"

    unknown = set(data) - set(FIELDS) - {"id_customer"}
    if unknown:
        return "Field tidak dikenal: " + ", ".join(sorted(unknown))

    for field in required_fields:
        value = data.get(field)

        if not isinstance(value, str) or not value.strip():
            return f"{field} wajib diisi dan harus berupa teks"

        if len(value) > FIELDS[field]:
            return f"{field} maksimal {FIELDS[field]} karakter"

    return None


def create():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {"message": "Body harus berupa JSON"}, 400

    id_customer = data.get("id_customer")

    if not isinstance(id_customer, str) or not id_customer.strip():
        return {"message": "id_customer wajib diisi"}, 400

    if len(id_customer) > 20:
        return {"message": "id_customer maksimal 20 karakter"}, 400

    error = validate(data, list(FIELDS))
    if error:
        return {"message": error}, 400

    if customer.get_by_id(id_customer):
        return {"message": "ID customer sudah digunakan"}, 409

    customer.create({
        "id_customer": id_customer,
        **{field: data[field] for field in FIELDS}
    })

    return {"message": "Customer berhasil ditambahkan"}, 201


def update(id_customer, partial=False):
    existing = customer.get_by_id(id_customer)

    if existing is None:
        return {"message": "Customer tidak ditemukan"}, 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {"message": "Body harus berupa JSON"}, 400

    if "id_customer" in data:
        return {"message": "id_customer tidak boleh diubah"}, 400

    if partial:
        if not data:
            return {"message": "Kirim field yang ingin diubah"}, 400

        error = validate(data, list(data))
        if error:
            return {"message": error}, 400

        merged = {
            field: data.get(field, existing[field])
            for field in FIELDS
        }
        customer.patch(id_customer, data)
    else:
        error = validate(data, list(FIELDS))
        if error:
            return {"message": error}, 400

        merged = {field: data[field] for field in FIELDS}
        customer.update(id_customer, merged)

    return {
        "message": "Data customer berhasil diperbarui",
        "data": {"id_customer": id_customer, **merged}
    }, 200


def delete(id_customer):
    if customer.get_by_id(id_customer) is None:
        return {"message": "Customer tidak ditemukan"}, 404

    try:
        customer.delete(id_customer)
    except Exception:
        return {
            "message": "Customer tidak dapat dihapus karena mungkin masih memiliki transaksi"
        }, 409

    return {"message": "Customer berhasil dihapus"}, 200
