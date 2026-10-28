
from flask import jsonify, request
from models import merk


# Validasi data merk
def validasi(data, wajib_lengkap=True):
    if not isinstance(data, dict):
        return "Data harus berupa JSON object."

    if not data:
        return "Data tidak boleh kosong."

    kolom_diizinkan = {"id_merk", "nama_merk"}

    # Memeriksa field yang tidak dikenal
    for kolom in data:
        if kolom not in kolom_diizinkan:
            return f"Field '{kolom}' tidak dikenali."

    # Memeriksa field wajib
    if wajib_lengkap:
        if "id_merk" not in data or "nama_merk" not in data:
            return "Field id_merk dan nama_merk wajib diisi."

    # Validasi ID merk
    if "id_merk" in data:
        if not isinstance(data["id_merk"], str):
            return "id_merk harus berupa teks."

        if not data["id_merk"].strip():
            return "id_merk tidak boleh kosong."

        if len(data["id_merk"]) > 20:
            return "id_merk maksimal 20 karakter."

    # Validasi nama merk
    if "nama_merk" in data:
        if not isinstance(data["nama_merk"], str):
            return "nama_merk harus berupa teks."

        if not data["nama_merk"].strip():
            return "nama_merk tidak boleh kosong."

        if len(data["nama_merk"]) > 50:
            return "nama_merk maksimal 50 karakter."

    return None


# GET: Mengambil semua data merk
def get_all():
    try:
        data = merk.get_all()

        return jsonify({
            "data": data,
            "message": "Data merk berhasil diambil"
        }), 200

    except Exception:
        return jsonify({
            "message": "Gagal mengambil data merk."
        }), 500


# GET: Mengambil data merk berdasarkan ID
def get_by_id(id_merk):
    try:
        data = merk.get_by_id(id_merk)

        if data is None:
            return jsonify({
                "message": "Data merk tidak ditemukan."
            }), 404

        return jsonify({
            "data": data,
            "message": "Data merk berhasil diambil"
        }), 200

    except Exception:
        return jsonify({
            "message": "Gagal mengambil data merk."
        }), 500


# POST: Menambahkan data merk
def create():
    data = request.get_json(silent=True)
    error = validasi(data)

    if error:
        return jsonify({
            "message": error
        }), 400

    try:
        # Memeriksa apakah ID sudah digunakan
        if merk.get_by_id(data["id_merk"]):
            return jsonify({
                "message": "ID merk sudah digunakan."
            }), 409

        merk.create(data)

        data_baru = merk.get_by_id(data["id_merk"])

        return jsonify({
            "message": "Data merk berhasil ditambahkan.",
            "data": data_baru
        }), 201

    except Exception:
        return jsonify({
            "message": (
                "Gagal menambahkan data merk. "
                "Periksa kembali data yang dikirim."
            )
        }), 400


# PUT: Mengganti seluruh data merk yang dapat diedit
def update(id_merk):
    data = request.get_json(silent=True)
    error = validasi(data)

    if error:
        return jsonify({
            "message": error
        }), 400

    # ID pada URL dan body harus sama
    if data["id_merk"] != id_merk:
        return jsonify({
            "message": "id_merk pada URL dan body harus sama."
        }), 400

    try:
        data_lama = merk.get_by_id(id_merk)

        if data_lama is None:
            return jsonify({
                "message": "Data merk tidak ditemukan."
            }), 404

        merk.update(id_merk, data)

        data_baru = merk.get_by_id(id_merk)

        return jsonify({
            "message": "Data merk berhasil diperbarui.",
            "data": data_baru
        }), 200

    except Exception:
        return jsonify({
            "message": "Gagal memperbarui data merk."
        }), 400


# PATCH: Memperbarui sebagian data merk
def patch(id_merk):
    data = request.get_json(silent=True)
    error = validasi(data, wajib_lengkap=False)

    if error:
        return jsonify({
            "message": error
        }), 400

    # Primary key tidak boleh diubah
    if "id_merk" in data:
        return jsonify({
            "message": "id_merk tidak dapat diubah."
        }), 400

    if "nama_merk" not in data:
        return jsonify({
            "message": "Field nama_merk harus diisi."
        }), 400

    try:
        data_lama = merk.get_by_id(id_merk)

        if data_lama is None:
            return jsonify({
                "message": "Data merk tidak ditemukan."
            }), 404

        merk.patch(id_merk, data)

        data_baru = merk.get_by_id(id_merk)

        return jsonify({
            "message": "Data merk berhasil diperbarui sebagian.",
            "data": data_baru
        }), 200

    except Exception:
        return jsonify({
            "message": "Gagal memperbarui data merk."
        }), 400


# DELETE: Menghapus data merk
def delete(id_merk):
    try:
        data_lama = merk.get_by_id(id_merk)

        if data_lama is None:
            return jsonify({
                "message": "Data merk tidak ditemukan."
            }), 404

        merk.delete(id_merk)

        return jsonify({
            "message": "Data merk berhasil dihapus."
        }), 200

    except Exception:
        return jsonify({
            "message": (
                "Gagal menghapus merk. Pastikan merk tidak sedang "
                "digunakan oleh data produk."
            )
        }), 409
