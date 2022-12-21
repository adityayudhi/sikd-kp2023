"""
@author: anovsiradj;
@version: 20190507;
@version/querybuilder: 20190409122905, 20190411, 20190415, 201905;
"""

import os
import warnings
from django.db import connection,connections
from types import SimpleNamespace
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.conf import settings

is_anov_host = True if ('IS_ANOV_HOST' in os.environ and int(os.environ['IS_ANOV_HOST']) == 1) else False

"""
TODO.
"""
class dick(SimpleNamespace):
	pass

"""
	querybuilder
	============
	digunakan untuk menghasilkan perintah SQL untuk melakukan CRUD sederhana.

	PEMAKAIAN
	---------
	params_tuple = (param1, param2, ...)
	params_list = [param1, param2, ...]
	contents_dict = {'k': 'key', 'v': 'value', ...}
	with querybuilder() as qb:
		qb.execute(
			'CREATE/INSERT|READ/SELECT|UPDATE|DELETE TABLENAME ... %s, %s, ...',
			param1, param2, ...,
			param1='key', param2='value', ...
		)
		qb.execute(
			'CREATE/INSERT|READ/SELECT|UPDATE|DELETE TABLENAME ... %s, %s, ...',
			*params_tuple|*params_list,
			**contents_dict
		)

	CREATE/INSERT
	--------------------------
	0>>>
	data = ('key','value')
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("INSERT INTO konfigurasi (k,v) VALUES (%s,%s)", *data)
	1>>>
	data = {'k': 'key', 'v': 'value'}
	with querybuilder('konfigurasi', **data) as qb: qb.create() # metode.1
	with querybuilder('konfigurasi') as qb: qb.create(**data)   # metode.2

	READ/SELECT
	----------------------
	# ONE:0>>>
	result_test = None
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT * FROM konfigurasi a WHERE a.k = %s", 'key')
		result_test = fn_fetch_all(cursor)
		result_test = result[0]
	# ONE:1>>>
	result_test = {}
	with querybuilder('konfigurasi', k='key') as qb: qb.result_one(result_test)

	# MANY:0>>>
	result = None
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT * FROM konfigurasi a WHERE a.k LIKE = %s", 'key_%%')
		result = fn_fetch_all(cursor)
	# MANY:1>>>
	result = []
	with querybuilder('konfigurasi', k=('LIKE', 'key_%%')) as qb:
		qb.read()
		qb.result_many(result)

	UPDATE
	------------
	# 0>>>
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute('UPDATE konfigurasi SET v = %s WHERE k = %s', 'value', 'key')
	# 1>>>
	primarykeys = ['k']
	contents = {'k': 'key', 'v': 'value'}
	with querybuilder('konfigurasi', *primarykeys, **contents) as qb: qb.update()

	DELETE
	------------
	# 0>>>
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute('DELETE FROM konfigurasi WHERE k = %s', 'key')
	# 1>>>
	with querybuilder('konfigurasi') as qb: qb.delete(**{'k': 'key'})

	CATATAN/KETERANGAN
	------------------
	# 0>>> === sebelum
	# 1>>> === sesudah
"""

class querybuilder:
	# OK
	def __init__(self, table=None, *args, **kwargs):
		self.table = table
		self.table_primarykeys = []
		self.table_contents = {}

		self.table_read_sort = ''
		self.table_read_sort_fields = []

		self.primarykeys(*args)
		self.contents(**kwargs)

		# ADD JOEL GI-JAN 22 ===================================
		# GET DATABASE LIST FROM setting.py
		keydb = []
		for x in settings.DATABASES.keys():
			if(x != 'default'):
				keydb.append(x) #2021,2022
		
		# GET SESSION KEY BY DATE 
		seskey = ''
		for s in Session.objects.filter(expire_date__gte=timezone.now()):
			try:
				seskey = s.session_key
			except:
				pass # if corrupted data

		# GET SESSION TAHUN BY KEY
		if (seskey != ''):
			session = Session.objects.get(session_key=seskey)
			th_sess = session.get_decoded().get('sipkd_tahun',None)
		else:
			th_sess = None

		if (th_sess != None):
			tahun = th_sess
		else:
			tahun = keydb[0]

		self.context = connections[tahun].cursor()
		# END ADD JOEL GI-JAN 22 ===================================

	# fed

	# OK
	def __enter__(self):
		return self
	# fed

	# OK
	def __exit__(self, exc_type, exc_value, traceback):
		self.context.close()
	# fed

	# OK
	def primarykeys(self,*args):
		for arg in args:
			if arg not in self.table_primarykeys:
				self.table_primarykeys.append(arg)
	# fed

	# OK
	def contents(self,**kwargs):
		for k,v in kwargs.items():
			self.table_contents[k] = v
		return self
	# fed

	# OK
	def create(self, *args, test=False, dump=False, **kwargs):
		self.primarykeys(*args)
		self.contents(**kwargs)

		keys=[]
		values=[]
		for k,v in self.table_contents.items():
			keys.append(k)
			values.append(v)

		stmt = 'INSERT into {0} ({1}) VALUES({2})'.format(
			self.table,
			','.join(keys),
			','.join(['%s'] * len(values))
		)

		if dump == True: print(stmt)
		if test == True: print(stmt % (*values,))
		else: self.context.execute(stmt, (*values,))

		return self
	# fed

	def update(self, *args, test=False, dump=False, **kwargs):
		self.primarykeys(*args)
		self.contents(**kwargs)

		get_keys_stmt=[]
		set_keys_stmt=[]
		values=[]

		"""
		yaelah, postgre tidak support column alias.
		https://www.postgresql.org/docs/9.6/sql-update.html
		"""
		for k,v in self.table_contents.items():
			if k not in self.table_primarykeys:
				if v.__class__.__name__ in ('list', 'tuple'):
					raise Exception('[update] jika "v" buka primarykeys, "v" tidak boleh array:"{}".'.format(v))
				# set_keys_stmt.append('abyz.{} = %s'.format(k))
				set_keys_stmt.append('"{}" = %s'.format(k))
				values.append(v)

		for k,v in self.table_contents.items():
			if k in self.table_primarykeys:
				if v.__class__.__name__ in ('list', 'tuple'):
					get_keys_stmt.append('abyz.{} {} %s'.format(k,v[0]))
					values.append(v[1])
				else:
					get_keys_stmt.append('abyz.{} = %s'.format(k))
					values.append(v)

		stmt = 'UPDATE {} abyz SET {} WHERE {}'.format(self.table, ' , '.join(set_keys_stmt) , ' AND '.join(get_keys_stmt))

		if dump == True: print(stmt)
		if test == True: print(stmt % (*values,))
		else: self.context.execute(stmt, (*values,))
	# fed

	def delete(self, *args, test=False, dump=False, **kwargs):
		if test == True: dump = True

		self.primarykeys(*args)
		self.contents(**kwargs)

		keys = []
		keys_stmt = []
		values = []
		for k,v in self.table_contents.items():
			keys.append(k)
			if v.__class__.__name__ in ('list', 'tuple'):
				keys_stmt.append('abyz.{} {} %s'.format(k,v[0]))
				values.append(v[1])
			else:
				keys_stmt.append('abyz.{} = %s'.format(k))
				values.append(v)

		stmt = 'DELETE FROM {} abyz WHERE {}'.format(self.table, ' AND '.join(keys_stmt))

		if dump == True: print(stmt)
		if test == True: print(stmt % (*values,))
		else: self.context.execute(stmt, (*values,))
	# fed

	def read(self, *args, test=False, dump=False, **kwargs):
		if test == True: dump = True

		self.primarykeys(*args)
		self.contents(**kwargs)

		keys = []
		keys_stmt = []
		values = []

		for k,v in self.table_contents.items():
			keys.append(k)
			if v.__class__.__name__ in ('list', 'tuple'):
				keys_stmt.append('abyz.{} {} %s'.format(k,v[0]))
				values.append(v[1])
			else:
				keys_stmt.append('abyz.{} = %s'.format(k))
				values.append(v)

		sort = ''
		if len(self.table_read_sort_fields) > 0:
			sort += 'ORDER BY '
			sort += ','.join(map(lambda x: 'abyz.' + x, self.table_read_sort_fields))
			sort += ' ' + self.table_read_sort

		stmt = 'SELECT abyz.* from {} abyz WHERE {} {}'.format(self.table, ' AND '.join(keys_stmt), sort)

		if dump == True: print(stmt)
		if test == True: print(stmt % (*values,))
		else: self.context.execute(stmt, (*values,))

		return self
	# fed

	# OK
	def read_sort(self, *args, sort=''):
		self.table_read_sort = sort.upper()
		for arg in args:
			if arg not in self.table_read_sort_fields:
				self.table_read_sort_fields.append(arg)
		return self
	# fed

	# OK
	def execute(self,statement, *args, **kwargs):
		self.context.execute(statement, *args, **kwargs)
		return self
	# fed

	# OK
	def result(self):
		fields = [f.name for f in self.context.description]
		for entry in self.context:
			yield dict(zip(fields,entry))
	# fed

	# OK
	def result_many(self,result=[]):
		for entry in self.result():
			result.append(entry)
		return result
	# fed

	def result_one(self,result={}):
		result.update(
			dict(zip(
				[f.name for f in self.context.description],
				self.context.fetchone(),
			))
		)
		return result

	# [DEPRECATED]
	def tablecolumns(self,table_schema,table_name,info={}):
		warnings.warn('deprecated', DeprecationWarning);
		return self.info_columns(table_schema,table_name,info);
	#

	# @version: 20190722; #
	def info_columns(self,table_schema,table_name,info={}):
		b = ''
		self.context.execute("SELECT a.column_name,a.data_type FROM information_schema.columns a WHERE a.table_schema = '{}' AND a.table_name = '{}'".format(table_schema,table_name))
		for b in self.context:
			if info.__class__.__name__ == 'dict': info[ str(b[0]).strip() ] = str(b[1]).strip();
			elif info.__class__.__name__ == 'list': info.append( b[0].strip() );
			else: raise Exception('unknown type(%s)' % info.__class__.__name__);
		del b
		return info
	# 

	# @version: 20190722; #
	# https://wiki.postgresql.org/wiki/Retrieve_primary_key_columns #
	def info_primarykeys(self, table_schema, table_name, info={}):
		b = ''
		self.context.execute("""
			SELECT a.attname, FORMAT_TYPE(a.atttypid, a.atttypmod) AS data_type
			FROM pg_index i JOIN pg_attribute a ON (a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey))
			WHERE i.indrelid = '{0}.{1}'::regclass AND i.indisprimary
		""".format(table_schema,table_name))
		for b in self.context:
			if info.__class__.__name__ == 'dict': info[ str(b[0]).strip() ] = str(b[1]).strip();
			elif info.__class__.__name__ == 'list': info.append( b[0].strip() );
			else: raise Exception('unknown type(%s)' % info.__class__.__name__);
		del b
		return info
	# 
# 
