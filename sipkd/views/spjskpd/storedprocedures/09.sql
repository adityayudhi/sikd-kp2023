/*
	@flex: ~/sipkd_AKUNTANSI_PEMDA/src/spjAkuntansiPemda/views/Akrual/VInputJurnalAkrualPPKD.mxml @ lihatBukti();
	@author: mbamad;
	@vendor: firebird;
	@origin: AKRUAL_VIEW_TRANSAKSI_PPKD();

	@usage: APP2 => "akuntansi" => "akuntansi akrual ppkd" => tambah(JURNAL-UMUM|JU) => browse|cari();
*/

/* [SAFE] */
DO $execute$ BEGIN PERFORM __rmfn__('akuntansi.anov_jurnal_ppkd_ju_browse'); END $execute$;

CREATE OR REPLACE FUNCTION akuntansi.anov_jurnal_ppkd_ju_browse(tahun VARCHAR, bulan INTEGER DEFAULT 0)
RETURNS TABLE(
	kodeurusan INTEGER, kodesuburusan INTEGER, kodeorganisasi VARCHAR,

	nobukti VARCHAR, jenisbukti VARCHAR,
	tanggalbukti TIMESTAMP /* ganti [tglbukti] menyesuaikan ${akuntansi.akrual_buku_jurnal} */,

	no_bku VARCHAR /* ganti [nobku] menyesuaikan ${akuntansi.akrual_buku_jurnal} */,
	tgl_bku TIMESTAMP,
	jenis_transaksi VARCHAR /* ganti [jenis_bku] menyesuaikan ${akuntansi.akrual_buku_jurnal} */,

	nobukukas VARCHAR, tglbukukas TIMESTAMP, jenisbukukas VARCHAR,
	nosp2d VARCHAR, tglsp2d TIMESTAMP, jenissp2d VARCHAR,

	keterangan TEXT /* ganti [deskripsi] menyesuaikan ${akuntansi.akrual_buku_jurnal} */,
	jumlah NUMERIC(15,2) /* ganti [nominal] supaya lebih general */,
	ispihakketiga INTEGER,
	penerima VARCHAR(128)
)
AS $storedprocedure$
/* @version: 20190724; @author: anovsiradj; */

#VARIABLE_CONFLICT use_variable
DECLARE isskpd INT := 1;
DECLARE sp2d_non_pihak3 VARCHAR[] := array['UP','GU','TU'];

BEGIN
	/* skpkd */
	SELECT a.kodeurusan,a.kodesuburusan,a.kodeorganisasi FROM master.master_organisasi a
	WHERE a.tahun = tahun AND a.kodeorganisasi <> '' AND a.skpkd = isskpd
	INTO kodeurusan,kodesuburusan,kodeorganisasi;

	/* #################################################################################################### */

	/* --- (mbamad) PENERBITAN SKP/SKR --- */
	FOR nobukti, tanggalbukti, keterangan, jenis_transaksi
	IN SELECT a.nomor, a.tanggal, a.uraian, a.jenis
	FROM penatausahaan.skp a WHERE a.tahun = tahun
	AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
	AND EXTRACT(MONTH FROM a.tanggal) = bulan
	AND a.isskpd = isskpd
	AND a.nomor NOT IN (
		SELECT b.nobukti FROM akuntansi.akrual_buku_jurnal b WHERE b.tahun = tahun
		AND b.kodeurusan = kodeurusan AND b.kodesuburusan = kodesuburusan AND b.kodeorganisasi = kodeorganisasi
		AND b.jenis_transaksi in ('SKP','SKR')
		AND b.isskpd = isskpd
	)
	GROUP BY a.nomor, a.tanggal, a.uraian, a.jenis LOOP
		penerima := NULL;

		/* (anov) explicit */
		jenisbukti := jenis_transaksi;

		SELECT COALESCE(sum(a.jumlah),0)
		FROM penatausahaan.skp_rincian a WHERE a.tahun = tahun
		AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
		AND a.nomor = nobukti INTO jumlah;

		RETURN NEXT;
	END LOOP;

	/* --- (mbamad) pindah buku bud --- */
	FOR nobukti, tanggalbukti, keterangan, jenissp2d, jenis_transaksi, no_bku
	IN SELECT a.nobukti, a.tanggal, a.deskripsi, a.jenissp2d, a.jenistransaksi, a.nobukukas
	FROM kasda.kasda_transaksi a WHERE a.tahun = tahun
	AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
	AND EXTRACT(MONTH FROM a.tanggal) = bulan
	AND a.jenistransaksi = 'PINDAHBUKU'
	AND a.kodesumberdana = 99
	AND a.nobukti NOT IN (
		SELECT b.nobukti FROM akuntansi.akrual_buku_jurnal b WHERE b.tahun = tahun
		AND b.kodeurusan = kodeurusan AND b.kodesuburusan = kodesuburusan AND b.kodeorganisasi = kodeorganisasi
		AND b.jenis_transaksi = a.jenistransaksi
		AND b.isskpd = isskpd
	)
	ORDER BY a.tanggal, a.nobukti LOOP
		penerima = 'BUD';

		/* (anov) explicit */
		nobukukas := no_bku;
		tglbukukas := tanggalbukti;
		jenisbukukas := jenis_transaksi;

		SELECT COALESCE(SUM(a.penerimaan),0) 
		FROM kasda.kasda_transaksi_detil a WHERE a.tahun = tahun
		AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
		AND a.nobukukas = no_bku INTO jumlah;

		RETURN NEXT;
	END LOOP;

	/* --- (mbamad) pengembalian tahun kemarin --- */
	FOR nobukti,tanggalbukti,keterangan,jenissp2d,jenis_transaksi,no_bku
	IN SELECT a.nobukti,a.tanggal,a.deskripsi,a.jenissp2d,a.jenistransaksi,a.nobukukas
	FROM kasda.kasda_transaksi a WHERE a.tahun = tahun
	AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
	AND EXTRACT(MONTH FROM a.tanggal) = bulan
	AND a.jenistransaksi = 'CONTRAKEMARIN'
	AND a.nobukti NOT IN (
		SELECT b.nobukti FROM akuntansi.akrual_buku_jurnal b WHERE b.tahun = tahun
		AND b.kodeurusan = kodeurusan AND b.kodesuburusan = kodesuburusan AND b.kodeorganisasi = kodeorganisasi
		AND b.jenis_transaksi = a.jenistransaksi
		AND b.isskpd = isskpd
	)
	ORDER BY a.tanggal, a.nobukti LOOP
	   penerima := 'BUD';

	   /* (anov) explicit */
	   nobukukas := no_bku;
	   tglbukukas := tanggalbukti;
	   jenisbukukas := jenis_transaksi;

	   SELECT COALESCE(SUM(a.penerimaan - a.pengeluaran), 0)
	   FROM kasda.kasda_transaksi_detil a WHERE a.tahun = tahun
	   AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
	   AND a.nobukukas = no_bku INTO jumlah;

	   RETURN NEXT;
	END LOOP;

	/* --- (mbamad) pengembalian tahun berjalan --- */
	FOR nobukti,tanggalbukti,keterangan,jenissp2d,jenis_transaksi,no_bku
	IN SELECT a.nobukti,a.tanggal,a.deskripsi,a.jenissp2d,a.jenistransaksi,a.nobukukas
	FROM kasda.kasda_transaksi a WHERE a.tahun = tahun
	AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
	AND EXTRACT(MONTH FROM a.tanggal) = bulan
	AND a.jenistransaksi = 'CONTRA'
	AND a.nobukti NOT IN (
		SELECT b.nobukti FROM akuntansi.akrual_buku_jurnal b WHERE b.tahun = tahun
		AND b.kodeurusan = kodeurusan AND b.kodesuburusan = kodesuburusan AND b.kodeorganisasi = kodeorganisasi
		AND b.jenis_transaksi = a.jenistransaksi
		AND b.isskpd = isskpd
	)
	ORDER BY a.tanggal,a.nobukti LOOP
	   penerima := 'BUD';

	   /* (anov) explicit */
	   nobukukas := no_bku;
	   tglbukukas := tanggalbukti;
	   jenisbukukas := jenis_transaksi;

	   SELECT COALESCE(SUM(a.penerimaan - a.pengeluaran), 0)
	   FROM kasda.kasda_transaksi_detil a WHERE a.tahun = tahun
	   AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
	   AND a.nobukukas = no_bku INTO jumlah;

	   RETURN NEXT;
	END LOOP;

	/* --- (mbamad) penerimaan pendapatan bud --- */
	FOR nobukti,tanggalbukti,keterangan,jenissp2d,jenis_transaksi,no_bku
	IN SELECT a.nobukti,a.tanggal,a.deskripsi,a.jenissp2d,a.jenistransaksi,a.nobukukas
	FROM kasda.kasda_transaksi a WHERE a.tahun = tahun 
	AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
	AND EXTRACT(MONTH FROM a.tanggal) = bulan
	AND a.jenistransaksi = 'STS'
	AND a.nobukti NOT IN (
		SELECT b.nobukti FROM akuntansi.akrual_buku_jurnal b WHERE b.tahun = tahun 
		AND b.kodeurusan = kodeurusan AND b.kodesuburusan = kodesuburusan AND b.kodeorganisasi = kodeorganisasi
		AND b.jenis_transaksi = a.jenistransaksi
		AND b.isskpd = isskpd
	)
	ORDER BY a.tanggal,a.nobukti LOOP
		/* (anov) explicit */
		nobukukas := no_bku;
		tglbukukas := tanggalbukti;
		jenisbukukas := jenis_transaksi;

		penerima := 'BUD';

		SELECT COALESCE(SUM(a.penerimaan - a.pengeluaran), 0)
		FROM kasda.kasda_transaksi_detil a WHERE a.tahun = tahun 
		AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi 
		AND a.nobukukas = no_bku INTO jumlah;

		RETURN NEXT;
	END LOOP;

	/* --- (mbamad) PENERBITAN SP2D KE SKPD --- */
	FOR nobukti,tanggalbukti,keterangan,jenissp2d,jenis_transaksi,no_bku
	IN SELECT a.nobukti,a.tanggal,a.deskripsi,a.jenissp2d,a.jenistransaksi,a.nobukukas
	FROM kasda.kasda_transaksi a WHERE a.tahun = tahun
	AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
	AND EXTRACT(MONTH FROM a.tanggal) = bulan
	AND a.jenistransaksi = 'SP2D'
	AND a.nobukti NOT IN (
		SELECT b.nobukti FROM akuntansi.akrual_buku_jurnal b WHERE b.tahun = tahun
		AND b.kodeurusan = kodeurusan AND b.kodesuburusan = kodesuburusan AND b.kodeorganisasi = kodeorganisasi
		AND b.jenis_transaksi = a.jenistransaksi
		AND b.isskpd = isskpd
	)
	ORDER BY a.tanggal,a.nobukti LOOP
		/* (anov) explicit */
		nobukukas := no_bku;
		tglbukukas := tanggalbukti;
		jenisbukukas := jenis_transaksi;

		SELECT a.namayangberhak FROM penatausahaan.sp2d a WHERE a.tahun = tahun
		AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
		AND a.nosp2d = nobukti INTO penerima;
		IF (UPPER(penerima) LIKE 'BEND%') THEN ispihakketiga := 0; ELSE ispihakketiga := 1; END IF;
		IF (jenissp2d = ANY(sp2d_non_pihak3)) THEN ispihakketiga := 0; END IF; /* (anov) supaya lebih spesifik */

		SELECT COALESCE(SUM(a.jumlah),0) FROM penatausahaan.sp2drincian a WHERE a.tahun = tahun
		AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
		AND a.nosp2d = nobukti INTO jumlah;

		RETURN NEXT;
	END LOOP;

	/* --- (mbamad) PENERBITAN SP2D KE SKPD YANG TIDAK CAIR --- */
	FOR nobukti,tanggalbukti,jenissp2d,keterangan
	IN SELECT
		a.nosp2d,a.tanggal,a.jenissp2d,
		('SP2D Tidak Cair pada No. '|| TRIM(a.nosp2d) || ' untuk ' || TRIM(a.statuskeperluan))
	FROM penatausahaan.sp2d a WHERE a.tahun = tahun
	AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
	AND EXTRACT(MONTH FROM a.tanggal) = bulan
	AND a.tglkasda IS NULL
	AND a.nosp2d NOT IN (
		SELECT b.nobukti FROM akuntansi.akrual_buku_jurnal b WHERE b.tahun = tahun
		AND b.kodeurusan = kodeurusan AND b.kodesuburusan = kodesuburusan AND b.kodeorganisasi = kodeorganisasi
		AND b.jenis_transaksi = 'TIDAKCAIR'
		AND b.isskpd = isskpd
	)
	ORDER BY a.tanggal,a.nosp2d LOOP
		no_bku := 0;
		jenis_transaksi := 'TIDAKCAIR';

		/* (anov) explicit */
		nosp2d := nobukti;
		tglsp2d := tanggalbukti;

		SELECT a.namayangberhak FROM penatausahaan.sp2d a WHERE a.tahun = tahun
		AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
		AND a.nosp2d = nobukti INTO penerima;
		IF (UPPER(penerima) LIKE 'BEND%') THEN ispihakketiga := 0; ELSE ispihakketiga := 1; END IF;
		IF (jenissp2d = ANY(sp2d_non_pihak3)) THEN ispihakketiga := 0; END IF; /* (anov) supaya lebih spesifik */

		SELECT COALESCE(SUM(a.jumlah),0) FROM penatausahaan.sp2drincian a WHERE a.tahun = tahun
		AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
		AND a.nosp2d = nobukti INTO jumlah;

		RETURN NEXT;
	END LOOP;

	/* #################################################################################################### */
END; $storedprocedure$ LANGUAGE plpgsql;

/* [LINT] */
DO $execute$ BEGIN
	PERFORM akuntansi.anov_jurnal_ppkd_ju_browse('2019');

	FOR i IN 1..12 LOOP
		PERFORM akuntansi.anov_jurnal_ppkd_ju_browse('2019', i);
	END LOOP;
END $execute$;
