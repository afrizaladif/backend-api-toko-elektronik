
from datetime import datetime
from decimal import Decimal, InvalidOperation
from flask import request
from models import detail_pembelian


EDITABLE_FIELDS = {
    "id_pembelian",
    "kode_serial",
    "harga_beli",
    "jumlah_pembelian",
    "diskon_pembelian"
}


def get_all():
    try:
        return {
            "message": "Data detail pembelian berhasil diambil",
            "data": detail_pembelian.get_all()
        }, 200
    except Exception:
        return {"message": "Gagal mengambil data detail pembelian"}, 500


def get_by_id(id_detail_pembelian):
    try:
        data = detail_pembelian.get_by_id(id_detail_pembelian)

        if data is None:
            return {"message": "Detail pembelian tidak ditemukan"}, 404

        return {"data": data}, 200
    except Exception:
        return {"message": "Gagal mengambil data detail pembelian"}, 500


def validate(data, partial=False):
    if not isinstance(data, dict):
        return "Body harus berupa JSON"

    if "id_detail_pembelian" in data:
        return "id_detail_pembelian tidak boleh diubah"

    unknown = set(data) - EDITABLE_FIELDS
    if unknown:
        return "Field tidak dikenal: " + ", ".join(sorted(unknown))

    if not partial:
        missing = EDITABLE_FIELDS - set(data)
        if missing:
            return "Field wajib dikirim: " + ", ".join(sorted(missing))
    elif not data:
        return "Kirim minimal satu field yang ingin diubah"

    for field in ("id_pembelian", "kode_serial"):
        if field in data:
            value = data[field]

            if not isinstance(value, str) or not value.strip():
                return f"{field} harus berupa teks yang tidak kosong"

            if len(value) > 20:
                return f"{field} maksimal 20 karakter"

    if "harga_beli" in data:
        value = data["harga_beli"]

        if isinstance(value, bool):
            return "harga_beli harus berupa angka"

        try:
            number = Decimal(str(value))
        except (InvalidOperation, ValueError):
            return "harga_beli harus berupa angka"

        if not number.is_finite() or number < 0:
            return "harga_beli harus berupa angka valid dan tidak negatif"

        if number.as_tuple().exponent < -2:
            return "harga_beli maksimal 2 angka di belakang koma"

        if len(number.as_tuple().digits) > 12:
            return "harga_beli melebihi batas DECIMAL(12,2)"

    if "jumlah_pembelian" in data:
        value = data["jumlah_pembelian"]

        if isinstance(value, bool) or not isinstance(value, int):
            return "jumlah_pembelian harus berupa bilangan bulat"

        if value <= 0:
            return "jumlah_pembelian harus lebih dari 0"

    if "diskon_pembelian" in data:
        value = data["diskon_pembelian"]

        if isinstance(value, bool):
            return "diskon_pembelian harus berupa angka"

        try:
            number = Decimal(str(value))
        except (InvalidOperation, ValueError):
            return "diskon_pembelian harus berupa angka"

        if not number.is_finite() or not (0 <= number <= 100):
            return "diskon_pembelian harus antara 0 sampai 100"

        if number.as_tuple().exponent < -2:
            return "diskon_pembelian maksimal 2 angka di belakang koma"

    return None


def create():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {"message": "Body harus berupa JSON"}, 400

    id_detail = data.get("id_detail_pembelian")

    if not isinstance(id_detail, str) or not id_detail.strip():
        return {"message": "id_detail_pembelian wajib diisi"}, 400

    if len(id_detail) > 20:
        return {"message": "id_detail_pembelian maksimal 20 karakter"}, 400

    error = validate(data)

    if error:
        return {"message": error}, 400

    try:
        if detail_pembelian.get_by_id(id_detail):
            return {"message": "ID detail pembelian sudah digunakan"}, 409

        detail_pembelian.create(data)

        return {"message": "Detail pembelian berhasil ditambahkan"}, 201

    except Exception:
        return {
            "message": "Gagal menambahkan detail pembelian. Periksa id_pembelian dan kode_serial."
        }, 400


def update(id_detail_pembelian, partial=False):
    try:
        existing = detail_pembelian.get_by_id(id_detail_pembelian)
    except Exception:
        return {"message": "Gagal mengambil data detail pembelian"}, 500

    if existing is None:
        return {"message": "Detail pembelian tidak ditemukan"}, 404

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
        detail_pembelian.patch(id_detail_pembelian, data)
    else:
        merged = data
        detail_pembelian.update(id_detail_pembelian, data)

    return {
        "message": "Detail pembelian berhasil diperbarui",
        "data": {
            "id_detail_pembelian": id_detail_pembelian,
            **merged
        }
    }, 200


def delete(id_detail_pembelian):
    try:
        if detail_pembelian.get_by_id(id_detail_pembelian) is None:
            return {"message": "Detail pembelian tidak ditemukan"}, 404

        detail_pembelian.delete(id_detail_pembelian)

        return {"message": "Detail pembelian berhasil dihapus"}, 200

    except Exception:
        return {
            "message": "Detail pembelian tidak dapat dihapus."
        }, 409
