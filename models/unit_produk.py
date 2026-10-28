
from db import get_connection


def get_all():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM unit_produk")
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


def get_by_id(kode_serial):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM unit_produk WHERE kode_serial = %s",
            (kode_serial,)
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
            INSERT INTO unit_produk (
                kode_serial,
                id_detail_supply,
                id_produk,
                status
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                data["kode_serial"],
                data["id_detail_supply"],
                data["id_produk"],
                data["status"]
            )
        )
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def update(kode_serial, data):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE unit_produk
            SET id_detail_supply = %s,
                id_produk = %s,
                status = %s
            WHERE kode_serial = %s
            """,
            (
                data["id_detail_supply"],
                data["id_produk"],
                data["status"],
                kode_serial
            )
        )
        connection.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        connection.close()


def patch(kode_serial, data):
    allowed_fields = {
        "id_detail_supply",
        "id_produk",
        "status"
    }

    fields = [field for field in data if field in allowed_fields]

    if not fields:
        return 0

    assignments = ", ".join(
        f"`{field}` = %s" for field in fields
    )
    values = [data[field] for field in fields]
    values.append(kode_serial)

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            f"""
            UPDATE unit_produk
            SET {assignments}
            WHERE kode_serial = %s
            """,
            tuple(values)
        )
        connection.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        connection.close()


def delete(kode_serial):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "DELETE FROM unit_produk WHERE kode_serial = %s",
            (kode_serial,)
        )
        connection.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        connection.close()
