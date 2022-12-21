/*
	@flex: ~/sipkd_AKUNTANSI_PEMDA/src/spjAkuntansiPemda/views/Akrual/VInputJurnalAkrualPPKD.mxml @ hasiltakcair(), hasilsp2d();
	@author: mbamad;
	@vendor: firebird;
	@origin: AKRUAL_TO_JURNAL_PPKD();

	@usage
	APP2 => "akuntansi" => "akuntansi akrual ppkd" => tambah(JURNAL-UMUM|JU) => browse|cari() => click()

	@notes
	kalo komentar berisi " --- *** --- ", berarti yg nulis mbamad. kalo tidak, itu saya.

	jika ada komen [TODO] dalam $storedprocedure$,
	maka bagian tersebut belum jadi atau belum saya validasi berdasarkan @origin.

	jika ada komen [TEST] dalam $storedprocedure$,
	maka bagian tersebut sudah saya validasi berdasarkan @origin,
	tapi belum saya test karena belum/tidak ada data.

	jika ada komen [DONE] dalam $storedprocedure$,
	maka bagian tersebut sudah saya validasi berdasarkan @origin dan sudah saya test dengan data.
*/

/* [SAFE] */
DO $execute$ BEGIN PERFORM __rmfn__('akuntansi.anov_akrual_to_jurnal_ppkd_ju_rincian'); END $execute$;

CREATE OR REPLACE FUNCTION akuntansi.anov_akrual_to_jurnal_ppkd_ju_rincian (
		tahun VARCHAR,
		jenis VARCHAR /* ganti [transaksi] supaya general, lalu [jenis] sebelumnya dihilangkan. */,
		nomor VARCHAR /* jika TIDAKCAIR maka pake NOSP2D || jika bukan TIDAKCAIR maka pake NOBUKUKAS  */
)
RETURNS TABLE (
		kode_rekening VARCHAR /* ganti [koderekening] supaya general */,
		urai_rekening VARCHAR /* ganti [uraian] supaya general */,
		kodeurusan INTEGER, kodesuburusan INTEGER, kodeorganisasi VARCHAR,
		kodebidang VARCHAR, kodeprogram INTEGER, kodekegiatan INTEGER,
		kodeakun INTEGER, kodekelompok INTEGER, kodejenis INTEGER, kodeobjek INTEGER, koderincianobjek INTEGER,
		urut INTEGER /* ganti [urutan] menyesuaikan ${akuntansi.akrual_jurnal_rincian} */,
		debet NUMERIC(15,2),
		kredit NUMERIC(15,2)
)
AS $storedprocedure$
	/* @version: 20190725; @author: anovsiradj; */

	#VARIABLE_CONFLICT use_variable

	DECLARE isskpd INTEGER := 1;
	DECLARE jumlah NUMERIC(15,2);
	DECLARE jenissp2d VARCHAR /* ganti [jenis_sp2d] menyesuaikan ${akuntansi.akrual_buku_jurnal} */;
	DECLARE sumberdana_kode INTEGER;
	DECLARE sumberdana_urai INTEGER;
	DECLARE sumberdana_rekbank INTEGER;
	DECLARE sp2d_jenis_default VARCHAR[] := array['UP','GU','TU','LS'];
	DECLARE skpkd VARCHAR;
	DECLARE counter INTEGER;

	sp2d_nosp2d VARCHAR;

	kasda_transaksi___nobukukas VARCHAR;
	kasda_transaksi___tanggal TIMESTAMP;
	kasda_transaksi___nobukti VARCHAR;
	kasda_transaksi___tglbukti TIMESTAMP;
	kasda_transaksi___jenissp2d VARCHAR;
	kasda_transaksi___kodesumberdana INTEGER;

	/* -- (mbamad) -- */
	DECLARE nobukukas VARCHAR(10);
	DECLARE xurai VARCHAR(255);
	DECLARE kodesumberdana integer;
	DECLARE xuraikas VARCHAR(255);
	DECLARE xkodesumberdana integer;
BEGIN
	/* skpkd */
	SELECT a.kodeurusan,a.kodesuburusan,a.kodeorganisasi, UPPER(TRIM(a.urai))
	FROM master.master_organisasi a WHERE a.tahun = tahun AND a.kodeorganisasi <> '' AND a.skpkd = isskpd
	INTO kodeurusan,kodesuburusan,kodeorganisasi, skpkd;

	IF(jenis = 'TIDAKCAIR') THEN /* [DONE] */
		urut := 0;

		/* explicit */
		sp2d_nosp2d := nomor;

		SELECT SUM(a.jumlah)
		FROM penatausahaan.sp2drincian a WHERE a.tahun = tahun
		AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
		AND a.nosp2d = sp2d_nosp2d
		INTO jumlah;

		/* jika sp2d/rincian kosong, berarti sp2d tidak ada, jika sp2d tidak ada, maka tidak perlu rincian. */
		IF (jumlah IS NULL) THEN RETURN; END IF;

		debet  := jumlah;
		kredit := 0;
		SELECT a.* FROM akuntansi.anov_jurnal_rekening(tahun,kodeurusan,kodesuburusan,kodeorganisasi) a
		WHERE a.kodeakun       = 3 AND a.kodekelompok     = 1 AND a.kodejenis        = 1
		AND a.kodeobjek        = 1 AND a.koderincianobjek = 1
		INTO kode_rekening,urai_rekening, kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek;
		urut := urut + 1;
		RETURN NEXT;

		debet  := 0;
		kredit := jumlah;
		SELECT a.* FROM akuntansi.anov_jurnal_rekening(tahun,kodeurusan,kodesuburusan,kodeorganisasi) a
		WHERE a.kodeakun       = 2 AND a.kodekelompok     = 1 AND a.kodejenis        = 6
		AND a.kodeobjek        = 5 AND a.koderincianobjek = 1
		INTO kode_rekening,urai_rekening, kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek;
		urut := urut + 1;
		RETURN NEXT;

	ELSE
		/* explicit */
		SELECT
			a.nobukukas,
			a.tanggal,
			a.nobukti,
			a.tglbukti,
			a.jenissp2d,
			a.kodesumberdana
		from kasda.kasda_transaksi a WHERE a.tahun = tahun AND a.nobukukas = nomor
		AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
		INTO
			kasda_transaksi___nobukukas,
			kasda_transaksi___tanggal,
			kasda_transaksi___nobukti,
			kasda_transaksi___tglbukti,
			kasda_transaksi___jenissp2d,
			kasda_transaksi___kodesumberdana
		;

		/* legacy */
		jenissp2d := kasda_transaksi___jenissp2d;
		kodesumberdana := kasda_transaksi___kodesumberdana;

		IF (jenis = 'PINDAHBUKU') THEN /* TEST */
			urut := 0;

			FOR sumberdana_kode,debet,kredit
			IN SELECT a.kd_sumber_dana,a.penerimaan,a.pengeluaran
			from kasda.kasda_transaksi_detil a WHERE a.tahun = tahun AND a.nobukukas = kasda_transaksi___nobukukas
			AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
			AND a.pengeluaran = 0
			LOOP
				urut := urut + 1;

				SELECT 
					a.kode_rekening,a.urai_rekening,
					a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek
				FROM akuntansi.anov_jurnal_rekening(tahun,kodeurusan,kodesuburusan,kodeorganisasi) a
				JOIN kasda.kasda_sumberdanarekening b ON (b.kodesumberdana = sumberdana_kode)
				WHERE a.kodeakun = 1 AND a.kodekelompok = 1 AND a.kodejenis = 1
				AND UPPER(TRIM(a.urai_rekening)) LIKE '%'||UPPER(TRIM(b.rekening))||'%'
				INTO
					kode_rekening,urai_rekening,
					kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek
				;

				RETURN NEXT;
			END LOOP;

			for sumberdana_kode,debet,kredit
			IN SELECT a.kd_sumber_dana,a.penerimaan,a.pengeluaran
			from kasda.kasda_transaksi_detil a WHERE a.tahun = tahun AND a.nobukukas = kasda_transaksi___nobukukas
			AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
			AND a.penerimaan = 0
			LOOP
				urut := urut + 1;

				SELECT 
					a.kode_rekening,a.urai_rekening,
					a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek
				FROM akuntansi.anov_jurnal_rekening(tahun,kodeurusan,kodesuburusan,kodeorganisasi) a
				JOIN kasda.kasda_sumberdanarekening b ON (b.kodesumberdana = sumberdana_kode)
				WHERE a.kodeakun = 1 AND a.kodekelompok = 1 AND a.kodejenis = 1
				AND UPPER(TRIM(a.urai_rekening)) LIKE '%'||UPPER(TRIM(b.rekening))||'%'
				INTO
					kode_rekening,urai_rekening,
					kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek
				;

				RETURN NEXT;
			END LOOP;

		ELSIF (jenis = 'SP2D' AND jenissp2d = ANY(sp2d_jenis_default)) THEN /* [TODO] */
			urut := 0;

			/* --- rk skpd --- */
			SELECT a.* FROM akuntansi.anov_jurnal_rekening(tahun,kodeurusan,kodesuburusan,kodeorganisasi) a
			WHERE a.kodeakun = 1 AND a.kodekelompok = 1 AND a.kodejenis = 8
			AND UPPER(TRIM(a.urai_rekening)) LIKE '%'||skpkd||'%'
			INTO kode_rekening,urai_rekening, kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek;

			kredit := 0;
			SELECT COALESCE(SUM(a.pengeluaran),0) INTO debet
			FROM kasda.kasda_transaksi_detil a WHERE a.tahun = tahun AND a.nobukukas = kasda_transaksi___nobukukas
			AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
			AND a.kodeakun <> 2;
			RETURN NEXT;

			/* --- kas di kasda --- */
			urut := 1;
			SELECT UPPER(TRIM(a.rekening)) FROM kasda.kasda_sumberdanarekening a
			WHERE a.kodesumberdana = sumberdana_kode INTO sumberdana_rekbank;

			SELECT a.* FROM akuntansi.anov_jurnal_rekening(tahun,kodeurusan,kodesuburusan,kodeorganisasi) a
			WHERE a.kodeakun = 1 AND a.kodekelompok = 1 AND a.kodejenis = 1
			AND UPPER(TRIM(a.urai_rekening)) LIKE '%'||sumberdana_rekbank||'%'
			INTO kode_rekening,urai_rekening, kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek;

			debet := 0;
			SELECT COALESCE(SUM(a.pengeluaran),0) FROM kasda.kasda_transaksi_detil a WHERE a.tahun = tahun
			AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
			AND a.nobukukas = nomor AND a.kodeakun <> 2 INTO kredit;
			RETURN NEXT;

			IF ((
				SELECT COALESCE(SUM(a.penerimaan - a.pengeluaran)) FROM kasda.kasda_transaksi_detil a WHERE a.tahun = tahun
				AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
				AND a.nobukukas = nomor AND a.kodeakun = 2
			) > 0) THEN
				/* --- (mbamad): kas di kasda; --- */
				urut := 2;

				SELECT UPPER(TRIM(a.rekening)) FROM kasda.kasda_sumberdanarekening a
				WHERE a.kodesumberdana = sumberdana_kode INTO sumberdana_rekbank;

				SELECT a.* FROM akuntansi.anov_jurnal_rekening(tahun,kodeurusan,kodesuburusan,kodeorganisasi) a
				WHERE a.kodeakun = 1 AND a.kodekelompok = 1 AND a.kodejenis = 1
				AND UPPER(TRIM(a.urai_rekening)) LIKE '%'||sumberdana_rekbank||'%'
				INTO kode_rekening,urai_rekening, kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek;

				kredit := 0;
				SELECT COALESCE(SUM(a.penerimaan - a.pengeluaran),0) FROM kasda.kasda_transaksi_detil a WHERE a.tahun = tahun
				AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
				AND a.nobukukas = nomor AND a.kodeakun = 2 INTO debet;
				RETURN NEXT;

				FOR
					kodebidang,kodeprogram,kodekegiatan,
					kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek,
					kode_rekening,urai_rekening,
					kredit
				IN SELECT
					s.kodebidang,s.kodeprogram,s.kodekegiatan,
					k.a_kodeakun,k.a_kodekelompok,k.a_kodejenis,k.a_kodeobjek,k.a_koderincianobjek,
					r.kode_rekening,r.urai_rekening,
					COALESCE((s.penerimaan - s.pengeluaran),0)
				FROM kasda.kasda_transaksi_detil s
				JOIN akuntansi.konversi_akrual k on (s.tahun = k.tahun
					AND s.kodeakun = k.kodeakun AND s.kodekelompok = k.kodekelompok AND s.kodejenis = k.kodejenis
					AND s.kodeobjek = k.kodeobjek AND s.koderincianobjek = k.koderincianobjek
				)
				JOIN akuntansi.anov_jurnal_rekening(tahun,
					kodeurusan,kodesuburusan,kodeorganisasi,
					kodebidang,kodeprogram,kodekegiatan
				) r ON (
					r.kodeakun = k.a_kodeakun AND r.kodekelompok = k.a_kodekelompok AND r.kodejenis = k.a_kodejenis
					AND r.kodeobjek = k.a_kodeobjek AND r.koderincianobjek = k.a_koderincianobjek
				)
				WHERE s.tahun = tahun
				AND s.kodeurusan = kodeurusan AND s.kodesuburusan = kodesuburusan AND s.kodeorganisasi = kodeorganisasi
				AND s.nobukukas = nomor AND s.kodeakun = 2 LOOP
					urut := urut + 1;
					debet := 0;

					RETURN NEXT;
				END LOOP;
			END IF;

		ELSIF (jenis = 'SP2D' AND jenissp2d = 'NON ANGG') THEN /* [TODO] */
			urut := 0;

			FOR
				kodebidang,kodeprogram,kodekegiatan,
				kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek,
				kode_rekening,urai_rekening,
				debet
			IN SELECT
				s.kodebidang,s.kodeprogram,s.kodekegiatan,
				k.a_kodeakun,k.a_kodekelompok,k.a_kodejenis,k.a_kodeobjek,k.a_koderincianobjek,
				r.kode_rekening,r.urai_rekening,
				COALESCE((sr.pengeluaran - sr.penerimaan),0)
			FROM kasda.kasda_transaksi_detil s
			JOIN akuntansi.konversi_akrual k on (s.tahun = k.tahun
				AND s.kodeakun = k.kodeakun AND s.kodekelompok = k.kodekelompok AND s.kodejenis = k.kodejenis
				AND s.kodeobjek = k.kodeobjek AND s.koderincianobjek = k.koderincianobjek
			)
			JOIN akuntansi.anov_jurnal_rekening(tahun,
				kodeurusan,kodesuburusan,kodeorganisasi,
				kodebidang,kodeprogram,kodekegiatan
			) r ON (
				r.kodeakun = k.a_kodeakun AND r.kodekelompok = k.a_kodekelompok AND r.kodejenis = k.a_kodejenis
				AND r.kodeobjek = k.a_kodeobjek AND r.koderincianobjek = k.a_koderincianobjek
			)
			WHERE s.tahun= tahun
			AND s.kodeurusan = kodeurusan AND s.kodesuburusan = kodesuburusan AND s.kodeorganisasi = kodeorganisasi
			AND s.nobukukas = nomor AND s.kodeakun = 2 LOOP
				urut := urut + 1;
				kredit := 0;

				RETURN NEXT;
			END LOOP;

			urut := urut + 1;

			SELECT UPPER(TRIM(a.rekening)) FROM kasda.kasda_sumberdanarekening a
			WHERE a.kodesumberdana = sumberdana_kode INTO sumberdana_rekbank;

			SELECT a.* FROM akuntansi.anov_jurnal_rekening(tahun,kodeurusan,kodesuburusan,kodeorganisasi) a
			WHERE a.kodeakun = 1 AND a.kodekelompok = 1 AND a.kodejenis = 1
			AND UPPER(TRIM(a.urai_rekening)) LIKE '%'||sumberdana_rekbank||'%'
			INTO kode_rekening,urai_rekening, kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek;

			SELECT COALESCE(SUM(a.pengeluaran - a.penerimaan),0) FROM kasda.kasda_transaksi_detil a WHERE a.tahun = tahun
			AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
			AND a.nobukukas = nomor AND a.kodeakun = 2 INTO kredit;
			debet := 0;

			RETURN NEXT;

		ELSIF (jenis = 'SP2D' AND jenissp2d = 'LS_PPKD') THEN /* [TODO] */
			/* --- (mbamad): beban terhadap kas di kasda; --- */
			FOR
				kodebidang,kodeprogram,kodekegiatan,
				kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek,
				kode_rekening,urai_rekening,
				debet
			IN SELECT 
				s.kodebidang,s.kodeprogram,s.kodekegiatan,
				k.lob_kodeakun, k.lob_kodekelompok,k.lob_kodejenis,k.lob_kodeobjek,k.lob_koderincianobjek,
				r.kode_rekening,r.urai_rekening,
				COALESCE(s.pengeluaran,0)
			FROM kasda.kasda_transaksi_detil s
			JOIN akuntansi.konversi_akrual k on (s.tahun = k.tahun
				AND s.kodeakun = k.kodeakun AND s.kodekelompok = k.kodekelompok AND s.kodejenis = k.kodejenis
				AND s.kodeobjek = k.kodeobjek AND s.koderincianobjek = k.koderincianobjek
			)
			JOIN akuntansi.anov_jurnal_rekening(tahun,
				kodeurusan,kodesuburusan,kodeorganisasi,
				kodebidang,kodeprogram,kodekegiatan
			) r ON (
				r.kodeakun = k.a_kodeakun AND r.kodekelompok = k.a_kodekelompok AND r.kodejenis = k.a_kodejenis
				AND r.kodeobjek = k.a_kodeobjek AND r.koderincianobjek = k.a_koderincianobjek
			)
			WHERE s.tahun = tahun
			AND s.kodeurusa = kodeurusan AND s.kodesuburusa = kodesuburusan AND s.kodeorganisasi = kodeorganisasi
			AND s.nobukukas = nomor
			AND s.kodeakun in(5,6) LOOP
				urut := urut + 1;

				kredit := 0;

				RETURN NEXT;
			END LOOP;

			urut := urut + 1;

			SELECT UPPER(TRIM(a.rekening)) FROM kasda.kasda_sumberdanarekening a
			WHERE a.kodesumberdana = sumberdana_kode INTO sumberdana_rekbank;

			SELECT a.* FROM akuntansi.anov_jurnal_rekening(tahun,kodeurusan,kodesuburusan,kodeorganisasi) a
			WHERE a.kodeakun = 1 AND a.kodekelompok = 1 AND a.kodejenis = 1
			AND UPPER(TRIM(a.urai_rekening)) LIKE '%'||sumberdana_rekbank||'%'
			INTO kode_rekening,urai_rekening, kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek;

			SELECT COALESCE(SUM(pengeluaran - penerimaan),0) FROM kasda.kasda_transaksi_detil WHERE a.tahun = tahun 
			AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
			AND a.nobukukas = nobukti INTO kredit;
			debet := 0;

			RETURN NEXT;

			/* --- (mbamad): realisasi; --- */
			FOR
				kodebidang,kodeprogram,kodekegiatan,
				kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek,
				kode_rekening,urai_rekening,
				debet
			IN SELECT
				s.kodebidang,s.kodeprogram,s.kodekegiatan,
				k.a_kodeakun,k.a_kodekelompok,k.a_kodejenis,k.a_kodeobjek,k.a_koderincianobjek,
				r.kode_rekening,r.urai_rekening,
				COALESCE(sr.pengeluaran,0)
			FROM kasda.kasda_transaksi_detil s
			JOIN akuntansi.konversi_akrual k on (s.tahun = k.tahun
				AND s.kodeakun = k.kodeakun AND s.kodekelompok = k.kodekelompok AND s.kodejenis = k.kodejenis
				AND s.kodeobjek = k.kodeobjek AND s.koderincianobjek = k.koderincianobjek
			)
			JOIN akuntansi.anov_jurnal_rekening(tahun,
				kodeurusan,kodesuburusan,kodeorganisasi,
				kodebidang,kodeprogram,kodekegiatan
			) r ON (
				r.kodeakun = k.a_kodeakun AND r.kodekelompok = k.a_kodekelompok AND r.kodejenis = k.a_kodejenis
				AND r.kodeobjek = k.a_kodeobjek AND r.koderincianobjek = k.a_koderincianobjek
			)
			WHERE s.tahun = tahun
			AND s.kodeurusan = kodeurusan AND s.kodesuburusan = kodesuburusan AND s.kodeorganisasi = kodeorganisasi
			AND s.nobukukas = nomor LOOP
				urut := urut + 1;

				kredit := 0;

				RETURN NEXT;
			END LOOP;

			/* --- (mbamad): perubahan sal; --- */
			urut := urut + 1;

			SELECT a.* FROM akuntansi.anov_jurnal_rekening(tahun,kodeurusan,kodesuburusan,kodeorganisasi) a
			WHERE a.kodeakun = 3 AND a.kodekelompok = 1 AND a.kodejenis = 2
			AND a.kodeobjek = 5 AND a.koderincianobjek = 1
			INTO kode_rekening,urai_rekening, kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek;

			SELECT COALESCE(SUM(a.pengeluaran),0) FROM kasda.kasda_transaksi_detil a WHERE a.tahun = tahun 
			AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
			AND a.nobukukas = nobukti INTO kredit;
			debet := 0;

			RETURN NEXT;

		ELSIF (jenis = 'CONTRA') THEN /* [TODO] */
			/* --- (mbamad): kas di kasda; --- */
			urut := 1;
			SELECT a.kodesumberdana FROM kasda.kasda_transaksi a WHERE a.tahun = tahun
			AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
			AND a.nobukukas = nomor INTO sumberdana_kode;

			SELECT a.rekening FROM kasda.kasda_sumberdanarekening a
			WHERE a.kodesumberdana = sumberdana_kode INTO sumberdana_rekbank;

			SELECT a.* FROM akuntansi.anov_jurnal_rekening(tahun,kodeurusan,kodesuburusan,kodeorganisasi) a
			WHERE a.kodeakun = 1 AND a.kodekelompok = 1 AND a.kodejenis = 1
			AND UPPER(TRIM(a.urai_rekening)) LIKE '%'||sumberdana_rekbank||'%'
			INTO kode_rekening,urai_rekening, kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek;

			SELECT COALESCE(SUM(a.penerimaan),0) FROM kasda.kasda_transaksi_detil a WHERE a.tahun = tahun
			AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
			AND a.nobukukas = nomor INTO debet;
			kredit := 0;
			RETURN NEXT;

			urut := urut + 1;
			SELECT a.* FROM akuntansi.anov_jurnal_rekening(tahun,kodeurusan,kodesuburusan,kodeorganisasi) a
			WHERE a.kodeakun = 1 AND a.kodekelompok = 1 AND a.kodejenis = 8
			AND UPPER(TRIM(a.urai_rekening)) LIKE '%'||skpkd||'%'
			INTO kode_rekening,urai_rekening, kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek;

			SELECT COALESCE(SUM(a.penerimaan),0) FROM kasda.kasda_transaksi_detil a WHERE a.tahun = tahun 
			AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
			AND a.nobukukas = nomor INTO kredit;
			debet := 0;
			RETURN NEXT;

		ELSIF (jenis IN ('STS','CONTRAKEMARIN')) THEN /* [TODO] */
			/* --- (mbamad): kas di kasda; --- */
			urut := 1;

			SELECT c.*
			FROM kasda.kasda_transaksi a
			JOIN kasda.kasda_sumberdanarekening b ON (b.kodesumberdana = a.kodesumberdana)
			JOIN akuntansi.anov_jurnal_rekening(tahun,kodeurusan,kodesuburusan,kodeorganisasi) c ON (
				c.kodeakun = 1 AND c.kodekelompok = 1 AND c.kodejenis = 1
				AND UPPER(TRIM(c.urai_rekening)) LIKE '%'||UPPER(TRIM(b.rekening))||'%'
			)
			WHERE a.tahun = tahun AND a.nobukukas = nomor
			AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
			INTO kode_rekening,urai_rekening, kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek;

			kredit := 0;
			SELECT COALESCE(SUM(a.penerimaan),0) INTO debet
			FROM kasda.kasda_transaksi_detil a WHERE a.tahun = tahun AND a.nobukukas = nomor
			AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi;
			RETURN NEXT;

			/* --- (mbamad): penerimaan sts skpd; --- */
			IF ((
				SELECT COUNT(*) FROM kasda.kasda_transaksi_detil a WHERE a.tahun = tahun AND a.nobukukas = nomor
				AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
				AND a.kodeakun = 4 AND a.kodekelompok = 1
			) > 0) THEN
				/* --- (mbamad): rk skpd; --- */
				urut := urut + 1;

				SELECT a.* FROM akuntansi.anov_jurnal_rekening(tahun,kodeurusan,kodesuburusan,kodeorganisasi) a
				WHERE a.kodeakun = 1 AND a.kodekelompok = 1 AND a.kodejenis = 8
				AND UPPER(TRIM(a.urai_rekening)) LIKE '%'||skpkd||'%'
				INTO kode_rekening,urai_rekening, kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek;

				debet := 0;
				SELECT COALESCE(SUM(a.penerimaan),0) INTO kredit
				FROM kasda.kasda_transaksi_detil a WHERE a.tahun = tahun AND a.nobukukas = nomor
				AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi;
				RETURN NEXT;
			END IF;

			/* --- (mbamad): pengembalian saldo kas bend tahun lalu; --- */
			IF ((
					SELECT COUNT(*) FROM kasda.kasda_transaksi_detil a WHERE a.tahun = tahun AND a.nobukukas = nomor
					AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
					AND a.kodeakun = 6 AND a.kodekelompok = 1
			) > 0) THEN
				urut := urut + 1;

				SELECT a.* FROM akuntansi.anov_jurnal_rekening(tahun,kodeurusan,kodesuburusan,kodeorganisasi) a
				WHERE a.kodeakun = 3 AND a.kodekelompok = 1 AND a.kodejenis = 1
				AND a.kodeobjek = 1 AND a.koderincianobjek = 1
				INTO kode_rekening,urai_rekening, kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek;

				debet := 0;
				SELECT COALESCE(SUM(a.penerimaan),0) INTO kredit
				FROM kasda.kasda_transaksi_detil a WHERE a.tahun = tahun AND a.nobukukas = nomor
				AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi;
				RETURN NEXT;

				/* --- (mbamad): perubahan sal; --- */
				urut := urut + 1;

				SELECT a.* FROM akuntansi.anov_jurnal_rekening(tahun,kodeurusan,kodesuburusan,kodeorganisasi) a
				WHERE a.kodeakun = 3 AND a.kodekelompok = 1 AND a.kodejenis = 2
				AND a.kodeobjek = 5 AND a.koderincianobjek = 1
				INTO kode_rekening,urai_rekening, kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek;

				kredit=0;
				SELECT COALESCE(SUM(a.penerimaan),0) INTO debet
				FROM kasda.kasda_transaksi_detil a WHERE a.tahun = tahun AND a.nobukukas = nomor
				AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi;
				RETURN NEXT;

				/* -- (mbamad): rekening lra; --- */
				FOR
					kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek
				IN SELECT
					k.a_kodeakun,k.a_kodekelompok,k.a_kodejenis,k.a_kodeobjek,k.a_koderincianobjek
				from kasda_transaksi_detil sr
				join konversi_akrual k on (sr.tahun=k.tahun
					AND sr.kodeakun=k.kodeakun AND sr.kodekelompok=k.kodekelompok AND sr.kodejenis=k.kodejenis
					AND sr.kodeobjek=k.kodeobjek AND sr.koderincianobjek=k.koderincianobjek
				)
				where sr.tahun = tahun AND sr.nobukukas = nomor
				AND sr.kodeurusan = kodeurusan AND sr.kodesuburusan = kodesuburusan AND sr.kodeorganisasi = kodeorganisasi
				LOOP
					urut := urut + 1;

					SELECT a.kode_rekening,a.urai_rekening
					FROM akuntansi.anov_jurnal_rekening(tahun,kodeurusan,kodesuburusan,kodeorganisasi) a
					WHERE a.kodeakun = kodeakun AND a.kodekelompok = kodekelompok AND a.kodejenis = kodejenis
					AND a.kodeobjek = kodeobjek AND a.koderincianobjek = koderincianobjek
					INTO kode_rekening,urai_rekening;

					debet := 0;
					SELECT COALESCE(SUM(a.penerimaan - a.pengeluaran),0) INTO kredit
					FROM kasda.kasda_transaksi_detil a WHERE a.tahun = tahun AND a.nobukukas = nomor
					AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi;

					RETURN NEXT;
				END LOOP;

				/* --- (mbamad) penerimaan sts ppkd; --- */
				IF ((
					SELECT COUNT(*) FROM kasda.kasda_transaksi_detil a WHERE a.tahun = tahun AND a.nobukukas = nomor
					AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
					AND a.kodeakun = 4 AND a.kodekelompok <> 1
				) > 0) THEN
					FOR kode_rekening,urai_rekening, kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek
					IN SELECT d.*
					FROM kasda.kasda_transaksi_detil s
					JOIN akuntansi.konversi_akrual k on (k.tahun = s.tahun
						AND k.kodeakun = s.kodeakun AND k.kodekelompok = s.kodekelompok AND k.kodejenis = s.kodejenis
						AND k.kodeobjek = s.kodeobjek AND k.koderincianobjek = s.koderincianobjek
					)
					JOIN akuntansi.konversi_akrual_piutang r ON (r.tahun = k.tahun
						AND r.kodeakun = k.a_kodeakun AND r.kodekelompok = k.a_kodekelompok AND r.kodejenis = k.a_kodejenis
						AND r.kodeobjek = k.a_kodeobjek AND r.koderincianobjek = k.a_koderincianobjek
					)
					JOIN akuntansi.anov_jurnal_rekening(r.tahun,
						s.kodeurusan,s.kodesuburusan,s.kodeorganisasi
					) d ON (d.kodeakun = r.a_kodeakun AND d.kodekelompok = r.a_kodekelompok AND d.kodejenis = r.a_kodejenis
						AND d.kodeobjek = r.a_kodeobjek AND d.koderincianobjek = r.a_koderincianobjek
					)
					where s.tahun = tahun AND s.nobukukas = nomor
					AND s.kodeurusan = kodeurusan AND s.kodesuburusan = kodesuburusan AND s.kodeorganisasi = kodeorganisasi
					LOOP
						urut := urut + 1;

						debet := 0;
						SELECT COALESCE(SUM(a.penerimaan - a.pengeluaran), 0) INTO kredit
						FROM kasda.kasda_transaksi_detil a WHERE a.tahun = tahun AND a.nobukukas = nomor
						AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi;

						RETURN NEXT;
					END LOOP;

					/* --- (mbamad): perubahan sal; --- */
					urut := urut + 1;

					SELECT a.* FROM akuntansi.anov_jurnal_rekening(tahun,kodeurusan,kodesuburusan,kodeorganisasi) a
					WHERE a.kodeakun = 3 AND a.kodekelompok = 1 AND a.kodejenis = 2
					AND a.kodeobjek = 5 AND a.koderincianobjek = 1
					INTO kode_rekening,urai_rekening, kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek;

					kredit := 0;
					SELECT COALESCE(SUM(a.penerimaan),0) INTO debet
					FROM kasda.kasda_transaksi_detil a WHERE a.tahun = tahun AND a.nobukukas = nomor
					AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
					AND kodeakun = 4;

					RETURN NEXT;

					/* --- (mbamad): rekening lra; --- */
					FOR kode_rekening,urai_rekening, kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek
					IN SELECT d.*
					FROM kasda.kasda_transaksi_detil s
					JOIN akuntansi.konversi_akrual k on (k.tahun = s.tahun
						AND k.kodeakun = s.kodeakun AND k.kodekelompok = s.kodekelompok AND k.kodejenis = s.kodejenis
						AND k.kodeobjek = s.kodeobjek AND k.koderincianobjek = s.koderincianobjek
					)
					JOIN akuntansi.anov_jurnal_rekening(k.tahun,
						s.kodeurusan,s.kodesuburusan,s.kodeorganisasi
					) d ON (d.kodeakun = k.a_kodeakun AND d.kodekelompok = k.a_kodekelompok AND d.kodejenis = k.a_kodejenis
						AND d.kodeobjek = k.a_kodeobjek AND d.koderincianobjek = k.a_koderincianobjek
					)
					where s.tahun = tahun AND s.nobukukas = nomor
					AND s.kodeurusan = kodeurusan AND s.kodesuburusan = kodesuburusan AND s.kodeorganisasi = kodeorganisasi
					LOOP
						urut := urut + 1;

						debet := 0;
						SELECT COALESCE(SUM(a.penerimaan - a.pengeluaran),0) INTO kredit
						FROM kasda.kasda_transaksi_detil a WHERE a.tahun = tahun AND a.nobukukas = nomor
						AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi;

						RETURN NEXT;
					END LOOP;
				END IF;
			END IF;

		/* diaktifkan jika sudah produksi */
		/* ELSE RAISE EXCEPTION 'unknown jenis(%) and nomor(%);', jenis, nomor; */
		END IF;
	END IF;
END $storedprocedure$ LANGUAGE plpgsql;


/* [LINT] */

/* seharusnya tidak akan muncul error */
DO $execute$ BEGIN PERFORM akuntansi.anov_akrual_to_jurnal_ppkd_ju_rincian('2019','TIDAKCAIR','anov/sp2d/01'); END $execute$;
DO $execute$ BEGIN PERFORM akuntansi.anov_akrual_to_jurnal_ppkd_ju_rincian('2019','PINDAHBUKU','kasda'); END $execute$;
DO $execute$ BEGIN PERFORM akuntansi.anov_akrual_to_jurnal_ppkd_ju_rincian('2019','STS','anov/STS'); END $execute$;
DO $execute$ BEGIN PERFORM akuntansi.anov_akrual_to_jurnal_ppkd_ju_rincian('2019','CONTRA','anov/CONTRA'); END $execute$;
DO $execute$ BEGIN PERFORM akuntansi.anov_akrual_to_jurnal_ppkd_ju_rincian('2019','CONTRAKEMARIN','anov/CONTRAKEMARIN'); END $execute$;

/* (SP2D/default) jika kasda-sp2d tidak ada, maka akan error (jika exception nyala) */
DO $execute$ BEGIN PERFORM akuntansi.anov_akrual_to_jurnal_ppkd_ju_rincian('2019','SP2D','kasda/sp2d/default'); /* sp2d_jenis_default */
EXCEPTION WHEN OTHERS THEN RAISE INFO '%', SQLERRM; END $execute$;

/* (SP2D/'NON ANGG') belum ada dumy|data untuk test  */
DO $execute$ BEGIN PERFORM akuntansi.anov_akrual_to_jurnal_ppkd_ju_rincian('2019','SP2D','kasda/sp2d/NON-ANGG');
EXCEPTION WHEN OTHERS THEN RAISE INFO '%', SQLERRM; END $execute$;

/* (SP2D/'LS_PPKD') belum ada dumy|data untuk test  */
DO $execute$ BEGIN PERFORM akuntansi.anov_akrual_to_jurnal_ppkd_ju_rincian('2019','SP2D','kasda/sp2d/LS_PPKD');
EXCEPTION WHEN OTHERS THEN RAISE INFO '%', SQLERRM; END $execute$;

DO $execute$ BEGIN PERFORM akuntansi.anov_akrual_to_jurnal_ppkd_ju_rincian('2019','WHATEVER','anov/999');
EXCEPTION WHEN OTHERS THEN RAISE INFO '%', SQLERRM; END $execute$;
