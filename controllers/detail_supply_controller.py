
from models import detail_supply
from flask import jsonify
from datetime import datetime


def validasi(data, wajib_lengkap=True):
    if not isinstance(data, dict):
        return "Data harus berupa JSON object."

    kolom_diizinkan = {
        "id_detail_supply",
        "id_supply",
        "id_produk",
        "jumlah_supply"
    }

    if not data:
        return "Data tidak boleh kosong."

    if wajib_lengkap:
        kolom_wajib = kolom_diizinkan
        if not kolom_wajib.issubset(data.keys()):
            return "Semua field wajib diisi."

    for kolom in data:
        if kolom not in kolom_diizinkan:
            return f"Field '{kolom}' tidak dikenali."

    for kolom in ("id_detail_supply", "id_supply", "id_produk"):
        if kolom in data:
            nilai = data[kolom]

            if not isinstance(nilai, str) or not nilai.strip():
                return f"{kolom} harus berupa teks dan tidak boleh kosong."

            if len(nilai) > 20:
                return f"{kolom} maksimal 20 karakter."

    if "jumlah_supply" in data:
        jumlah = data["jumlah_supply"]

        if isinstance(jumlah, bool) or not isinstance(jumlah, int):
            return "jumlah_supply harus berupa bilangan bulat."

        if jumlah <= 0:
            return "jumlah_supply harus lebih besar dari 0."

    return None


def get_all():
    try:
        return jsonify(detail_supply.get_all()), 200
    except Exception:
        return jsonify({"pesan": "Gagal mengambil data detail supply."}), 500


def get_by_id(id_detail_supply):
    try:
        data = detail_supply.get_by_id(id_detail_supply)

        if data is None:
            return jsonify({"pesan": "Data detail supply tidak ditemukan."}), 404

        return jsonify(data), 200
    except Exception:
        return jsonify({"pesan": "Gagal mengambil data detail supply."}), 500


def create():
    from flask import request

    data = request.get_json(silent=True)
    error = validasi(data)

    if error:
        return jsonify({"pesan": error}), 400

    try:
        if detail_supply.get_by_id(data["id_detail_supply"]):
            return jsonify({"pesan": "ID detail supply sudah digunakan."}), 409

        detail_supply.create(data)

        return jsonify({
            "pesan": "Data detail supply berhasil ditambahkan.",
            "data": detail_supply.get_by_id(data["id_detail_supply"])
        }), 201

    except Exception:
        return jsonify({
            "pesan": "Gagal menambahkan data. Pastikan ID supply dan ID produk tersedia."
        }), 400


def update(id_detail_supply):
    from flask import request

    data = request.get_json(silent=True)
    error = validasi(data)

    if error:
        return jsonify({"pesan": error}), 400

    try:
        if not detail_supply.get_by_id(id_detail_supply):
            return jsonify({"pesan": "Data detail supply tidak ditemukan."}), 404

        detail_supply.update(id_detail_supply, data)

        return jsonify({
            "pesan": "Data detail supply berhasil diperbarui.",
            "data": detail_supply.get_by_id(id_detail_supply)
        }), 200

    except Exception:
        return jsonify({
            "pesan": "Gagal memperbarui data. Periksa kembali ID supply dan ID produk."
        }), 400


def patch(id_detail_supply):
    from flask import request

    data = request.get_json(silent=True)
    error = validasi(data, wajib_lengkap=False)

    if error:
        return jsonify({"pesan": error}), 400

    if "id_detail_supply" in data:
        return jsonify({
            "pesan": "id_detail_supply tidak dapat diubah."
        }), 400

    try:
        if not detail_supply.get_by_id(id_detail_supply):
            return jsonify({"pesan": "Data detail supply tidak ditemukan."}), 404

        if not any(
            kolom in data
            for kolom in ("id_supply", "id_produk", "jumlah_supply")
        ):
            return jsonify({
                "pesan": "Tidak ada field yang dapat diperbarui."
            }), 400

        detail_supply.patch(id_detail_supply, data)

        return jsonify({
            "pesan": "Data detail supply berhasil diperbarui sebagian.",
            "data": detail_supply.get_by_id(id_detail_supply)
        }), 200

    except Exception:
        return jsonify({
            "pesan": "Gagal memperbarui data. Periksa kembali ID supply dan ID produk."
        }), 400


def delete(id_detail_supply):
    try:
        if not detail_supply.get_by_id(id_detail_supply):
            return jsonify({"pesan": "Data detail supply tidak ditemukan."}), 404

        detail_supply.delete(id_detail_supply)

        return jsonify({
            "pesan": "Data detail supply berhasil dihapus."
        }), 200

    except Exception:
        return jsonify({
            "pesan": "Gagal menghapus data detail supply. Periksa relasi dengan tabel lain."
        }), 400
