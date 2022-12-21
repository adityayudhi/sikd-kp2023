from ...spjskpd.anov import *

jenisjenis = {
	'Akuntansi PPKD': {
		'': {'teks': ' --- Pilih Jenis Laporan Akuntansi PPKD --- ', 'fr3': ''},
		'bju': {'teks': 'Buku Jurnal Umum ( JU )', 'fr3': 'PPKSKPD/Akrual/PPKDBukuJurnal.fr3',},
		'bbb': {'teks': 'Buku Besar ( BB )', 'jenisakun': True, 'fr3': 'PPKSKPD/Akrual/PPKDBukuBesar.fr3',},
		'bjp': {'teks': 'Buku Jurnal Penyesuaian', 'fr3': 'PPKSKPD/Akrual/PPKDBukuJurnalPenyesuaian.fr3',},
		'nes': {'teks': 'Neraca Saldo',   'fr3': 'PPKSKPD/Akrual/PPKDNeracaSaldo.fr3',},
		'jup': {'teks': 'Jurnal Penutup', 'fr3': 'PPKSKPD/Akrual/PPKDJurnalPenutup.fr3',},
		'kek': {'teks': 'Kertas Kerja',   'fr3': 'PPKSKPD/Akrual/PPKDKertasKerja.fr3',},
		'prognosis': {'teks': 'Laporan Realisasi Semester Pertama (Prognosis)', 'fr3': 'PPKSKPD/Akrual/PPKDPrognosis.fr3',},
		'lra': {'teks': 'Laporan Realisasi Anggaran', 'fr3': 'PPKSKPD/Akrual/PPKDLRA.fr3',},
		'lro': {'teks': 'Laporan Operasional', 'fr3': 'PPKSKPD/Akrual/PPKDLO.fr3',},
		'nrc': {'teks': 'Neraca', 'fr3': 'PPKSKPD/Akrual/PPKDNERACA.fr3',},
		'lpe': {'teks': 'Laporan Perubahan Ekuitas', 'fr3': 'PPKSKPD/Akrual/PPKDLPE.fr3',},
		'kkk': {'teks': 'Kertas Kerja Konsolidasi',  'fr3': 'PPKSKPD/Akrual/PPKDKonsolidasi.fr3',},
	},
	'Akuntansi Pemda': {
		'': {'teks': ' --- Pilih Jenis Laporan Akuntansi Pemda --- ', 'fr3': ''},
		'lra': {'teks': 'Laporan Realisasi Anggaran (LRA) Pemda', 'fr3': 'AKUNTANSIPEMDA/Akrual/LraPemda.fr3',},
		'lop': {'teks': 'Laporan Operasional (LO) Pemda', 'fr3': 'AKUNTANSIPEMDA/Akrual/LoPemda.fr3',},
		'nep': {'teks': 'Neraca Pemda ( Versi Pmd 64 ) ', 'fr3': 'AKUNTANSIPEMDA/Akrual/NeracaPemda.fr3',},
		'wag': {'teks': 'Worksheet LRA Gabungan', 'fr3': 'AKUNTANSIPEMDA/Akrual/WorksheetLra.fr3',},
		'wog': {'teks': 'Worksheet LO Gabungan',  'fr3': 'AKUNTANSIPEMDA/Akrual/WorksheetLO.fr3',},
		'sal': {'teks': 'Laporan Perubahan SAL Pemda', 'fr3': 'AKUNTANSIPEMDA/Akrual/SALPemda.fr3',},
		'lpe': {'teks': 'Laporan Perubahan Ekuitas (LPE) Pemda', 'fr3': 'AKUNTANSIPEMDA/Akrual/lpePemda.fr3',},
		'lak': {'teks': 'Laporan Arus Kas', 'fr3': 'AKUNTANSIPEMDA/Akrual/ArusKasPemda.fr3',},
		'neg': {'teks': 'Neraca Gabungan',  'fr3': 'AKUNTANSIPEMDA/Akrual/WorksheetNeraca.fr3',},
		'ne1': {'teks': 'Neraca V.1', 'fr3': 'AKUNTANSIPEMDA/Akrual/NeracaPemdaV1.fr3',},
		'ne2': {'teks': 'Neraca V.2', 'fr3': 'AKUNTANSIPEMDA/Akrual/NeracaPemdaV2.fr3',},
		'ne3': {'teks': 'Neraca V.3', 'fr3': 'AKUNTANSIPEMDA/Akrual/NeracaPemdaV3.fr3',},
	},
}

def jenisakun(tahun):
	result = []

	with querybuilder() as qb:
		qb.execute("""
			SELECT a.kodeakun as kode, a.urai as teks FROM akuntansi.akrual_master_rekening a
			WHERE a.tahun = %s AND a.kodeakun <> 0 AND a.kodekelompok = 0
			ORDER BY a.kodeakun
		""", (tahun,))
		qb.result_many(result)

	return result
# 

def pejabat(tahun):
	result = []

	with querybuilder() as qb:
		qb.execute("""
			SELECT a.* FROM master.pejabat_skpkd a WHERE a.tahun = %s
			AND a.jenissistem = 2 ORDER BY a.id
		""", (tahun,))
		qb.result_many(result)

	return result
# 
