from django.urls import path, include
from . import (
	pmd13,
	akrual,
)

urlpatterns = [
	path('pmd13/', include([
		path('', pmd13.index, name='akuntansi_masterekening_pmd13_index'),
		path('browse', pmd13.browse, name='akuntansi_masterekening_pmd13_browse'),
	])),
	path('akrual/', include([
		path('', akrual.index, name='akuntansi_masterekening_akrual_index'),
		path('browse', akrual.browse, name='akuntansi_masterekening_akrual_browse'),
		path('save', akrual.save, name='akuntansi_masterekening_akrual_save'),
		path('rm', akrual.rm, name='akuntansi_masterekening_akrual_rm'),
	])),
]
