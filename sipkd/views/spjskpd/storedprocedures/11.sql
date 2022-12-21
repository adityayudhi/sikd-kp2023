DO $execute$ BEGIN PERFORM __rmfn__('akuntansi.anov_akrual_concat_kode_rekening'); END $execute$;

CREATE OR REPLACE FUNCTION akuntansi.anov_akrual_concat_kode_rekening(
	IN kodeurusan INTEGER,
	IN kodesuburusan INTEGER,
	IN kodeorganisasi VARCHAR,

	IN kodebidang VARCHAR DEFAULT NULL,
	IN kodeprogram INTEGER DEFAULT NULL,
	IN kodekegiatan INTEGER DEFAULT NULL,

	IN kodeakun INTEGER DEFAULT 0,
	IN kodekelompok INTEGER DEFAULT 0,
	IN kodejenis INTEGER DEFAULT 0,
	IN kodeobjek INTEGER DEFAULT 0,
	IN koderincianobjek INTEGER DEFAULT 0,

	IN lead_length INTEGER DEFAULT 2,
	IN lead_prefix VARCHAR DEFAULT 0,

	OUT kode_rekening VARCHAR
) AS $storedprocedure$
/* @author: anovsiradj; @version: 20190726; */
BEGIN
	IF (kodebidang IS NULL OR kodebidang = '') THEN
		kodebidang := kodeurusan||'.'||LPAD(kodesuburusan::VARCHAR, lead_length, lead_prefix);
	END IF;
	IF (kodeprogram IS NULL) THEN kodeprogram := 0; END IF;
	IF (kodekegiatan IS NULL) THEN kodekegiatan := 0; END IF;

	kode_rekening := (
		kodebidang||'.'||kodeorganisasi||'.'||
		LPAD(kodeprogram::VARCHAR, lead_length, lead_prefix)||'.'||
		LPAD(kodekegiatan::VARCHAR, lead_length, lead_prefix)||' - '||
		kodeakun||'.'||kodekelompok||'.'||kodejenis||'.'||
		LPAD(kodeobjek::VARCHAR,lead_length,lead_prefix)||'.'||
		LPAD(koderincianobjek::VARCHAR,lead_length,lead_prefix)||
		''
	);
END;
$storedprocedure$ LANGUAGE plpgsql;

DO $execute$ BEGIN
	PERFORM akuntansi.anov_akrual_concat_kode_rekening(1,2,'03');
	PERFORM akuntansi.anov_akrual_concat_kode_rekening(1,2,'03', NULL,NULL,NULL);
	PERFORM akuntansi.anov_akrual_concat_kode_rekening(1,2,'03', NULL,NULL,NULL, 1,2,3,4,5);
END $execute$;
