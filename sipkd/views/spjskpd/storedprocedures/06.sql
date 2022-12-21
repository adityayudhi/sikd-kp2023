/*
	@flex: ~/sipkd_AKUNTANSI_PEMDA/src/spjAkuntansiPemda/views/Akrual/VInputJurnalAkrualPPKD.mxml @ tampilkanPenutupLra();
	@origin: AKRUAL_VIEW_PENUTUP_LRA_PPKD();
	@author: mbamad;
*/

DO $execute$ BEGIN PERFORM __rmfn__('akuntansi.anov_jurnal_ppkd_penutup_lra'); END $execute$;

CREATE OR REPLACE FUNCTION akuntansi.anov_jurnal_ppkd_penutup_lra(
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
/* @version: 20190718; @author: anovsiradj; */

#VARIABLE_CONFLICT use_variable
DECLARE isskpd INT := 1;
DECLARE xjumlah NUMERIC(15,2);
DECLARE xbelanja NUMERIC(15,2);
DECLARE xpendapatan NUMERIC(15,2);
DECLARE xpenutup NUMERIC(15,2);

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

	/* --- (mbamad): pendapatan lra dan penerimaaan pembiyaan dulu; --- */
	FOR
		kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek,
		xjumlah
	IN SELECT
		sr.kodeakun,sr.kodekelompok,sr.kodejenis,sr.kodeobjek,sr.koderincianobjek,
		COALESCE(SUM(sr.kredit - sr.debet), 0)
	FROM akuntansi.akrual_jurnal_rincian sr 
	JOIN akuntansi.akrual_buku_jurnal s on (sr.tahun=s.tahun
		and sr.kodeurusan = s.kodeurusan and sr.kodesuburusan = s.kodesuburusan and sr.kodeorganisasi = s.kodeorganisasi
		and sr.isskpd = s.isskpd
		and sr.noref = s.noref
	)
	where sr.tahun = tahun
	and sr.kodeurusan = kodeurusan and sr.kodesuburusan = kodesuburusan and sr.kodeorganisasi = kodeorganisasi
	and s.tanggalbukti >= tglawal and s.tanggalbukti <= tglakhir
	and ( sr.kodeakun = 4 or (sr.kodeakun = 7 and sr.kodekelompok = 1) )
	and s.jenisjurnal NOT IN (4)
	and s.isskpd = isskpd
	group by sr.kodeakun,sr.kodekelompok,sr.kodejenis,sr.kodeobjek,sr.koderincianobjek
	order by sr.kodeakun,sr.kodekelompok,sr.kodejenis,sr.kodeobjek,sr.koderincianobjek
	LOOP
		SELECT a.kode_rekening,a.urai_rekening FROM akuntansi.anov_jurnal_rekening(tahun,kodeurusan,kodesuburusan,kodeorganisasi) a
		WHERE a.kodeakun = kodeakun AND a.kodekelompok = kodekelompok AND a.kodejenis = kodejenis
		AND a.kodeobjek = kodeobjek AND a.koderincianobjek = koderincianobjek
		INTO kode_rekening,urai_rekening;

		debet  := 0;
		kredit := 0;
		IF(xjumlah > 0) THEN
			debet  := xjumlah;
			kredit := 0;
		END IF;

		RETURN NEXT;
	END LOOP;

	/* --- (mbamad): surplus defisit lra; --- */
	SELECT COALESCE(SUM(sr.debet - sr.kredit),0)
	FROM akuntansi.akrual_jurnal_rincian sr
	JOIN akuntansi.akrual_buku_jurnal s on (sr.tahun = s.tahun
		and sr.kodeurusan = s.kodeurusan and sr.kodesuburusan = s.kodesuburusan and sr.kodeorganisasi = s.kodeorganisasi
		and sr.isskpd = s.isskpd and sr.noref = s.noref
	)
	where sr.tahun = tahun
	and sr.kodeurusan = kodeurusan and sr.kodesuburusan = kodesuburusan and sr.kodeorganisasi = kodeorganisasi
	and s.tanggalbukti >= tglawal and s.tanggalbukti <= tglakhir
	and ( sr.kodeakun IN (5,6) or (sr.kodeakun = 7 and sr.kodekelompok = 2) )
	and s.jenisjurnal NOT IN (4)
	and s.isskpd = isskpd
	INTO xbelanja;
	RAISE NOTICE 'xbelanja: %;', xbelanja;

	select COALESCE(SUM(sr.kredit - sr.debet), 0)
	from akuntansi.akrual_jurnal_rincian sr 
	join akuntansi.akrual_buku_jurnal s on (sr.tahun = s.tahun
		and sr.kodeurusan = s.kodeurusan and sr.kodesuburusan = s.kodesuburusan and sr.kodeorganisasi = s.kodeorganisasi
		and sr.isskpd = s.isskpd and sr.noref = s.noref
	)
	where sr.tahun = tahun
	and sr.kodeurusan = kodeurusan and sr.kodesuburusan = kodesuburusan and sr.kodeorganisasi = kodeorganisasi
	and s.tanggalbukti >= tglawal and s.tanggalbukti <= tglakhir
	and ( ( sr.kodeakun=4) or (sr.kodeakun=7 and sr.kodekelompok=1 ) )
	and s.jenisjurnal NOT IN (4)
	and s.isskpd = isskpd
	into xpendapatan;
	RAISE NOTICE 'xpendapatan: %;', xpendapatan;

	SELECT a.* FROM akuntansi.anov_jurnal_rekening(tahun,kodeurusan,kodesuburusan,kodeorganisasi) a
	WHERE a.kodeakun = 3 AND a.kodekelompok = 1 AND a.kodejenis = 2
	AND a.kodeobjek = 6 AND a.koderincianobjek = 1
	INTO kode_rekening,urai_rekening, kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek;
	debet  := 0;
	kredit := 0;
	xjumlah  := xpendapatan - xbelanja;
	xpenutup := xjumlah;
	IF(xjumlah < 0) THEN
		debet  := ABS(xjumlah);
		kredit := 0;
	END IF;
	IF(xjumlah > 0) THEN
		debet  := 0;
		kredit := xjumlah;
	END IF;

	RAISE NOTICE 'xjumlah: %; xpenutup: %; debet: %; kredit: %;', xjumlah, xpenutup, debet, kredit;
	RETURN NEXT;

	IF((
		SELECT COUNT(*)
		FROM akuntansi.akrual_jurnal_rincian sr
		JOIN akuntansi.akrual_buku_jurnal s ON (sr.tahun = s.tahun
			and sr.kodeurusan = s.kodeurusan and sr.kodesuburusan = s.kodesuburusan and sr.kodeorganisasi = s.kodeorganisasi
			and sr.isskpd = s.isskpd and sr.noref = s.noref
		)
		where sr.tahun = tahun
		and sr.kodeurusan = kodeurusan and sr.kodesuburusan = kodesuburusan and sr.kodeorganisasi = kodeorganisasi
		and s.tanggalbukti >= tglawal and s.tanggalbukti <= tglakhir
		and ( sr.kodeakun in (5,6) or (sr.kodeakun=7 and sr.kodekelompok=2) )
		and s.jenisjurnal not in (4)
		and s.isskpd = isskpd
	) > 0) THEN
		/* --- (mbamad): belanja lra; --- */
		FOR
			kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek,
			xjumlah
		IN SELECT
			sr.kodeakun,sr.kodekelompok,sr.kodejenis,sr.kodeobjek,sr.koderincianobjek,
			COALESCE(SUM(sr.debet - sr.kredit))
		from akrual_jurnal_rincian sr 
		join akrual_buku_jurnal s ON (sr.tahun=s.tahun
			and sr.kodeurusan = s.kodeurusan and sr.kodesuburusan = s.kodesuburusan and sr.kodeorganisasi = s.kodeorganisasi
			and sr.isskpd = s.isskpd and sr.noref = s.noref
		)
		where sr.tahun = tahun
		and sr.kodeurusan = kodeurusan and sr.kodesuburusan = kodesuburusan and sr.kodeorganisasi = kodeorganisasi
		and s.tanggalbukti >= tglawal and s.tanggalbukti <= tglakhir
		and ( sr.kodeakun in (5,6) or (sr.kodeakun=7 and sr.kodekelompok=2) )
		and s.jenisjurnal not in (4)
		and s.isskpd = isskpd
		group by sr.kodeakun,sr.kodekelompok,sr.kodejenis,sr.kodeobjek,sr.koderincianobjek
		LOOP
			SELECT a.kode_rekening,a.urai_rekening FROM akuntansi.anov_jurnal_rekening(tahun, kodeurusan,kodesuburusan,kodeorganisasi) a
			WHERE a.kodeakun = kodeakun AND a.kodekelompok = kodekelompok AND a.kodejenis = kodejenis
			AND a.kodeobjek = kodeobjek AND a.koderincianobjek = koderincianobjek
			INTO kode_rekening,urai_rekening;

			debet  := 0;
			kredit := 0;
			IF(xjumlah > 0) THEN
				kredit := xjumlah;
				debet  := 0;
			END IF;

			RETURN NEXT;
		END LOOP;

		/* --- (mbamad): ekuitas sal terhadap surplus defisit; --- */

		SELECT a.* FROM akuntansi.anov_jurnal_rekening(tahun,kodeurusan,kodesuburusan,kodeorganisasi) a
		WHERE a.kodeakun = 3 AND a.kodekelompok = 1 AND a.kodejenis = 2
		AND a.kodeobjek = 5 AND a.koderincianobjek = 1
		INTO kode_rekening,urai_rekening, kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek;
		debet  := 0;
		kredit := 0;
		if(xpenutup < 0) THEN
			debet  := ABS(xpenutup);
			kredit := 0;
		end if;
		if(xpenutup > 0) then
			debet  := 0;
			kredit := xpenutup;
		end if;
		RETURN NEXT;

		SELECT a.* FROM akuntansi.anov_jurnal_rekening(tahun,kodeurusan,kodesuburusan,kodeorganisasi) a
		WHERE a.kodeakun = 3 AND a.kodekelompok = 1 AND a.kodejenis = 2
		AND a.kodeobjek = 6 AND a.koderincianobjek = 1
		INTO kode_rekening,urai_rekening, kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek;
		debet  := 0;
		kredit := 0;
		IF(xpenutup < 0) THEN
			debet  := 0;
			kredit := ABS(xpenutup);
		END IF;
		if(xpenutup > 0) THEN
			debet  := xpenutup;
			kredit := 0;
		end if;
		RETURN NEXT;
	END IF;

	/* #################################################################################################### */
END;
$storedprocedure$ LANGUAGE plpgsql;

/* [LINT] */
DO $execute$ BEGIN
	PERFORM akuntansi.anov_jurnal_ppkd_penutup_lra('2019');
	PERFORM akuntansi.anov_jurnal_ppkd_penutup_lra('2019','2019-04-01','2019-09-30');
END $execute$;
