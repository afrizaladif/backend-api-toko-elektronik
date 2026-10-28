
from db import get_connection


def get_all():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM produk")
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


def get_by_id(id_produk):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM produk WHERE id_produk = %s",
            (id_produk,)
        )
        return cursor.fetchone()
    finally:
        cursor.close()
        connection.close()


def create(data):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO produk (
                id_produk, id_merk, id_kategori, nama_produk,
                harga_produk, stok, diskon_produk
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                data["id_produk"],
                data["id_merk"],
                data["id_kategori"],
                data["nama_produk"],
                data["harga_produk"],
                data.get("stok"),
                data["diskon_produk"]
            )
        )
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def update(id_produk, data):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE produk
            SET id_merk = %s,
                id_kategori = %s,
                nama_produk = %s,
                harga_produk = %s,
                stok = %s,
                diskon_produk = %s
            WHERE id_produk = %s
            """,
            (
                data["id_merk"],
                data["id_kategori"],
                data["nama_produk"],
                data["harga_produk"],
                data.get("stok"),
                data["diskon_produk"],
                id_produk
            )
        )
        connection.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        connection.close()


def patch(id_produk, data):
    allowed_fields = {
        "id_merk",
        "id_kategori",
        "nama_produk",
        "harga_produk",
        "stok",
        "diskon_produk"
    }

    fields = [field for field in data if field in allowed_fields]

    if not fields:
        return 0

    assignments = ", ".join(
        f"{field} = %s" for field in fields
    )
    values = [data[field] for field in fields]
    values.append(id_produk)

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            f"UPDATE produk SET {assignments} WHERE id_produk = %s",
            tuple(values)
        )
        connection.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        connection.close()


def delete(id_produk):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "DELETE FROM produk WHERE id_produk = %s",
            (id_produk,)
        )
        connection.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        connection.close()
