
from decimal import Decimal, InvalidOperation
from flask import request
from models import produk


FIELDS = {
    "id_merk",
    "id_kategori",
    "nama_produk",
    "harga_produk",
    "stok",
    "diskon_produk"
}


def get_all():
    try:
        return {
            "message": "Data produk berhasil diambil",
            "data": produk.get_all()
        }, 200
    except Exception:
        return {"message": "Gagal mengambil data produk"}, 500


def get_by_id(id_produk):
    try:
        data = produk.get_by_id(id_produk)

        if data is None:
            return {"message": "Produk tidak ditemukan"}, 404

        return {"data": data}, 200
    except Exception:
        return {"message": "Gagal mengambil data produk"}, 500


def validate(data, partial=False):
    if not isinstance(data, dict):
        return "Body harus berupa JSON"

    if "id_produk" in data:
        return "id_produk tidak boleh diubah"

    unknown = set(data) - FIELDS
    if unknown:
        return "Field tidak dikenal: " + ", ".join(sorted(unknown))

    if not partial:
        missing = FIELDS - set(data)
        if missing:
            return "Field wajib dikirim: " + ", ".join(sorted(missing))

    if partial and not data:
        return "Kirim minimal satu field yang ingin diubah"

    for field in ("id_merk", "id_kategori", "nama_produk"):
        if field in data:
            value = data[field]

            if not isinstance(value, str) or not value.strip():
                return f"{field} harus berupa teks yang tidak kosong"

            max_length = 255 if field == "nama_produk" else 20
            if len(value) > max_length:
                return f"{field} maksimal {max_length} karakter"

    for field in ("harga_produk", "diskon_produk"):
        if field in data:
            value = data[field]

            if isinstance(value, bool):
                return f"{field} harus berupa angka"

            try:
                number = Decimal(str(value))
            except (InvalidOperation, ValueError):
                return f"{field} harus berupa angka"

            if not number.is_finite():
                return f"{field} harus berupa angka yang valid"

            if field == "harga_produk" and number < 0:
                return "harga_produk tidak boleh negatif"

            if field == "diskon_produk" and not (0 <= number <= 100):
                return "diskon_produk harus antara 0 sampai 100"

            if number.as_tuple().exponent < -2:
                return f"{field} maksimal 2 angka di belakang koma"

    if "stok" in data and data["stok"] is not None:
        value = data["stok"]

        if isinstance(value, bool) or not isinstance(value, int):
            return "stok harus berupa bilangan bulat atau null"

        if value < 0:
            return "stok tidak boleh negatif"

    return None


def create():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {"message": "Body harus berupa JSON"}, 400

    id_produk = data.get("id_produk")

    if not isinstance(id_produk, str) or not id_produk.strip():
        return {"message": "id_produk wajib diisi"}, 400

    if len(id_produk) > 20:
        return {"message": "id_produk maksimal 20 karakter"}, 400

    error = validate(data)
    if error:
        return {"message": error}, 400

    try:
        if produk.get_by_id(id_produk):
            return {"message": "ID produk sudah digunakan"}, 409

        produk.create({
            "id_produk": id_produk,
            **data
        })

        return {"message": "Produk berhasil ditambahkan"}, 201

    except Exception:
        return {
            "message": "Gagal menambahkan produk. Periksa id_merk, id_kategori, dan foreign key."
        }, 400


def update(id_produk, partial=False):
    try:
        existing = produk.get_by_id(id_produk)
    except Exception:
        return {"message": "Gagal mengambil data produk"}, 500

    if existing is None:
        return {"message": "Produk tidak ditemukan"}, 404

    data = request.get_json(silent=True)
    error = validate(data, partial=partial)

    if error:
        return {"message": error}, 400

    if partial:
        merged = {field: existing[field] for field in FIELDS}
        merged.update(data)
        update_data = data
        # PATCH hanya mengubah field yang dikirim.
        # Jika stok dikirim null, stok akan menjadi NULL.
    else:
        merged = data
        update_data = data

    try:
        produk.patch(id_produk, update_data) if partial else produk.update(
            id_produk, update_data
        )

        return {
            "message": "Produk berhasil diperbarui",
            "data": {"id_produk": id_produk, **merged}
        }, 200

    except Exception:
        return {
            "message": "Gagal memperbarui produk. Periksa relasi merk dan kategori."
        }, 400


def delete(id_produk):
    try:
        if produk.get_by_id(id_produk) is None:
            return {"message": "Produk tidak ditemukan"}, 404

        produk.delete(id_produk)
        return {"message": "Produk berhasil dihapus"}, 200

    except Exception:
        return {
            "message": "Produk tidak dapat dihapus karena mungkin masih direferensikan tabel lain."
        }, 409
