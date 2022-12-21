DO $execute$ BEGIN PERFORM __rmfn__('akuntansi.anov_jurnal_rekening'); END $execute$;

CREATE OR REPLACE FUNCTION akuntansi.anov_jurnal_rekening(
	tahun VARCHAR,
	kodeurusan INTEGER, kodesuburusan INTEGER, kodeorganisasi VARCHAR,
	kodebidang VARCHAR DEFAULT NULL,
	kodeprogram INTEGER DEFAULT NULL,
	kodekegiatan INTEGER DEFAULT NULL
)
RETURNS TABLE(
	kode_rekening VARCHAR, urai_rekening VARCHAR,
	kodeakun INTEGER, kodekelompok INTEGER, kodejenis INTEGER, kodeobjek INTEGER, koderincianobjek INTEGER
)
AS $storedprocedure$
/* @author: anovsiradj; @version: 20190718, 20190724; */

#VARIABLE_CONFLICT use_variable
DECLARE lead_length INTEGER := 2;
DECLARE lead_prefix VARCHAR := 0;

BEGIN
	IF (kodebidang IS NULL OR kodebidang = '') THEN
		kodebidang := kodeurusan||'.'||LPAD(kodesuburusan::VARCHAR, lead_length, lead_prefix);
	END IF;
	IF (kodeprogram IS NULL) THEN kodeprogram := 0; END IF;
	IF (kodekegiatan IS NULL) THEN kodekegiatan := 0; END IF;

	FOR
		kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek,
		urai_rekening
	IN SELECT
		a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek,
		a.urai
	FROM akuntansi.akrual_master_rekening a WHERE a.tahun = tahun AND a.koderincianobjek <> 0
	ORDER BY a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek
	LOOP
		kode_rekening := (
			kodebidang||'.'||
			TRIM(kodeorganisasi)||'.'||
			LPAD(kodeprogram::VARCHAR, lead_length, lead_prefix)||'.'||
			LPAD(kodekegiatan::VARCHAR, lead_length, lead_prefix)||' - '||
			kodeakun||'.'||kodekelompok||'.'||kodejenis||'.'||
			LPAD(kodeobjek::VARCHAR,lead_length,lead_prefix)||'.'||
			LPAD(koderincianobjek::VARCHAR,lead_length,lead_prefix)||
			''
		);

		RETURN NEXT;
	END LOOP;
END;
$storedprocedure$ LANGUAGE plpgsql;

DO $execute$ BEGIN
	PERFORM akuntansi.anov_jurnal_rekening('2019',1,2,'03');
END $execute$;
