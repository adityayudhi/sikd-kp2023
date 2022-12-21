from django.urls import path, include
from .views import (
	main,
	spjpengeluaranskpd,
	__spjpengeluaranskpd,
	# akrual,
)

urlpatterns = [
	path('main/', include([
		path('nobkuauto', main.nobkuauto, name='spjskpd_main_nobkuauto'),
		path('skpd', main.skpd, name='spjskpd_main_skpd'),
		path('pejabat', main.pejabat, name='spjskpd_main_pejabat'),
		path('potongan', main.potongan, name='spjskpd_main_potongan'),
		path('report', main.report, name='spjskpd_main_report'),
	])),
	path('spjpengeluaranskpd/', include([
		path('', spjpengeluaranskpd.index, name='spjskpd_spjpengeluaranskpd_index'),
		path('list', spjpengeluaranskpd.data, name='spjskpd_spjpengeluaranskpd_list'),
		path('rm', spjpengeluaranskpd.rm, name='spjskpd_spjpengeluaranskpd_rm'),
		path('save', spjpengeluaranskpd.save, name='spjskpd_spjpengeluaranskpd_save'),
		path('pergeseran/', include([
			path('save', __spjpengeluaranskpd.pergeseran.save, name='spjskpd_spjpengeluaranskpd_pergeseran_save'),
			path('rm', __spjpengeluaranskpd.pergeseran.rm, name='spjskpd_spjpengeluaranskpd_pergeseran_rm'),
		])),
		path('saldoawal/', include([
			path('save', __spjpengeluaranskpd.saldoawal.save, name='spjskpd_pengeluaran_saldoawal_save'),
		])),
		path('upgu/', include([
			path('browse', __spjpengeluaranskpd.upgu.browse, name='spjskpd_spjpengeluaranskpd_upgu_browse'),
			path('sp2drincian', __spjpengeluaranskpd.upgu.sp2drincian, name='spjskpd_spjpengeluaranskpd_upgu_sp2drincian'),
			path('spjrincian', __spjpengeluaranskpd.upgu.spjrincian, name='spjskpd_spjpengeluaranskpd_upgu_spjrincian'),
			path('bkurincian', __spjpengeluaranskpd.upgu.bkurincian, name='spjskpd_spjpengeluaranskpd_upgu_bkurincian'),
		])),
		path('lsgj/', include([
			path('browse', __spjpengeluaranskpd.lsgj.browse, name='spjskpd_spjpengeluaranskpd_lsgj_browse'),
			path('rincian_sp2d', __spjpengeluaranskpd.lsgj.rincian_sp2d, name='spjskpd_spjpengeluaranskpd_lsgj_rinciansp2d'),
			path('rincian_bayar', __spjpengeluaranskpd.lsgj.rincian_bayar, name='spjskpd_spjpengeluaranskpd_lsgj_rincianbayar'),
			path('bkurincian', __spjpengeluaranskpd.lsgj.bkurincian, name='spjskpd_spjpengeluaranskpd_lsgj_bkurincian'),
		])),
		path('barjas/', include([
			path('browse', __spjpengeluaranskpd.barjas.browse, name='spjskpd_pengeluaran_barjas_browse'),
			path('rincian_sp2d', __spjpengeluaranskpd.barjas.rincian_sp2d, name='spjskpd_pengeluaran_barjas_rinciansp2d'),
			path('rincian_spj', __spjpengeluaranskpd.barjas.rincian_spj, name='spjskpd_pengeluaran_barjas_rincianspj'),
			path('bkurincian', __spjpengeluaranskpd.barjas.bkurincian, name='spjskpd_pengeluaran_barjas_bkurincian'),
			path('kegiatan_browse', __spjpengeluaranskpd.barjas.kegiatan_browse, name='spjskpd_pengeluaran_barjas_kegiatanbrowse'),
		])),
		path('tu/', include([
			path('browse', __spjpengeluaranskpd.tu.browse, name='spjskpd_pengeluaran_tu_browse'),
			path('sp2drincian', __spjpengeluaranskpd.tu.sp2drincian, name='spjskpd_spjpengeluaranskpd_tu_sp2drincian'),
			path('bkurincian', __spjpengeluaranskpd.tu.bkurincian, name='spjskpd_spjpengeluaranskpd_tu_bkurincian'),
			path('spjrincian', __spjpengeluaranskpd.tu.spjrincian, name='spjskpd_spjpengeluaranskpd_tu_spjrincian'),
		])),
		path('pajak/', include([
			path('noauto', __spjpengeluaranskpd.pajak.noauto, name='spjskpd_pengeluaran_pajak_noauto'),
			path('bkurincian', __spjpengeluaranskpd. pajak.bkurincian, name='spjskpd_pengeluaran_pajak_bkurincian'),
			path('browse', __spjpengeluaranskpd.pajak.browse, name='spjskpd_pengeluaran_pajak_browse'),
		])),
		path('panjar/', include([
			path('load', __spjpengeluaranskpd.panjar.load, name='spjskpd_spjpengeluaranskpd_panjar_load'),
			path('browse', __spjpengeluaranskpd.panjar.browse, name='spjskpd_pengeluaran_panjar_browse'),
		])),
		path('rkppkd/', include([
			path('browse', __spjpengeluaranskpd.rkppkd.browse, name='spjskpd_pengeluaran_rkppkd_browse'),
			path('stsrincian', __spjpengeluaranskpd.rkppkd.stsrincian, name='spjskpd_pengeluaran_rkppkd_stsrincian'),
			path('bkurincian', __spjpengeluaranskpd.rkppkd.bkurincian, name='spjskpd_pengeluaran_rkppkd_bkurincian'),
		])),

		path('pelimpahan/', include([
			path('load', __spjpengeluaranskpd.pelimpahan.load, name='spjskpd_spjpengeluaranskpd_pelimpahan_load'),
			path('browse', __spjpengeluaranskpd.pelimpahan.browse, name='spjskpd_pengeluaran_pelimpahan_browse'),
			path('browse/benda_keluar', __spjpengeluaranskpd.pelimpahan.browse_bendaKeluar, name='spjskpd_benda_keluar_browse'),
			path('save/pelimpahan', __spjpengeluaranskpd.pelimpahan.save_pelimpahan, name='spjskpd_spjpengeluaranskpd_limpahan_save'),
		])),
	])),

	# path('tahun_min_1/<str:jenis>/', include([
	# 	path('', tahun_min_1.index, name='spjskpd-tahun_min_1-index'),
	# 	path('save', tahun_min_1.save, name='spjskpd-tahun_min_1-save'),
	# 	path('load', tahun_min_1.load, name='spjskpd-tahun_min_1-load'),
	# ])),

	# 20190705113958. TIDAK JADI. (~/views/spjskpd/storedprocedures/04.sql)
	# path('akrual/', include([
	# 	path('', akrual.index, name='spjskpd-akrual-index'),
	# 	path('data', akrual.data, name='spjskpd-akrual-data'),
	# 	path('save', akrual.save, name='spjskpd-akrual-save'),
	# ])),
]
