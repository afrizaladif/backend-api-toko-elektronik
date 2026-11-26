
import os
import jwt

from datetime import datetime, timedelta, timezone
from flask import jsonify, request
from dotenv import load_dotenv
from werkzeug.security import check_password_hash

from db import get_connection
from models import users


load_dotenv()


# ==========================================
# MEMBUAT JWT ADMIN
# ==========================================

def generate_admin_token(admin):
    secret_key = os.getenv("JWT_SECRET_KEY")
    issuer = os.getenv("JWT_ISSUER")
    audience = os.getenv("JWT_AUDIENCE")

    if not secret_key:
        raise RuntimeError("JWT_SECRET_KEY belum diatur")

    waktu_sekarang = datetime.now(timezone.utc)

    payload = {
        "id_user": admin["id_user"],
        "role": "admin",
        "iss": issuer,
        "aud": audience,
        "iat": waktu_sekarang,
        "exp": waktu_sekarang + timedelta(hours=2)
    }

    token = jwt.encode(
        payload,
        secret_key,
        algorithm="HS256"
    )

    return token


# ==========================================
# LOGIN ADMIN
# ==========================================

def admin_login():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "status": "error",
            "message": "Request harus berupa JSON"
        }), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "status": "error",
            "message": "Email dan password wajib diisi"
        }), 400

    conn = None
    cursor = None

    try:
        conn = get_connection()

        cursor = conn.cursor(dictionary=True)

        # Mengambil data admin berdasarkan email
        query = """
            SELECT
                id_user,
                nama_user,
                email,
                password,
                role
            FROM users
            WHERE email = %s
              AND role = 'admin'
            LIMIT 1
        """

        cursor.execute(query, (email,))
        admin = cursor.fetchone()

        # Admin tidak ditemukan
        if not admin:
            return jsonify({
                "status": "error",
                "message": "Email atau password salah"
            }), 401

        # Memeriksa password yang tersimpan dalam bentuk hash
        password_hash = admin.get("password")

        if not password_hash or not check_password_hash(
            password_hash,
            password
        ):
            return jsonify({
                "status": "error",
                "message": "Email atau password salah"
            }), 401

        # Membuat JWT setelah login berhasil
        token = generate_admin_token(admin)

        return jsonify({
            "status": "success",
            "message": "Autentikasi admin berhasil",
            "role": "admin",
            "token": token,
            "data": {
                "id_user": admin["id_user"],
                "nama_user": admin["nama_user"],
                "email": admin["email"]
            }
        }), 200

    except Exception as error:
        print("Error admin_login:", error)

        return jsonify({
            "status": "error",
            "message": "Terjadi kesalahan saat login admin"
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()


# ==========================================
# REGISTRASI ADMIN
# ==========================================

def create_admin():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "status": "error",
            "message": "Request harus berupa JSON"
        }), 400

    required_fields = [
        "nama_user",
        "email",
        "password",
        "no_telepon"
    ]

    if not all(data.get(field) for field in required_fields):
        return jsonify({
            "status": "error",
            "message": "Semua field wajib diisi"
        }), 400

    # Memastikan role yang dibuat adalah admin
    data["role"] = "admin"

    try:
        admin_id = users.create_admin(data)

        return jsonify({
            "status": "success",
            "message": "Data admin berhasil ditambahkan",
            "id_user": admin_id
        }), 201

    except ValueError as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 400

    except Exception as error:
        print("Error create_admin:", error)

        return jsonify({
            "status": "error",
            "message": "Gagal membuat akun admin"
        }), 500
