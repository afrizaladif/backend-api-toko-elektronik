
from db import get_connection


def get_all():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM customer")
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


def get_by_id(id_customer):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM customer WHERE id_customer = %s",
            (id_customer,)
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
            INSERT INTO customer (
                id_customer,
                nama_customer,
                email_customer,
                password,
                no_telpon_customer
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                data["id_customer"],
                data["nama_customer"],
                data["email_customer"],
                data["password"],
                data["no_telpon_customer"]
            )
        )
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def update(id_customer, data):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE customer
            SET nama_customer = %s,
                email_customer = %s,
                password = %s,
                no_telpon_customer = %s
            WHERE id_customer = %s
            """,
            (
                data["nama_customer"],
                data["email_customer"],
                data["password"],
                data["no_telpon_customer"],
                id_customer
            )
        )
        connection.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        connection.close()


def patch(id_customer, data):
    allowed_fields = {
        "nama_customer",
        "email_customer",
        "password",
        "no_telpon_customer"
    }

    fields = [field for field in data if field in allowed_fields]

    if not fields:
        return 0

    assignments = ", ".join(f"{field} = %s" for field in fields)
    values = [data[field] for field in fields]
    values.append(id_customer)

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            f"UPDATE customer SET {assignments} WHERE id_customer = %s",
            tuple(values)
        )
        connection.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        connection.close()


def delete(id_customer):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "DELETE FROM customer WHERE id_customer = %s",
            (id_customer,)
        )
        connection.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        connection.close()
