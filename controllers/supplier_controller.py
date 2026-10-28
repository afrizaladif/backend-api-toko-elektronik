
from flask import request
from models import supplier


FIELDS = {
    "nama_supplier": 50,
    "alamat_supplier": 50,
    "no_telpon_supplier": 50
}


def get_all():
    try:
        return {
            "message": "Data supplier berhasil diambil",
            "data": supplier.get_all()
        }, 200
    except Exception:
        return {"message": "Gagal mengambil data supplier"}, 500


def get_by_id(id_supplier):
    try:
        data = supplier.get_by_id(id_supplier)

        if data is None:
            return {"message": "Supplier tidak ditemukan"}, 404

        return {"data": data}, 200
    except Exception:
        return {"message": "Gagal mengambil data supplier"}, 500


def validate(data, required_fields):
    if not isinstance(data, dict):
        return "Body harus berupa JSON"

    unknown = set(data) - set(FIELDS) - {"id_supplier"}

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

    id_supplier = data.get("id_supplier")

    if not isinstance(id_supplier, str) or not id_supplier.strip():
        return {"message": "id_supplier wajib diisi"}, 400

    if len(id_supplier) > 20:
        return {"message": "id_supplier maksimal 20 karakter"}, 400

    error = validate(data, list(FIELDS))

    if error:
        return {"message": error}, 400

    try:
        if supplier.get_by_id(id_supplier):
            return {"message": "ID supplier sudah digunakan"}, 409

        supplier.create({
            "id_supplier": id_supplier,
            **{field: data[field] for field in FIELDS}
        })

        return {"message": "Supplier berhasil ditambahkan"}, 201

    except Exception:
        return {"message": "Gagal menambahkan supplier"}, 400


def update(id_supplier, partial=False):
    try:
        existing = supplier.get_by_id(id_supplier)
    except Exception:
        return {"message": "Gagal mengambil data supplier"}, 500

    if existing is None:
        return {"message": "Supplier tidak ditemukan"}, 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {"message": "Body harus berupa JSON"}, 400

    if "id_supplier" in data:
        return {"message": "id_supplier tidak boleh diubah"}, 400

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

        supplier.patch(id_supplier, data)

    else:
        error = validate(data, list(FIELDS))

        if error:
            return {"message": error}, 400

        merged = {field: data[field] for field in FIELDS}
        supplier.update(id_supplier, merged)

    return {
        "message": "Supplier berhasil diperbarui",
        "data": {"id_supplier": id_supplier, **merged}
    }, 200


def delete(id_supplier):
    try:
        if supplier.get_by_id(id_supplier) is None:
            return {"message": "Supplier tidak ditemukan"}, 404

        supplier.delete(id_supplier)

        return {"message": "Supplier berhasil dihapus"}, 200

    except Exception:
        return {
            "message": "Supplier tidak dapat dihapus karena mungkin masih digunakan oleh tabel supply."
        }, 409
