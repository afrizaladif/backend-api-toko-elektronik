
import os
import hmac
from functools import wraps

from flask import request, jsonify
from dotenv import load_dotenv

# Memuat konfigurasi dari file .env
load_dotenv()


def api_key_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        # Mengambil API Key dari header request
        api_key = request.headers.get("x-api-key")

        # Mengambil API Key Admin dari .env
        api_key_valid = os.getenv("API_KEY_ADMIN")

        # Memeriksa konfigurasi API Key
        if not api_key_valid:
            return jsonify({
                "status": "error",
                "message": "Konfigurasi API Key Admin belum diatur"
            }), 500

        # Memeriksa API Key yang dikirim client
        if not api_key or not hmac.compare_digest(
            api_key, api_key_valid
        ):
            return jsonify({
                "status": "error",
                "message": "API Key tidak valid"
            }), 401

        # Jika valid, lanjutkan ke controller
        return f(*args, **kwargs)

    return decorated
