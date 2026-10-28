
from db import get_connection


def get_all():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM supplier")
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


def get_by_id(id_supplier):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM supplier WHERE id_supplier = %s",
            (id_supplier,)
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
            INSERT INTO supplier (
                id_supplier,
                nama_supplier,
                alamat_supplier,
                no_telpon_supplier
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                data["id_supplier"],
                data["nama_supplier"],
                data["alamat_supplier"],
                data["no_telpon_supplier"]
            )
        )
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def update(id_supplier, data):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE supplier
            SET nama_supplier = %s,
                alamat_supplier = %s,
                no_telpon_supplier = %s
            WHERE id_supplier = %s
            """,
            (
                data["nama_supplier"],
                data["alamat_supplier"],
                data["no_telpon_supplier"],
                id_supplier
            )
        )
        connection.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        connection.close()


def patch(id_supplier, data):
    allowed_fields = {
        "nama_supplier",
        "alamat_supplier",
        "no_telpon_supplier"
    }

    fields = [field for field in data if field in allowed_fields]

    if not fields:
        return 0

    assignments = ", ".join(
        f"`{field}` = %s" for field in fields
    )
    values = [data[field] for field in fields]
    values.append(id_supplier)

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            f"UPDATE supplier SET {assignments} WHERE id_supplier = %s",
            tuple(values)
        )
        connection.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        connection.close()


def delete(id_supplier):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "DELETE FROM supplier WHERE id_supplier = %s",
            (id_supplier,)
        )
        connection.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        connection.close()
