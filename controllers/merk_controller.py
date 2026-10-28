
from flask import jsonify, request
from models import merk


def validasi(data, wajib_lengkap=True):
    if not isinstance(data, dict):
        return "Data harus berupa JSON object."

    if not data:
        return "Data tidak boleh kosong."

    kolom_diizinkan = {"id_merk", "nama_merk"}

    for kolom in data:
        if kolom not in kolom_diizinkan:
            return f"Field '{kolom}' tidak dikenali."

    if wajib_lengkap:
        if "id_merk" not in data or "nama_merk" not in data:
            return "Field id_merk dan nama_merk wajib diisi."

    if "id_merk" in data:
        if not isinstance(data["id_merk"], str):
            return "id_merk harus berupa teks."

        if not data["id_merk"].strip():
            return "id_merk tidak boleh kosong."

        if len(data["id_merk"]) > 20:
            return "id_merk maksimal 20 karakter."

    if "nama_merk" in data:
        if not isinstance(data["nama_merk"], str):
            return "nama_merk harus berupa teks."

        if not data["nama_merk"].strip():
            return "nama_merk tidak boleh kosong."

        if len(data["nama_merk"]) > 50:
            return "nama_merk maksimal 50 karakter."

    return None


def get_all():
    try:
        return jsonify(merk.get_all()), 200
    except Exception:
        return jsonify({
            "pesan": "Gagal mengambil data merk."
        }), 500


def get_by_id(id_merk):
    try:
        data = merk.get_by_id(id_merk)

        if data is None:
            return jsonify({
                "pesan": "Data merk tidak ditemukan."
            }), 404

        return jsonify(data), 200
    except Exception:
        return jsonify({
            "pesan": "Gagal mengambil data merk."
        }), 500


def create():
    data = request.get_json(silent=True)
    error = validasi(data)

    if error:
        return jsonify({"pesan": error}), 400

    try:
        if merk.get_by_id(data["id_merk"]):
            return jsonify({
                "pesan": "ID merk sudah digunakan."
            }), 409

        merk.create(data)

        return jsonify({
            "pesan": "Data merk berhasil ditambahkan.",
            "data": merk.get_by_id(data["id_merk"])
        }), 201
    except Exception:
        return jsonify({
            "pesan": "Gagal menambahkan data merk."
        }), 400


def update(id_merk):
    data = request.get_json(silent=True)
    error = validasi(data)

    if error:
        return jsonify({"pesan": error}), 400

    if data["id_merk"] != id_merk:
        return jsonify({
            "pesan": "id_merk pada URL dan body harus sama."
        }), 400

    try:
        if not merk.get_by_id(id_merk):
            return jsonify({
                "pesan": "Data merk tidak ditemukan."
            }), 404

        merk.update(id_merk, data)

        return jsonify({
            "pesan": "Data merk berhasil diperbarui.",
            "data": merk.get_by_id(id_merk)
        }), 200
    except Exception:
        return jsonify({
            "pesan": "Gagal memperbarui data merk."
        }), 400


def patch(id_merk):
    data = request.get_json(silent=True)
    error = validasi(data, wajib_lengkap=False)

    if error:
        return jsonify({"pesan": error}), 400

    if "id_merk" in data:
        return jsonify({
            "pesan": "id_merk tidak dapat diubah."
        }), 400

    if "nama_merk" not in data:
        return jsonify({
            "pesan": "Field nama_merk harus diisi."
        }), 400

    try:
        if not merk.get_by_id(id_merk):
            return jsonify({
                "pesan": "Data merk tidak ditemukan."
            }), 404

        merk.patch(id_merk, data)

        return jsonify({
            "pesan": "Data merk berhasil diperbarui sebagian.",
            "data": merk.get_by_id(id_merk)
        }), 200
    except Exception:
        return jsonify({
            "pesan": "Gagal memperbarui data merk."
        }), 400


def delete(id_merk):
    try:
        if not merk.get_by_id(id_merk):
            return jsonify({
                "pesan": "Data merk tidak ditemukan."
            }), 404

        merk.delete(id_merk)

        return jsonify({
            "pesan": "Data merk berhasil dihapus."
        }), 200
    except Exception:
        return jsonify({
            "pesan": (
                "Gagal menghapus merk. Pastikan merk tidak sedang "
                "digunakan oleh data produk."
            )
        }), 400
