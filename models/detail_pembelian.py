
from db import get_connection


def get_all():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM detail_pembelian")
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


def get_by_id(id_detail_pembelian):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT * FROM detail_pembelian
            WHERE id_detail_pembelian = %s
            """,
            (id_detail_pembelian,)
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
            INSERT INTO detail_pembelian (
                id_detail_pembelian,
                id_pembelian,
                kode_serial,
                harga_beli,
                jumlah_pembelian,
                diskon_pembelian
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                data["id_detail_pembelian"],
                data["id_pembelian"],
                data["kode_serial"],
                data["harga_beli"],
                data["jumlah_pembelian"],
                data["diskon_pembelian"]
            )
        )
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def update(id_detail_pembelian, data):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE detail_pembelian
            SET id_pembelian = %s,
                kode_serial = %s,
                harga_beli = %s,
                jumlah_pembelian = %s,
                diskon_pembelian = %s
            WHERE id_detail_pembelian = %s
            """,
            (
                data["id_pembelian"],
                data["kode_serial"],
                data["harga_beli"],
                data["jumlah_pembelian"],
                data["diskon_pembelian"],
                id_detail_pembelian
            )
        )
        connection.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        connection.close()


def patch(id_detail_pembelian, data):
    allowed_fields = {
        "id_pembelian",
        "kode_serial",
        "harga_beli",
        "jumlah_pembelian",
        "diskon_pembelian"
    }

    fields = [field for field in data if field in allowed_fields]

    if not fields:
        return 0

    assignments = ", ".join(
        f"`{field}` = %s" for field in fields
    )
    values = [data[field] for field in fields]
    values.append(id_detail_pembelian)

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            f"""
            UPDATE detail_pembelian
            SET {assignments}
            WHERE id_detail_pembelian = %s
            """,
            tuple(values)
        )
        connection.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        connection.close()


def delete(id_detail_pembelian):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM detail_pembelian
            WHERE id_detail_pembelian = %s
            """,
            (id_detail_pembelian,)
        )
        connection.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        connection.close()
