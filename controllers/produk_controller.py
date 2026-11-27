
from decimal import Decimal, InvalidOperation

from flask import request
from models import produk


# Field produk yang boleh ditambahkan atau diperbarui
FIELDS = {
    "id_merk",
    "id_kategori",
    "nama_produk",
    "harga_produk",
    "stok",
    "diskon_produk"
}


# ==========================================
# VALIDASI DATA PRODUK
# ==========================================

def validate(data, partial=False, allow_id=False):
    """
    Memvalidasi data produk.

    partial=True:
        Untuk PATCH, field yang dikirim saja yang divalidasi.

    allow_id=True:
        Untuk POST, id_produk boleh dikirim.
    """

    if not isinstance(data, dict):
        return "Body harus berupa JSON object"

    # ID produk hanya boleh dikirim saat POST
    if not allow_id and "id_produk" in data:
        return "id_produk tidak boleh diubah"

    allowed_fields = set(FIELDS)

    if allow_id:
        allowed_fields.add("id_produk")

    unknown_fields = set(data.keys()) - allowed_fields

    if unknown_fields:
        return (
            "Field tidak dikenal: "
            + ", ".join(sorted(unknown_fields))
        )

    # POST dan PUT harus mengirim seluruh field
    if not partial:
        missing_fields = FIELDS - set(data.keys())

        if missing_fields:
            return (
                "Field wajib dikirim: "
                + ", ".join(sorted(missing_fields))
            )

    # PATCH harus mengirim minimal satu field
    if partial and not data:
        return "Kirim minimal satu field yang ingin diubah"

    # Validasi field teks
    text_fields = {
        "id_merk": 20,
        "id_kategori": 20,
        "nama_produk": 255
    }

    for field, max_length in text_fields.items():

        if field not in data:
            continue

        value = data[field]

        if not isinstance(value, str) or not value.strip():
            return f"{field} harus berupa teks yang tidak kosong"

        if len(value.strip()) > max_length:
            return f"{field} maksimal {max_length} karakter"

    # Validasi harga dan diskon
    numeric_fields = (
        "harga_produk",
        "diskon_produk"
    )

    for field in numeric_fields:

        if field not in data:
            continue

        value = data[field]

        if isinstance(value, bool):
            return f"{field} harus berupa angka"

        try:
            number = Decimal(str(value))

        except (InvalidOperation, ValueError, TypeError):
            return f"{field} harus berupa angka"

        if not number.is_finite():
            return f"{field} harus berupa angka yang valid"

        if field == "harga_produk" and number < 0:
            return "harga_produk tidak boleh negatif"

        if field == "diskon_produk":
            if number < 0 or number > 100:
                return "diskon_produk harus antara 0 sampai 100"

        if number.as_tuple().exponent < -2:
            return f"{field} maksimal 2 angka di belakang koma"

    # Validasi stok
    if "stok" in data:

        value = data["stok"]

        if value is not None:
            if isinstance(value, bool) or not isinstance(value, int):
                return "stok harus berupa bilangan bulat atau null"

            if value < 0:
                return "stok tidak boleh negatif"

    return None


# ==========================================
# GET SEMUA PRODUK
# ==========================================

def get_all():

    try:
        data = produk.get_all()

        return {
            "message": "Data produk berhasil diambil",
            "data": data
        }, 200

    except Exception:
        return {
            "message": "Gagal mengambil data produk"
        }, 500


# ==========================================
# GET PRODUK BERDASARKAN ID
# ==========================================

def get_by_id(id_produk):

    try:
        data = produk.get_by_id(id_produk)

        if data is None:
            return {
                "message": "Produk tidak ditemukan"
            }, 404

        return {
            "data": data
        }, 200

    except Exception:
        return {
            "message": "Gagal mengambil data produk"
        }, 500


# ==========================================
# POST TAMBAH PRODUK
# ==========================================

def create():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {
            "message": "Body harus berupa JSON object"
        }, 400

    id_produk = data.get("id_produk")

    if not isinstance(id_produk, str) or not id_produk.strip():
        return {
            "message": "id_produk wajib diisi"
        }, 400

    id_produk = id_produk.strip()

    if len(id_produk) > 20:
        return {
            "message": "id_produk maksimal 20 karakter"
        }, 400

    error = validate(data, allow_id=True)

    if error:
        return {
            "message": error
        }, 400

    product_data = {
        key: value
        for key, value in data.items()
        if key != "id_produk"
    }

    try:
        # Cek ID produk apakah sudah digunakan
        existing = produk.get_by_id(id_produk)

        if existing is not None:
            return {
                "message": "ID produk sudah digunakan"
            }, 409

        produk.create({
            "id_produk": id_produk,
            **product_data
        })

        return {
            "message": "Produk berhasil ditambahkan",
            "data": {
                "id_produk": id_produk,
                **product_data
            }
        }, 201

    except Exception:
        return {
            "message": (
                "Gagal menambahkan produk. "
                "Periksa ID produk, merk, kategori, "
                "dan relasi foreign key."
            )
        }, 400


# ==========================================
# PUT DAN PATCH UPDATE PRODUK
# ==========================================

def update(id_produk, partial=False):

    # Pastikan produk tersedia
    try:
        existing = produk.get_by_id(id_produk)

    except Exception:
        return {
            "message": "Gagal mengambil data produk"
        }, 500

    if existing is None:
        return {
            "message": "Produk tidak ditemukan"
        }, 404

    data = request.get_json(silent=True)

    error = validate(
        data,
        partial=partial
    )

    if error:
        return {
            "message": error
        }, 400

    if partial:
        # PATCH hanya memperbarui field yang dikirim
        update_data = data

        merged_data = {
            field: existing.get(field)
            for field in FIELDS
        }

        merged_data.update(data)

    else:
        # PUT mengganti seluruh atribut produk
        update_data = data
        merged_data = data

    try:

        if partial:
            produk.patch(
                id_produk,
                update_data
            )

        else:
            produk.update(
                id_produk,
                update_data
            )

        return {
            "message": "Produk berhasil diperbarui",
            "data": {
                "id_produk": id_produk,
                **merged_data
            }
        }, 200

    except Exception:
        return {
            "message": (
                "Gagal memperbarui produk. "
                "Periksa data merk, kategori, "
                "dan relasi foreign key."
            )
        }, 400


# ==========================================
# DELETE PRODUK
# ==========================================

def delete(id_produk):

    try:
        existing = produk.get_by_id(id_produk)

        if existing is None:
            return {
                "message": "Produk tidak ditemukan"
            }, 404

        produk.delete(id_produk)

        return {
            "message": "Produk berhasil dihapus"
        }, 200

    except Exception:
        return {
            "message": (
                "Produk tidak dapat dihapus karena "
                "mungkin masih direferensikan tabel lain."
            )
        }, 409
