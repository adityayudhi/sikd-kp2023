/*
	[ABANDONED][DEPRECATED][UNUSED]
	20190705113958. TIDAK JADI (~/views/spjskpd/storedprocedures/04.sql).
	barusan telp yudhi, dia yang akan kerjakan [SPJ SKPD]>[Akuntansi SKPD Basis Akrual],
	lalu saya kerjakan yang [Akuntansi]>[Akuntansi Akrual PPKD].
*/

DO $execute$ BEGIN
	PERFORM __rmfn__('akuntansi.anov_akrual_rincian_penutup_lra');
END $execute$;

CREATE OR REPLACE FUNCTION akuntansi.anov_akrual_rincian_penutup_lra(
	xtahun ANYELEMENT,
	kodeurusan INTEGER, kodesuburusan INTEGER, xkodeorganisasi ANYELEMENT,
	isskpd SMALLINT DEFAULT NULL,
	tglawal TIMESTAMP DEFAULT NULL,
	tglakhir TIMESTAMP DEFAULT NULL
) RETURNS TABLE(
	kodebidang VARCHAR(8), kodeprogram INTEGER, kodekegiatan INTEGER,
	kodeakun INTEGER, kodekelompok INTEGER, kodejenis INTEGER, kodeobjek INTEGER, koderincianobjek INTEGER,
	kode_rekening TEXT,
	urai_rekening TEXT,
	debet NUMERIC(15,2),
	kredit NUMERIC(15,2)
) AS $storedprocedure$
/* @version: ?; @origin: AKRUAL_VIEW_PENUTUP_LRA(); @author: anovsiradj; */

#VARIABLE_CONFLICT use_variable
DECLARE
	tahun VARCHAR(8);
	kodeorganisasi VARCHAR(8);
	xjumlah NUMERIC(15,2);
	xbelanja NUMERIC(15,2);
	xpendapatan NUMERIC(15,2);
	xpenutup NUMERIC(15,2);

BEGIN
	tahun = xtahun;
	kodeorganisasi = LPAD(xkodeorganisasi, '0');

	IF(tglawal IS NULL) THEN tglawal := tahun || '-01-01'; END IF;
	IF(tglakhir IS NULL) THEN tglakhir := tahun || '-12-31'; END IF;

	IF(isskpd IS NULL) THEN
		SELECT a.skpkd FROM master.master_organisasi a WHERE a.tahun = tahun
		AND a.kodeurusan = kodeurusan AND a.kodesuburusan = a.kodesuburusan AND a.kodeorganisasi = a.kodeorganisasi
		INTO isskpd;
	END IF;

	/* 01: PENDAPATAN LRA; */
	FOR
		kodebidang,kodeprogram,kodekegiatan,
		kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek,
		xjumlah
	IN SELECT
		a.kodebidang,a.kodeprogram,a.kodekegiatan,
		a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek,
		SUM(a.kredit-a.debet)
	FROM akuntansi.akrual_jurnal_rincian a 
	JOIN  akuntansi.akrual_buku_jurnal b ON (a.tahun = b.tahun
		AND a.kodeurusan = b.kodeurusan AND a.kodesuburusan = b.kodesuburusan AND a.kodeorganisasi = b.kodeorganisasi
		AND a.isskpd = b.isskpd
		AND a.noref = b.noref
	)
	WHERE a.tahun = tahun 
	AND a.kodeurusan = kodeurusan AND a.kodesuburusan = kodesuburusan AND a.kodeorganisasi = kodeorganisasi
	AND a.kodeakun = 4
	AND b.isskpd = isskpd
	AND b.jenisjurnal NOT IN (4)
	AND b.tanggalbukti >= tglawal AND b.tanggalbukti <= tglakhir
	GROUP BY a.kodebidang,a.kodeprogram,a.kodekegiatan,a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek
	ORDER BY a.kodebidang,a.kodeprogram,a.kodekegiatan,a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek
	LOOP
		/* saya penasaran, apakah memang penulisan nya memang harus seperti ini,
		lalu dimana penempatan kode(bidang|program|kegiatan)nya? */
		kode_rekening = (
			kodeurusan||'.'||LZERO(kodesuburusan,2,'0')||'.'||kodeorganisasi||'.0.0-'||
			kodeakun||'.'||kodekelompok||'.'||kodejenis||'.'||LZERO(kodeobjek,2,'0')||'.'||LZERO(koderincianobjek,2,'0')
		);

		 SELECT a.urai FROM akuntansi.akrual_master_rekening a WHERE a.tahun = tahun
		 AND a.kodeakun = kodeakun AND a.kodekelompok = kodekelompok
		 AND a.kodejenis = kodejenis AND a.kodeobjek = kodeobjek AND a.koderincianobjek = koderincianobjek
		 INTO urai_rekening;
		 if(xjumlah IS NULL) THEN xjumlah=0; END IF;
		 if(xjumlah > 0) THEN
		 	debet = xjumlah;
		 	kredit = 0;
		 END IF;

		 RETURN NEXT;
	END LOOP;

/* SURPLUS DEFISIT LRA */
/*
select sum(sr.debet-sr.kredit) from akrual_jurnal_rincian sr  join  akrual_buku_jurnal s on
(sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.isskpd=s.isskpd and sr.noref=s.noref)
where sr.tahun=:tahun and sr.kodeurusan=:kodeurusan and sr.kodesuburusan=:kodesuburusan and sr.kodeorganisasi=:kodeorganisasi and s.tanggalbukti>='01-jan-'||:tahun
and s.tanggalbukti<=:tglakhir and s.jenisjurnal not in (4)  and sr.isskpd=:ISSKPD
and sr.kodeakun=5 into :xbelanja;
if  (:xbelanja is null) then xbelanja=0;

select sum(sr.kredit-sr.debet) from akrual_jurnal_rincian sr  join  akrual_buku_jurnal s on
(sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.isskpd=s.isskpd and sr.noref=s.noref)
where sr.tahun=:tahun and sr.kodeurusan=:kodeurusan and sr.kodesuburusan=:kodesuburusan and sr.kodeorganisasi=:kodeorganisasi and s.tanggalbukti>='01-jan-'||:tahun
and s.tanggalbukti<=:tglakhir  and s.jenisjurnal not in (4)  and sr.isskpd=:ISSKPD
and sr.kodeakun=4 into :xpendapatan;

if  (:xpendapatan is null) then xpendapatan=0;
select  kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek,urai from akrual_master_rekening where tahun=:tahun
and kodeakun=3 and kodekelompok=1 and kodejenis=2 and kodeobjek=6 and koderincianobjek=1
into  kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek,uraian;
koderekening=:kodeurusan||'.'||lzero(:kodesuburusan,2,'0')||'.'||:kodeorganisasi||'.00.00-'||:kodeakun||'.'||:kodekelompok||'.'||:kodejenis||'.'||lzero(:kodeobjek,2,'0')||'.'||lzero(:koderincianobjek,2,'0');
xjumlah=:xpendapatan-:xbelanja;
xpenutup=:xjumlah;
if  (:xjumlah < 0) then
begin
	 debet=-1*(:xjumlah);  kredit=0;
end
if  (:xjumlah > 0) then
begin
	 kredit=(:xjumlah); debet=0;
end
suspend;
*/

/*-- BELANJA LRA -- */
/*
for select sr.kodeakun,sr.kodekelompok,sr.kodejenis,sr.kodeobjek,sr.koderincianobjek,sum(sr.debet-sr.kredit) from akrual_jurnal_rincian sr  join  akrual_buku_jurnal s on
(sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.isskpd=s.isskpd and sr.noref=s.noref)
where sr.tahun=:tahun and sr.kodeurusan=:kodeurusan and sr.kodesuburusan=:kodesuburusan and sr.kodeorganisasi=:kodeorganisasi and s.tanggalbukti>='01-jan-'||:tahun
and s.tanggalbukti<=:tglakhir
and sr.kodeakun=5   and s.jenisjurnal not in (4)  and sr.isskpd=:ISSKPD
group by sr.kodeakun,sr.kodekelompok,sr.kodejenis,sr.kodeobjek,sr.koderincianobjek
into kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek,xjumlah
do
begin
	 koderekening=:kodeurusan||'.'||lzero(:kodesuburusan,2,'0')||'.'||:kodeorganisasi||'.00.00-'||:kodeakun||'.'||:kodekelompok||'.'||:kodejenis||'.'||lzero(:kodeobjek,2,'0')||'.'||lzero(:koderincianobjek,2,'0');
	 select urai from akrual_master_rekening where tahun=:tahun and kodeakun=:kodeakun and kodekelompok=:kodekelompok
	 and kodejenis=:kodejenis and kodeobjek=:kodeobjek and koderincianobjek=:koderincianobjek into uraian;
	 if  (xjumlah is null) then xjumlah=0;
	 if  (xjumlah>0) then
	 begin
			kredit=:xjumlah;debet=0;
	 end
	 suspend;
end
*/

--ekuitas sal terhadap surplus defisit--
/*
select  kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek,urai from akrual_master_rekening where tahun=:tahun
and kodeakun=3 and kodekelompok=1 and kodejenis=2 and kodeobjek=5 and koderincianobjek=1
into  kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek,uraian;
koderekening=:kodeurusan||'.'||lzero(:kodesuburusan,2,'0')||'.'||:kodeorganisasi||'.00.00-'||:kodeakun||'.'||:kodekelompok||'.'||:kodejenis||'.'||lzero(:kodeobjek,2,'0')||'.'||lzero(:koderincianobjek,2,'0');
if  (xpenutup<0) then
begin
		 debet=-1*(:xpenutup); kredit=0;
end
if  (xpenutup>0) then
begin
		 debet=0; kredit=:xpenutup;
end
suspend;
*/

/*
select  kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek,urai from akrual_master_rekening where tahun=:tahun
and kodeakun=3 and kodekelompok=1 and kodejenis=2 and kodeobjek=6 and koderincianobjek=1
into  kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek,uraian;
koderekening=:kodeurusan||'.'||lzero(:kodesuburusan,2,'0')||'.'||:kodeorganisasi||'.00.00-'||:kodeakun||'.'||:kodekelompok||'.'||:kodejenis||'.'||lzero(:kodeobjek,2,'0')||'.'||lzero(:koderincianobjek,2,'0');
if  (xpenutup<0) then
begin
		 kredit=-1*(:xpenutup);
		 debet=0;
end
if  (xpenutup>0) then
begin
		 kredit=0; debet=:xpenutup;
end
suspend;
*/

END;
$storedprocedure$ LANGUAGE plpgsql;

DO $execute$ BEGIN
	PERFORM akuntansi.anov_akrual_rincian_penutup_lra(2019,1,1,1);
END $execute$;
