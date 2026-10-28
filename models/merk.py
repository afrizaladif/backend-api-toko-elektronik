
from db import get_connection


def get_all():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM merk")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def get_by_id(id_merk):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM merk WHERE id_merk = %s",
            (id_merk,)
        )
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def create(data):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        sql = """
            INSERT INTO merk (id_merk, nama_merk)
            VALUES (%s, %s)
        """

        cursor.execute(
            sql,
            (data["id_merk"], data["nama_merk"])
        )

        conn.commit()
        return True
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def update(id_merk, data):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        sql = """
            UPDATE merk
            SET nama_merk = %s
            WHERE id_merk = %s
        """

        cursor.execute(
            sql,
            (data["nama_merk"], id_merk)
        )

        conn.commit()
        return cursor.rowcount
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def patch(id_merk, data):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        sql = """
            UPDATE merk
            SET nama_merk = %s
            WHERE id_merk = %s
        """

        cursor.execute(
            sql,
            (data["nama_merk"], id_merk)
        )

        conn.commit()
        return cursor.rowcount
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def delete(id_merk):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "DELETE FROM merk WHERE id_merk = %s",
            (id_merk,)
        )

        conn.commit()
        return cursor.rowcount
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
