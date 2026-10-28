
from flask import Flask, jsonify
from db import get_connection

# Import routes setiap tabel
from routes.customer_routes import customer_bp
from routes.produk_routes import produk_bp
from routes.pembelian_routes import pembelian_bp
from routes.supplier_routes import supplier_bp
from routes.detail_pembelian_routes import detail_pembelian_bp
from routes.unit_produk_routes import unit_produk_bp
from routes.supply_routes import supply_bp
from routes.detail_supply_routes import detail_supply_bp
from routes.merk_routes import merk_bp

app = Flask(__name__)

# Registrasi Blueprint
app.register_blueprint(customer_bp)
app.register_blueprint(produk_bp)
app.register_blueprint(pembelian_bp)
app.register_blueprint(supplier_bp)
app.register_blueprint(detail_pembelian_bp)
app.register_blueprint(unit_produk_bp)
app.register_blueprint(supply_bp)
app.register_blueprint(detail_supply_bp)
app.register_blueprint(merk_bp)


# Endpoint halaman utama
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "pesan": "Backend API Toko Elektronik aktif.",
        "status": "success"
    }), 200


# Endpoint untuk mengecek koneksi database
@app.route("/test-db", methods=["GET"])
def test_db():
    conn = None

    try:
        conn = get_connection()

        if conn.is_connected():
            return jsonify({
                "pesan": "Koneksi database berhasil.",
                "database": "api",
                "status": "success"
            }), 200

        return jsonify({
            "pesan": "Koneksi database gagal.",
            "status": "error"
        }), 500

    except Exception:
        return jsonify({
            "pesan": "Tidak dapat terhubung ke database.",
            "status": "error"
        }), 500

    finally:
        if conn is not None and conn.is_connected():
            conn.close()


# Menjalankan server Flask
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
