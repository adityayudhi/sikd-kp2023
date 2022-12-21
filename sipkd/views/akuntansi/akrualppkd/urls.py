from django.urls import (path, include, )
from . import main

urlpatterns = [
	path('', main.index, name='akuntansi-akrualppkd-index'),
	path('data', main.data, name='akuntansi-akrualppkd-data'),
	path('save', main.save, name='akuntansi-akrualppkd-save'),
	path('destroy', main.destroy, name='akuntansi-akrualppkd-destroy'),
	path('posting', main.posting, name='akuntansi-akrualppkd-posting'),
	path('browse', main.browse, name='akuntansi-akrualppkd-browse'),
	path('rincian_update', main.rincian_update, name='akuntansi-akrualppkd-rincian_update'),
	path('rincian_create', main.rincian_create, name='akuntansi-akrualppkd-rincian_create'),
	path('default', main.rekening_default, name='akuntansi-akrualppkd-rekening-default'),
	path('rekening', main.rekening, name='akuntansi-akrualppkd-rekening'),
	path('norefauto', main.norefauto, name='akuntansi-akrualppkd-norefauto'),
	# path('report', main.report, name='spjskpd_main_report'),
]
