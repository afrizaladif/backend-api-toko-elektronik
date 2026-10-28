
from db import get_connection


def get_all():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM pembelian")
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


def get_by_id(id_pembelian):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM pembelian WHERE id_pembelian = %s",
            (id_pembelian,)
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
            INSERT INTO pembelian (
                id_pembelian, id_customer, tanggal_pembelian,
                total_harga, tipe_diskon
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                data["id_pembelian"],
                data["id_customer"],
                data["tanggal_pembelian"],
                data["total_harga"],
                data["tipe_diskon"]
            )
        )
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def update(id_pembelian, data):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            UPDATE pembelian
            SET id_customer = %s,
                tanggal_pembelian = %s,
                total_harga = %s,
                tipe_diskon = %s
            WHERE id_pembelian = %s
            """,
            (
                data["id_customer"],
                data["tanggal_pembelian"],
                data["total_harga"],
                data["tipe_diskon"],
                id_pembelian
            )
        )
        connection.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        connection.close()


def patch(id_pembelian, data):
    allowed_fields = {
        "id_customer",
        "tanggal_pembelian",
        "total_harga",
        "tipe_diskon"
    }

    fields = [field for field in data if field in allowed_fields]
    if not fields:
        return 0

    assignments = ", ".join(f"`{field}` = %s" for field in fields)
    values = [data[field] for field in fields]
    values.append(id_pembelian)

    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            f"UPDATE pembelian SET {assignments} WHERE id_pembelian = %s",
            tuple(values)
        )
        connection.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        connection.close()


def delete(id_pembelian):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "DELETE FROM pembelian WHERE id_pembelian = %s",
            (id_pembelian,)
        )
        connection.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        connection.close()
