
from datetime import datetime
from flask import request
from models import supply


EDITABLE_FIELDS = {
    "id_supplier",
    "tanggal_supply"
}


def get_all():
    try:
        return {
            "message": "Data supply berhasil diambil",
            "data": supply.get_all()
        }, 200
    except Exception:
        return {"message": "Gagal mengambil data supply"}, 500


def get_by_id(id_supply):
    try:
        data = supply.get_by_id(id_supply)

        if data is None:
            return {"message": "Data supply tidak ditemukan"}, 404

        return {"data": data}, 200
    except Exception:
        return {"message": "Gagal mengambil data supply"}, 500


def validate(data, partial=False):
    if not isinstance(data, dict):
        return "Body harus berupa JSON"

    if "id_supply" in data:
        return "id_supply tidak boleh diubah"

    unknown = set(data) - EDITABLE_FIELDS

    if unknown:
        return "Field tidak dikenal: " + ", ".join(sorted(unknown))

    if not partial:
        missing = EDITABLE_FIELDS - set(data)

        if missing:
            return "Field wajib dikirim: " + ", ".join(sorted(missing))

    elif not data:
        return "Kirim minimal satu field yang ingin diubah"

    if "id_supplier" in data:
        value = data["id_supplier"]

        if not isinstance(value, str) or not value.strip():
            return "id_supplier wajib berupa teks yang tidak kosong"

        if len(value) > 20:
            return "id_supplier maksimal 20 karakter"

    if "tanggal_supply" in data:
        value = data["tanggal_supply"]

        if not isinstance(value, str):
            return "tanggal_supply harus berupa teks tanggal/waktu"

        try:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return "Format tanggal harus YYYY-MM-DD HH:MM:SS"

    return None


def create():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {"message": "Body harus berupa JSON"}, 400

    id_supply = data.get("id_supply")

    if not isinstance(id_supply, str) or not id_supply.strip():
        return {"message": "id_supply wajib diisi"}, 400

    if len(id_supply) > 20:
        return {"message": "id_supply maksimal 20 karakter"}, 400

    error = validate(data)

    if error:
        return {"message": error}, 400

    try:
        if supply.get_by_id(id_supply):
            return {"message": "ID supply sudah digunakan"}, 409

        supply.create(data)

        return {"message": "Data supply berhasil ditambahkan"}, 201

    except Exception:
        return {
            "message": "Gagal menambahkan supply. Periksa id_supplier dan format tanggal."
        }, 400


def update(id_supply, partial=False):
    try:
        existing = supply.get_by_id(id_supply)
    except Exception:
        return {"message": "Gagal mengambil data supply"}, 500

    if existing is None:
        return {"message": "Data supply tidak ditemukan"}, 404

    data = request.get_json(silent=True)
    error = validate(data, partial=partial)

    if error:
        return {"message": error}, 400

    if partial:
        merged = {
            field: existing[field]
            for field in EDITABLE_FIELDS
        }
        merged.update(data)
        supply.patch(id_supply, data)
    else:
        merged = data
        supply.update(id_supply, data)

    return {
        "message": "Data supply berhasil diperbarui",
        "data": {"id_supply": id_supply, **merged}
    }, 200


def delete(id_supply):
    try:
        if supply.get_by_id(id_supply) is None:
            return {"message": "Data supply tidak ditemukan"}, 404

        supply.delete(id_supply)

        return {"message": "Data supply berhasil dihapus"}, 200

    except Exception:
        return {
            "message": "Data supply tidak dapat dihapus karena mungkin masih memiliki detail supply."
        }, 409
