from django.urls import path, include, re_path
from .views import *

urlpatterns = [
	path('main/', include([
		path('autonobukas/', main.autonobukas, name='kasda_autonobukas'),
		path('mdl_afektasi/<str:jenis>/', main.mdl_afektasi, name='kasda_mdl_afektasi'),
		path('cek_nobukti/', main.cek_nobukti, name='kasda_cek_nobukti'),
		path('tbl_afektasi/', main.tbl_afektasi, name='kasda_tbl_afektasi'),
		path('list_kasda/<str:jenis>/', main.list_kasda, name='kasda_list_transaksi'),
		path('load_data/', main.load_data, name='kasda_load_data'),

		# ADD JOEL ======
		path('list_kasda_srvside/<str:jenis>/', main.list_kasda_srvside, name='list_kasda_srvside'),
		path('mdl_afektasi_srvside/<str:jenis>/<str:jenis1>/', main.mdl_afektasi_srvside, name='kasda_mdl_afektasi_srvside'),
	])),
	path('pencairansp2d/', include([
		path('', kasda_sp2d.index, name='pencairansp2d_index'),
		path('list_transaksi_sp2d', kasda_sp2d.list_transaksi_sp2dViews, name='list_transaksi_sp2d'),
		path('list_kasda_sp2d', kasda_sp2d.list_kasda_sp2dViews, name='list_kasda_sp2d'),
		path('afektasi_sp2d', kasda_sp2d.render_afektasi_sp2dViews, name='render_afektasi_sp2d'),
		path('simpan_kasda_sp2d', kasda_sp2d.simpan_kasda_sp2dViews, name='simpan_kasda_sp2d'),
		path('edit_kasda_sp2d', kasda_sp2d.edit_kasda_sp2dViews, name='edit_kasda_sp2d'),
		path('del_transact', kasda_sp2d.del_transactViews, name='del_transact'),

		# ADD JOEL 07 Jan 22
		path('list_transaksi_sp2d_srvside', kasda_sp2d.list_transaksi_sp2d_srvsideViews, name='list_transaksi_sp2d_srvside'),
		path('list_kasda_sp2d_srvside', kasda_sp2d.list_kasda_sp2d_srvsideViews, name='list_kasda_sp2d_srvside'),
	])),
	path('setorsts/', include([
		path('', kasda_sts.index, name='setorsts_index'),
		path('simpan/<str:jenis>/', kasda_sts.simpan, name='kasda_sts_save'),
	])),
	path('nota/', include([
		path('', kasda_nota.index, name='nota_index'),
		path('simpan/<str:jenis>/', kasda_nota.simpan, name='kasda_nota_save'),
	])),
	path('saldoawal/', include([
		path('', kasda_saldo.index, name='saldo_index'),
		path('simpan/<str:jenis>/', kasda_saldo.simpan, name='kasda_simpan_saldo'),
	])),
	path('tahunberjalan/', include([
		path('', kasda_tahunberjalan.index, name='tahunberjalan_index'),
		path('simpan/<str:jenis>/', kasda_tahunberjalan.simpan, name='kasda_tahunberjalan_save'),
	])),
	path('tahunkemarin/', include([
		path('', kasda_tahunkemarin.index, name='tahunkemarin_index'),
		path('simpan/<str:jenis>/', kasda_tahunkemarin.simpan, name='kasda_contrakemarin_save'),
	])),
	path('pindahbuku/', include([
		path('', kasda_pindahbuku.index, name='pindahbuku_index'),
		path('simpan/<str:jenis>/', kasda_pindahbuku.simpan, name='kasda_pindahbuku_save'),
		path('load_data/', kasda_pindahbuku.load_data, name='kasda_pindahbuku_load_data'),
	])),

	path('lap_bend_umum/', include([
		path('', kasda_lap_bend_umum.index, name='lap_bend_umum_index'),
	])),
	path('lap_bukubesar/', include([
		path('', kasda_lap_bukubesar.index, name='lap_bukubesar_index'),
	])),
	path('lap_bukubesarsp2d/', include([
		path('', kasda_lap_bukubesarsp2d.index, name='lap_bukubesarsp2d_index'),
	])),
]