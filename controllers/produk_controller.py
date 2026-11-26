from decimal import Decimal, InvalidOperation

from flask import request, g

from models import produk, activity_log


# Field produk yang dapat ditambahkan dan diperbarui
FIELDS = {
    "id_merk",
    "id_kategori",
    "nama_produk",
    "harga_produk",
    "stok",
    "diskon_produk"
}


# ==========================================
# HELPER LOGGING
# ==========================================

def get_id_user():
    """
    Mengambil ID user dari hasil autentikasi JWT.

    Sesuaikan dengan middleware JWT kamu.
    """

    # Jika middleware JWT menyimpan ID di g.id_user
    if hasattr(g, "id_user"):
        return g.id_user

    # Jika middleware JWT menyimpan ID di g.user_id
    if hasattr(g, "user_id"):
        return g.user_id

    # Jika middleware JWT menyimpan user dalam dictionary
    if hasattr(g, "user") and isinstance(g.user, dict):
        return g.user.get("id_user")

    return None


def catat_aktivitas(aktivitas, status_code):
    try:
        current_user = getattr(g, "current_user", None)

        print("JWT PAYLOAD:", current_user)

        if not isinstance(current_user, dict):
            print("ERROR: g.current_user bukan dictionary")
            return

        id_user = current_user.get("id_user")

        print("ID USER DARI JWT:", id_user)

        if not id_user:
            print("ERROR: id_user tidak ada di token JWT")
            return

        activity_log.create(
            id_user=id_user,
            aktivitas=aktivitas,
            endpoint=request.path,
            method=request.method,
            status_code=status_code,
            ip_address=request.remote_addr
        )

        print("Activity log berhasil disimpan untuk:", id_user)

    except Exception as error:
        print("Gagal mencatat aktivitas:", error)


# ==========================================
# GET SEMUA PRODUK
# ==========================================

def get_all():

    try:
        data = produk.get_all()

        catat_aktivitas(
            aktivitas="Melihat Semua Produk",
            status_code=200
        )

        return {
            "message": "Data produk berhasil diambil",
            "data": data
        }, 200

    except Exception as error:
        print("Error get_all produk:", error)

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

        catat_aktivitas(
            aktivitas="Melihat Detail Produk",
            status_code=200
        )

        return {
            "data": data
        }, 200

    except Exception as error:
        print("Error get_by_id produk:", error)

        return {
            "message": "Gagal mengambil data produk"
        }, 500


# ==========================================
# VALIDASI DATA PRODUK
# ==========================================

def validate(data, partial=False, allow_id=False):

    if not isinstance(data, dict):
        return "Body harus berupa JSON"

    # ID tidak boleh diubah kecuali saat POST
    if not allow_id and "id_produk" in data:
        return "id_produk tidak boleh diubah"

    # Memeriksa field yang tidak dikenal
    unknown = set(data) - FIELDS

    if allow_id:
        unknown.discard("id_produk")

    if unknown:
        return (
            "Field tidak dikenal: "
            + ", ".join(sorted(unknown))
        )

    # Memeriksa field wajib untuk POST dan PUT
    if not partial:
        missing = FIELDS - set(data)

        if missing:
            return (
                "Field wajib dikirim: "
                + ", ".join(sorted(missing))
            )

    # PATCH minimal mengirim satu field
    if partial and not data:
        return "Kirim minimal satu field yang ingin diubah"

    # Validasi field bertipe teks
    for field in (
        "id_merk",
        "id_kategori",
        "nama_produk"
    ):

        if field in data:
            value = data[field]

            if not isinstance(value, str) or not value.strip():
                return (
                    f"{field} harus berupa teks "
                    "yang tidak kosong"
                )

            max_length = (
                255 if field == "nama_produk" else 20
            )

            if len(value) > max_length:
                return (
                    f"{field} maksimal "
                    f"{max_length} karakter"
                )

    # Validasi harga dan diskon
    for field in (
        "harga_produk",
        "diskon_produk"
    ):

        if field in data:
            value = data[field]

            if isinstance(value, bool):
                return f"{field} harus berupa angka"

            try:
                number = Decimal(str(value))

            except (InvalidOperation, ValueError):
                return f"{field} harus berupa angka"

            if not number.is_finite():
                return (
                    f"{field} harus berupa angka "
                    "yang valid"
                )

            if field == "harga_produk" and number < 0:
                return "harga_produk tidak boleh negatif"

            if field == "diskon_produk":
                if not (0 <= number <= 100):
                    return (
                        "diskon_produk harus "
                        "antara 0 sampai 100"
                    )

            if number.as_tuple().exponent < -2:
                return (
                    f"{field} maksimal 2 angka "
                    "di belakang koma"
                )

    # Validasi stok
    if "stok" in data and data["stok"] is not None:

        value = data["stok"]

        if (
            isinstance(value, bool)
            or not isinstance(value, int)
        ):
            return (
                "stok harus berupa bilangan "
                "bulat atau null"
            )

        if value < 0:
            return "stok tidak boleh negatif"

    return None


# ==========================================
# POST TAMBAH PRODUK
# ==========================================

def create():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {
            "message": "Body harus berupa JSON"
        }, 400

    id_produk = data.get("id_produk")

    # Validasi ID produk
    if not isinstance(id_produk, str) or not id_produk.strip():
        return {
            "message": "id_produk wajib diisi"
        }, 400

    id_produk = id_produk.strip()

    if len(id_produk) > 20:
        return {
            "message": "id_produk maksimal 20 karakter"
        }, 400

    # Validasi seluruh data dengan mengizinkan ID
    error = validate(data, allow_id=True)

    if error:
        return {
            "message": error
        }, 400

    try:

        # Memeriksa apakah ID sudah digunakan
        if produk.get_by_id(id_produk):
            return {
                "message": "ID produk sudah digunakan"
            }, 409

        # Memisahkan ID dari atribut produk
        product_data = {
            key: value
            for key, value in data.items()
            if key != "id_produk"
        }

        # Menyimpan produk
        produk.create({
            "id_produk": id_produk,
            **product_data
        })

        # Logging setelah produk berhasil dibuat
        catat_aktivitas(
            aktivitas="Tambah Produk",
            status_code=201
        )

        return {
            "message": "Produk berhasil ditambahkan",
            "data": {
                "id_produk": id_produk,
                **product_data
            }
        }, 201

    except Exception as error:
        print("Error create produk:", error)

        return {
            "message": (
                "Gagal menambahkan produk. "
                "Periksa id_merk, id_kategori, "
                "dan foreign key."
            )
        }, 400


# ==========================================
# PUT DAN PATCH UPDATE PRODUK
# ==========================================

def update(id_produk, partial=False):

    try:
        existing = produk.get_by_id(id_produk)

    except Exception as error:
        print("Error mengambil produk:", error)

        return {
            "message": "Gagal mengambil data produk"
        }, 500

    if existing is None:
        return {
            "message": "Produk tidak ditemukan"
        }, 404

    data = request.get_json(silent=True)

    # Validasi data update
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
        merged = {
            field: existing[field]
            for field in FIELDS
        }

        merged.update(data)

        update_data = data

    else:

        # PUT mengganti seluruh atribut produk
        merged = data
        update_data = data

    try:

        if partial:
            produk.patch(
                id_produk,
                update_data
            )

            aktivitas = "Patch Produk"

        else:
            produk.update(
                id_produk,
                update_data
            )

            aktivitas = "Update Produk"

        # Logging setelah update berhasil
        catat_aktivitas(
            aktivitas=aktivitas,
            status_code=200
        )

        return {
            "message": "Produk berhasil diperbarui",
            "data": {
                "id_produk": id_produk,
                **merged
            }
        }, 200

    except Exception as error:
        print("Error update produk:", error)

        return {
            "message": (
                "Gagal memperbarui produk. "
                "Periksa relasi merk dan kategori."
            )
        }, 400


# ==========================================
# DELETE PRODUK
# ==========================================

def delete(id_produk):

    try:

        if produk.get_by_id(id_produk) is None:
            return {
                "message": "Produk tidak ditemukan"
            }, 404

        produk.delete(id_produk)

        # Logging setelah produk berhasil dihapus
        catat_aktivitas(
            aktivitas="Hapus Produk",
            status_code=200
        )

        return {
            "message": "Produk berhasil dihapus"
        }, 200

    except Exception as error:
        print("Error delete produk:", error)

        return {
            "message": (
                "Produk tidak dapat dihapus karena "
                "mungkin masih direferensikan tabel lain."
            )
        }, 409
