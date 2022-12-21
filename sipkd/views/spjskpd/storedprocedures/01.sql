DO $execute$ BEGIN PERFORM __rmfn__('pertanggungjawaban.anov_bku_skpd'); END $execute$;

CREATE OR REPLACE FUNCTION pertanggungjawaban.anov_bku_skpd(
	tahun CHAR(4),
	kodeurusan INTEGER,
	kodesuburusan INTEGER,
	kodeorganisasi CHAR(8),
	bulan INTEGER,
	username VARCHAR(64)
) returns table(
	no_bku INTEGER,
	tgl_bku TIMESTAMP,
	jenis_bku VARCHAR(64),
	jenis_bku_urai VARCHAR(64),
	urai text,
	penerimaan NUMERIC(15,2),
	pengeluaran NUMERIC(15,2),
	bukti VARCHAR(128),
	tgl_bukti TIMESTAMP,
	jenis_sp2d CHAR(16),
	nospj VARCHAR(64),
	simpananbank SMALLINT, is_simpananbank SMALLINT,
	is_pihak_ketiga SMALLINT, is_pihakketiga SMALLINT, pihakketiga SMALLINT,
	is_bendahara_pembantu CHAR(1), is_bendaharapembantu CHAR(1), pembantu CHAR(1),
	uname VARCHAR(64)
) AS $storedprocedure$
/*
@author anovsiradj
@version 20190410,20190412-174500,20190514-160533

@flex:
/sipkd_SPJSKPD/src/spjskpd/views/VBKU.mxml:ambilData()

@usage:
select * from pertanggungjawaban.anov_bku_skpd('2019',1,1,'01',5,'ADMIN');

@input:
pada kolom:tahun/kolom:kodeorganisasi selalu trim, karena alasan;

@output:
pada db:firebird, kolom:cek selalu nol, jadi saya hilangkan saja;
ohh, kolom:cek hanya digunakan pada flex, jadi kalo saya hilangkan tidak masalah.
*/

#variable_conflict use_variable
DECLARE
	xpembantu CHAR(1);
	xisskpd SMALLINT := 0;
	_terima_ VARCHAR[] := array['SP2D-GJ' , 'SP2D-LS', 'SP2D', 'PUNGUT-PAJAK', 'KOREKSI PENERIMAAN' , 'RK-PPKD'];
	_keluar_ VARCHAR[] := array['BAYAR-GJ', 'SPJ-LS' , 'SPJ' , 'SETOR-PAJAK' , 'KOREKSI PENGELUARAN', 'RK-PPKD'];
	_prefix_ VARCHAR[] := array['SP2D','SPJ','RK-PPKD'];

BEGIN
	tahun := TRIM(tahun);
	kodeorganisasi := TRIM(kodeorganisasi);

	/*
	SELECT z.is_bendahara_pembantu INTO xpembantu FROM penatausahaan.pengguna z
	WHERE UPPER(z.uname) = UPPER(username) LIMIT 1;
	-- RAISE NOTICE 'xpembantu = %', xpembantu;
	*/

	FOR
		no_bku,tgl_bku,jenis_bku,
		urai,
		penerimaan, pengeluaran,
		bukti, tgl_bukti, jenis_sp2d, nospj,
		pembantu,
		simpananbank,
		pihakketiga,
		uname
	IN SELECT
		a.no_bku, a.tgl_bku, a.jenis_bku,
		a.urai,
		a.penerimaan, a.pengeluaran,
		a.bukti, a.tgl_bukti, a.jenis_sp2d, a.nospj,
		a.is_bendahara_pembantu,
		a.simpananbank,
		a.is_pihak_ketiga,
		a.uname
	FROM pertanggungjawaban.skpd_bku a WHERE a.tahun = tahun
	AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND TRIM(a.kodeorganisasi) = kodeorganisasi
	AND extract(month FROM a.tgl_bku) = bulan
	AND a.isskpd = xisskpd
	ORDER BY a.tgl_bku,a.no_bku
	LOOP
		/* ... */
		is_simpananbank = simpananbank;
		is_pihakketiga = pihakketiga;
		is_pihak_ketiga = pihakketiga;
		is_bendaharapembantu = pembantu;
		is_bendahara_pembantu = pembantu;
		jenis_bku_urai = jenis_bku;

		IF(jenis_bku = ANY(_prefix_)) THEN
			jenis_bku_urai = jenis_bku || '-' || jenis_sp2d;
		END IF;

		IF (jenis_bku = ANY(_terima_)) THEN
			SELECT COALESCE(SUM(b.penerimaan),0) INTO penerimaan
			FROM pertanggungjawaban.skpd_bkurincian b WHERE b.tahun = tahun
			AND b.kodeurusan= kodeurusan AND b.kodesuburusan = kodesuburusan and TRIM(b.kodeorganisasi) = kodeorganisasi
			AND b.no_bku = no_bku
			AND b.isskpd = xisskpd;
		END IF;

		IF (jenis_bku = ANY(_keluar_)) THEN
			SELECT COALESCE(SUM(b.pengeluaran),0) INTO pengeluaran
			FROM pertanggungjawaban.skpd_bkurincian b WHERE b.tahun = tahun
			and b.kodeurusan = kodeurusan AND b.kodesuburusan = kodesuburusan AND TRIM(b.kodeorganisasi) = kodeorganisasi
			AND b.no_bku = no_bku
			AND b.isskpd = xisskpd;
		END IF;

		RETURN NEXT; -- a.k.a suspend
	END LOOP;
END;
$storedprocedure$ LANGUAGE plpgsql;
