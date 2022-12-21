DO $execute$ BEGIN PERFORM __rmfn__('akuntansi.anov_jurnal_ppkd'); END $execute$;

CREATE OR REPLACE FUNCTION akuntansi.anov_jurnal_ppkd(tahun VARCHAR, bulan INTEGER)
RETURNS TABLE(
	kodeurusan INTEGER,
	kodesuburusan INTEGER,
	kodeorganisasi VARCHAR,
	noref VARCHAR,
	nobukti VARCHAR,
	tanggalbukti TIMESTAMP,
	jenis_transaksi VARCHAR,
	jenisjurnal SMALLINT, jenisjurnal_urai VARCHAR,
	posting SMALLINT, posting_urai VARCHAR,
	debet NUMERIC(15,2),
	kredit NUMERIC(15,2),
	no_bku INTEGER,
	jenissp2d VARCHAR,
	username VARCHAR,
	keterangan VARCHAR
)
AS $storedprocedure$
/* @author: anovsiradj; @version: 20190703-origin, 20190708; */

#VARIABLE_CONFLICT use_variable
DECLARE isskpd INT := 1;

BEGIN
	SELECT a.kodeurusan,a.kodesuburusan,a.kodeorganisasi FROM master.master_organisasi a
	WHERE a.tahun = tahun AND a.kodeorganisasi <> '' AND a.skpkd = isskpd
	INTO kodeurusan,kodesuburusan,kodeorganisasi;

	FOR
		noref,
		jenis_transaksi,
		nobukti, tanggalbukti,
		jenisjurnal, jenisjurnal_urai,
		posting, posting_urai,
		no_bku,
		username,
		jenissp2d,
		keterangan
	IN SELECT
		a.noref,
		a.jenis_transaksi,
		a.nobukti, a.tanggalbukti,
		a.jenisjurnal, b.uraian,
		a.posting, __iif__(a.posting = 0, 'Belum Posting'::VARCHAR, 'Sudah Posting'::VARCHAR),
		a.no_bku,
		a.username,
		a.jenissp2d,
		a.keterangan
	FROM akuntansi.akrual_buku_jurnal a
	LEFT JOIN akuntansi.akrual_jenis_jurnal b ON (b.id = a.jenisjurnal /* AND b.isskpd = a.isskpd */)
	WHERE a.tahun = tahun
	AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
	AND a.isskpd = isskpd
	AND EXTRACT(MONTH FROM a.tanggalbukti) = bulan
	ORDER BY a.tanggalbukti, a.noref
	LOOP
		SELECT COALESCE(SUM(a.debet),0), COALESCE(SUM(a.kredit),0)
		FROM akuntansi.akrual_jurnal_rincian a WHERE a.tahun = tahun
		AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
		AND a.isskpd = isskpd AND a.noref = noref
		INTO debet, kredit;

		RETURN NEXT;
	END LOOP;
END;
$storedprocedure$ LANGUAGE plpgsql;

/* [LINT] */
DO $execute$ BEGIN
	FOR i IN 1..12 LOOP
		RAISE INFO '%',i;
		PERFORM akuntansi.anov_jurnal_ppkd('2019',i);
	END LOOP;
END $execute$;
