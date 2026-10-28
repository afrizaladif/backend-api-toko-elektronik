
from datetime import datetime
from flask import request
from models import pembelian


EDITABLE_FIELDS = {
    "id_customer",
    "tanggal_pembelian",
    "total_harga",
    "tipe_diskon"
}


def get_all():
    try:
        return {
            "message": "Data pembelian berhasil diambil",
            "data": pembelian.get_all()
        }, 200
    except Exception:
        return {"message": "Gagal mengambil data pembelian"}, 500


def get_by_id(id_pembelian):
    try:
        data = pembelian.get_by_id(id_pembelian)

        if data is None:
            return {"message": "Pembelian tidak ditemukan"}, 404

        return {"data": data}, 200
    except Exception:
        return {"message": "Gagal mengambil data pembelian"}, 500


def validate(data, partial=False):
    if not isinstance(data, dict):
        return "Body harus berupa JSON"

    if "id_pembelian" in data:
        return "id_pembelian tidak boleh diubah"

    unknown = set(data) - EDITABLE_FIELDS
    if unknown:
        return "Field tidak dikenal: " + ", ".join(sorted(unknown))

    if not partial:
        missing = EDITABLE_FIELDS - set(data)
        if missing:
            return "Field wajib dikirim: " + ", ".join(sorted(missing))
    elif not data:
        return "Kirim minimal satu field yang ingin diubah"

    if "id_customer" in data:
        value = data["id_customer"]

        if not isinstance(value, str) or not value.strip():
            return "id_customer harus berupa teks"

        if len(value) > 20:
            return "id_customer maksimal 20 karakter"

    if "tanggal_pembelian" in data:
        value = data["tanggal_pembelian"]

        if not isinstance(value, str):
            return "tanggal_pembelian harus berupa teks"

        try:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return "Format tanggal harus YYYY-MM-DD HH:MM:SS"

    if "total_harga" in data:
        value = data["total_harga"]

        if isinstance(value, bool) or not isinstance(value, int):
            return "total_harga harus berupa bilangan bulat"

        if value < 0:
            return "total_harga tidak boleh negatif"

    if "tipe_diskon" in data:
        value = data["tipe_diskon"]

        if isinstance(value, bool) or not isinstance(value, int):
            return "tipe_diskon harus berupa bilangan bulat"

        if not -128 <= value <= 127:
            return "tipe_diskon di luar rentang TINYINT bertanda"

    return None


def create():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {"message": "Body harus berupa JSON"}, 400

    id_pembelian = data.get("id_pembelian")

    if not isinstance(id_pembelian, str) or not id_pembelian.strip():
        return {"message": "id_pembelian wajib diisi"}, 400

    if len(id_pembelian) > 20:
        return {"message": "id_pembelian maksimal 20 karakter"}, 400

    error = validate(data)
    if error:
        return {"message": error}, 400

    try:
        if pembelian.get_by_id(id_pembelian):
            return {"message": "ID pembelian sudah digunakan"}, 409

        pembelian.create(data)

        return {"message": "Pembelian berhasil ditambahkan"}, 201
    except Exception:
        return {
            "message": "Gagal menambahkan pembelian. Periksa id_customer dan format data."
        }, 400


def update(id_pembelian, partial=False):
    try:
        existing = pembelian.get_by_id(id_pembelian)
    except Exception:
        return {"message": "Gagal mengambil data pembelian"}, 500

    if existing is None:
        return {"message": "Pembelian tidak ditemukan"}, 404

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
        pembelian.patch(id_pembelian, data)
    else:
        merged = data
        pembelian.update(id_pembelian, data)

    return {
        "message": "Pembelian berhasil diperbarui",
        "data": {"id_pembelian": id_pembelian, **merged}
    }, 200


def delete(id_pembelian):
    try:
        if pembelian.get_by_id(id_pembelian) is None:
            return {"message": "Pembelian tidak ditemukan"}, 404

        pembelian.delete(id_pembelian)
        return {"message": "Pembelian berhasil dihapus"}, 200
    except Exception:
        return {
            "message": "Pembelian tidak dapat dihapus karena mungkin masih memiliki detail pembelian."
        }, 409
