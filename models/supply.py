
from db import get_connection


def get_all():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM supply")
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


def get_by_id(id_supply):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM supply WHERE id_supply = %s",
            (id_supply,)
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
            INSERT INTO supply (
                id_supply,
                id_supplier,
                tanggal_supply
            )
            VALUES (%s, %s, %s)
            """,
            (
                data["id_supply"],
                data["id_supplier"],
                data["tanggal_supply"]
            )
        )
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def update(id_supply, data):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE supply
            SET id_supplier = %s,
                tanggal_supply = %s
            WHERE id_supply = %s
            """,
            (
                data["id_supplier"],
                data["tanggal_supply"],
                id_supply
            )
        )
        connection.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        connection.close()


def patch(id_supply, data):
    allowed_fields = {
        "id_supplier",
        "tanggal_supply"
    }

    fields = [field for field in data if field in allowed_fields]

    if not fields:
        return 0

    assignments = ", ".join(
        f"`{field}` = %s" for field in fields
    )
    values = [data[field] for field in fields]
    values.append(id_supply)

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            f"UPDATE supply SET {assignments} WHERE id_supply = %s",
            tuple(values)
        )
        connection.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        connection.close()


def delete(id_supply):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "DELETE FROM supply WHERE id_supply = %s",
            (id_supply,)
        )
        connection.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        connection.close()
