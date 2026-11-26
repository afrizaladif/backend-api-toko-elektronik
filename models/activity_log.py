
import uuid

from db import get_connection


# ==========================================
# MEMBUAT ID LOG
# ==========================================

def generate_id_log():
    """
    Membuat ID log sepanjang 10 karakter.
    Contoh: LOGA1B2C3D
    """
    return "LOG" + uuid.uuid4().hex[:7].upper()


# ==========================================
# MENYIMPAN ACTIVITY LOG
# ==========================================

def create(
    id_user,
    aktivitas,
    endpoint,
    method,
    status_code,
    ip_address
):
    koneksi = None
    cursor = None

    try:
        koneksi = get_connection()
        cursor = koneksi.cursor()

        id_log = generate_id_log()

        sql = """
            INSERT INTO activity_logs (
                id_log,
                id_user,
                aktivitas,
                endpoint,
                method,
                status_code,
                ip_address
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        data = (
            id_log,
            id_user,
            aktivitas,
            endpoint,
            method,
            status_code,
            ip_address
        )

        cursor.execute(sql, data)
        koneksi.commit()

        return id_log

    except Exception:
        if koneksi:
            koneksi.rollback()

        raise

    finally:
        if cursor:
            cursor.close()

        if koneksi:
            koneksi.close()


# ==========================================
# MENGAMBIL SEMUA ACTIVITY LOG
# ==========================================

def get_all():
    koneksi = None
    cursor = None

    try:
        koneksi = get_connection()
        cursor = koneksi.cursor(dictionary=True)

        sql = """
            SELECT
                id_log,
                id_user,
                aktivitas,
                endpoint,
                method,
                status_code,
                ip_address,
                created_at
            FROM activity_logs
            ORDER BY created_at DESC
        """

        cursor.execute(sql)

        return cursor.fetchall()

    finally:
        if cursor:
            cursor.close()

        if koneksi:
            koneksi.close()


# ==========================================
# MENGAMBIL LOG BERDASARKAN USER
# ==========================================

def get_by_user(id_user):
    koneksi = None
    cursor = None

    try:
        koneksi = get_connection()
        cursor = koneksi.cursor(dictionary=True)

        sql = """
            SELECT
                id_log,
                id_user,
                aktivitas,
                endpoint,
                method,
                status_code,
                ip_address,
                created_at
            FROM activity_logs
            WHERE id_user = %s
            ORDER BY created_at DESC
        """

        cursor.execute(sql, (id_user,))

        return cursor.fetchall()

    finally:
        if cursor:
            cursor.close()

        if koneksi:
            koneksi.close()
