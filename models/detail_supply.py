
from db import get_connection


def get_all():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM detail_supply")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def get_by_id(id_detail_supply):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM detail_supply WHERE id_detail_supply = %s",
            (id_detail_supply,)
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
            INSERT INTO detail_supply (
                id_detail_supply,
                id_supply,
                id_produk,
                jumlah_supply
            ) VALUES (%s, %s, %s, %s)
        """

        values = (
            data["id_detail_supply"],
            data["id_supply"],
            data["id_produk"],
            data["jumlah_supply"]
        )

        cursor.execute(sql, values)
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def update(id_detail_supply, data):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        sql = """
            UPDATE detail_supply
            SET id_supply = %s,
                id_produk = %s,
                jumlah_supply = %s
            WHERE id_detail_supply = %s
        """

        values = (
            data["id_supply"],
            data["id_produk"],
            data["jumlah_supply"],
            id_detail_supply
        )

        cursor.execute(sql, values)
        conn.commit()
        return cursor.rowcount
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def patch(id_detail_supply, data):
    kolom_diizinkan = {
        "id_supply",
        "id_produk",
        "jumlah_supply"
    }

    perubahan = {
        key: value
        for key, value in data.items()
        if key in kolom_diizinkan
    }

    if not perubahan:
        return 0

    conn = get_connection()
    cursor = conn.cursor()

    try:
        set_clause = ", ".join(
            f"{kolom} = %s" for kolom in perubahan
        )

        sql = f"""
            UPDATE detail_supply
            SET {set_clause}
            WHERE id_detail_supply = %s
        """

        values = list(perubahan.values())
        values.append(id_detail_supply)

        cursor.execute(sql, tuple(values))
        conn.commit()
        return cursor.rowcount
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def delete(id_detail_supply):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "DELETE FROM detail_supply WHERE id_detail_supply = %s",
            (id_detail_supply,)
        )
        conn.commit()
        return cursor.rowcount
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
