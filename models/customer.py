
from db import get_connection
from werkzeug.security import generate_password_hash


# Field yang boleh diperbarui
ALLOWED_FIELDS = {
    "nama_customer",
    "email_customer",
    "password",
    "no_telpon_customer"
}

# Field wajib untuk membuat customer
REQUIRED_FIELDS = {
    "id_customer",
    "nama_customer",
    "email_customer",
    "password",
    "no_telpon_customer"
}


def get_all():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                id_customer,
                nama_customer,
                email_customer,
                no_telpon_customer
            FROM customer
        """)

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


def get_by_id(id_customer):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                id_customer,
                nama_customer,
                email_customer,
                no_telpon_customer
            FROM customer
            WHERE id_customer = %s
        """, (id_customer,))

        return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()


def create(data):
    missing_fields = REQUIRED_FIELDS - set(data.keys())

    if missing_fields:
        raise ValueError(
            f"Field wajib belum lengkap: {', '.join(sorted(missing_fields))}"
        )

    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Hash password sebelum disimpan
        password_hash = generate_password_hash(data["password"])

        cursor.execute("""
            INSERT INTO customer (
                id_customer,
                nama_customer,
                email_customer,
                password,
                no_telpon_customer
            )
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data["id_customer"],
            data["nama_customer"],
            data["email_customer"],
            password_hash,
            data["no_telpon_customer"]
        ))

        connection.commit()
        return cursor.rowcount

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


def update(id_customer, data):
    # PUT harus mengirim seluruh atribut yang dapat diubah
    missing_fields = ALLOWED_FIELDS - set(data.keys())

    if missing_fields:
        raise ValueError(
            f"Field PUT belum lengkap: {', '.join(sorted(missing_fields))}"
        )

    # Primary key tidak boleh diubah
    if "id_customer" in data:
        raise ValueError("id_customer tidak boleh diubah")

    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Hash password baru
        password_hash = generate_password_hash(data["password"])

        cursor.execute("""
            UPDATE customer
            SET
                nama_customer = %s,
                email_customer = %s,
                password = %s,
                no_telpon_customer = %s
            WHERE id_customer = %s
        """, (
            data["nama_customer"],
            data["email_customer"],
            password_hash,
            data["no_telpon_customer"],
            id_customer
        ))

        connection.commit()
        return cursor.rowcount

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


def patch(id_customer, data):
    # Primary key tidak boleh diubah
    if "id_customer" in data:
        raise ValueError("id_customer tidak boleh diubah")

    # Tolak field yang tidak diizinkan
    invalid_fields = set(data.keys()) - ALLOWED_FIELDS

    if invalid_fields:
        raise ValueError(
            f"Field tidak diizinkan: {', '.join(sorted(invalid_fields))}"
        )

    # PATCH tidak boleh menerima JSON Body kosong
    if not data:
        raise ValueError("Tidak ada data yang ingin diperbarui")

    connection = get_connection()
    cursor = connection.cursor()

    try:
        fields = list(data.keys())

        # Buat query berdasarkan field yang dikirim
        assignments = ", ".join(
            f"{field} = %s" for field in fields
        )

        values = []

        for field in fields:
            value = data[field]

            # Hash password jika password ikut diperbarui
            if field == "password":
                value = generate_password_hash(value)

            values.append(value)

        values.append(id_customer)

        cursor.execute(
            f"""
            UPDATE customer
            SET {assignments}
            WHERE id_customer = %s
            """,
            tuple(values)
        )

        connection.commit()
        return cursor.rowcount

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


def delete(id_customer):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            DELETE FROM customer
            WHERE id_customer = %s
        """, (id_customer,))

        connection.commit()
        return cursor.rowcount

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()
