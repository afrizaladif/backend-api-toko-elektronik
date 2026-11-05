
from db import get_connection
from werkzeug.security import generate_password_hash


# Field yang boleh diperbarui
ALLOWED_FIELDS = (
    "nama_customer",
    "email_customer",
    "password",
    "no_telpon_customer"
)

# Field wajib untuk membuat customer dan PUT
REQUIRED_FIELDS = set(ALLOWED_FIELDS)


# ==============================
# GET ALL CUSTOMER
# ==============================
def get_all():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True, buffered=True)

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


# ==============================
# GET CUSTOMER BY ID
# ==============================
def get_by_id(id_customer):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True, buffered=True)

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


# ==============================
# CREATE CUSTOMER (POST)
# ==============================
def create(data):
    # Validasi field wajib
    missing_fields = REQUIRED_FIELDS - set(data.keys())

    if missing_fields:
        raise ValueError(
            "Field wajib belum lengkap: "
            + ", ".join(sorted(missing_fields))
        )

    # Tolak field yang tidak dikenal
    invalid_fields = set(data.keys()) - REQUIRED_FIELDS

    if invalid_fields:
        raise ValueError(
            "Field tidak diizinkan: "
            + ", ".join(sorted(invalid_fields))
        )

    # Validasi nilai
    for field in ALLOWED_FIELDS:
        value = data[field]

        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"{field} wajib diisi dan harus berupa teks"
            )

    connection = get_connection()
    cursor = connection.cursor(buffered=True)

    lock_acquired = False

    try:
        # Mengunci proses pembuatan ID
        cursor.execute("""
            SELECT GET_LOCK('customer_id_generation', 10)
        """)

        result = cursor.fetchone()

        if result is None or result[0] != 1:
            raise RuntimeError(
                "Gagal mendapatkan kunci pembuatan ID customer"
            )

        lock_acquired = True

        # Mengambil ID customer terbesar
        cursor.execute("""
            SELECT id_customer
            FROM customer
            WHERE id_customer REGEXP '^CUS[0-9]+$'
            ORDER BY CAST(SUBSTRING(id_customer, 4) AS UNSIGNED) DESC
            LIMIT 1
        """)

        result = cursor.fetchone()

        if result is None:
            new_number = 1
        else:
            last_number = int(result[0][3:])
            new_number = last_number + 1

        # Membuat ID otomatis
        id_customer = f"CUS{new_number:03d}"

        # Hash password
        password_hash = generate_password_hash(
            data["password"]
        )

        # Menyimpan data customer
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
            id_customer,
            data["nama_customer"],
            data["email_customer"],
            password_hash,
            data["no_telpon_customer"]
        ))

        connection.commit()

        return id_customer

    except Exception:
        connection.rollback()
        raise

    finally:
        # Melepaskan lock setelah proses selesai
        if lock_acquired:
            try:
                cursor.execute("""
                    SELECT RELEASE_LOCK('customer_id_generation')
                """)
                cursor.fetchone()

            except Exception as e:
                print("ERROR RELEASE LOCK:", repr(e))

        cursor.close()
        connection.close()


# ==============================
# UPDATE CUSTOMER (PUT)
# ==============================
def update(id_customer, data):
    # PUT wajib mengirim seluruh field
    missing_fields = REQUIRED_FIELDS - set(data.keys())

    if missing_fields:
        raise ValueError(
            "Field PUT belum lengkap: "
            + ", ".join(sorted(missing_fields))
        )

    # Tolak field yang tidak dikenal
    invalid_fields = set(data.keys()) - REQUIRED_FIELDS

    if invalid_fields:
        raise ValueError(
            "Field tidak diizinkan: "
            + ", ".join(sorted(invalid_fields))
        )

    # Validasi nilai
    for field in ALLOWED_FIELDS:
        value = data[field]

        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"{field} wajib diisi dan harus berupa teks"
            )

    connection = get_connection()
    cursor = connection.cursor(buffered=True)

    try:
        # Hash password sebelum disimpan
        password_hash = generate_password_hash(
            data["password"]
        )

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

        affected_rows = cursor.rowcount

        connection.commit()

        return affected_rows

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


# ==============================
# PATCH CUSTOMER
# ==============================
def patch(id_customer, data):
    # Tolak field yang tidak dikenal
    invalid_fields = set(data.keys()) - set(ALLOWED_FIELDS)

    if invalid_fields:
        raise ValueError(
            "Field tidak diizinkan: "
            + ", ".join(sorted(invalid_fields))
        )

    if not data:
        raise ValueError(
            "Tidak ada data yang ingin diperbarui"
        )

    # Validasi nilai
    for field, value in data.items():
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"{field} wajib berupa teks dan tidak boleh kosong"
            )

    connection = get_connection()
    cursor = connection.cursor(buffered=True)

    try:
        # Mengambil field yang dikirim pengguna
        fields = [
            field for field in ALLOWED_FIELDS
            if field in data
        ]

        assignments = ", ".join(
            f"{field} = %s" for field in fields
        )

        values = []

        for field in fields:
            value = data[field]

            # Hash password jika diperbarui
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

        affected_rows = cursor.rowcount

        connection.commit()

        return affected_rows

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


# ==============================
# DELETE CUSTOMER
# ==============================
def delete(id_customer):
    connection = get_connection()
    cursor = connection.cursor(buffered=True)

    try:
        cursor.execute("""
            DELETE FROM customer
            WHERE id_customer = %s
        """, (id_customer,))

        affected_rows = cursor.rowcount

        connection.commit()

        return affected_rows

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()
