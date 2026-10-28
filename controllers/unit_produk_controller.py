
from flask import request
from models import unit_produk


EDITABLE_FIELDS = {
    "id_detail_supply",
    "id_produk",
    "status"
}


def get_all():
    try:
        return {
            "message": "Data unit produk berhasil diambil",
            "data": unit_produk.get_all()
        }, 200
    except Exception:
        return {"message": "Gagal mengambil data unit produk"}, 500


def get_by_id(kode_serial):
    try:
        data = unit_produk.get_by_id(kode_serial)

        if data is None:
            return {"message": "Unit produk tidak ditemukan"}, 404

        return {"data": data}, 200
    except Exception:
        return {"message": "Gagal mengambil data unit produk"}, 500


def validate(data, partial=False):
    if not isinstance(data, dict):
        return "Body harus berupa JSON"

    if "kode_serial" in data:
        return "kode_serial tidak boleh diubah"

    unknown = set(data) - EDITABLE_FIELDS

    if unknown:
        return "Field tidak dikenal: " + ", ".join(sorted(unknown))

    if not partial:
        missing = EDITABLE_FIELDS - set(data)

        if missing:
            return "Field wajib dikirim: " + ", ".join(sorted(missing))

    elif not data:
        return "Kirim minimal satu field yang ingin diubah"

    for field in EDITABLE_FIELDS:
        if field in data:
            value = data[field]

            if not isinstance(value, str) or not value.strip():
                return f"{field} wajib berupa teks yang tidak kosong"

            if len(value) > 20:
                return f"{field} maksimal 20 karakter"

    return None


def create():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {"message": "Body harus berupa JSON"}, 400

    kode_serial = data.get("kode_serial")

    if not isinstance(kode_serial, str) or not kode_serial.strip():
        return {"message": "kode_serial wajib diisi"}, 400

    if len(kode_serial) > 20:
        return {"message": "kode_serial maksimal 20 karakter"}, 400

    error = validate(data)

    if error:
        return {"message": error}, 400

    try:
        if unit_produk.get_by_id(kode_serial):
            return {"message": "Kode serial sudah digunakan"}, 409

        unit_produk.create(data)

        return {"message": "Unit produk berhasil ditambahkan"}, 201

    except Exception:
        return {
            "message": "Gagal menambahkan unit produk. Periksa id_detail_supply dan id_produk."
        }, 400


def update(kode_serial, partial=False):
    try:
        existing = unit_produk.get_by_id(kode_serial)
    except Exception:
        return {"message": "Gagal mengambil data unit produk"}, 500

    if existing is None:
        return {"message": "Unit produk tidak ditemukan"}, 404

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
        unit_produk.patch(kode_serial, data)
    else:
        merged = data
        unit_produk.update(kode_serial, data)

    return {
        "message": "Unit produk berhasil diperbarui",
        "data": {
            "kode_serial": kode_serial,
            **merged
        }
    }, 200


def delete(kode_serial):
    try:
        if unit_produk.get_by_id(kode_serial) is None:
            return {"message": "Unit produk tidak ditemukan"}, 404

        unit_produk.delete(kode_serial)

        return {"message": "Unit produk berhasil dihapus"}, 200

    except Exception:
        return {
            "message": "Unit produk tidak dapat dihapus karena mungkin masih digunakan dalam detail pembelian."
        }, 409
