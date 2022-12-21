/*
	@flex: ~/sipkd_AKUNTANSI_PEMDA/src/spjAkuntansiPemda/views/Akrual/VInputJurnalAkrualPPKD.mxml @ tampilkanPenutupLO();
	@origin: AKRUAL_VIEW_PENUTUP_LO_PPKD();
	@author: mbamad, ali;
*/

DO $execute$ BEGIN PERFORM __rmfn__('akuntansi.anov_jurnal_ppkd_penutup_lo'); END $execute$;

CREATE OR REPLACE FUNCTION akuntansi.anov_jurnal_ppkd_penutup_lo(
	tahun VARCHAR,
	tglawal TIMESTAMP DEFAULT NULL, tglakhir TIMESTAMP DEFAULT NULL
)
RETURNS TABLE(
	kode_rekening VARCHAR, urai_rekening VARCHAR,
	kodeurusan INTEGER, kodesuburusan INTEGER, kodeorganisasi VARCHAR,
	kodeakun INTEGER, kodekelompok INTEGER, kodejenis INTEGER, kodeobjek INTEGER, koderincianobjek INTEGER,
	debet NUMERIC(15,2), kredit NUMERIC(15,2)
)
AS $storedprocedure$
/* @version: 20190719; @author: anovsiradj; */

#VARIABLE_CONFLICT use_variable
DECLARE isskpd INT := 1;
DECLARE xjumlah NUMERIC(15,2) := 0;

BEGIN
	tahun := TRIM(tahun);
	IF(tglawal IS NULL) THEN tglawal := (tahun||'-01-01')::TIMESTAMP; END IF;
	IF(tglakhir IS NULL) THEN tglakhir := (tahun||'-12-31')::TIMESTAMP; END IF;

	-- ppkd
	SELECT a.kodeurusan,a.kodesuburusan,TRIM(a.kodeorganisasi) FROM master.master_organisasi a
	WHERE TRIM(a.tahun) = tahun AND TRIM(a.kodeorganisasi) <> '' AND a.skpkd = isskpd
	INTO kodeurusan,kodesuburusan,kodeorganisasi;

	kodeorganisasi = TRIM(kodeorganisasi);

	/* #################################################################################################### */

	/* (ali) modified by ali; */

	/* --- (mbamad): pendapatan lo; --- */
	xjumlah := 0;
	FOR 
		kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek,
		debet,kredit
	IN SELECT
		sr.kodeakun,sr.kodekelompok,sr.kodejenis,sr.kodeobjek,sr.koderincianobjek,
		COALESCE(sum(sr.kredit - sr.debet), 0), 0
	from akuntansi.akrual_jurnal_rincian sr
	join akuntansi.akrual_buku_jurnal s on (sr.tahun = s.tahun
		and sr.kodeurusan = s.kodeurusan and sr.kodesuburusan = s.kodesuburusan and sr.kodeorganisasi = s.kodeorganisasi 
		and sr.isskpd = s.isskpd and sr.noref = s.noref
	)
	where sr.tahun = tahun 
	and sr.kodeurusan = kodeurusan and sr.kodesuburusan = kodesuburusan and sr.kodeorganisasi = kodeorganisasi 
	and s.tanggalbukti >= tglawal and s.tanggalbukti <= tglakhir
	and s.jenisjurnal NOT IN (5)
	and sr.kodeakun = 8
	and s.isskpd = isskpd
	and s.posting = 1
	group by sr.kodeakun,sr.kodekelompok,sr.kodejenis,sr.kodeobjek,sr.koderincianobjek
	order by sr.kodeakun,sr.kodekelompok,sr.kodejenis,sr.kodeobjek,sr.koderincianobjek
	LOOP
		SELECT a.kode_rekening,a.urai_rekening FROM akuntansi.anov_jurnal_rekening(tahun, kodeurusan,kodesuburusan,kodeorganisasi) a
		WHERE a.kodeakun = kodeakun AND a.kodekelompok = kodekelompok AND a.kodejenis = kodejenis
		AND a.kodeobjek = kodeobjek AND a.koderincianobjek = koderincianobjek
		INTO kode_rekening,urai_rekening;

		xjumlah := xjumlah + debet;

		RETURN NEXT;
	END LOOP;

	/* --- (mbamad): surplus defisit pendapatan lo; --- */
	IF(xjumlah > 0) THEN
	  SELECT a.* FROM akuntansi.anov_jurnal_rekening(tahun,kodeurusan,kodesuburusan,kodeorganisasi) a
	  WHERE a.kodeakun = 3 AND a.kodekelompok = 1 AND a.kodejenis = 1
	  AND a.kodeobjek = 2 AND a.koderincianobjek = 1
	  INTO kode_rekening,urai_rekening, kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek;

	  debet  := 0;
	  kredit := xjumlah;

	  RETURN NEXT;
	END IF;

	xjumlah := 0;

	/* --- (mbamad): beban lo; --- */
	FOR 
		kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek,
		debet,kredit
	IN SELECT
		sr.kodeakun,sr.kodekelompok,sr.kodejenis,sr.kodeobjek,sr.koderincianobjek,
		0, COALESCE(SUM(sr.debet - sr.kredit), 0)
	from akuntansi.akrual_jurnal_rincian sr 
	join akuntansi.akrual_buku_jurnal s on (sr.tahun = s.tahun
		and sr.kodeurusan = s.kodeurusan and sr.kodesuburusan = s.kodesuburusan and sr.kodeorganisasi = s.kodeorganisasi 
		and sr.isskpd = s.isskpd and sr.noref = s.noref
	)
	WHERE sr.tahun = tahun 
	and sr.kodeurusan = kodeurusan and sr.kodesuburusan = kodesuburusan and sr.kodeorganisasi = kodeorganisasi 
	and s.isskpd = isskpd
	and sr.kodeakun = 9
	and s.jenisjurnal NOT IN (5)
	and s.tanggalbukti >= tglawal and s.tanggalbukti <= tglakhir
	and s.posting = 1
	GROUP BY sr.kodeakun,sr.kodekelompok,sr.kodejenis,sr.kodeobjek,sr.koderincianobjek
	LOOP
		SELECT a.kode_rekening,a.urai_rekening FROM akuntansi.anov_jurnal_rekening(tahun, kodeurusan,kodesuburusan,kodeorganisasi) a
		WHERE a.kodeakun = kodeakun AND a.kodekelompok = kodekelompok AND a.kodejenis = kodejenis
		AND a.kodeobjek = kodeobjek AND a.koderincianobjek = koderincianobjek
		INTO kode_rekening,urai_rekening;

		xjumlah := xjumlah + kredit; 

		RETURN NEXT;
	END LOOP;

	/* --- (mbamad): surplus defisit beban lo; --- */
	IF(xjumlah > 0) THEN
	  SELECT a.* FROM akuntansi.anov_jurnal_rekening(tahun,kodeurusan,kodesuburusan,kodeorganisasi) a
	  WHERE a.kodeakun = 3 AND a.kodekelompok = 1 AND a.kodejenis = 1
	  AND a.kodeobjek = 2 AND a.koderincianobjek = 1
	  INTO kode_rekening,urai_rekening, kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek;

	  debet  := xjumlah;
	  kredit := 0;

	  RETURN NEXT;
	END IF;

	/* #################################################################################################### */

END;
$storedprocedure$ LANGUAGE plpgsql;

/* [TEST] */
DO $execute$ BEGIN
	PERFORM akuntansi.anov_jurnal_ppkd_penutup_lo('2019');
	PERFORM akuntansi.anov_jurnal_ppkd_penutup_lo('2019','2019-01-01','2019-06-30');
END $execute$;
