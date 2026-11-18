
from db import get_connection
from werkzeug.security import generate_password_hash


# =====================================
# KONFIGURASI FIELD
# =====================================

ALLOWED_FIELDS = (
    "nama_user",
    "email",
    "password",
    "no_telepon"
)

REQUIRED_FIELDS = set(ALLOWED_FIELDS)


# =====================================
# VALIDASI DATA USER
# =====================================

def validate_data(data):
    if not isinstance(data, dict):
        raise ValueError("Data harus berupa JSON object")

    missing_fields = REQUIRED_FIELDS - set(data.keys())

    if missing_fields:
        raise ValueError(
            "Field wajib belum lengkap: "
            + ", ".join(sorted(missing_fields))
        )

    invalid_fields = set(data.keys()) - REQUIRED_FIELDS

    if invalid_fields:
        raise ValueError(
            "Field tidak diizinkan: "
            + ", ".join(sorted(invalid_fields))
        )

    for field in ALLOWED_FIELDS:
        value = data[field]

        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"{field} wajib diisi dan harus berupa teks"
            )

    if "@" not in data["email"]:
        raise ValueError("Format email tidak valid")


# =====================================
# GET ALL USERS
# =====================================

def get_all():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True, buffered=True)

    try:
        cursor.execute("""
            SELECT
                id_user,
                nama_user,
                email,
                no_telepon,
                role,
                created_at,
                updated_at
            FROM users
        """)

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


# =====================================
# GET USER BY ID
# =====================================

def get_by_id(id_user):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True, buffered=True)

    try:
        cursor.execute("""
            SELECT
                id_user,
                nama_user,
                email,
                no_telepon,
                role,
                created_at,
                updated_at
            FROM users
            WHERE id_user = %s
        """, (id_user,))

        return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()


# =====================================
# GET USER BY EMAIL
# KHUSUS KEBUTUHAN LOGIN CUSTOMER
# =====================================

def get_by_email(email):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True, buffered=True)

    try:
        cursor.execute("""
            SELECT
                id_user,
                nama_user,
                email,
                password,
                role
            FROM users
            WHERE email = %s
        """, (email,))

        return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()


# =====================================
# CREATE USER BERDASARKAN ROLE
# =====================================

def _create_user(data, role):
    validate_data(data)

    connection = get_connection()
    cursor = connection.cursor(buffered=True)

    lock_acquired = False

    try:
        # Mengunci proses pembuatan ID
        cursor.execute(
            "SELECT GET_LOCK(%s, 10)",
            ("user_id_generation",)
        )

        result = cursor.fetchone()

        if result is None or result[0] != 1:
            raise RuntimeError(
                "Gagal mendapatkan kunci pembuatan ID user"
            )

        lock_acquired = True

        # Memeriksa email
        cursor.execute("""
            SELECT id_user
            FROM users
            WHERE email = %s
            LIMIT 1
        """, (data["email"],))

        if cursor.fetchone():
            raise ValueError("Email sudah terdaftar")

        # Mengambil ID user terbesar
        cursor.execute("""
            SELECT id_user
            FROM users
            WHERE id_user REGEXP '^USR[0-9]+$'
            ORDER BY CAST(SUBSTRING(id_user, 4) AS UNSIGNED) DESC
            LIMIT 1
        """)

        result = cursor.fetchone()

        if result is None:
            new_number = 1
        else:
            last_number = int(result[0][3:])
            new_number = last_number + 1

        id_user = f"USR{new_number:03d}"

        # Hash password
        password_hash = generate_password_hash(data["password"])

        # Menyimpan user
        cursor.execute("""
            INSERT INTO users (
                id_user,
                nama_user,
                email,
                password,
                no_telepon,
                role
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            id_user,
            data["nama_user"],
            data["email"],
            password_hash,
            data["no_telepon"],
            role
        ))

        connection.commit()

        return id_user

    except Exception:
        connection.rollback()
        raise

    finally:
        if lock_acquired:
            try:
                cursor.execute(
                    "SELECT RELEASE_LOCK(%s)",
                    ("user_id_generation",)
                )
                cursor.fetchone()

            except Exception as e:
                print("ERROR RELEASE USER LOCK:", repr(e))

        cursor.close()
        connection.close()


# =====================================
# CREATE CUSTOMER (POST)
# =====================================

def create(data):
    return _create_user(data, "customer")


# =====================================
# CREATE ADMIN
# =====================================

def create_admin(data):
    return _create_user(data, "admin")


# =====================================
# UPDATE USER (PUT)
# =====================================

def update(id_user, data):
    validate_data(data)

    connection = get_connection()
    cursor = connection.cursor(buffered=True)

    try:
        password_hash = generate_password_hash(data["password"])

        cursor.execute("""
            UPDATE users
            SET
                nama_user = %s,
                email = %s,
                password = %s,
                no_telepon = %s
            WHERE id_user = %s
        """, (
            data["nama_user"],
            data["email"],
            password_hash,
            data["no_telepon"],
            id_user
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


# =====================================
# PATCH USER
# =====================================

def patch(id_user, data):
    if not isinstance(data, dict):
        raise ValueError("Data harus berupa JSON object")

    invalid_fields = set(data.keys()) - set(ALLOWED_FIELDS)

    if invalid_fields:
        raise ValueError(
            "Field tidak diizinkan: "
            + ", ".join(sorted(invalid_fields))
        )

    if not data:
        raise ValueError("Tidak ada data yang ingin diperbarui")

    for field, value in data.items():
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"{field} wajib berupa teks dan tidak boleh kosong"
            )

    if "email" in data and "@" not in data["email"]:
        raise ValueError("Format email tidak valid")

    connection = get_connection()
    cursor = connection.cursor(buffered=True)

    try:
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

            if field == "password":
                value = generate_password_hash(value)

            values.append(value)

        values.append(id_user)

        cursor.execute(
            f"""
            UPDATE users
            SET {assignments}
            WHERE id_user = %s
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


# =====================================
# DELETE USER
# =====================================

def delete(id_user):
    connection = get_connection()
    cursor = connection.cursor(buffered=True)

    try:
        cursor.execute("""
            DELETE FROM users
            WHERE id_user = %s
        """, (id_user,))

        affected_rows = cursor.rowcount
        connection.commit()

        return affected_rows

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()
