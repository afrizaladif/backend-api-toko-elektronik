CREATE TABLE IF NOT EXISTS `Customer` (
	`id_customer` CHAR(20) NOT NULL,
	`nama_customer` VARCHAR(50) NOT NULL,
	`email_customer` VARCHAR(50) NOT NULL,
	`password` VARCHAR(50) NOT NULL,
	`no_telpon_customer` VARCHAR(50) NOT NULL,
	PRIMARY KEY(`id_customer`)
);


CREATE TABLE IF NOT EXISTS `pembelian` (
	`id_pembelian` CHAR(20) NOT NULL UNIQUE,
	`id_customer` CHAR(20) NOT NULL,
	`tanggal_pembelian` DATETIME NOT NULL,
	`total_harga` INTEGER NOT NULL,
	`tipe_diskon` TINYINT NOT NULL,
	PRIMARY KEY(`id_pembelian`)
);


CREATE TABLE IF NOT EXISTS `detail_pembelian` (
	`id_detail_pembelian` CHAR(20) NOT NULL UNIQUE,
	`id_pembelian` CHAR(20) NOT NULL,
	`kode_serial` CHAR(20) NOT NULL,
	`harga_beli` DECIMAL(12,2) NOT NULL,
	`jumlah_pembelian` INTEGER NOT NULL,
	`diskon_pembelian` DECIMAL(5,2) NOT NULL,
	PRIMARY KEY(`id_detail_pembelian`)
);


CREATE TABLE IF NOT EXISTS `produk` (
	`id_produk` CHAR(20) NOT NULL UNIQUE,
	`id_merk` CHAR(20) NOT NULL,
	`id_kategori` CHAR(20) NOT NULL,
	`nama_produk` VARCHAR(255) NOT NULL,
	`harga_produk` DECIMAL(12,2) NOT NULL,
	`stok` INTEGER,
	`diskon_produk` DECIMAL(5,2) NOT NULL,
	PRIMARY KEY(`id_produk`)
);


CREATE TABLE IF NOT EXISTS `kategori` (
	`id_kategori` CHAR(20) NOT NULL UNIQUE,
	`nama_kategori` VARCHAR(50) NOT NULL,
	PRIMARY KEY(`id_kategori`)
);


CREATE TABLE IF NOT EXISTS `merk` (
	`id_merk` CHAR(20) NOT NULL UNIQUE,
	`nama_merk` VARCHAR(50) NOT NULL,
	PRIMARY KEY(`id_merk`)
);


CREATE TABLE IF NOT EXISTS `supply` (
	`id_supply` CHAR(20) NOT NULL UNIQUE,
	`id_supplier` CHAR(20) NOT NULL,
	`tanggal_supply` DATETIME NOT NULL,
	PRIMARY KEY(`id_supply`)
);


CREATE TABLE IF NOT EXISTS `supplier` (
	`id_supplier` CHAR(20) NOT NULL UNIQUE,
	`nama_supplier` VARCHAR(50) NOT NULL,
	`alamat_supplier` VARCHAR(50) NOT NULL,
	`no_telpon_supplier` VARCHAR(50) NOT NULL,
	PRIMARY KEY(`id_supplier`)
);


CREATE TABLE IF NOT EXISTS `detail_supply` (
	`id_detail_supply` CHAR(20) NOT NULL,
	`id_supply` CHAR(20) NOT NULL,
	`id_produk` CHAR(20) NOT NULL,
	`jumlah_supply` INTEGER NOT NULL,
	PRIMARY KEY(`id_detail_supply`)
);


CREATE TABLE IF NOT EXISTS `unit_produk` (
	`kode_serial` CHAR(20) NOT NULL,
	`id_detail_supply` CHAR(20) NOT NULL,
	`id_produk` CHAR(20) NOT NULL,
	`status` VARCHAR(20) NOT NULL,
	PRIMARY KEY(`kode_serial`)
);


ALTER TABLE `unit_produk`
ADD FOREIGN KEY(`id_produk`) REFERENCES `produk`(`id_produk`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `pembelian`
ADD FOREIGN KEY(`id_customer`) REFERENCES `Customer`(`id_customer`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `detail_pembelian`
ADD FOREIGN KEY(`id_pembelian`) REFERENCES `pembelian`(`id_pembelian`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `produk`
ADD FOREIGN KEY(`id_merk`) REFERENCES `merk`(`id_merk`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `produk`
ADD FOREIGN KEY(`id_kategori`) REFERENCES `kategori`(`id_kategori`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `supply`
ADD FOREIGN KEY(`id_supplier`) REFERENCES `supplier`(`id_supplier`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `detail_supply`
ADD FOREIGN KEY(`id_supply`) REFERENCES `supply`(`id_supply`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `detail_supply`
ADD FOREIGN KEY(`id_produk`) REFERENCES `produk`(`id_produk`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `unit_produk`
ADD FOREIGN KEY(`id_detail_supply`) REFERENCES `detail_supply`(`id_detail_supply`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `detail_pembelian`
ADD FOREIGN KEY(`kode_serial`) REFERENCES `unit_produk`(`kode_serial`)
ON UPDATE NO ACTION ON DELETE NO ACTION;