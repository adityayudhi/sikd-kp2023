from sipkd import config as cfg
from sipkd.views.spjskpd.anov import *

koderekening_fields = [
	'kodeakun',
	'kodekelompok',
	'kodejenis',
	'kodeobjek',
	'koderincianobjek',
]

masterekening_fields = {}
masterekeningakrual_fields = {}
with querybuilder() as qb:
	qb.tablecolumns('master', 'master_rekening', masterekening_fields)
	qb.tablecolumns('akuntansi', 'akrual_master_rekening', masterekeningakrual_fields)

# masterekening_primarykeys = [
# 	'tahun',
# 	*koderekening_fields,
# ]
