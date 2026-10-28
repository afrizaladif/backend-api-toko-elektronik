
from flask import Flask
from db import get_connection
from routes.kategori_routes import kategori_bp
from routes.customer_routes import customer_bp
from routes.produk_routes import produk_bp

app = Flask(__name__)

# Mendaftarkan routes kategori
app.register_blueprint(kategori_bp)

# Mendaftarkan routes customer
app.register_blueprint(customer_bp)

app.register_blueprint(produk_bp)

# Endpoint utama
@app.route("/", methods=["GET"])
def home():
    return {
        "message": "REST API Toko Elektronik berjalan",
        "status": "success"
    }, 200


# Endpoint untuk mengecek koneksi database
@app.route("/test-db", methods=["GET"])
def test_db():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE()")

        database = cursor.fetchone()[0]

        return {
            "message": "Koneksi database berhasil",
            "database": database
        }, 200

    except Exception:
        app.logger.exception("Koneksi database gagal")
        return {
            "message": "Koneksi database gagal",
            "status": "error"
        }, 500

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
