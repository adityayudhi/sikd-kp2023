from django.urls import path, include, re_path
from django.urls import path, include
from django.conf.urls import url

from . import views
# from . import report

app_name = 'sipkd'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('login/proseslogin', views.proseslogin, name='proseslogin'),
    # PUBLIC
    path('public/list_organisasi', views.list_organisasi, name='list_organisasi'),
    path('public/list_kegiatan', views.list_kegiatan, name='list_kegiatan'),
    path('public/load_modal/', views.load_modal, name='load_modal'),
    path('public/ambil_bendahara/', views.ambil_bendahara, name='ambil_bendahara'),
    path('konfig/settingorganisasi/mdl_keg', views.mdl_kegiatan, name='mdl_kegiatan'), #ADD JOEL 28 JAN 2019
    path('public/link_is_skpkd/', views.is_skpkd, name='link_is_skpkd'),
    path('public/modal_search_rekening/', views.modal_search_rekening, name='modal_search_rekening'),
    
    # Tambahan Yudhi
    path('loadtree/<str:jenis>/<str:jenis2>/<str:jenis3>/', views.loadtree, name='loadtree'),
    path('modal_organisasi/<int:jenis>/<str:jenis2>/', views.modal_organisasi, name='modal_organisasi'),
    path('loadmodal_rekening/<str:jenis>/', views.loadmodal_rekening, name='loadmodal_rekening'),
    path('cekrekening/<str:jenis>/<str:jenis2>/', views.cekrekening, name='cekrekening'),
    path('loadtabel_upload/<str:jenis>/', views.loadtabel_upload, name='loadtabel_upload'),
    path('modalupload/<str:jenis>/', views.modalupload, name='modalupload'),    
    path('render_prog_keg/', views.render_prog_keg, name='render_prog_keg'),
    path('upload_praskpd/', views.upload_praskpd, name='upload_praskpd'),
    path('upload_prappkd/', views.upload_prappkd, name='upload_prappkd'),
    path('read_file_fa/', views.read_file_fa, name='read_file_fa'),
    path('coba/', views.coba, name='coba'),
    path('modal_shb', views.modal_shb, name='modal_shb'),
    path('pejabat_pengguna/', views.pejabat_pengguna, name='pejabat_pengguna'),
    path('get_pagu_sumberdana', views.get_pagu_sumberdana, name='get_pagu_sumberdana'),   
    
    # Akhir Tambahan 
    path('konfig/settingpengguna/', views.settingpengguna, name='settingpengguna'),
    path('konfig/isimodal/', views.isimodal, name='isimodal'),
    path('konfig/get_organisasi/', views.get_organisasi, name='get_organisasi'),
    path('konfig/cek_data_user/', views.cek_data_user, name='cek_data_user'),
    path('konfig/cek_data_user/', views.cek_data_user, name='cek_data_user'),
    path('konfig/save_user/', views.save_user, name='save_user'),
    path('konfig/hapus_user/', views.hapus_user, name='hapus_user'),
    path('konfig/settingorganisasi/modal', views.mdl_organisasi, name='mdl_organisasi'),
    path('konfig/settingorganisasi/mdl_keg', views.mdl_kegiatan, name='mdl_kegiatan'), #ADD JOEL 28 JAN 2019    
    path('konfig/ubahpwd/', views.ubahpwd, name='ubahpwd'),
    path('konfig/ubahpassword/', views.ubahpassword, name='ubahpassword'),
    path('konfig/save_ubahpwd/', views.save_ubahpwd, name='save_ubahpwd'),
 
    path('konfig/masterjabatan/', views.masterjabatan, name='masterjabatan'),
    path('konfig/jabatanmodal/', views.jabatanmodal, name='jabatanmodal'),
    path('konfig/updatejabatan/', views.updatejabatan, name='updatejabatan'),
    path('konfig/get_listJabatan/', views.get_listJabatan, name='get_listJabatan'),
    path('konfig/save_jabatan/', views.save_jabatan, name='save_jabatan'),
    path('konfig/hapus_jabatan/', views.hapus_jabatan, name='hapus_jabatan'),
    path('konfig/terbilang/', views.get_terbilang, name='get_terbilang'),
    
    path('konfig/pejabatskpd/', views.pejabatskpd, name='pejabatskpd'),
    path('konfig/pejabatskpd/list', views.getpejabatskpd, name='getpejabatskpd'),
    path('konfig/pejabatskpd/combo', views.combopejabatskpd, name='combopejabatskpd'),
    path('konfig/pejabatskpd/aksi', views.savepejabatskpd, name='savepejabatskpd'),
    path('konfig/pejabatskpd/add', views.addpejabatskpd, name='addpejabatskpd'),
    path('konfig/pejabatskpd/delete', views.deletepejabatskpd, name='deletepejabatskpd'),
    path('konfig/pejabatskpd/load_bank_pejabat', views.load_bank_pejabat, name='load_bank_pejabat'),
    path('konfig/pejabatskpd/pejabat_modal', views.pejabat_modal, name="pejabat_modal"),

    path('konfig/pejabatskpkd/', views.pejabatskpkd, name='pejabatskpkd'),
    path('konfig/pejabatskpkd/add', views.addpejabatskpkd, name='addpejabatskpkd'),    
    path('konfig/pejabatskpkd/aksi', views.saveskpkd, name='saveskpkd'),    
    path('konfig/pejabatskpkd/combo', views.combopejabatskpkd, name='combopejabatskpkd'),
    path('konfig/pejabatskpkd/delete', views.deletepejabatskpkd, name='deletepejabatskpkd'),

    path('konfig/dasarhukum/', views.dasarhukum, name='dasarhukum'),
    path('konfig/dasarhukum/list', views.getdasarhukum, name='getdasarhukum'),
    path('konfig/dasarhukum/calendar', views.tgldasarhukum, name='tgldasarhukum'),
    path('konfig/dasarhukum/simpan', views.savedasarhukum, name='savedasarhukum'),
    path('konfig/dasarhukum/add', views.adddasarhukum, name='adddasarhukum'),
    path('konfig/dasarhukum/delete', views.deletedasarhukum, name='deletedasarhukum'),

    path('konfig/sumberdana/', views.sumberdana, name='sumberdana'),
    path('konfig/sumberdanamodal/', views.sumberdanamodal, name='sumberdanamodal'),
    path('konfig/sumberdanaskpd/load_bank_sumberdana', views.load_bank_sumberdana, name='load_bank_sumberdana'),
    path('konfig/savesumberdana/', views.savesumberdana, name='savesumberdana'),
    path('konfig/sumberdanaskpd/', views.sumberdanaskpd, name='sumberdanaskpd'),
    path('konfig/sumberdanaskpd/ceksumber', views.cek_rekening, name='cek_rekening'),
    path('konfig/sumberdanaskpd/add', views.addsumberdanaskpd, name='addsumberdanaskpd'),
    path('konfig/sumberdanaskpd/combo', views.combosumberdanaskpd, name='combosumberdanaskpd'),
    path('konfig/sumberdanaskpd/simpan', views.savesumberdanaskpd, name='savesumberdanaskpd'),
    path('konfig/sumberdanaskpd/delete', views.deletesumberdanaskpd, name='deletesumberdanaskpd'),

    path('konfig/settingtagihan/', views.settingtagihan, name='settingtagihan'),
    path('konfig/settingtagihan/simpan', views.savesettingtagihan, name='savesettingtagihan'),

    path('konfig/settingbendahara/', views.settingbendahara, name='settingbendahara'),
    path('konfig/settingbendahara/modal', views.modal_bendahara, name='modal_bendahara'),
    path('konfig/settingbendahara/list_bendahara', views.getbendahara, name='getbendahara'),
    path('konfig/settingbendahara/delete', views.hapus_bendahara, name='hapus_bendahara'),
    path('konfig/settingbendahara/save', views.simpan_bendahara, name='simpan_bendahara'),
    path('konfig/settingbendahara/cek_bendahara', views.cek_bendahara, name='cek_bendahara'),


    path('konfig/settingperubahan/', views.settingperubahan, name='settingperubahan'),
    path('konfig/settingperubahan/aksi', views.editperubahan, name='editperubahan'),
    path('konfig/settingquery/', views.settingquery, name='settingquery'),



    # JOEL ADD ==============================================================
    path('konfig/settinghakakses/', views.setting_hakakses, name='setting_hakakses'),
    path('konfig/settinghakakses/tabel', views.tabel_setting_hakakses, name='tabel_setting_hakakses'),
    path('konfig/settingmenu/', views.setting_menu, name='setting_menu'),
    path('konfig/settingmenu/tabel', views.tabel_setting_menu, name='tabel_setting_menu'),
    path('konfig/settingmenu/modal', views.modal_setting_menu, name='modal_setting_menu'),
    path('konfig/settingmenu/aweso', views.aweso_setting_menu, name='aweso_setting_menu'),

    # ADD ---- joel 2021---- rekening pencairan loadmodal_rekpen
    path('konfig/rekpencairan/', views.rekening_pencairan, name='rekening_pencairan'),
    path('konfig/kontrak/load_bank_pencairan', views.load_bank_pencairan, name='load_bank_pencairan'),
    path('konfig/kontrak/pencairan', views.combopencairanskpd, name='combopencairanskpd'),
    path('konfig/rekpen_mdl/', views.loadmodal_rekpen, name='loadmodal_rekpen'),
    path('konfig/rekpen_save/', views.simpan_rekpen, name='simpan_rekpen'),
    path('konfig/rekpen_delt/', views.hapus_rekpen, name='hapus_rekpen'),

    # ADD ---- joel 28 Des 2021 ---- autosugestion bendahara dan pihak ketiga
    path('konfig/autosugestion/', views.autosugestion_bndhr, name='autosugestion_bndhr'),

    # # ADD ======= JOEL 2021 ======= UPLOD GAJI
    path('konfig/uplod_sp2dgaji/', views.uplod_sp2dgaji, name='uplod_sp2dgaji'),
    path('konfig/uplod_sp2dgaji/tabel', views.uplod_sp2dgaji_list, name='uplod_sp2dgaji_list'),
    path('konfig/uplod_sp2dgaji/temp', views.uplod_sp2dgaji_temp, name='uplod_sp2dgaji_temp'),
    path('konfig/uplod_sp2dgaji/dump', views.uplod_sp2dgaji_dump, name='uplod_sp2dgaji_dump'),
    path('konfig/uplod_sp2dgaji/delt', views.uplod_sp2dgaji_hapus, name='uplod_sp2dgaji_hapus'),

    # # ADD ======= JOEL 1 Mar 2022 =========== Ambil EXCEL dari aplikasi SIPD
    path('konfig/uplod_excelsipd/', views.uplod_excelsipd, name='uplod_excelsipd'),
    path('konfig/uplod_excelsipd/tabel', views.uplod_excelsipd_list, name='uplod_excelsipd_list'),
    path('konfig/uplod_excelsipd/temp', views.uplod_excelsipd_temp, name='uplod_excelsipd_temp'),
    path('konfig/uplod_excelsipd/dump', views.uplod_excelsipd_dump, name='uplod_excelsipd_dump'),
    path('konfig/uplod_excelsipd/delt', views.uplod_excelsipd_hapus, name='uplod_excelsipd_hapus'),

# MODUL SPD
	path('spd/',views.spd, name='spd'),
    path('spd/pengisianskup/', views.pengisianskup, name='pengisianskup'),
    path('spd/spdbtl/', views.spdbtl, name='spdbtl'),
    path('spd/spdbl/', views.spdbl, name='spdbl'),
    path('spd/pengeluaranpembiayaan/', views.pengeluaranpembiayaan, name='pengeluaranpembiayaan'),
    path('spd/persetujuanspd/', views.persetujuanspd, name='persetujuanspd'),
    path('spd/lockanggaran/', views.lockanggaran, name='lockanggaran'),
    path('spd/kontrolanggaran/', views.kontrolanggaran, name='kontrolanggaran'),
    path('spd/kontrolspd/', views.kontrolspd, name='kontrolspd'),
    path('spd/laporanspd/', views.laporanspd, name='laporanspd'),
# FUNGSI CRUD SPD
    path('spd/rinci_spd/', views.rinci_spd, name='rinci_spd'),
    path('spd/link_tabel_rinci_spd/', views.link_tabel_rinci_spd, name='link_tabel_rinci_spd'),
    # path('spd/modal_rinci_spd/', views.modal_rinci_spd, name='modal_rinci_spd'),
    path('spd/link_simpan_spd/', views.simpan_spd, name='link_simpan_spd'),
    path('spd/link_hapus_spd/', views.hapus_spd, name='link_hapus_spd'),
    path('spd/link_render_cetak_spd/', views.render_cetak_spd, name='link_render_cetak_spd'),
    path('spd/link_cetak_spd/', views.cetak_spd, name='link_cetak_spd'),

    path('spd/pengisianskup/link_data_skup/', views.data_skup, name='link_data_skup'),
    path('spd/pengisianskup/link_modal_tambah_skup/', views.modal_tambah_skup, name='link_modal_tambah_skup'),
    path('spd/pengisianskup/link_modal_edit_skup/', views.modal_edit_skup, name='link_modal_edit_skup'),
    path('spd/pengisianskup/save_skup/', views.aksi_simpan_skup, name='save_skup'),

    path('spd/persetujuanspd/link_load_draft_persetujuan_spd/', views.load_draft_spd, name='link_load_draft_persetujuan_spd'),
    path('spd/persetujuanspd/link_setuju_draft/', views.setuju_draft_spd, name="link_setuju_draft"),

	path('spd/kontrolspd/link_ambil_spd_kontrol/', views.ambil_spd_kontrol, name="link_ambil_spd_kontrol"),
    path('spd/kontrolspd/ambilSPDUser/', views.ambilSPDUser, name="ambilSPDUser"),
	path('spd/lockanggaran/link_ambil_skpkd/', views.ambil_skpkd, name="ambil_skpkd"),
    path('spd/lockanggaran/link_insert_lock/', views.insert_lock, name="link_insert_lock"),

    path('spd/kontrolanggaran/link_load_kontrol_anggaran/', views.load_kontrolanggaran, name="load_kontrolanggaran"),
    path('spd/kontrolanggaran/link_laporan_kpra/', views.laporan_kpra, name="link_laporan_kpra"),

    path('spd/anggarankas/', views.anggarankas, name="anggarankas"),
    path('spd/anggarankas/tabsanggarankas', views.tabsanggarankas, name="tabsanggarankas"),
    path('spd/anggarankas/aksianggarankas', views.aksianggarankas, name="aksianggarankas"),
    path('spd/anggarankas/aksipersetujuanrka', views.aksipersetujuanrka, name="aksipersetujuanrka"),

    # # # SPD DENGAN RINCIAAAN =======================================
    path('spd/spd_kep/',views.spd_kep, name='spd_kep'),
    path('spd/spd_kep/rinci_spd_kep/', views.rinci_spd_kep, name='rinci_spd_kep'),
    path('spd/spd_kep/link_tabel_rinci_spd_kep/', views.link_tabel_rinci_spd_kep, name='link_tabel_rinci_spd_kep'),
    path('spd/spd_kep/modal_rinci_spd_kep/', views.modal_rinci_spd_kep, name='modal_rinci_spd_kep'),
    path('spd/spd_kep/link_simpan_spd_kep/', views.simpan_spd_kep, name='link_simpan_spd_kep'),
    path('spd/spd_kep/link_hapus_spd_kep/', views.hapus_spd_kep, name='link_hapus_spd_kep'),
    path('spd/spd_kep/link_render_cetak_spd_kep/', views.render_cetak_spd_kep, name='link_render_cetak_spd_kep'),
    path('spd/spd_kep/link_cetak_spd_kep/', views.cetak_spd_kep, name='link_cetak_spd_kep'),
    
    # # # SPD BULANAN =======================================
    path('spd/spd_bul/',views.spd_bul, name='spd_bul'),
    path('spd/spd_bul/rinci_spd_bul/', views.rinci_spd_bul, name='rinci_spd_bul'),
    path('spd/spd_bul/link_tabel_rinci_spd_bul/', views.link_tabel_rinci_spd_bul, name='link_tabel_rinci_spd_bul'),
    # path('spd/spd_bul/modal_rinci_spd_bul/', views.modal_rinci_spd_bul, name='modal_rinci_spd_bul'),
    path('spd/spd_bul/link_simpan_spd_bul/', views.simpan_spd_bul, name='link_simpan_spd_bul'),
    path('spd/spd_bul/link_hapus_spd_bul/', views.hapus_spd_bul, name='link_hapus_spd_bul'),
    path('spd/spd_bul/link_render_cetak_spd_bul/', views.render_cetak_spd_bul, name='link_render_cetak_spd_bul'),
    path('spd/spd_bul/link_cetak_spd_bul/', views.cetak_spd_bul, name='link_cetak_spd_bul'),

    # autonospd
    path('spd/spd_kep/autonospd_kep/', views.autonospd_kep, name='autonospd_kep'),
    path('spd/cetakdpa', views.cetakdpa, name='cetakdpa'),
    path('spd/load_data_cetak_dpa', views.load_data_cetak_dpa, name='load_data_cetak_dpa'),

	# END FUNGSI CRUD SPD
# END MODUL SPD
# MODUL SPP ==============================================================
    path('spp/<str:jenis>/', views.sppup, name='sppup'),
    path('konfig/up/load_bank_up', views.load_bank_up, name='load_bank_up'),
    path('spp/up/detail', views.getsppupskpd, name='getsppupskpd'),
    path('spp/up/cek_up', views.ceksppup, name='ceksppup'),
    path('spp/up/cekskup', views.cekskup, name='cekskup'),
    path('spp/up/simpan', views.savesppup, name='savesppup'),
    path('spp/up/delete', views.deletesppup, name='deletesppup'),
    path('spp/loadspp/<str:jenis>', views.loadspp, name='loadspp'),
    path('spp/up/loadbendahara', views.loadbendahara, name='loadbendahara'),
    path('spp/list/<str:jenis>', views.listafektasi, name='listafektasi'),
    # path('spp/persetujuanskpd', views.persetujuanskpd, name='persetujuanskpd'),
    path('spp/persetujuanskpd/aksi', views.setuju_draft, name='setuju_draft'),
    path('spp/persetujuanskpd/list', views.listpersetujuan, name='listpersetujuan'),
    path('spp/loadppkd/<str:jenis>', views.loadppkd, name='loadppkd'),
    path('spp/ambilspp/<str:jenis>',views.ambilspp,name='ambilspp'),
    path('spp/ambilspd',views.ambilspd,name='ambilspd'),
    path('spp/loadlaporanspp/<str:jenis>',views.loadlaporanspp,name='loadlaporanspp'),
    path('spp/cetaklaporanspp/<str:jenis>',views.cetaklaporanspp,name='cetaklaporanspp'),
    path('spp/listspj/<str:jenis>', views.listdataspj, name='listdataspj'),
    path('spp/ceknomerspp', views.ceknomerspp, name='ceknomerspp'),
    path('spp/simpanspp/<str:jenis>', views.simpanspp, name='simpanspp'),
    path('spp/laporanspp/<str:jenis>', views.laporanspp, name='laporanspp'),
    path('spp/cetakregisterspp',views.cetakregisterspp, name='cetakregisterspp'),
    path('spp/loadlpjspp/<str:jenis>',views.loadlpjspp, name='loadlpjspp'),
    path('spp/listlpjspp/<str:jenis>', views.listlpjspp, name='listlpjspp'),
    path('spp/ambilkegiatan', views.ambilkegiatan, name='ambilkegiatan'),
    path('spp/loadkegiatan', views.loadkegiatan, name='loadkegiatan'),
    path('spp/getnewnospj/<str:jenis>', views.getnewnospj, name='getnewnospj'),
    path('spp/listkegiatanlpj', views.listkegiatanlpj, name='listkegiatanlpj'),
    path('spp/addkegiatanlpj', views.addkegiatanlpj, name='addkegiatanlpj'),
    path('spp/simpankegiatanlpj', views.simpankegiatanlpj, name='simpankegiatanlpj'),
    path('spp/listrekeninglpj', views.listrekeninglpj, name='listrekeninglpj'),
    path('spp/deletelpj', views.deletelpj, name='deletelpj'),
    path('spp/listlpjupgu/<str:jenis>', views.listlpjupgu, name='listlpjupgu'),
    path('spp/cek_no_spd', views.cek_no_spd, name='cek_no_spd'),
    path('spp/simpanlpjrincian/<str:jenis>', views.simpanlpjrincian, name='simpanlpjrincian'),
    path('spp/deleterincianlpj',views.deleterincianlpj, name='deleterincianlpj'),
    path('spp/deletekegiatanlpj',views.deletekegiatanlpj, name='deletekegiatanlpj'),
    path('spp/getkegiatan',views.getkegiatan, name='getkegiatan'),
    path('spp/getbelanja',views.getbelanja, name='getbelanja'),
    path('spp/getdatalpjtu',views.getdatalpjtu, name='getdatalpjtu'),
    path('spp/listrekeninglpjtu',views.listrekeninglpjtu, name='listrekeninglpjtu'),
    path('spp/updatelpjtu',views.updatelpjtu, name='updatelpjtu'),
    path('spp/loadlaporanlpj/<str:jenis>',views.loadlaporanlpj, name='loadlaporanlpj'),
    path('spp/cetaklaporanlpj/<str:jenis>',views.cetaklaporanlpj,name='cetaklaporanlpj'),
    path('spp/getdatapengembalian',views.getdatapengembalian,name='getdatapengembalian'),
    path('spp/getlistrinciansts',views.getlistrinciansts,name='getlistrinciansts'),
    path('spp/getlistrincianstsls',views.getlistrincianstsls,name='getlistrincianstsls'),
    path('spp/simpanpengembaliansts',views.simpanpengembaliansts,name='simpanpengembaliansts'),
    path('spp/getnolpj',views.getnolpj,name='getnolpj'),
    path('spp/loadlpjsts',views.loadlpjsts,name='loadlpjsts'),
    path('spp/sumspptu',views.sumspptu,name='sumspptu'),
    path('spp/hitungsisatu',views.hitungsisatu,name='hitungsisatu'),
    path('spp/loadmodalsp2d',views.loadmodalsp2d,name='loadmodalsp2d'),
    path('spp/loadpihakketiga',views.loadpihakketiga,name='loadpihakketiga'),
    path('spp/cektanggaldpa',views.cektanggaldpa,name='cektanggaldpa'),
    path('spp/getkwitansi',views.getkwitansi,name='getkwitansi'),
    path('spp/lpjupgutu_mdl_cut',views.lpjupgutu_mdl_cut,name='lpjupgutu_mdl_cut'), 
    path('spp/lpjupgutu_modal_potongan',views.lpjupgutu_modal_potongan,name='lpjupgutu_modal_potongan'), 
    path('spp/lpjupgu/kuwitansi',views.lpgupgutu_kuwitansi,name='lpgupgutu_kuwitansi'), 
    
    # SPP GU
    path('konfig/gu/load_bank_gu', views.load_bank_gu, name='load_bank_gu'),

    # SPP TU MULTI
    path('spp/get_multi_kegiatan', views.get_multi_kegiatan, name='get_multi_kegiatan'),
    path('spp/tu/load_bank_tu', views.load_bank_tu, name='load_bank_tu'),
    path('spp/tu/load_bank_tunihil', views.load_bank_tunihil, name='load_bank_tunihil'), 

    
    # KONTRAK DAN BAST 
    path('kontrak/',views.kontrak,name='kontrak'),
    path('konfig/kontrak/load_bank_kontrak', views.load_bank_kontrak, name='load_bank_kontrak'),
    path('konfig/kontrak/combo', views.combokontrakskpd, name='combokontrakskpd'),
    path('konfig/kontrak/load_bank_bast', views.load_bank_bast, name='load_bank_bast'),
    path('konfig/kontrak/combobast', views.combobastskpd, name='combobastskpd'),
    path('kontrak/tabel_kontrak', views.tabel_kontrak, name="tabel_kontrak"),
    path('kontrak/listafektasi_kontrak', views.listafektasi_kontrak, name="listafektasi_kontrak"),
    path('kontrak/modal/', views.kontrak_modal, name="kontrak_modal"),
    path('kontrak/modal_edit/', views.modal_kontrak_edit, name="modal_kontrak_edit"),
    path('kontrak/loadkegiatan', views.loadkegiatan_kontrak, name='loadkegiatan_kontrak'),
    path('kontrak/load_sumberdana', views.load_sumberdana_kontrak, name='load_sumberdana_kontrak'),
    path('kontrak/load_rekening_pendapatan', views.load_rekening_pendapatan, name='load_rekening_pendapatan'),
    path('kontrak/load_kontrak', views.load_kontrak, name='load_kontrak'),
    path('kontrak/simpan/<str:jenis>', views.simpan_kontrak, name="simpan_kontrak"),
    path('bast/',views.bast,name='bast'),
    path('bast/simpan/<str:jenis>', views.simpan_bast, name="simpan_bast"),
    path('bast/modal',views.bast_modal,name='bast_modal'),
    path('bast/tabel_bast', views.tabel_bast, name="tabel_bast"),
    path('bast/modal_edit/', views.modal_bast_edit, name="modal_bast_edit"),

    ### PERMOHONAN SPP === JOEL 17 OCT 22 ==============
    path('spp/permohonan/tu',views.mohon_spptu,name='mohon_spptu'),
    path('spp/permohonan/tu/save',views.mohon_spptu_simpan,name='mohon_spptu_simpan'),
    path('spp/permohonan/tu/load/<str:jenis>',views.mohon_spptu_load,name='mohon_spptu_load'),
    path('spp/permohonan/tu/delete',views.mohon_spptu_delete,name='mohon_spptu_delete'),
    path('spp/permohonan/tu/validasi',views.mohon_spptu_setujui,name='mohon_spptu_setujui'),
    path('spp/permohonan/tu/validasi/list',views.mohon_spptu_setujui_list,name='mohon_spptu_setujui_list'),
    path('spp/permohonan/tu/validasi/<str:jenis>',views.mohon_spptu_setujui_action,name='mohon_spptu_setujui_action'),

    ### SP3B === JOEL 7 NOV 22 ==============
    path('spp/sp3b/id',views.sp3b_index,name='sp3b_index'),
    path('spp/sp3b/kg',views.sp3b_kegiatan,name='sp3b_kegiatan'),
    path('spp/sp3b/pd',views.sp3b_pendapatan,name='sp3b_pendapatan'),
    path('spp/sp3b/bd',views.sp3b_bendahara,name='sp3b_bendahara'),
    path('spp/sp3b/af',views.sp3b_afektasi,name='sp3b_afektasi'),
    path('spp/sp3b/pt',views.sp3b_potongan,name='sp3b_potongan'),
    path('spp/sp3b/cn',views.sp3b_ceknomor,name='sp3b_ceknomor'), 
    path('spp/sp3b/sp',views.sp3b_simpan,name='sp3b_simpan'),
    path('spp/sp3b/ld',views.sp3b_load,name='sp3b_load'),
    path('spp/sp3b/dl',views.sp3b_delete,name='sp3b_delete'),
    path('spp/sp3b/rp',views.sp3b_report,name='sp3b_report'),
    
#END MODUL SPP    

# MODUL SPM ==============================================================
    path('spm/<str:jenis_spm>/', views.spm, name='spm'),
    path('spm/<str:jenis_spm>/simpan_lsppkd/', views.spm_save, name='spm_save'),
    path('spm/<str:jenis_spm>/load_bank_up/', views.load_bank_up, name='load_bank_up'),
    path('spm/<str:jenis_spm>/simpan_up/', views.spm_save_up, name='spm_save_up'),
    path('spm/<str:jenis_spm>/load_bank_gu/', views.load_bank_gu, name='load_bank_gu'),
    path('spm/<str:jenis_spm>/simpan_gu/', views.spm_save_gu, name='spm_save_gu'),
    path('spm/<str:jenis_spm>/load_bank_tu/', views.load_bank_tu, name='load_bank_tu'),
    path('spm/<str:jenis_spm>/simpan_tu/', views.spm_save_tu, name='spm_save_tu'),
    path('spm/<str:jenis_spm>/simpan_gj/', views.spm_save_gj, name='spm_save_gj'),
    path('spm/<str:jenis_spm>/load_bank_ls/', views.load_bank_ls, name='load_bank_ls'),
    path('spm/<str:jenis_spm>/simpan_ls/', views.spm_save_ls, name='spm_save_ls'),
    path('spm/<str:jenis_spm>/simpan_gu_nihil/', views.spm_save_gu_nihil, name='spm_save_gu_nihil'),
    path('spm/<str:jenis_spm>/simpan_non_angg/', views.spm_save_non_angg, name='spm_save_non_angg'),
    path('spm/<str:jenis_spm>/simpan_tu_nihil/', views.spm_save_tu_nihil, name='spm_save_tu_nihil'),
    path('spm/<str:jenis_spm>/delete_spm/', views.spm_delete, name='spm_delete'),
    path('spm/<str:jenis_spm>/cek_spm/', views.cek_spm, name='cek_spm'),
    path('spm/<str:jenis_spm>/cek_pejabat/', views.cek_pejabat, name='cek_pejabat'),
    path('spm/<str:jenis_spm>/render_pengguna_anggaran/', views.render_pengguna_anggaran, name='render_pengguna_anggaran'),
    path('spm/<str:jenis_spm>/load_modal_spm/', views.load_modal_spm, name='load_modal_spm'),
    path('spm/cetaklaporanspm/<str:jenis_spm>',views.cetaklaporanspm,name='cetaklaporanspm'),
    path('spm/cetakspm',views.cetakspm,name='cetakspm'),
    path('spm/tabel/<str:jenis_spm>/', views.tbl_afektasi_spm, name='tbl_afektasi_spm'),
    path('spm/generate_rinci_spm/<str:jenis_spm>/', views.generate_rinci_spm, name='generate_rinci_spm'),
    path('spm/generate_rinci_spp/<str:jenis_spm>/', views.generate_rinci_spp, name='generate_rinci_spp'),
    path('spm/generate_tbl_spm/<str:jenis_spm>/', views.generate_tbl_spm, name='generate_tbl_spm'),
    path('spm/generate_afektasi_spm/<str:jenis_spm>/', views.generate_afektasi_spm, name='generate_afektasi_spm'),
    path('spm/generate_tbl_dasar_spd/<str:jenis_spm>/', views.generate_tbl_dasar_spd, name='generate_tbl_dasar_spd'),
    path('spm/generate_tbl_dasar_spd_to_spp/<str:jenis_spm>/', views.generate_tbl_dasar_spd_to_spp, name='generate_tbl_dasar_spd_to_spp'),
    path('spm/generate_rekening/<str:jenis_spm>/', views.generate_rekening, name='generate_rekening'),
    path('spm/persetujuanskpd/list', views.listpersetujuan_spm, name='listpersetujuan_spm'),
    path('spm/persetujuanskpd/aksi', views.setuju_draft_spm, name='setuju_draft_spm'),
# MODUL SPM ==============================================================

# SP2D JOEL ===========================================================================================
    path('sp2d/ppkdbtl/', views.sp2d_ppkdbtl, name='sp2d_ppkdbtl'),
    path('sp2d/ppkdbtl/sumberdana', views.sp2d_ppkdbtl_sumberdana, name='sp2d_ppkdbtl_sumberdana'),
    path('sp2d/ppkdbtl/rekening', views.sp2d_ppkdbtl_rekening, name='sp2d_ppkdbtl_rekening'),
    path('sp2d/ppkdbtl/tabel', views.sp2d_ppkdbtl_tabel, name='sp2d_ppkdbtl_tabel'),
    path('sp2d/ppkdbtl/spm', views.sp2d_ppkdbtl_ambil_spm, name='sp2d_ppkdbtl_ambil_spm'),
    path('sp2d/ppkdbtl/sp2d', views.sp2d_ppkdbtl_ambil_sp2d, name='sp2d_ppkdbtl_ambil_sp2d'),
    path('sp2d/ppkdbtl/lap_frm', views.sp2d_ppkdbtl_frm_lap, name='sp2d_ppkdbtl_frm_lap'),
    path('sp2d/ppkdbtl/cek_nosp2d', views.cek_nosp2d, name='cek_nosp2d'),
    path('sp2d/ppkdbtl/one/<str:jenis>', views.sp2d_ppkdbtl_simpan, name='sp2d_ppkdbtl_simpan'),

    path('sp2d/barjas/', views.sp2d_barjas, name='sp2d_barjas'),
    path('sp2d/barjas/sumberdana', views.sp2d_barjas_sumberdana, name='sp2d_barjas_sumberdana'),
    path('sp2d/barjas/rekening', views.sp2d_barjas_rekening, name='sp2d_barjas_rekening'),
    path('sp2d/barjas/tabel', views.sp2d_barjas_tabel, name='sp2d_barjas_tabel'),
    path('sp2d/barjas/spm', views.sp2d_barjas_ambil_spm, name='sp2d_barjas_ambil_spm'),
    path('sp2d/barjas/spm_src_sp2d', views.sp2d_barjas_cari_spm_sp2d, name='sp2d_barjas_cari_spm_sp2d'),
    path('sp2d/barjas/cut', views.sp2d_barjas_potongan, name='sp2d_barjas_potongan'),
    path('sp2d/barjas/mdl_cut', views.sp2d_barjas_mdl_cut, name='sp2d_barjas_mdl_cut'),
    path('sp2d/barjas/sp2d', views.sp2d_barjas_ambil_sp2d, name='sp2d_barjas_ambil_sp2d'),
    path('sp2d/barjas/lap_frm', views.sp2d_barjas_frm_lap, name='sp2d_barjas_frm_lap'),
    path('sp2d/barjas/one/<str:jenis>', views.sp2d_barjas_simpan, name='sp2d_barjas_simpan'),

    path('sp2d/gaji/', views.sp2d_gaji, name='sp2d_gaji'),
    path('sp2d/gaji/sumberdana', views.sp2d_gaji_sumberdana, name='sp2d_gaji_sumberdana'),
    path('sp2d/gaji/rekening', views.sp2d_gaji_rekening, name='sp2d_gaji_rekening'),
    path('sp2d/gaji/tabel', views.sp2d_gaji_tabel, name='sp2d_gaji_tabel'),
    path('sp2d/gaji/spm', views.sp2d_gaji_ambil_spm, name='sp2d_gaji_ambil_spm'),
    path('sp2d/gaji/cut', views.sp2d_gaji_potongan, name='sp2d_gaji_potongan'),
    path('sp2d/gaji/mdl_cut', views.sp2d_gaji_mdl_cut, name='sp2d_gaji_mdl_cut'),
    path('sp2d/gaji/sp2d', views.sp2d_gaji_ambil_sp2d, name='sp2d_gaji_ambil_sp2d'),
    path('sp2d/gaji/lap_frm', views.sp2d_gaji_frm_lap, name='sp2d_gaji_frm_lap'),
    path('sp2d/gaji/one/<str:jenis>', views.sp2d_gaji_simpan, name='sp2d_gaji_simpan'),

    path('sp2d/ppkdnonangg/', views.sp2d_ppkdnonangg, name='sp2d_ppkdnonangg'),
    path('sp2d/ppkdnonangg/sumberdana', views.sp2d_nona_sumberdana, name='sp2d_nona_sumberdana'),
    path('sp2d/ppkdnonangg/rekening', views.sp2d_nona_rekening, name='sp2d_nona_rekening'),
    path('sp2d/ppkdnonangg/tabel', views.sp2d_nona_tabel, name='sp2d_nona_tabel'),
    path('sp2d/ppkdnonangg/spm', views.sp2d_nona_ambil_spm, name='sp2d_nona_ambil_spm'),
    path('sp2d/ppkdnonangg/sp2d', views.sp2d_nona_ambil_sp2d, name='sp2d_nona_ambil_sp2d'),
    path('sp2d/ppkdnonangg/lap_frm', views.sp2d_nona_frm_lap, name='sp2d_nona_frm_lap'),
    path('sp2d/ppkdnonangg/one/<str:jenis>', views.sp2d_nona_simpan, name='sp2d_nona_simpan'),

    path('sp2d/penolakansp2d/', views.sp2d_penolakan, name='sp2d_penolakan'),
    path('sp2d/penolakansp2d/input', views.sp2d_penolakan_mdl_input, name='sp2d_penolakan_mdl_input'),
    path('sp2d/penolakansp2d/cari', views.sp2d_penolakan_mdl_cari, name='sp2d_penolakan_mdl_cari'),
    path('sp2d/penolakansp2d/one/<str:jenis>', views.sp2d_penolakan_simpan, name='sp2d_penolakan_simpan'),
    path('sp2d/penolakansp2d/lap_frm', views.sp2d_penolakan_frm_lap, name='sp2d_penolakan_frm_lap'),

    path('sp2d/persetujuansp2d/', views.persetujuansp2d, name='persetujuansp2d'),
    path('sp2d/persetujuansp2d/tabel', views.sp2d_persetujuan_tabel, name='sp2d_persetujuan_tabel'),
    path('sp2d/persetujuansp2d/one/<str:jenis>', views.sp2d_persetujuan_simpan, name='sp2d_persetujuan_simpan'),

    path('sp2d/advissp2d/', views.advissp2d, name='advissp2d'),
    path('sp2d/advissp2d/one/<str:jenis>', views.sp2d_advis_simpan, name='sp2d_advis_simpan'),
    path('sp2d/advissp2d/tabel/<str:jenis>', views.sp2d_advis_tabel, name='sp2d_advis_tabel'),
    path('sp2d/advissp2d/modal/<str:jenis>', views.sp2d_advis_modal, name='sp2d_advis_modal'),
    path('sp2d/advissp2d/get_no', views.get_noAdvis, name='get_noAdvis'),

    path('sp2d/pengesahlpj/', views.sp2d_in_pengesahlpj, name='sp2d_in_pengesahlpj'),
    path('sp2d/pengesahlpj/src_bku/<str:jenis>', views.mdl_src_sp2d_for_bku, name='mdl_src_sp2d_for_bku'),
    path('sp2d/pengesahlpj/src_lpj/<str:jenis>', views.mdl_src_sp2d_lpj_tu_gu, name='mdl_src_sp2d_lpj_tu_gu'),
    path('sp2d/pengesahlpj/src_spj/<str:jenis>', views.mdl_src_sp2d_spj, name='mdl_src_sp2d_spj'),
    path('sp2d/pengesahlpj/mdl', views.sp2d_pengesahlpj_modal, name='sp2d_pengesahlpj_modal'),
    path('sp2d/pengesahlpj/tbl', views.sp2d_pengesahlpj_tabel, name='sp2d_pengesahlpj_tabel'),
    path('sp2d/pengesahlpj/one/<str:jenis0>/<str:jenis1>', views.sp2d_pengesahlpj_simpan, name='sp2d_pengesahlpj_simpan'),

    path('sp2d/lockspjskpd/', views.sp2d_lockspjskpd, name='sp2d_lockspjskpd'),
    path('sp2d/lockspjskpd/tbl', views.sp2d_lockspjskpd_tabel, name='sp2d_lockspjskpd_tabel'),
    path('sp2d/lockspjskpd/one/<str:jenis>', views.sp2d_lockspjskpd_simpan, name='sp2d_lockspjskpd_simpan'),

    path('sp2d/lockspjtgl/', views.sp2d_lockspjtgl, name='sp2d_lockspjtgl'),
    path('sp2d/lockspjtgl/tbl', views.sp2d_lockspjtgl_tabel, name='sp2d_lockspjtgl_tabel'),
    path('sp2d/lockspjtgl/one/<str:jenis>', views.sp2d_lockspjtgl_simpan, name='sp2d_lockspjtgl_simpan'),
    
    path('sp2d/laporan/', views.sp2d_laporan, name='sp2d_laporan'),
    path('sp2d/laporan/skpkd', views.sp2d_laporan_skpkd, name='sp2d_laporan_skpkd'),

    # -------- SP2D YUDHI --------
    path('sp2d/link_ambilsp2d/', views.ambilsp2d, name="link_ambilsp2d"),
    path('sp2d/link_ambilspm/', views.ambilspm, name="link_ambilspm"),
    path('sp2d/link_ambilBank/', views.ambilBank, name="link_ambilBank"),
    path('sp2d/link_ambilRekening/', views.ambilRekening, name="link_ambilRekening"),
    path('sp2d/link_ambilSumberDanaAwal/', views.ambilSumberDanaAwal, name="link_ambilSumberDanaAwal"),
    path('sp2d/link_hapus_gutugunihil/', views.hapus_gutugunihil, name="link_hapus_gutugunihil"),
    path('sp2d/link_simpan_gutugunihil/<str:jenisnya>/', views.simpan_gutugunihil, name="link_simpan_gutugunihil"),
    path('sp2d/link_render_cetak_sp2dgu_tu_nihil/', views.render_cetak_sp2dgu_tu_nihil, name="link_render_cetak_sp2dgu_tu_nihil"),
    path('sp2d/cetak_sp2dgu_tu_nihil/', views.cetak_sp2dgu_tu_nihil, name="cetak_sp2dgu_tu_nihil"),
    path('sp2d/link_ambilKegiatan/', views.ambilKegiatan, name="link_ambilKegiatan"),
    path('sp2d/link_ambilKegiatan_spm/', views.ambilKegiatan_spm, name="link_ambilKegiatan_spm"),    

    path('sp2d/up/', views.up, name="up"),
    path('sp2d/up/load_bank_up', views.load_bank_up, name="load_bank_up"),
    path('sp2d/up/cekdataUP/', views.cekdataUP, name="cekdataUP"),
    path('sp2d/up/link_cekdataSKUP/', views.cekdataSKUP, name="link_cekdataSKUP"),
    path('sp2d/up/link_ambilUP/', views.ambilUP, name="link_ambilUP"),
    path('sp2d/up/link_ambil_spm/', views.ambil_spm, name="link_ambil_spm"),
    path('sp2d/up/link_simpan_sp2d/', views.simpan_sp2d, name="link_simpan_sp2d"),
    path('sp2d/up/link_render_cetak_sp2dup/', views.render_cetak_sp2dup, name="link_render_cetak_sp2dup"),
    path('sp2d/up/link_cetak_sp2dup/', views.cetak_sp2dup, name="link_cetak_sp2dup"),
    path('sp2d/up/link_hapus_sp2d/', views.hapus_sp2d, name="link_hapus_sp2d"),
    path('sp2d/up/link_ambilbankData/', views.ambilbankData, name="link_ambilbankData"),

   # UBAHAN KEPMEN
    path('sp2d/gu/', views.gu, name="gu"),
    path('sp2d/gu/load_bank_gu', views.load_bank_gu, name="load_bank_gu"),
    path('sp2d/gu/sumberdana', views.sp2d_gu_kepmen_sumberdana, name='sp2d_gu_kepmen_sumberdana'),
    path('sp2d/gu/rekening', views.sp2d_gu_kepmen_rekening, name='sp2d_gu_kepmen_rekening'),
    path('sp2d/gu/tabel', views.sp2d_gu_kepmen_tabel, name='sp2d_gu_kepmen_tabel'),
    path('sp2d/gu/spm', views.sp2d_gu_kepmen_ambil_spm, name='sp2d_gu_kepmen_ambil_spm'),
    path('sp2d/gu/spm_src_sp2d', views.sp2d_gu_kepmen_cari_spm_sp2d, name='sp2d_gu_kepmen_cari_spm_sp2d'),
    path('sp2d/gu/cut', views.sp2d_gu_kepmen_potongan, name='sp2d_gu_kepmen_potongan'),
    path('sp2d/gu/mdl_cut', views.sp2d_gu_kepmen_mdl_cut, name='sp2d_gu_kepmen_mdl_cut'),
    path('sp2d/gu/sp2d', views.sp2d_gu_kepmen_ambil_sp2d, name='sp2d_gu_kepmen_ambil_sp2d'),
    path('sp2d/gu/lap_frm', views.sp2d_gu_kepmen_frm_lap, name='sp2d_gu_kepmen_frm_lap'),
    path('sp2d/gu/one/<str:jenis>', views.sp2d_gu_kepmen_simpan, name='sp2d_gu_kepmen_simpan'),
    
    path('sp2d/tu/', views.tu, name="tu"),
    path('sp2d/tu/load_bank_tu', views.load_bank_tu, name="load_bank_tu"),
    path('sp2d/tu/sumberdana', views.sp2d_tu_kepmen_sumberdana, name='sp2d_tu_kepmen_sumberdana'),
    path('sp2d/tu/rekening', views.sp2d_tu_kepmen_rekening, name='sp2d_tu_kepmen_rekening'),
    path('sp2d/tu/tabel', views.sp2d_tu_kepmen_tabel, name='sp2d_tu_kepmen_tabel'),
    path('sp2d/tu/spm', views.sp2d_tu_kepmen_ambil_spm, name='sp2d_tu_kepmen_ambil_spm'),
    path('sp2d/tu/spm_src_sp2d', views.sp2d_tu_kepmen_cari_spm_sp2d, name='sp2d_tu_kepmen_cari_spm_sp2d'),
    path('sp2d/tu/cut', views.sp2d_tu_kepmen_potongan, name='sp2d_tu_kepmen_potongan'),
    path('sp2d/tu/mdl_cut', views.sp2d_tu_kepmen_mdl_cut, name='sp2d_tu_kepmen_mdl_cut'),
    path('sp2d/tu/sp2d', views.sp2d_tu_kepmen_ambil_sp2d, name='sp2d_tu_kepmen_ambil_sp2d'),
    path('sp2d/tu/lap_frm', views.sp2d_tu_kepmen_frm_lap, name='sp2d_tu_kepmen_frm_lap'),
    path('sp2d/tu/one/<str:jenis>', views.sp2d_tu_kepmen_simpan, name='sp2d_tu_kepmen_simpan'),
    # LS
    path('sp2d/ls/load_bank_ls', views.load_bank_ls, name="load_bank_ls"),

    #path('sp2d/tu/link_cektu', views.cekTU, name = "link_cektu"),
    path('sp2d/gunihil/', views.gunihil, name="gunihil"),
    path('sp2d/gunihil/load_bank_gunihil', views.load_bank_gunihil, name="load_bank_gunihil"),

    # SP2D TU NIHIL
    path('sp2d/tunihil/', views.tunihil, name="tunihil"),

    # SPJ YUDHI
    path('spjskpd/spjbendterima/', views.spjbendterima, name="spjbendterima"),
    path('spjskpd/spjbendterima/refreshdata_spjbendterima/', views.refreshdata_spjbendterima, name="link_refreshdata_spjbendterima"),
    path('spjskpd/spjbendterima/aksibos/', views.hapus_spjbendterima, name="hapus_spjbendterima"),
    path('spjskpd/spjbendterima/tambah_spjbendterima_terima/<str:jenisnya>/<str:no_bku>/<str:nobukti>/<str:jenisterima>/', views.tambah_spjbendterima_terima, name="tambah_spjbendterima_terima"),
    path('spjskpd/spjbendterima/input_tambah_penerimaan/<str:jenisnya>/', views.input_tambah_penerimaan, name="input_tambah_penerimaan"),
    path('spjskpd/spjbendterima/link_cetak_bendterima/', views.cetak_bendterima, name="link_cetak_bendterima"),
    path('spjskpd/spjbendterima/link_printout_bendterima/', views.printout_bendterima, name="link_printout_bendterima"),

    path('spjppkd/spjbendterimappkd/', views.spjbendterimappkd, name="spjbendterimappkd"),
    path('spjppkd/spjbendterimappkd/refreshdata_spjbendterimappkd/', views.refreshdata_spjbendterimappkd, name="link_refreshdata_spjbendterimappkd"),
    path('spjppkd/spjbendterimappkd/aksibos/', views.hapus_spjbendterimappkd, name="hapus_spjbendterimappkd"),
    path('spjppkd/spjbendterimappkd/tambah_spjbendterimappkd_terima/<str:jenisnya>/<str:no_bku>/<str:nobukti>/<str:jenisterima>/', views.tambah_spjbendterimappkd_terima, name="tambah_spjbendterimappkd_terima"),
    path('spjppkd/spjbendterimappkd/input_tambah_penerimaan/<str:jenisnya>/', views.input_tambah_penerimaanppkd, name="input_tambah_penerimaanppkd"),
    path('spjppkd/spjbendterimappkd/link_cetak_bendterima/', views.cetak_bendterimappkd, name="link_cetak_bendterimappkd"),
    path('spjppkd/spjbendterimappkd/link_printout_bendterima/', views.printout_bendterimappkd, name="link_printout_bendterimappkd"),
    # END SPJ YUDHI
    # -------- END SP2D YUDHI --------
	path('spjskpd/', include('sipkd.views.spjskpd.urls')),
    path('spjskpd/akuntansiakrual', views.buku_jurnal_akrual, name="buku_jurnal_akrual"),

    path('spjskpd/akuntansiakrual/input_akrual_skpd', views.modal_tambah_akrual_skpd, name="link_modal_tambah_akrual_skpd"),
    path('spjskpd/akuntansiakrual/noref_baru_akrual_skpd', views.noref_baru_akrual_skpd, name="linl_noref_baru_akrual_skpd"),
    path('spjskpd/akuntansiakrual/tampilkantransaksi_akrual_skpd', views.tampilkantransaksi_akrual_skpd, name="link_tampilkantransaksi_akrual_skpd"),
    path('spjskpd/akuntansiakrual/tampilaknpenutup_lra_skpd', views.tampilaknpenutup_lra_skpd, name="link_tampilaknpenutup_lra_skpd"),
    path('spjskpd/akuntansiakrual/tampilaknpenutup_lo_skpd', views.tampilaknpenutup_lo_skpd, name="link_tampilaknpenutup_lo_skpd"),
    path('spjskpd/akuntansiakrual/tampilkanTransaksiSKP_akrual_skpd', views.tampilkanTransaksiSKP_akrual_skpd, name="link_tampilkanTransaksiSKP_akrual_skpd"),
    path('spjskpd/akuntansiakrual/tampilkanTransaksisp2b_akrual_skpd', views.tampilkanTransaksisp2b_akrual_skpd, name="link_tampilkanTransaksisp2b_akrual_skpd"),
    path('spjskpd/akuntansiakrual/simpan_akrual_skpd', views.simpan_akrual_skpd, name="link_simpan_akrual_skpd"),
    path('spjskpd/akuntansiakrual/cetak_laporan_akrual_skpd', views.cetak_laporan_akrual_skpd, name="link_cetak_laporan_akrual_skpd"),
    path('spjskpd/akuntansiakrual/ambil_data_akrual_skpd', views.ambil_data_akrual_skpd, name="link_ambil_data_akrual_skpd"),


    path('spjskpd/akuntansiakrual/list', views.list_jurnal_akrual, name='list_jurnal_akrual'),
    path('spjskpd/akuntansiakrual/posting', views.posting_jurnal, name='posting_jurnal'),
    path('spjskpd/akuntansiakrual/delete', views.delete_jurnal, name='delete_jurnal'),
    path('spjskpd/loadlaporanakrual',views.loadlaporanakrual, name='loadlaporanakrual'),
    path('spjskpd/loadlaporanakrual/pengguna',views.loadpenggunaanggaran, name='loadpenggunaanggaran'),

     # SPJPPKD JOEL 17 6 19 ==================================
    path('spjppkd/skp_skr_skpd/', views.get_skp_skr_skpd, name="get_skp_skr_skpd"),
    path('spjppkd/skp_skr_skpd/tbl0', views.skpskr_skpd_get_tbl_awal, name="skpskr_skpd_get_tbl_awal"),
    path('spjppkd/skp_skr_skpd/mdl0', views.skpskr_skpd_modal_in, name="skpskr_skpd_modal_in"), 
    path('spjppkd/skp_skr_skpd/mdl1', views.skpskr_skpd_modal_rek, name="skpskr_skpd_modal_rek"),
    path('spjppkd/skp_skr_skpd/mdl2', views.skpskr_skpd_modal_edit, name="skpskr_skpd_modal_edit"),
    path('spjppkd/skp_skr_skpd/one/<str:jenis>', views.skpskr_skpd_set_simpan, name="skpskr_skpd_set_simpan"),
    path('spjppkd/skp_skr_skpd/rep', views.skpskr_skpd_frm_lap, name="skpskr_skpd_frm_lap"),


    # SPJPPKD JOEL 09 7 19 ==================================
    path('spjppkd/skp_skr_ppkd/', views.get_skp_skr_ppkd, name="get_skp_skr_ppkd"),
    path('spjppkd/skp_skr_ppkd/tbl0', views.skpskr_ppkd_get_tbl_awal, name="skpskr_ppkd_get_tbl_awal"),
    path('spjppkd/skp_skr_ppkd/mdl0', views.skpskr_ppkd_modal_in, name="skpskr_ppkd_modal_in"), 
    path('spjppkd/skp_skr_ppkd/mdl1', views.skpskr_ppkd_modal_rek, name="skpskr_ppkd_modal_rek"),
    path('spjppkd/skp_skr_ppkd/mdl2', views.skpskr_ppkd_modal_edit, name="skpskr_ppkd_modal_edit"),
    path('spjppkd/skp_skr_ppkd/one/<str:jenis>', views.skpskr_ppkd_set_simpan, name="skpskr_ppkd_set_simpan"),
    path('spjppkd/skp_skr_ppkd/rep', views.skpskr_ppkd_frm_lap, name="skpskr_ppkd_frm_lap"),
    # END SPJPPKD ===========================================

    # ---- JOEL 14 5 19 ------------------
    path('spjskpd/skp_skr/', views.get_skp_skr, name="get_skp_skr"),
    path('spjskpd/skp_skr/tbl0', views.skpskr_get_tbl_awal, name="skpskr_get_tbl_awal"),
    path('spjskpd/skp_skr/mdl0', views.skpskr_modal_in, name="skpskr_modal_in"), 
    path('spjskpd/skp_skr/mdl1', views.skpskr_modal_rek, name="skpskr_modal_rek"),
    path('spjskpd/skp_skr/mdl10', views.skpskr_modal_rek_srvside, name="skpskr_modal_rek_srvside"),
    path('spjskpd/skp_skr/mdl2', views.skpskr_modal_edit, name="skpskr_modal_edit"),
    path('spjskpd/skp_skr/one/<str:jenis>', views.skpskr_set_simpan, name="skpskr_set_simpan"),
    path('spjskpd/skp_skr/rep', views.skpskr_frm_lap, name="skpskr_frm_lap"),

    # ---- JOEL 20 5 19 ------------------
    path('akuntansi/konversirekeningakrual/', views.get_koreak_load, name="get_koreak_load"),
    path('akuntansi/konversirekeningakrual/tbl1', views.koreak_get_tbl_awal, name="koreak_get_tbl_awal"),
    path('akuntansi/konversirekeningakrual/get1', views.koreak_modal_in, name="koreak_modal_in"),
    path('akuntansi/konversirekeningakrual/lap', views.koreak_frm_lap, name="koreak_frm_lap"),
    path('akuntansi/konversirekeningakrual/mdl0/<str:jenis>', views.mdl_akrual_rekening, name="mdl_akrual_rekening"),
    path('akuntansi/konversirekeningakrual/one/<str:jenis>', views.koreak_set_simpan, name="koreak_set_simpan"),

    # ---- JOEL 20 5 19 ------------------
    path('akuntansi/konversipiutang/', views.get_konpiu_load, name="get_konpiu_load"),
    path('akuntansi/konversipiutang/mdl', views.konpiu_modal_in, name="konpiu_modal_in"),
    path('akuntansi/konversipiutang/one/<str:jenis>', views.konpiu_set_simpan, name="konpiu_set_simpan"),

    # ---- JOEL 18 4 19 ------------------
    # path('sp2d/tunihil/', views.get_tunihil, name="get_tunihil"),
    # path('sp2d/tunihil/tbl', views.sp2d_tunihil_tabel, name="sp2d_tunihil_tabel"),
    # path('sp2d/tunihil/tblrek', views.sp2d_tunihil_tabel_rekening, name="sp2d_tunihil_tabel_rekening"),
    # path('sp2d/tunihil/spm', views.sp2d_tunihil_ambil_spm, name="sp2d_tunihil_ambil_spm"),
    # path('sp2d/tunihil/rek', views.sp2d_tunihil_rekening, name="sp2d_tunihil_rekening"),
    # path('sp2d/tunihil/one/<str:jenis>', views.sp2d_tu_nihil_simpan, name="sp2d_tu_nihil_simpan"),
    # path('sp2d/tunihil/lpj/<str:jenis>', views.mdl_src_sp2d_lpj_tu, name="mdl_src_sp2d_lpj_tu"),
    # path('sp2d/tunihil/get0', views.sp2d_tunihil_ambil_lpj, name="sp2d_tunihil_ambil_lpj"), 
    # path('sp2d/tunihil/get1', views.sp2d_tunihil_ambil_sp2d, name="sp2d_tunihil_ambil_sp2d"),
    # path('sp2d/tunihil/lap', views.sp2d_tu_nihil_frm_lap, name="sp2d_tu_nihil_frm_lap"),
    # ---- JOEL 18 4 19 END --------------

    # ---------- AKUNTANSI ----------------
    # path('akuntansi/laporanlrabulanan/', views.laporan_realisasi_pemda, name='laporan_realisasi_pemda'),
    # path('akuntansi/laporanverifikasi/',views.laporan_verifikasi, name='laporan_verifikasi'),

    # ---------- AAN ----------------------
# ---- MODUL SPJ SKPD Mauludy ------------------
    path('spjskpd/<str:jenis_data_spj_skpd>/', views.data_spj_skpd, name='data_spj_skpd'),
    path('spjskpd/<str:jenis_data_spj_skpd>/get_data_spjskpd', views.get_data_spjskpd, name='get_data_spjskpd'),
    path('spjskpd/<str:jenis_data_spj_skpd>/simpan_data_spjskpd', views.simpan_data_spjskpd, name='simpan_data_spjskpd'),
    # ---- MODUL SPJ SKPD Mauludy ------------------
    # ANOV
    path('spjskpd0/', include('sipkd.views.spjskpd.urls')),
    path('akuntansi/masterekening/', include('sipkd.views.akuntansi.masterekening.urls')),
    path('akuntansi/akrualppkd/', include('sipkd.views.akuntansi.akrualppkd.urls')),
    # END anov
    
    # Akuntansi Yudhi
    path('akuntansi/akuntansiakrualppkd/', views.akuntansiakrualppkd, name='akuntansiakrualppkd'),    
    # END akuntansi yudhi
    
    # ---- MODUL Akuntansi Mauludy ------------------
    path('akuntansi/<str:jenis_akuntansi>/', views.akuntansi, name='akuntansi'),
    path('akuntansi/<str:jenis_akuntansi>/get_data_ppkd', views.get_data_ppkd, name='get_data_ppkd'),
    path('akuntansi/<str:jenis_akuntansi>/simpan_data_ppkd', views.simpan_data_ppkd, name='simpan_data_ppkd'),
    path('akuntansi/<str:jenis_akuntansi>/get_lampiran_perda/', views.getlampiranperda, name='getlampiranperda'),
    path('akuntansi/<str:jenis_akuntansi>/delete_lampiran_perda/', views.deletelampiranperda, name='deletelampiranperda'),
    path('akuntansi/<str:jenis_akuntansi>/add_lampiran_perda/', views.addlampiranperda, name='addlampiranperda'),
    path('akuntansi/<str:jenis_akuntansi>/save_lampiran_perda/', views.savelampiranperda, name='savelampiranperda'),
    path('akuntansi/cetak_laporan', views.cetak_laporan, name='cetak_laporan'),
    # ---- MODUL Akuntansi Mauludy ------------------

    # ---- MODUL KASDA ------------------------
    path('kasda/', include('sipkd.views.kasda.urls')),
    # ---- MODUL KASDA ------------------------
    # ambil jurnal 
    path('spjskpd/akuntansiakrual/ambil_jurnal', views.modal_ambil_jurnal, name="modal_ambil_jurnal"),
    path('spjskpd/akuntansiakrual/modal_rekening_jurnal', views.modal_rekening_jurnal, name="modal_rekening_jurnal"),
    

    # tambahan list data sp2d modal serverside
    path('sp2d/list_modal_sp2d/', views.list_modal_sp2d, name="list_modal_sp2d"),
    path('sp2d/load_data_sp2d_serverside/<str:jenis>/<str:jenis0>', views.load_data_sp2d_serverside, name="load_data_sp2d_serverside"),
    # end tambahan list data sp2d modal serverside

    path('spp/lpj/persetujuanlpj/', views.persetujuanlpjskpd, name='persetujuanlpjskpd'),
    path('spp/lpj/listpersetujuanlpj/', views.listpersetujuanlpj, name='listpersetujuanlpj'),
    path('spp/lpj/setuju_draftlpj/', views.setuju_draftlpj, name='setuju_draftlpj'),

    # # ---- JOEL 23 FEB 22 ------------------
    path('akuntansi/laporanlkpd/cetak', views.print_lap_lkpd, name="print_lap_lkpd"),
    path('public/generate_nomor_auto/', views.generate_nomor_auto, name="generate_nomor_auto"),


    # YUDHI 20 OCT 2022
    path('konfig/sync_datasipd/', views.sync_datasipd, name="sync_datasipd"),
    path('konfig/sync_datasipd/tabssync', views.tabssyncsipd, name="tabssyncsipd"),
    path('konfig/sync_datasipd/modal_upload_syncsipd/<str:page>/', views.modal_upload_syncsipd, name="modal_upload_syncsipd"),

    # TAMBAHAN SP2B ---- JOEL * 22 OCT 21 ------ 
    path('sp2d/sp2b/', views.sp2b_awal, name="sp2b_awal"),
    path('sp2d/sp2b/sumberdana', views.sp2b_sumberdana, name='sp2b_sumberdana'),
    path('sp2d/sp2b/rekening', views.sp2b_rekening, name='sp2b_rekening'),
    path('sp2d/sp2b/tabel', views.sp2b_tabel, name='sp2b_tabel'),
    path('sp2d/sp2b/spm', views.sp2b_ambil_spm, name='sp2b_ambil_spm'),
    path('sp2d/sp2b/spm_src_sp2d', views.sp2b_cari_spm_sp2b, name='sp2b_cari_spm_sp2b'),
    path('sp2d/sp2b/cut', views.sp2b_potongan, name='sp2b_potongan'),
    path('sp2d/sp2b/mdl_cut', views.sp2b_mdl_cut, name='sp2b_mdl_cut'),
    path('sp2d/sp2b/sp2d', views.sp2b_ambil_sp2b, name='sp2b_ambil_sp2b'),
    path('sp2d/sp2b/lap_frm', views.sp2b_frm_lap, name='sp2b_frm_lap'),
    path('sp2d/sp2b/one/<str:jenis>', views.sp2b_simpan, name='sp2b_simpan'),
    path('sp2d/sp2b/cek_nosp2b', views.cek_nosp2b, name='cek_nosp2b'),
	
	# TAMBAHAN BKP
    # path('spp/listbkp/<str:jenis>', views.listdatabkp, name='listdatabkp'),
    # path('spp/listkegiatanbkp', views.listkegiatanbkp, name='listkegiatanbkp'),
    # path('spp/addkegiatanbkp', views.addkegiatanbkp, name='addkegiatanbkp'),

    # TAMBAHAN BKP ========== BY. JOEL ==== 25 NOV 22 ====================  simpanlpjrincian
    path('spp/bkp/<str:jenis>', views.bkp_index, name='bkp_index'),
    path('spp/bkp/list/<str:jenis>', views.bkp_list, name='bkp_list'),
    path('spp/bkp/list/aksi/delete', views.bkp_list_delete, name='bkp_list_delete'),
    path('spp/bkp/laporan/<str:jenis>', views.bkp_laporan, name='bkp_laporan'),
    path('spp/bkp/kegiatan/list', views.bkp_kegiatan, name='bkp_kegiatan'),
    path('spp/bkp/kegiatan/add', views.bkp_kegiatan_add, name='bkp_kegiatan_add'),
    path('spp/bkp/kegiatan/save', views.bkp_kegiatan_save, name='bkp_kegiatan_save'),
    path('spp/bkp/kegiatan/update', views.bkp_kegiatan_update, name='bkp_kegiatan_update'),
    path('spp/bkp/kegiatan/delete', views.bkp_kegiatan_delete, name='bkp_kegiatan_delete'),
    path('spp/bkp/nopspj/<str:jenis>', views.getnew_nopspj, name='getnew_nopspj'),
    path('spp/bkp/nospd/cek', views.bkp_cek_nospd, name='bkp_cek_nospd'),
    path('spp/bkp/rekening/list', views.bkp_rekening_list, name='bkp_rekening_list'),
    path('spp/bkp/rincian/list/<str:jenis>', views.bkp_rincian_list, name='bkp_rincian_list'),
    path('spp/bkp/rincian/save/<str:jenis>', views.bkp_rincian_save, name='bkp_rincian_save'),
    path('spp/bkp/rincian/delete/<str:jenis>', views.bkp_rincian_delete, name='bkp_rincian_delete'),
    path('spp/bkp/modal/potongan', views.bkp_modal_potongan, name='bkp_modal_potongan'),
    path('spp/bkp/modal/kwitansi', views.bkp_modal_kwitansi, name='bkp_modal_kwitansi'),
    # PERSETUJUAN PERMOHONAN di form LPJ upgu ========================
    path('spp/listpermohonanlpj', views.listpermohonanlpj, name='listpermohonanlpj'),
    path('kontrak/pihakketiga/search', views.load_perusahaan, name='load_perusahaan'),

    ]
