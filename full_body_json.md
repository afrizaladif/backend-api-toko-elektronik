# Body JSON Postman — Backend API Toko Elektronik

Dokumen ini berisi contoh body JSON untuk POST, PUT, dan PATCH pada 10 resource API. GET dan DELETE umumnya tidak memerlukan body.

> **Penting:** contoh ini mengikuti field pada skema database yang dibahas. Sesuaikan dengan validasi controller aktif. Pastikan ID baru belum digunakan dan seluruh foreign key sudah ada. Untuk PUT, beberapa controller mungkin mengharuskan ID di body sama dengan ID pada URL. Nilai tanggal mengikuti format yang mungkin diterima controller/database.

## Cara menggunakan
1. Pilih method dan URL sesuai tabel.
2. Di Postman, pilih **Body → raw → JSON**.
3. Untuk PATCH, kirim hanya field yang ingin diubah dan pastikan field itu diizinkan controller.
4. Ganti ID contoh jika sudah ada di database.

## GET dan DELETE
- `GET /api/{resource}` — tidak memakai body.
- `GET /api/{resource}/{id}` — tidak memakai body.
- `DELETE /api/{resource}/{id}` — tidak memakai body.

## Customer

- **POST:** `/api/customer`
- **PUT:** `/api/customer/CUS006`
- **PATCH:** `/api/customer/CUS006`

### POST body
```json
{
  "id_customer": "CUS006",
  "nama_customer": "Budi Santoso",
  "email_customer": "budi@example.com",
  "password": "contohPassword123",
  "no_telpon_customer": "081234567890"
}
```

### PUT body
```json
{
  "nama_customer": "Budi Santoso",
  "email_customer": "budi.updated@example.com",
  "password": "contohPassword456",
  "no_telpon_customer": "081234567891"
}
```

### PATCH body
```json
{
  "nama_customer": "Budi Santoso Baru"
}
```

## Produk

- **POST:** `/api/produk`
- **PUT:** `/api/produk/PRD006`
- **PATCH:** `/api/produk/PRD006`

### POST body
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

### PUT body
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

### PATCH body
```json
{
  "stok": 8
}
```

## Kategori

- **POST:** `/api/kategori`
- **PUT:** `/api/kategori/KAT006`
- **PATCH:** `/api/kategori/KAT006`

### POST body
```json
{
  "id_kategori": "KAT006",
  "nama_kategori": "Audio"
}
```

### PUT body
```json
{
  "id_kategori": "KAT006",
  "nama_kategori": "Audio"
}
```

### PATCH body
```json
{
  "nama_kategori": "Perangkat Audio"
}
```

## Merk

- **POST:** `/api/merk`
- **PUT:** `/api/merk/MRK006`
- **PATCH:** `/api/merk/MRK006`

### POST body
```json
{
  "id_merk": "MRK006",
  "nama_merk": "Sony"
}
```

### PUT body
```json
{
  "id_merk": "MRK006",
  "nama_merk": "Sony"
}
```

### PATCH body
```json
{
  "nama_merk": "Sony Electronics"
}
```

## Supplier

- **POST:** `/api/supplier`
- **PUT:** `/api/supplier/SUP006`
- **PATCH:** `/api/supplier/SUP006`

### POST body
```json
{
  "id_supplier": "SUP006",
  "nama_supplier": "PT Sumber Elektronik",
  "alamat_supplier": "Jl. Merdeka No. 10",
  "no_telpon_supplier": "081234567892"
}
```

### PUT body
```json
{
  "id_supplier": "SUP006",
  "nama_supplier": "PT Sumber Elektronik",
  "alamat_supplier": "Jl. Merdeka No. 10",
  "no_telpon_supplier": "081234567892"
}
```

### PATCH body
```json
{
  "alamat_supplier": "Jl. Pahlawan No. 20"
}
```

## Supply

- **POST:** `/api/supply`
- **PUT:** `/api/supply/SUPPLY006`
- **PATCH:** `/api/supply/SUPPLY006`

### POST body
```json
{
  "id_supply": "SUPPLY006",
  "id_supplier": "SUP001",
  "tanggal_supply": "2026-10-29 09:00:00"
}
```

### PUT body
```json
{
  "id_supply": "SUPPLY006",
  "id_supplier": "SUP001",
  "tanggal_supply": "2026-10-29 09:00:00"
}
```

### PATCH body
```json
{
  "tanggal_supply": "2026-10-30 10:00:00"
}
```

## Detail Supply

- **POST:** `/api/detail-supply`
- **PUT:** `/api/detail-supply/DS006`
- **PATCH:** `/api/detail-supply/DS006`

### POST body
```json
{
  "id_detail_supply": "DS006",
  "id_supply": "SUPPLY001",
  "id_produk": "PRD001",
  "jumlah_supply": 5
}
```

### PUT body
```json
{
  "id_detail_supply": "DS006",
  "id_supply": "SUPPLY001",
  "id_produk": "PRD001",
  "jumlah_supply": 5
}
```

### PATCH body
```json
{
  "jumlah_supply": 6
}
```

## Unit Produk

- **POST:** `/api/unit-produk`
- **PUT:** `/api/unit-produk/SRL006`
- **PATCH:** `/api/unit-produk/SRL006`

### POST body
```json
{
  "kode_serial": "SRL006",
  "id_detail_supply": "DS001",
  "id_produk": "PRD001",
  "status": "Tersedia"
}
```

### PUT body
```json
{
  "kode_serial": "SRL006",
  "id_detail_supply": "DS001",
  "id_produk": "PRD001",
  "status": "Tersedia"
}
```

### PATCH body
```json
{
  "status": "Terjual"
}
```

## Pembelian

- **POST:** `/api/pembelian`
- **PUT:** `/api/pembelian/BL006`
- **PATCH:** `/api/pembelian/BL006`

### POST body
```json
{
  "id_pembelian": "BL006",
  "id_customer": "CUS001",
  "tanggal_pembelian": "2026-10-29 10:00:00",
  "total_harga": 5499000,
  "tipe_diskon": 0
}
```

### PUT body
```json
{
  "id_pembelian": "BL006",
  "id_customer": "CUS001",
  "tanggal_pembelian": "2026-10-29 10:00:00",
  "total_harga": 5499000,
  "tipe_diskon": 0
}
```

### PATCH body
```json
{
  "total_harga": 5399000
}
```

## Detail Pembelian

- **POST:** `/api/detail-pembelian`
- **PUT:** `/api/detail-pembelian/DPB006`
- **PATCH:** `/api/detail-pembelian/DPB006`

### POST body
```json
{
  "id_detail_pembelian": "DPB006",
  "id_pembelian": "BL001",
  "kode_serial": "SRL001",
  "harga_beli": 5499000,
  "jumlah_pembelian": 1,
  "diskon_pembelian": 5
}
```

### PUT body
```json
{
  "id_detail_pembelian": "DPB006",
  "id_pembelian": "BL001",
  "kode_serial": "SRL001",
  "harga_beli": 5499000,
  "jumlah_pembelian": 1,
  "diskon_pembelian": 5
}
```

### PATCH body
```json
{
  "diskon_pembelian": 7
}
```

## Catatan validasi
- Nilai numerik dikirim sebagai angka, bukan teks. Contoh benar: `"stok": 2`, bukan `"stok": "2"`.
- Nilai teks menggunakan tanda kutip.
- Untuk `Customer`, nama tabel di database mungkin menggunakan huruf besar `Customer`; nama tabel tidak mengubah bentuk body JSON.
- Relasi database memakai foreign key; POST/PUT dapat gagal bila ID referensi tidak tersedia.
- DELETE bisa ditolak jika record masih direferensikan tabel lain.
- Contoh ini adalah template pengujian, bukan jaminan semua request diterima tanpa penyesuaian controller.