
from flask import request
from models import kategori


def get_all():
    return {
        "message": "Data kategori berhasil diambil",
        "data": kategori.get_all()
    }, 200


def get_by_id(id_kategori):
    data = kategori.get_by_id(id_kategori)

    if data is None:
        return {"message": "Kategori tidak ditemukan"}, 404

    return {"data": data}, 200


def create():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {"message": "Body harus berupa JSON"}, 400

    id_kategori = data.get("id_kategori")
    nama_kategori = data.get("nama_kategori")

    if not isinstance(id_kategori, str) or not id_kategori.strip():
        return {"message": "id_kategori wajib diisi"}, 400

    if not isinstance(nama_kategori, str) or not nama_kategori.strip():
        return {"message": "nama_kategori wajib diisi"}, 400

    if len(id_kategori) > 20 or len(nama_kategori) > 50:
        return {"message": "Panjang data melebihi batas kolom"}, 400

    if kategori.get_by_id(id_kategori):
        return {"message": "ID kategori sudah digunakan"}, 409

    kategori.create({
        "id_kategori": id_kategori,
        "nama_kategori": nama_kategori
    })

    return {
        "message": "Kategori berhasil ditambahkan",
        "data": {
            "id_kategori": id_kategori,
            "nama_kategori": nama_kategori
        }
    }, 201


def update(id_kategori, partial=False):
    existing = kategori.get_by_id(id_kategori)

    if existing is None:
        return {"message": "Kategori tidak ditemukan"}, 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {"message": "Body harus berupa JSON"}, 400

    if "id_kategori" in data:
        return {"message": "ID kategori tidak boleh diubah"}, 400

    if not partial and "nama_kategori" not in data:
        return {"message": "nama_kategori wajib dikirim untuk PUT"}, 400

    if partial and not data:
        return {"message": "Kirim field yang ingin diubah"}, 400

    if set(data.keys()) - {"nama_kategori"}:
        return {"message": "Field yang dikirim tidak dikenal"}, 400

    if "nama_kategori" in data:
        nama = data["nama_kategori"]

        if not isinstance(nama, str) or not nama.strip():
            return {"message": "nama_kategori harus berupa teks"}, 400

        if len(nama) > 50:
            return {"message": "nama_kategori maksimal 50 karakter"}, 400

    # PUT mengganti representasi kategori; PATCH mempertahankan
    # field yang tidak dikirim.
    nama_baru = data.get("nama_kategori", existing["nama_kategori"])
    kategori.update(id_kategori, {"nama_kategori": nama_baru})

    return {
        "message": "Kategori berhasil diperbarui",
        "data": {
            "id_kategori": id_kategori,
            "nama_kategori": nama_baru
        }
    }, 200


def delete(id_kategori):
    if kategori.get_by_id(id_kategori) is None:
        return {"message": "Kategori tidak ditemukan"}, 404

    kategori.delete(id_kategori)

    return {"message": "Kategori berhasil dihapus"}, 200
