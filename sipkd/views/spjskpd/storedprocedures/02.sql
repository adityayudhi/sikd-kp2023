DO $execute$ BEGIN
	PERFORM __rmfn__('pertanggungjawaban.anov_skpd_stsrincian_pengembalian');
END $execute$;

CREATE OR REPLACE FUNCTION pertanggungjawaban.anov_skpd_stsrincian_pengembalian(
	in_tahun CHARACTER,
	in_kodeurusan integer,
	in_kodesuburusan integer,
	in_kodeorganisasi CHARACTER,
	in_jenis CHARACTER VARYING,
	in_nosts CHARACTER VARYING
)
RETURNS TABLE(
	kode_rekening TEXT,
	urai_rekening TEXT,
	kodebidang VARCHAR(8),
	kodeprogram INTEGER,
	kodekegiatan INTEGER,
	kodeakun INTEGER,
	kodekelompok INTEGER,
	kodejenis INTEGER,
	kodeobjek INTEGER,
	koderincianobjek INTEGER,
	jumlah NUMERIC(15,2)
) 
AS $storedprocedure$
/*

	20190701

	PENDING.
	saya pake skpd_view_rincianpengembalian() dulu,
	karena masih belum tau kegunaan dari function tersebut.

*/
#variable_conflict use_variable
DECLARE
	ret record;
	xisskpd SMALLINT := 0;
	rec_pengembalian record;
	rec_belanja record;
	var_xjumlah integer;
BEGIN
IF (UPPER(in_jenis) = 'GJ') THEN
	FOR
		kode_rekening,
		kodebidang,kodeprogram,kodekegiatan,
		kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek
	IN SELECT
		(
			a.kodeurusan||'.'||LPAD(a.kodesuburusan::text,2,'0')||'.'||a.kodeorganisasi||'.0.0-'||
			a.kodeakun||'.'||a.kodekelompok||'.'||a.kodejenis||'.'||LPAD(a.kodeobjek::text,2,'0')||'.'||LPAD(a.koderincianobjek::text,2,'0')
		),
		a.kodebidang,a.kodeprogram,a.kodekegiatan,
		a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek
	FROM penatausahaan.sp2drincian a WHERE a.tahun = in_tahun
	AND a.kodeurusan = in_kodeurusan AND a.kodesuburusan = in_kodesuburusan AND a.kodeorganisasi = in_kodeorganisasi
	AND a.kodeprogram = 0 AND a.kodekegiatan = 0
	AND a.kodeakun = 5 AND a.kodekelompok = 1 AND a.kodejenis = 1
	GROUP BY a.tahun,
	a.kodeurusan,a.kodesuburusan,a.kodeorganisasi, a.kodebidang,a.kodeprogram,a.kodekegiatan,
	a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek
	ORDER BY
	a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek
	LOOP
		SELECT b.urai FROM master.master_rekening b WHERE b.tahun = in_tahun
		AND b.kodeakun = kodeakun AND b.kodekelompok = kodekelompok AND b.kodejenis = kodejenis AND b.kodeobjek = kodeobjek AND b.koderincianobjek = koderincianobjek
		into urai_rekening;

		SELECT b.jumlah FROM pertanggungjawaban.skpd_rincian_pengembalian b WHERE b.tahun = in_tahun
		AND b.kodeurusan = in_kodeurusan AND b.kodesuburusan = in_kodesuburusan AND b.kodeorganisasi = in_kodeorganisasi
		AND b.nosts=in_nosts 
		AND b.kodeprogram = 0 AND b.kodekegiatan = 0
		AND b.kodeakun = kodeakun AND b.kodekelompok = kodekelompok AND b.kodejenis= kodejenis AND b.kodeobjek = kodeobjek AND b.koderincianobjek = koderincianobjek
		into jumlah;
		jumlah = COALESCE(jumlah,0);
		RETURN NEXT;
	END LOOP;
ELSEIF ( upper(in_jenis) = 'LS' ) THEN
	FOR
		kodebidang,kodeprogram,kodekegiatan
	IN SELECT
		sp.kodebidang,sp.kodeprogram,sp.kodekegiatan
	from penatausahaan.sp2drincian sp join penatausahaan.sp2d s on
	(
		sp.tahun=s.tahun and sp.kodeurusan=s.kodeurusan and sp.kodesuburusan=s.kodesuburusan and sp.kodeorganisasi=s.kodeorganisasi
			and sp.nosp2d=s.nosp2d
	)
	where sp.tahun=in_tahun 
	and sp.kodeurusan=in_kodeurusan and sp.kodesuburusan=in_kodesuburusan and sp.kodeorganisasi=in_kodeorganisasi 
	and s.JENISSP2D='LS'
	group by sp.kodebidang,sp.kodeprogram,sp.kodekegiatan
	order by sp.kodebidang,sp.kodeprogram,sp.kodekegiatan
	LOOP
		ret.kodebidang = rec_pengembalian.kodebidang;
			ret.kodeprogram = rec_pengembalian.kodeprogram;
			ret.kodekegiatan = rec_pengembalian.kodekegiatan;
			
			if  (ret.kodeprogram =  0) then ret.urai='Belanja Tidak Langsung'; end if;
			if  (ret.kodeprogram <> 0) then
				select distinct urai from penatausahaan.kegiatan where tahun=in_tahun and kodeurusan=in_kodeurusan and kodesuburusan=in_kodesuburusan
					and kodeorganisasi=in_kodeorganisasi and kodebidang=ret.kodebidang and kodekegiatan=ret.kodekegiatan and kodeprogram=ret.kodeprogram
					into ret.urai;
			end if;
			
			ret.kodekegiatan1 = ret.kodebidang||'.'||trim(in_kodeorganisasi)||'.'||ret.kodeprogram||'.'||ret.kodekegiatan;
			select count(*) from pertanggungjawaban.skpd_rincian_pengembalian where tahun=in_tahun and kodeurusan=in_kodeurusan and kodesuburusan=in_kodesuburusan and kodeorganisasi=in_kodeorganisasi
			and kodebidang=ret.kodebidang and kodeprogram=ret.kodeprogram and kodekegiatan=ret.kodekegiatan and nosts=in_nosts
			into var_xjumlah;
			
			if(var_xjumlah > 0) then ret.cek=1; else ret.cek=0; end if;
			ret.isbold=0;
		
			-- RETURN NEXT ret;
			
			for rec_belanja in
				select kodebidang,kodeprogram,kodekegiatan,kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek from penatausahaan.belanja
					where tahun=in_tahun and kodeurusan=in_kodeurusan and kodesuburusan=in_kodesuburusan and kodeorganisasi=in_kodeorganisasi
					and kodebidang=ret.kodebidang and kodeprogram=ret.kodeprogram and kodekegiatan=ret.kodekegiatan
					order by kodebidang,kodeprogram,kodekegiatan,kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek
					LOOP
						ret.kodebidang = rec_belanja.kodebidang;
							ret.kodeprogram = rec_belanja.kodeprogram;
							ret.kodekegiatan = rec_belanja.kodekegiatan;
							ret.kodeakun = rec_belanja.kodeakun;
							ret.kodekelompok = rec_belanja.kodekelompok;
							ret.kodejenis = rec_belanja.kodejenis;
							ret.kodeobjek = rec_belanja.kodeobjek;
							ret.koderincianobjek = rec_belanja.koderincianobjek;
							
							ret.koderekening=ret.kodebidang||'.'||trim(in_kodeorganisasi)||'.'||ret.kodeprogram||'.'||ret.kodekegiatan||' - '||
					ret.kodeakun||'.'||ret.kodekelompok||'.'||ret.kodejenis||'.'||lpad(ret.kodeobjek::text,2,'0')||'.'||lpad(ret.koderincianobjek::text,2,'0');
							ret.isbold = 1;
							
							SELECT distinct urai from master.master_rekening where tahun=in_tahun and kodeakun=ret.kodeakun
							and kodekelompok=ret.kodekelompok and kodejenis=ret.kodejenis and kodeobjek=ret.kodeobjek and koderincianobjek=ret.koderincianobjek
							into ret.urai;
							
							select (CASE WHEN sum(jumlah) is NULL THEN 0 ELSE sum(jumlah) END) as jumlah from  pertanggungjawaban.skpd_rincian_pengembalian where tahun=in_tahun and kodeurusan=in_kodeurusan and kodesuburusan=in_kodesuburusan
							and kodeorganisasi=in_kodeorganisasi and nosts=in_nosts and kodebidang=ret.kodebidang
							and kodeprogram=ret.kodeprogram and kodekegiatan=ret.kodekegiatan and kodeakun=ret.kodeakun and kodekelompok=ret.kodekelompok and kodejenis=ret.kodejenis
							and kodeobjek=ret.kodeobjek and koderincianobjek=ret.koderincianobjek into ret.jumlah;
							
							-- RETURN NEXT ret;
					END LOOP;
	END LOOP;
END IF;
END;
$storedprocedure$ LANGUAGE plpgsql;
