# Dokumentasi REST API Toko Elektronik

Dokumentasi ini berisi panduan pengujian backend API Toko Elektronik menggunakan Flask dan MySQL melalui Postman.

> **Catatan:** Endpoint di bawah mengikuti pola route yang dibahas dalam proyek. Cocokkan kembali dengan route yang benar-benar terdaftar di kode Flask, terutama untuk nama path seperti `detail-supply`, `unit-produk`, dan `detail-pembelian`.

## 1. Informasi Umum

- **Base URL lokal:** `http://127.0.0.1:5000`
- **Format data:** JSON
- **Header untuk request dengan body:** `Content-Type: application/json`
- **Framework backend:** Flask
- **Database:** MySQL

### Endpoint pemeriksaan sistem

| Method | URL | Kegunaan |
|---|---|---|
| GET | `http://127.0.0.1:5000/` | Memastikan server Flask aktif |
| GET | `http://127.0.0.1:5000/test-db` | Memeriksa koneksi database |

## 2. HTTP Method

| Method | Fungsi | Body |
|---|---|---|
| `GET` | Mengambil semua data atau satu data berdasarkan ID | Tidak diperlukan |
| `POST` | Menambahkan data baru | JSON sesuai field wajib |
| `PUT` | Memperbarui data secara keseluruhan | Seluruh field wajib sesuai validasi |
| `PATCH` | Memperbarui sebagian data | Hanya field yang ingin diubah |
| `DELETE` | Menghapus data berdasarkan ID | Tidak diperlukan |

## 3. Daftar Endpoint

Ganti `{id}` dengan ID record yang tersedia di database.

| Resource | GET semua data | GET berdasarkan ID | POST | PUT | PATCH | DELETE |
|---|---|---|---|---|---|---|
| Customer | `GET /api/customer` | `GET /api/customer/{id}` | `POST /api/customer` | `PUT /api/customer/{id}` | `PATCH /api/customer/{id}` | `DELETE /api/customer/{id}` |
| Produk | `GET /api/produk` | `GET /api/produk/{id}` | `POST /api/produk` | `PUT /api/produk/{id}` | `PATCH /api/produk/{id}` | `DELETE /api/produk/{id}` |
| Kategori | `GET /api/kategori` | `GET /api/kategori/{id}` | `POST /api/kategori` | `PUT /api/kategori/{id}` | `PATCH /api/kategori/{id}` | `DELETE /api/kategori/{id}` |
| Merk | `GET /api/merk` | `GET /api/merk/{id}` | `POST /api/merk` | `PUT /api/merk/{id}` | `PATCH /api/merk/{id}` | `DELETE /api/merk/{id}` |
| Supplier | `GET /api/supplier` | `GET /api/supplier/{id}` | `POST /api/supplier` | `PUT /api/supplier/{id}` | `PATCH /api/supplier/{id}` | `DELETE /api/supplier/{id}` |
| Supply | `GET /api/supply` | `GET /api/supply/{id}` | `POST /api/supply` | `PUT /api/supply/{id}` | `PATCH /api/supply/{id}` | `DELETE /api/supply/{id}` |
| Detail Supply | `GET /api/detail-supply` | `GET /api/detail-supply/{id}` | `POST /api/detail-supply` | `PUT /api/detail-supply/{id}` | `PATCH /api/detail-supply/{id}` | `DELETE /api/detail-supply/{id}` |
| Unit Produk | `GET /api/unit-produk` | `GET /api/unit-produk/{id}` | `POST /api/unit-produk` | `PUT /api/unit-produk/{id}` | `PATCH /api/unit-produk/{id}` | `DELETE /api/unit-produk/{id}` |
| Pembelian | `GET /api/pembelian` | `GET /api/pembelian/{id}` | `POST /api/pembelian` | `PUT /api/pembelian/{id}` | `PATCH /api/pembelian/{id}` | `DELETE /api/pembelian/{id}` |
| Detail Pembelian | `GET /api/detail-pembelian` | `GET /api/detail-pembelian/{id}` | `POST /api/detail-pembelian` | `PUT /api/detail-pembelian/{id}` | `PATCH /api/detail-pembelian/{id}` | `DELETE /api/detail-pembelian/{id}` |

### Contoh ID untuk pengujian

| Resource | Contoh ID |
|---|---|
| Customer | `CUS001` |
| Produk | `PRD001` |
| Kategori | `KAT001` |
| Merk | `MRK001` |
| Supplier | `SUP001` |
| Supply | `SUPPLY001` |
| Detail Supply | `DS001` |
| Unit Produk | `SRL001` |
| Pembelian | `BL001` |
| Detail Pembelian | `DPB001` |

Contoh ID di atas hanya digunakan jika record tersebut benar-benar ada di database kamu.

## 4. Contoh Pengujian di Postman

Untuk request yang menggunakan body, pilih **Body → raw → JSON**.

### 4.1 POST — menambahkan produk

- **Method:** `POST`
- **URL:** `http://127.0.0.1:5000/api/produk`

```json
{
  "id_produk": "PRD006",
  "id_merk": "MRK001",
  "id_kategori": "KAT001",
  "nama_produk": "Samsung Galaxy A56",
  "harga_produk": 5999000,
  "stok": 10,
  "diskon_produk": 5
}
```

Pastikan `MRK001` dan `KAT001` sudah tersedia di database, serta `PRD006` belum digunakan.

### 4.2 PUT — memperbarui seluruh data produk

- **Method:** `PUT`
- **URL:** `http://127.0.0.1:5000/api/produk/PRD001`

```json
{
  "id_produk": "PRD001",
  "id_merk": "MRK001",
  "id_kategori": "KAT001",
  "nama_produk": "Samsung Galaxy A55",
  "harga_produk": 5499000,
  "stok": 10,
  "diskon_produk": 5
}
```

Contoh ini mengasumsikan controller PUT menerima semua field yang dicantumkan dan ID di body harus sama dengan ID pada URL.

### 4.3 PATCH — memperbarui sebagian data produk

- **Method:** `PATCH`
- **URL:** `http://127.0.0.1:5000/api/produk/PRD001`

```json
{
  "stok": 2
}
```

PATCH mengirim field yang ingin diubah saja, selama field tersebut diizinkan oleh validasi controller.

## 5. Field Utama Setiap Tabel

| Tabel | Field |
|---|---|
| Customer | `id_customer`, `nama_customer`, `email_customer`, `password`, `no_telpon_customer` |
| Produk | `id_produk`, `id_merk`, `id_kategori`, `nama_produk`, `harga_produk`, `stok`, `diskon_produk` |
| Kategori | `id_kategori`, `nama_kategori` |
| Merk | `id_merk`, `nama_merk` |
| Supplier | `id_supplier`, `nama_supplier`, `alamat_supplier`, `no_telpon_supplier` |
| Supply | `id_supply`, `id_supplier`, `tanggal_supply` |
| Detail Supply | `id_detail_supply`, `id_supply`, `id_produk`, `jumlah_supply` |
| Unit Produk | `kode_serial`, `id_detail_supply`, `id_produk`, `status` |
| Pembelian | `id_pembelian`, `id_customer`, `tanggal_pembelian`, `total_harga`, `tipe_diskon` |
| Detail Pembelian | `id_detail_pembelian`, `id_pembelian`, `kode_serial`, `harga_beli`, `jumlah_pembelian`, `diskon_pembelian` |

## 6. Urutan Pengujian yang Disarankan

1. Jalankan aplikasi Flask dan pastikan server berjalan pada port `5000`.
2. Jalankan `GET /` untuk memastikan server aktif.
3. Jalankan `GET /test-db` untuk memeriksa koneksi database.
4. Uji `GET` semua data pada setiap resource.
5. Uji `GET` berdasarkan ID dengan ID yang tersedia.
6. Uji `POST` dengan ID baru dan foreign key yang valid.
7. Uji `PUT` dengan seluruh field wajib sesuai validasi controller.
8. Uji `PATCH` dengan satu atau beberapa field yang ingin diubah.
9. Uji `DELETE` hanya pada data pengujian yang aman dihapus.

## 7. Status HTTP yang Umum

| Status | Arti |
|---|---|
| `200 OK` | Request berhasil, misalnya GET, PUT, PATCH, atau DELETE |
| `201 Created` | Data baru berhasil dibuat |
| `400 Bad Request` | JSON atau validasi field tidak sesuai |
| `404 Not Found` | Endpoint atau data berdasarkan ID tidak ditemukan |
| `409 Conflict` | Terjadi konflik, misalnya ID duplikat atau foreign key menghalangi penghapusan |
| `500 Internal Server Error` | Terjadi kesalahan pada server atau proses database |

Status yang dikembalikan dapat berbeda sesuai implementasi controller.

## 8. Catatan Penting

- Kirim nilai numerik sebagai angka JSON, bukan teks. Benar: `"stok": 2`; salah: `"stok": "2"`.
- Field teks harus menggunakan tanda kutip, misalnya `"nama_produk": "Samsung Galaxy A55"`.
- Pastikan setiap foreign key mengacu pada data yang tersedia di database.
- Penghapusan dapat ditolak jika record masih digunakan tabel lain karena relasi database menggunakan `ON DELETE NO ACTION`.
- Jangan mengirim POST berulang kali dengan ID yang sama jika ID tersebut sudah ada.
- Untuk request PUT dan PATCH, ikuti field yang diizinkan dan aturan validasi pada controller masing-masing.
