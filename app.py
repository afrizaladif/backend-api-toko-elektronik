from flask import Flask, jsonify
from db import get_connection


# ==========================================
# IMPORT ROUTES / BLUEPRINT
# ==========================================

from routes.users_routes import users_bp
from routes.produk_routes import produk_bp
from routes.pembelian_routes import pembelian_bp
from routes.supplier_routes import supplier_bp
from routes.detail_pembelian_routes import detail_pembelian_bp
from routes.unit_produk_routes import unit_produk_bp
from routes.supply_routes import supply_bp
from routes.detail_supply_routes import detail_supply_bp
from routes.merk_routes import merk_bp
from routes.kategori_routes import kategori_bp
from routes.activity_log_routes import activity_log_bp
from middleware.activity_log import register_activity_logger


# ==========================================
# IMPORT ROUTES AUTENTIKASI
# ==========================================

from routes.auth.auth_routes import auth_bp
from routes.auth.admin_auth_routes import admin_auth_bp


# ==========================================
# INISIALISASI FLASK
# ==========================================

app = Flask(__name__)
register_activity_logger(app)

# ==========================================
# REGISTRASI BLUEPRINT
# ==========================================

# Blueprint data utama
app.register_blueprint(users_bp)
app.register_blueprint(produk_bp)
app.register_blueprint(pembelian_bp)
app.register_blueprint(supplier_bp)
app.register_blueprint(detail_pembelian_bp)
app.register_blueprint(unit_produk_bp)
app.register_blueprint(supply_bp)
app.register_blueprint(detail_supply_bp)
app.register_blueprint(merk_bp)
app.register_blueprint(kategori_bp)
app.register_blueprint(activity_log_bp)


# ==========================================
# REGISTRASI BLUEPRINT AUTENTIKASI
# ==========================================

# Blueprint autentikasi user
# Route di dalam auth_bp akan mendapatkan prefix /api
app.register_blueprint(
    auth_bp,
    url_prefix="/api"
)


# Blueprint autentikasi admin
# Route admin sudah memiliki prefix /api di dalam file route
app.register_blueprint(
    admin_auth_bp
)


# ==========================================
# ENDPOINT HALAMAN UTAMA
# ==========================================

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "success",
        "pesan": "Backend API Toko Elektronik aktif."
    }), 200


# ==========================================
# ENDPOINT CEK KONEKSI DATABASE
# ==========================================

@app.route("/test-db", methods=["GET"])
def test_db():
    conn = None

    try:
        conn = get_connection()

        if conn is None:
            return jsonify({
                "status": "error",
                "pesan": "Koneksi database gagal."
            }), 500

        if conn.is_connected():
            return jsonify({
                "status": "success",
                "pesan": "Koneksi database berhasil.",
                "database": "api"
            }), 200

        return jsonify({
            "status": "error",
            "pesan": "Koneksi database tidak aktif."
        }), 500

    except Exception as error:
        print("Error koneksi database:", error)

        return jsonify({
            "status": "error",
            "pesan": "Tidak dapat terhubung ke database."
        }), 500

    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception as error:
                print("Error menutup koneksi database:", error)


# ==========================================
# PENANGANAN ERROR 404
# ==========================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "status": "error",
        "message": "Endpoint tidak ditemukan."
    }), 404


# ==========================================
# PENANGANAN ERROR 500
# ==========================================

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "status": "error",
        "message": "Terjadi kesalahan pada server."
    }), 500



if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )