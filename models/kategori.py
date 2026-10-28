
from db import get_connection


def get_all():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM kategori")
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


def get_by_id(id_kategori):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM kategori WHERE id_kategori = %s",
            (id_kategori,)
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
            INSERT INTO kategori (id_kategori, nama_kategori)
            VALUES (%s, %s)
            """,
            (data["id_kategori"], data["nama_kategori"])
        )
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def update(id_kategori, data):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE kategori
            SET nama_kategori = %s
            WHERE id_kategori = %s
            """,
            (data["nama_kategori"], id_kategori)
        )
        connection.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        connection.close()


def delete(id_kategori):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "DELETE FROM kategori WHERE id_kategori = %s",
            (id_kategori,)
        )
        connection.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        connection.close()
