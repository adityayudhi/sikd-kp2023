/*
FLEX:/sipkd_SPJSKPD/src/spjskpd/views/VBKU.mxml@ambilData()
*/

select 
0 as cek,
s.no_bku,
s.tgl_bku,
s.urai,
s.jenis_bku,
s.bukti,
case
	when jenis_bku in ('SALDOAWAL','SIMPANAN-BANK','KAS-TUNAI','PANJAR') and s.penerimaan <>0  then s.penerimaan
	when jenis_bku  in ('SP2D-GJ','SP2D','PUNGUT-PAJAK','KOREKSI PENERIMAAN','RK-PPKD')
		then (
			select sum (sr.penerimaan) 
			from pertanggungjawaban.skpd_bkurincian sr where sr.tahun=s.tahun
			and sr.kodeurusan=s.kodeurusan and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi
			and sr.no_bku=s.no_bku and sr.isskpd=s.isskpd 
		)
end as penerimaan,
case
	when jenis_bku in ('SALDOAWAL','SIMPANAN-BANK','KAS-TUNAI','PANJAR') and s.pengeluaran <>0  then s.pengeluaran 
	when jenis_bku  in ('BAYAR-GJ','SPJ','SETOR-PAJAK','KOREKSI PENGELUARAN','RK-PPKD')
		then (
			select sum (sr.pengeluaran)
			from pertanggungjawaban.skpd_bkurincian sr where sr.tahun=s.tahun
			and sr.kodeurusan=s.kodeurusan and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi 
			and sr.no_bku=s.no_bku and sr.isskpd=s.isskpd 
		)  
end as pengeluaran,
s.jenis_sp2d

from pertanggungjawaban.skpd_bku s where s.tahun=(?)
and s.isskpd=0
and s.kodeurusan=(?) and s.kodesuburusan=(?) and s.kodeorganisasi=(?)
and extract (month from s.tgl_bku)=(?)
order by s.tgl_bku,s.no_bku
