
import os
import uuid

from datetime import datetime, timedelta, timezone

import jwt

from flask import request, jsonify
from werkzeug.security import check_password_hash
from dotenv import load_dotenv

from models import users

load_dotenv()


def login():

    # Mengambil data JSON
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "status": "error",
            "message": "Request body harus berupa JSON"
        }), 400

    email = data.get("email")
    password = data.get("password")

    # Validasi input
    if not isinstance(email, str) or not isinstance(password, str):
        return jsonify({
            "status": "error",
            "message": "Email dan password wajib diisi"
        }), 400

    email = email.strip()

    if not email or not password:
        return jsonify({
            "status": "error",
            "message": "Email dan password wajib diisi"
        }), 400

    # Memeriksa konfigurasi JWT
    secret_key = os.getenv("JWT_SECRET_KEY")
    issuer = os.getenv("JWT_ISSUER")
    audience = os.getenv("JWT_AUDIENCE")

    if not secret_key or not issuer or not audience:
        return jsonify({
            "status": "error",
            "message": "Konfigurasi JWT belum lengkap"
        }), 500

    # Mencari user berdasarkan email
    user = users.get_by_email(email)

    if not user:
        return jsonify({
            "status": "error",
            "message": "Email atau password salah"
        }), 401

    # Memeriksa password
    if not check_password_hash(user["password"], password):
        return jsonify({
            "status": "error",
            "message": "Email atau password salah"
        }), 401

    # Membuat JWT Claims
    sekarang = datetime.now(timezone.utc)

    payload = {
        "iss": issuer,
        "sub": str(user["id_user"]),
        "aud": audience,
        "iat": int(sekarang.timestamp()),
        "exp": int((sekarang + timedelta(hours=1)).timestamp()),
        "jti": str(uuid.uuid4()),

        # Custom Claims
        "user_id": user["id_user"],
        "nama": user["nama_user"],
        "email": user["email"],
        "role": user["role"]
    }

    # Generate JWT
    token = jwt.encode(
        payload,
        secret_key,
        algorithm="HS256"
    )

    # Respons login berhasil
    return jsonify({
        "status": "success",
        "message": "Login berhasil",
        "access_token": token,
        "token_type": "Bearer",
        "expires_in": 3600,
        "user": {
            "id": user["id_user"],
            "nama": user["nama_user"],
            "email": user["email"],
            "role": user["role"]
        }
    }), 200
