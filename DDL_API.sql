
-- =========================================
-- 1. TABEL USERS
-- =========================================

CREATE TABLE IF NOT EXISTS `users` (
    `id_user` CHAR(20) NOT NULL,
    `nama_user` VARCHAR(50) NOT NULL,
    `email` VARCHAR(50) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    `no_telepon` VARCHAR(50) NOT NULL,
    `role` VARCHAR(20) NOT NULL DEFAULT 'customer',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id_user`),
    UNIQUE (`email`)
);


-- =========================================
-- 2. TABEL PEMBELIAN
-- =========================================

CREATE TABLE IF NOT EXISTS `pembelian` (
    `id_pembelian` CHAR(20) NOT NULL,
    `id_user` CHAR(20) NOT NULL,
    `tanggal_pembelian` DATETIME NOT NULL,
    `total_harga` DECIMAL(12,2) NOT NULL,
    `tipe_diskon` TINYINT NOT NULL,
    PRIMARY KEY (`id_pembelian`)
);


-- =========================================
-- 3. TABEL DETAIL PEMBELIAN
-- =========================================

CREATE TABLE IF NOT EXISTS `detail_pembelian` (
    `id_detail_pembelian` CHAR(20) NOT NULL,
    `id_pembelian` CHAR(20) NOT NULL,
    `kode_serial` CHAR(20) NOT NULL,
    `harga_beli` DECIMAL(12,2) NOT NULL,
    `jumlah_pembelian` INT NOT NULL,
    `diskon_pembelian` DECIMAL(5,2) NOT NULL,
    PRIMARY KEY (`id_detail_pembelian`)
);


-- =========================================
-- 4. TABEL PRODUK
-- =========================================

CREATE TABLE IF NOT EXISTS `produk` (
    `id_produk` CHAR(20) NOT NULL,
    `id_merk` CHAR(20) NOT NULL,
    `id_kategori` CHAR(20) NOT NULL,
    `nama_produk` VARCHAR(255) NOT NULL,
    `harga_produk` DECIMAL(12,2) NOT NULL,
    `stok` INT DEFAULT 0,
    `diskon_produk` DECIMAL(5,2) NOT NULL DEFAULT 0,
    PRIMARY KEY (`id_produk`)
);


-- =========================================
-- 5. TABEL KATEGORI
-- =========================================

CREATE TABLE IF NOT EXISTS `kategori` (
    `id_kategori` CHAR(20) NOT NULL,
    `nama_kategori` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`id_kategori`)
);


-- =========================================
-- 6. TABEL MERK
-- =========================================

CREATE TABLE IF NOT EXISTS `merk` (
    `id_merk` CHAR(20) NOT NULL,
    `nama_merk` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`id_merk`)
);


-- =========================================
-- 7. TABEL SUPPLY
-- =========================================

CREATE TABLE IF NOT EXISTS `supply` (
    `id_supply` CHAR(20) NOT NULL,
    `id_supplier` CHAR(20) NOT NULL,
    `tanggal_supply` DATETIME NOT NULL,
    PRIMARY KEY (`id_supply`)
);


-- =========================================
-- 8. TABEL SUPPLIER
-- =========================================

CREATE TABLE IF NOT EXISTS `supplier` (
    `id_supplier` CHAR(20) NOT NULL,
    `nama_supplier` VARCHAR(50) NOT NULL,
    `alamat_supplier` VARCHAR(255) NOT NULL,
    `no_telpon_supplier` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`id_supplier`)
);


-- =========================================
-- 9. TABEL DETAIL SUPPLY
-- =========================================

CREATE TABLE IF NOT EXISTS `detail_supply` (
    `id_detail_supply` CHAR(20) NOT NULL,
    `id_supply` CHAR(20) NOT NULL,
    `id_produk` CHAR(20) NOT NULL,
    `jumlah_supply` INT NOT NULL,
    PRIMARY KEY (`id_detail_supply`)
);


-- =========================================
-- 10. TABEL UNIT PRODUK
-- =========================================

CREATE TABLE IF NOT EXISTS `unit_produk` (
    `kode_serial` CHAR(20) NOT NULL,
    `id_detail_supply` CHAR(20) NOT NULL,
    `id_produk` CHAR(20) NOT NULL,
    `status` VARCHAR(20) NOT NULL,
    PRIMARY KEY (`kode_serial`)
);


-- =========================================
-- FOREIGN KEY
-- =========================================

-- Pembelian -> Users
ALTER TABLE `pembelian`
ADD CONSTRAINT `fk_pembelian_users`
FOREIGN KEY (`id_user`)
REFERENCES `users` (`id_user`)
ON UPDATE NO ACTION
ON DELETE NO ACTION;


-- Detail Pembelian -> Pembelian
ALTER TABLE `detail_pembelian`
ADD CONSTRAINT `fk_detail_pembelian_pembelian`
FOREIGN KEY (`id_pembelian`)
REFERENCES `pembelian` (`id_pembelian`)
ON UPDATE NO ACTION
ON DELETE NO ACTION;


-- Detail Pembelian -> Unit Produk
ALTER TABLE `detail_pembelian`
ADD CONSTRAINT `fk_detail_pembelian_unit_produk`
FOREIGN KEY (`kode_serial`)
REFERENCES `unit_produk` (`kode_serial`)
ON UPDATE NO ACTION
ON DELETE NO ACTION;


-- Produk -> Merk
ALTER TABLE `produk`
ADD CONSTRAINT `fk_produk_merk`
FOREIGN KEY (`id_merk`)
REFERENCES `merk` (`id_merk`)
ON UPDATE NO ACTION
ON DELETE NO ACTION;


-- Produk -> Kategori
ALTER TABLE `produk`
ADD CONSTRAINT `fk_produk_kategori`
FOREIGN KEY (`id_kategori`)
REFERENCES `kategori` (`id_kategori`)
ON UPDATE NO ACTION
ON DELETE NO ACTION;


-- Supply -> Supplier
ALTER TABLE `supply`
ADD CONSTRAINT `fk_supply_supplier`
FOREIGN KEY (`id_supplier`)
REFERENCES `supplier` (`id_supplier`)
ON UPDATE NO ACTION
ON DELETE NO ACTION;


-- Detail Supply -> Supply
ALTER TABLE `detail_supply`
ADD CONSTRAINT `fk_detail_supply_supply`
FOREIGN KEY (`id_supply`)
REFERENCES `supply` (`id_supply`)
ON UPDATE NO ACTION
ON DELETE NO ACTION;


-- Detail Supply -> Produk
ALTER TABLE `detail_supply`
ADD CONSTRAINT `fk_detail_supply_produk`
FOREIGN KEY (`id_produk`)
REFERENCES `produk` (`id_produk`)
ON UPDATE NO ACTION
ON DELETE NO ACTION;


-- Unit Produk -> Detail Supply
ALTER TABLE `unit_produk`
ADD CONSTRAINT `fk_unit_produk_detail_supply`
FOREIGN KEY (`id_detail_supply`)
REFERENCES `detail_supply` (`id_detail_supply`)
ON UPDATE NO ACTION
ON DELETE NO ACTION;


-- Unit Produk -> Produk
ALTER TABLE `unit_produk`
ADD CONSTRAINT `fk_unit_produk_produk`
FOREIGN KEY (`id_produk`)
REFERENCES `produk` (`id_produk`)
ON UPDATE NO ACTION
ON DELETE NO ACTION;
