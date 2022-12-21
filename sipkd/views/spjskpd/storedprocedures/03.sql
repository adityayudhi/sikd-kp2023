/*
	[ABANDONED][UNUSED][DEPRECATED]
	@see ~/04.sql
*/

DO $execute$ BEGIN
	PERFORM __rmfn__('akuntansi.anov_jurnal_skpd');
END $execute$;

CREATE OR REPLACE FUNCTION akuntansi.anov_jurnal_skpd(
	tahun CHAR(8),
	kodeurusan INTEGER,
	kodesuburusan INTEGER,
	kodeorganisasi CHAR(8),
	bulan INTEGER
)
RETURNS TABLE(
	noref VARCHAR(16),
	nobukti VARCHAR(128),
	tanggalbukti TIMESTAMP,
	jenisjurnal SMALLINT,
	jenisjurnal_urai VARCHAR(64),
	jenis_transaksi VARCHAR(32),
	jenis_sp2d VARCHAR(32),
	posting SMALLINT,
	posting_urai VARCHAR(32),
	debet NUMERIC(15,2),
	kredit NUMERIC(15,2),
	keterangan TEXT
)
AS $storedprocedure$
/* @version: 20190703; @author: anovsiradj; */
#VARIABLE_CONFLICT use_variable
DECLARE
	xisskpd SMALLINT := 0;
BEGIN
	tahun := TRIM(tahun);
	kodeorganisasi := TRIM(kodeorganisasi);

	FOR
		noref,
		nobukti, tanggalbukti,
		jenisjurnal, jenisjurnal_urai,
		posting, posting_urai,
		keterangan
	IN SELECT
		a.noref,
		a.nobukti, a.tanggalbukti,
		a.jenisjurnal, b.uraian,
		a.posting, __iif__(a.posting = 0, 'Belum Posting'::text, 'Sudah Posting'::text),
		a.keterangan
	FROM akuntansi.akrual_buku_jurnal a
	LEFT JOIN akuntansi.akrual_jenis_jurnal b ON (b.id = a.jenisjurnal AND b.isskpd = a.isskpd)
	WHERE a.tahun = tahun
	AND a.kodeurusan = kodeurusan AND a.kodesuburusan = a.kodesuburusan AND a.kodeorganisasi = a.kodeorganisasi
	AND a.isskpd = xisskpd
	AND EXTRACT(MONTH FROM a.tanggalbukti) = bulan
	ORDER BY a.tanggalbukti, a.noref
	LOOP
		SELECT COALESCE(SUM(a.debet),0), COALESCE(SUM(a.kredit),0)
		FROM akuntansi.akrual_jurnal_rincian a WHERE a.tahun = tahun
		AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
		AND a.isskpd = xisskpd AND a.noref = noref
		INTO debet, kredit;

		RETURN NEXT; -- a.k.a suspend
	END LOOP;
END;
$storedprocedure$ LANGUAGE plpgsql;
