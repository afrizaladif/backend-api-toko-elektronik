
import os
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

        # Mengambil API Key yang tersimpan di .env
        api_key_valid = os.getenv("API_KEY")

        # Memastikan konfigurasi API Key tersedia
        if not api_key_valid:
            return jsonify({
                "status": "error",
                "message": "Konfigurasi API Key belum diatur"
            }), 500

        # Memeriksa API Key dari client
        if not api_key or api_key != api_key_valid:
            return jsonify({
                "status": "error",
                "message": "API Key tidak valid"
            }), 401

        # Jika valid, lanjutkan ke fungsi berikutnya
        return f(*args, **kwargs)

    return decorated
