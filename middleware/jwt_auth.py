import os
import jwt

from functools import wraps
from flask import request, jsonify, g
from dotenv import load_dotenv


# ==========================================
# LOAD ENVIRONMENT
# ==========================================

load_dotenv()


# ==========================================
# MIDDLEWARE JWT AUTHENTICATION
# ==========================================

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({
                "status": "error",
                "message": "Authorization header tidak ditemukan"
            }), 401

        if not auth_header.startswith("Bearer "):
            return jsonify({
                "status": "error",
                "message": "Format token harus Bearer <token>"
            }), 401

        token = auth_header.split(" ", 1)[1].strip()

        if not token:
            return jsonify({
                "status": "error",
                "message": "Token tidak boleh kosong"
            }), 401

        secret_key = os.getenv("JWT_SECRET_KEY")

        if not secret_key:
            return jsonify({
                "status": "error",
                "message": "JWT_SECRET_KEY belum dikonfigurasi"
            }), 500

        try:
            payload = jwt.decode(
                token,
                secret_key,
                algorithms=["HS256"],
                issuer=os.getenv("JWT_ISSUER"),
                audience=os.getenv("JWT_AUDIENCE")
            )

            id_user = payload.get("id_user")
            role = payload.get("role")

            if not id_user or not role:
                return jsonify({
                    "status": "error",
                    "message": "Token tidak memiliki informasi pengguna yang lengkap"
                }), 401

            g.current_user = payload

        except jwt.ExpiredSignatureError:
            return jsonify({
                "status": "error",
                "message": "Token sudah kedaluwarsa"
            }), 401

        except jwt.InvalidIssuerError:
            return jsonify({
                "status": "error",
                "message": "Issuer token tidak valid"
            }), 401

        except jwt.InvalidAudienceError:
            return jsonify({
                "status": "error",
                "message": "Audience token tidak valid"
            }), 401

        except jwt.InvalidTokenError:
            return jsonify({
                "status": "error",
                "message": "Token tidak valid"
            }), 401


        return f(*args, **kwargs)

    return decorated