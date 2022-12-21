from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseServerError
from ...anov import *
from .. import main
import re

isskpd = 0
angg_kegiatan_fields = None
jenisjenis = {
	'SP2D': 'Penerimaan SP2D LS',
	'SPJ': 'Pertanggung Jawaban SPJ LS',
}
sekarang_penerimaan_re = 'SP2D'

rincian_re_match = '\w+\[\w+\]\[\]'
rincian_re_capture = '(\w+)\[(\w+)\]\[\]'
rincian_re_replace = '{}[{}][]'

# OK
def browse(request):
	must = ['tahun','kodeurusan','kodesuburusan','kodeorganisasi','kodeunit','jenis_bku']
	for n in must:
		try: request.GET[n]
		except Exception as err:
			return HttpResponseServerError(err, content_type='text/plain');

	jenis_bku = request.GET['jenis_bku'];
	data = []
	cond = (
		request.GET['tahun'],
		request.GET['kodeurusan'], request.GET['kodesuburusan'], request.GET['kodeorganisasi'],
		request.GET['kodeunit'],
	)

	if jenis_bku == 'SP2D':
		with querybuilder() as qb:
			qb.execute(
			"""
				SELECT
			    -- a.tahun,a.kodeurusan,a.kodesuburusan,a.kodeorganisasi,a.kodeunit,
			    b.kodebidang,b.kodeprogram,b.kodekegiatan,b.kodesubkegiatan,
			    b.kodebidang||'.'||b.kodeprogram||'.'||b.kodekegiatan||'.'||b.kodesubkegiatan as kegiatan_kode,
			    c.urai as kegiatan_urai,
			    a.nosp2d, a.nosp2d as bukti,
			    a.jenissp2d, a.jenissp2d as jenis_sp2d,
			    a.tanggal, a.tanggal as tgl_bukti,
			    a.tglkasda, a.tglkasda as tgl_bku,
			    a.namayangberhak,
			    a.informasi, a.informasi as urai,
			    a.nospm,
			    a.tglspm,
			    b.jumlah

			    FROM penatausahaan.sp2d a
			    RIGHT JOIN (SELECT b.tahun,
			        b.kodeurusan,b.kodesuburusan,b.kodeorganisasi,b.kodeunit,
			        b.kodebidang,b.kodeprogram,b.kodekegiatan,b.kodesubkegiatan,
			        b.nosp2d,
			        COALESCE(SUM(b.jumlah),0) as jumlah
			        FROM penatausahaan.sp2drincian b GROUP BY b.tahun,
			        b.kodeurusan,b.kodesuburusan,b.kodeorganisasi,b.kodeunit,
			        b.kodebidang,b.kodeprogram,b.kodekegiatan,b.kodesubkegiatan,
			        b.nosp2d
			    ) b ON (b.tahun = a.tahun
			        AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan 
			        AND b.kodeorganisasi = a.kodeorganisasi AND b.kodeunit = a.kodeunit
			        AND b.nosp2d = a.nosp2d
			    )
			    LEFT JOIN (
                	SELECT tahun, kodeurusan, kodesuburusan, kodeorganisasi, kodeunit, kodebidang, kodeprogram, kodekegiatan, kodesubkegiatan, urai 
                    FROM penatausahaan.kegiatan
                    UNION
                    SELECT tahun, kodeurusan, kodesuburusan, kodeorganisasi, kodeunit, '5.02' as kodebidang, 0 as kodeprogram, '0.0' as kodekegiatan, 0 as kodesubkegiatan, 'PENGELUARAN PEMBIAYAAN' as urai
                    FROM penatausahaan.pembiayaan
                    UNION
                    SELECT tahun, kodeurusan, kodesuburusan, kodeorganisasi, kodeunit, '5.02' as kodebidang, 1 as kodeprogram, '0.0' as kodekegiatan, 0 as kodesubkegiatan, 'PENGELUARAN PEMBIAYAAN' as urai
                    FROM penatausahaan.pembiayaan
                )as  c on (c.tahun = a.tahun
			        AND c.kodeurusan = a.kodeurusan AND c.kodesuburusan = a.kodesuburusan 
			        AND c.kodeorganisasi = a.kodeorganisasi AND c.kodeunit = a.kodeunit
			        AND c.kodebidang = b.kodebidang AND c.kodeprogram = b.kodeprogram 
			        AND c.kodekegiatan = b.kodekegiatan AND c.kodesubkegiatan = b.kodesubkegiatan
			    )

			    WHERE a.tahun = %s
			    AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s
			    AND a.kodeunit = %s
			    AND a.jenissp2d = 'LS'

			    AND NOT EXISTS (
			        SELECT 1 FROM pertanggungjawaban.skpd_bku z WHERE z.tahun = a.tahun
			        AND z.kodeurusan = a.kodeurusan AND z.kodesuburusan = a.kodesuburusan 
			        AND z.kodeorganisasi = a.kodeorganisasi AND z.kodeunit = a.kodeunit
			        AND z.jenis_bku = 'SP2D' AND z.jenis_sp2d = 'LS'
			        AND z.bukti = a.nosp2d
			    )
			""", cond)
			qb.result_many(data);

	elif jenis_bku == 'SPJ':
		with querybuilder() as qb:
			qb.execute(
			"""
				SELECT
				b.kodebidang,b.kodeprogram,b.kodekegiatan,b.kodesubkegiatan,
				b.kodebidang||'.'||b.kodeprogram||'.'||b.kodekegiatan||'.'||b.kodesubkegiatan as kegiatan_kode, 
				c.urai as kegiatan_urai,
				a.no_bku, a.tgl_bku,
				a.bukti, a.tgl_bukti, a.jenis_sp2d,
				a.is_pihak_ketiga, a.simpananbank,
				a.urai,
				COALESCE(b.penerimaan,0) AS jumlah

				FROM pertanggungjawaban.skpd_bku a
				RIGHT JOIN (SELECT b.tahun,
					b.kodeurusan,b.kodesuburusan,b.kodeorganisasi,b.kodeunit,
					b.kodebidang,b.kodeprogram,b.kodekegiatan,b.kodesubkegiatan,
					b.no_bku,b.isskpd,
					SUM(b.penerimaan) AS penerimaan
					FROM pertanggungjawaban.skpd_bkurincian b WHERE b.kodeakun in (5,6) GROUP BY b.tahun,
					b.kodeurusan,b.kodesuburusan,b.kodeorganisasi,b.kodeunit,
					b.kodebidang,b.kodeprogram,b.kodekegiatan,b.kodesubkegiatan,
					b.no_bku,b.isskpd
				) b on (b.tahun = a.tahun
					AND b.kodeurusan=a.kodeurusan AND b.kodesuburusan = a.kodesuburusan 
					AND b.kodeorganisasi = a.kodeorganisasi
					AND b.kodeunit = a.kodeunit
					AND b.no_bku = a.no_bku AND b.isskpd = a.isskpd
				)
				LEFT JOIN (
                	SELECT tahun, kodeurusan, kodesuburusan, kodeorganisasi, kodeunit, kodebidang, kodeprogram, kodekegiatan, kodesubkegiatan, urai 
                    FROM penatausahaan.kegiatan
                    UNION
                    SELECT tahun, kodeurusan, kodesuburusan, kodeorganisasi, kodeunit, '5.02' as kodebidang, 0 as kodeprogram, '0.0' as kodekegiatan, 0 as kodesubkegiatan, 'PENGELUARAN PEMBIAYAAN' as urai
                    FROM penatausahaan.pembiayaan
                    UNION
                    SELECT tahun, kodeurusan, kodesuburusan, kodeorganisasi, kodeunit, '5.02' as kodebidang, 1 as kodeprogram, '0.0' as kodekegiatan, 0 as kodesubkegiatan, 'PENGELUARAN PEMBIAYAAN' as urai
                    FROM penatausahaan.pembiayaan
                )as  c on (c.tahun = a.tahun
			        AND c.kodeurusan = a.kodeurusan AND c.kodesuburusan = a.kodesuburusan 
			        AND c.kodeorganisasi = a.kodeorganisasi AND c.kodeunit = a.kodeunit
			        AND c.kodebidang = b.kodebidang AND c.kodeprogram = b.kodeprogram 
			        AND c.kodekegiatan = b.kodekegiatan AND c.kodesubkegiatan = b.kodesubkegiatan
			    )

			    WHERE a.tahun = %s
				AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s AND a.kodeunit = %s
				AND a.jenis_bku LIKE '%%SP2D%%' AND a.jenis_sp2d = 'LS'
				AND a.isskpd = %s

				AND NOT EXISTS (
					SELECT 1 FROM pertanggungjawaban.skpd_bku z WHERE z.tahun = a.tahun
					AND z.kodeurusan = a.kodeurusan AND z.kodesuburusan = a.kodesuburusan 
					AND z.kodeorganisasi = a.kodeorganisasi
					AND z.kodeunit = a.kodeunit
					AND z.jenis_bku LIKE '%%SPJ%%' AND z.jenis_sp2d = 'LS'
					AND z.bukti = a.bukti
				)
			""", (*cond, isskpd));
			qb.result_many(data);

	else: return HttpResponseServerError('jenis_bku ?? "%s"' % jenis_bku, content_type='text/plain');

	return JsonResponse(data, safe=False)
# 

# OK
def rincian_sp2d(rq):
	data = {'rincian': [], 'potongan': []}
	cond_0 = (
		rq.GET['nosp2d'],
		rq.GET['tahun'],
		rq.GET['kodeurusan'],rq.GET['kodesuburusan'],rq.GET['kodeorganisasi'],rq.GET['kodeunit'],
		rq.GET['kodebidang'],rq.GET['kodeprogram'],rq.GET['kodekegiatan'],rq.GET['kodesubkegiatan'],
	)
	cond_1 = (
		rq.GET['tahun'],
		rq.GET['kodeurusan'],rq.GET['kodesuburusan'],rq.GET['kodeorganisasi'],rq.GET['kodeunit'],
		rq.GET['nosp2d'],
	)

	with querybuilder() as qb:
		qb.execute("""
			SELECT DISTINCT (
						a.kodebidang || '.' || a.kodeorganisasi || '.' || a.kodeprogram || '.' || a.kodekegiatan || '.' || a.kodesubkegiatan || '-' || a.kodeakun || '.' || a.kodekelompok || '.' || a.kodejenis || '.' || LPAD(a.kodeobjek::text, 2, '0') || '.' || LPAD(a.koderincianobjek::text, 2, '0') || '.' || LPAD(a.kodesubrincianobjek::text, 3, '0')
					) AS kode_rekening,
					(
						SELECT b.urai
						FROM master.master_rekening b
						WHERE b.tahun = a.tahun
							AND b.kodeakun = a.kodeakun
							AND b.kodekelompok = a.kodekelompok
							AND b.kodejenis = a.kodejenis
							AND b.kodeobjek = a.kodeobjek
							AND b.koderincianobjek = a.koderincianobjek
							AND b.kodesubrincianobjek = a.kodesubrincianobjek
					) as urai_rekening,
					-- a.tahun,
					-- a.kodeurusan,a.kodesuburusan,a.kodeorganisasi,a.kodeunit,
					a.kodebidang,
					a.kodeprogram,
					a.kodekegiatan,
					a.kodesubkegiatan,
					a.kodeakun,
					a.kodekelompok,
					a.kodejenis,
					a.kodeobjek,
					a.koderincianobjek,
					a.kodesubrincianobjek,
					(
						CASE WHEN a.kodeakun = 6 THEN
							(SELECT b.jumlah_p
								FROM penatausahaan.pembiayaan b
								WHERE b.tahun = a.tahun
									AND b.kodeurusan = a.kodeurusan
									AND b.kodesuburusan = a.kodesuburusan
									AND b.kodeorganisasi = a.kodeorganisasi
									AND b.kodeunit = a.kodeunit
									AND b.kodeakun = a.kodeakun
									AND b.kodekelompok = a.kodekelompok
									AND b.kodejenis = a.kodejenis
									AND b.kodeobjek = a.kodeobjek
									AND b.koderincianobjek = a.koderincianobjek
									AND b.kodesubrincianobjek = a.kodesubrincianobjek)
						else
							(SELECT b.jumlah_p
							FROM penatausahaan.belanja b
							WHERE b.tahun = a.tahun
								AND b.kodeurusan = a.kodeurusan
								AND b.kodesuburusan = a.kodesuburusan
								AND b.kodeorganisasi = a.kodeorganisasi
								AND b.kodeunit = a.kodeunit
								AND b.kodebidang = a.kodebidang
								AND b.kodeprogram = a.kodeprogram
								AND b.kodekegiatan = a.kodekegiatan
								AND b.kodesubkegiatan = a.kodesubkegiatan
								AND b.kodeakun = a.kodeakun
								AND b.kodekelompok = a.kodekelompok
								AND b.kodejenis = a.kodejenis
								AND b.kodeobjek = a.kodeobjek
								AND b.koderincianobjek = a.koderincianobjek
								AND b.kodesubrincianobjek = a.kodesubrincianobjek)
						end
					) as anggaran,
					a.jumlah as penerimaan
				FROM penatausahaan.sp2drincian a
				WHERE a.nosp2d = %s
					AND a.tahun = %s
					AND a.kodeurusan = %s
					AND a.kodesuburusan = %s
					AND a.kodeorganisasi = %s
					AND a.kodeunit = %s
					AND a.kodebidang = %s
					AND a.kodeprogram = %s
					AND a.kodekegiatan = %s
					AND a.kodesubkegiatan = %s
				ORDER BY a.kodeakun,
					a.kodekelompok,
					a.kodejenis,
					a.kodeobjek,
					a.koderincianobjek,
					a.kodesubrincianobjek
		""", cond_0)
		qb.result_many(data['rincian'])

	with querybuilder() as qb:
		qb.execute("""
			SELECT
		    '' AS kodebidang, 0 AS kodeprogram, 0 AS kodekegiatan, 0 AS kodesubkegiatan,
		    b.kodeakun, b.kodekelompok, b.kodejenis, b.kodeobjek, b.koderincianobjek, b.kodesubrincianobjek,
		    a.rekeningpotongan AS kode_rekening,
		    b.urai AS urai_rekening,
		    SUM(a.jumlah) AS penerimaan

		    FROM penatausahaan.sp2dpotongan a
		    JOIN master.master_rekening b on (b.tahun = a.tahun
		       AND (
		            b.kodeakun||'.'||b.kodekelompok||'.'||b.kodejenis||'.'||
		            LPAD(b.kodeobjek::text,2,'0')||'.'||LPAD(b.koderincianobjek::text,2,'0')
		            ||'.'||LPAD(b.kodesubrincianobjek::text,3,'0')
		        ) = a.rekeningpotongan
		    )

		    WHERE a.tahun = %s
		    AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s AND a.kodeunit = %s
		    AND a.nosp2d = %s

		    GROUP BY b.kodeakun, b.kodekelompok, b.kodejenis, b.kodeobjek, b.koderincianobjek, 
		    b.kodesubrincianobjek, a.rekeningpotongan, b.urai
		    ORDER BY a.rekeningpotongan
		""", cond_1)
		qb.result_many(data['potongan'])

	return JsonResponse(data, safe=False)
# 

def rincian_spj(rq):
	data = {'rincian': [], 'potongan': []}

	cond_0 = (
		rq.GET['no_bku'],
		rq.GET['tahun'],
		rq.GET['kodeurusan'],rq.GET['kodesuburusan'],rq.GET['kodeorganisasi'],rq.GET['kodeunit'],
		rq.GET['kodebidang'],rq.GET['kodeprogram'],rq.GET['kodekegiatan'],rq.GET['kodesubkegiatan'],
	)

	with querybuilder() as qb:
		qb.execute("""
			SELECT DISTINCT
			a.kodebidang,a.kodeprogram,a.kodekegiatan,a.kodesubkegiatan,
			a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek,a.kodesubrincianobjek,
			(
				a.kodeurusan||'.'||
				LPAD(a.kodesuburusan::text,2,'0')||'.'||
				a.kodeorganisasi||'.0.0-'|| 
				a.kodeakun||'.'||a.kodekelompok||'.'||a.kodejenis||'.'||
				LPAD(a.kodeobjek::text,2,'0')||'.'||LPAD(a.koderincianobjek::text,2,'0')
				||'.'||LPAD(a.kodesubrincianobjek::text,3,'0')
			) AS kode_rekening,
			(
				SELECT b.urai as urai_rekening FROM master.master_rekening b WHERE b.tahun = a.tahun
				AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis 
				AND b.kodeobjek = a.kodeobjek AND b.koderincianobjek = a.koderincianobjek
				AND b.kodesubrincianobjek = a.kodesubrincianobjek
			),

			a.jumlah_p AS anggaran,
			 b.penerimaan AS pengeluaran

			FROM (
					SELECT tahun, kodeurusan, kodesuburusan, kodeorganisasi, kodeunit, kodebidang, kodeprogram, kodekegiatan, kodesubkegiatan, kodeakun, kodekelompok, kodejenis, kodeobjek, koderincianobjek, kodesubrincianobjek, jumlah_p FROM penatausahaan.belanja
					UNION
					SELECT tahun, kodeurusan, kodesuburusan, kodeorganisasi, kodeunit, '5.02' as kodebidang, 0 as kodeprogram, '0.0' as kodekegiatan, 0 as kodesubkegiatan, kodeakun, kodekelompok, kodejenis, kodeobjek, koderincianobjek, kodesubrincianobjek, jumlah_p FROM penatausahaan.pembiayaan
					UNION
					SELECT tahun, kodeurusan, kodesuburusan, kodeorganisasi, kodeunit, '5.02' as kodebidang, 1 as kodeprogram, '0.0' as kodekegiatan, 0 as kodesubkegiatan, kodeakun, kodekelompok, kodejenis, kodeobjek, koderincianobjek, kodesubrincianobjek, jumlah_p FROM penatausahaan.pembiayaan
				) as a 
            JOIN 
            pertanggungjawaban.skpd_bkurincian b ON (
            	b.tahun = a.tahun
				AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan 
				AND b.kodeorganisasi = a.kodeorganisasi
				AND b.kodeunit = a.kodeunit
				AND b.kodebidang = a.kodebidang AND b.kodeprogram = a.kodeprogram 
				AND b.kodekegiatan = a.kodekegiatan AND b.kodesubkegiatan = a.kodesubkegiatan
				AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis 
				AND b.kodeobjek = a.kodeobjek AND b.koderincianobjek = a.koderincianobjek
				AND b.kodesubrincianobjek = a.kodesubrincianobjek
				AND b.no_bku = %s
            )
			WHERE a.tahun = %s
			AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s AND a.kodeunit = %s
			AND a.kodebidang = %s AND a.kodeprogram = %s AND a.kodekegiatan = %s AND a.kodesubkegiatan = %s

			order by a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek,a.kodesubrincianobjek
		""", cond_0)
		qb.result_many(data['rincian'])

	bkupotongan(rq, jenis_bku='SP2D', is_return=False, data=data['potongan'])
	for n in data['potongan']:
		n['pengeluaran'] = n['penerimaan']
		del n['penerimaan']

	return JsonResponse(data, safe=False)
# 


# ?!
def kegiatan_browse(rq):
	global angg_kegiatan_fields
	if angg_kegiatan_fields == None:
		with querybuilder() as qb:
			angg_kegiatan_fields = {}
			qb.tablecolumns('penatausahaan','kegiatan', angg_kegiatan_fields)

	data = []
	cond = {
		'tahun': rq.GET['tahun'],
		'kodeorganisasi': rq.GET['kodeorganisasi'],
		'kodekegiatan': rq.GET['kodekegiatan'],
	}

	for k in rq.GET:
		if k in angg_kegiatan_fields:
			cond[k] = rq.GET[k]

	with querybuilder('penatausahaan.kegiatan', **cond) as qb: qb.read().result_many(data)
	
	return JsonResponse(data, safe=False)
	pass
# 

def bkurincian(rq):

	data = {'rincian': [], 'potongan': [], 'entry': {}}
	try:
		no_bku = rq.GET['no_bku']
		jenis_bku = rq.GET['jenis_bku']
		cond = (
			no_bku,
			rq.GET['tahun'],
			rq.GET['kodeurusan'], rq.GET['kodesuburusan'], rq.GET['kodeorganisasi'], rq.GET['kodeunit'],
		)
	except Exception as err: return HttpResponseServerError('%s is unknown' % err, content_type='text/plain')
	
	with querybuilder() as qb:
		qb.execute("""
			SELECT
				a.kodebidang, a.kodeprogram, a.kodekegiatan, a.kodesubkegiatan,
				a.kodebidang||'.'||a.kodeprogram||'.'||a.kodekegiatan||'.'||a.kodesubkegiatan as kegiatan_kode,
				(
					CASE WHEN a.kodeakun = 6 THEN
						'PENGELUARAN PEMBIAYAAN'
					else
						(SELECT b.urai as kegiatan_urai FROM penatausahaan.kegiatan b WHERE b.tahun = a.tahun
						AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan 
						AND b.kodeorganisasi = a.kodeorganisasi
						AND b.kodeunit = a.kodeunit
						AND b.kodebidang = a.kodebidang AND b.kodeprogram = a.kodeprogram 
						AND b.kodekegiatan = a.kodekegiatan
						AND b.kodesubkegiatan = a.kodesubkegiatan)
					end

				)
				FROM pertanggungjawaban.skpd_bkurincian a WHERE a.tahun = %s
				AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s
				AND a.kodeunit = %s
				AND a.no_bku = %s
				AND a.kodebidang <> '' 
				AND a.isskpd = %s
		""", (
			rq.GET['tahun'],rq.GET['kodeurusan'], rq.GET['kodesuburusan'], rq.GET['kodeorganisasi'],
			rq.GET['kodeunit'],no_bku,isskpd,
		))
		qb.result_one(data['entry'])

	sekarang = 'pengeluaran';
	if re.search(sekarang_penerimaan_re, jenis_bku): sekarang = 'penerimaan'

	cond = (
		*cond,
		data['entry']['kodebidang'],
		data['entry']['kodeprogram'],
		data['entry']['kodekegiatan'],
		data['entry']['kodesubkegiatan'],
	)

	with querybuilder() as qb:
		qb.execute("""
			SELECT DISTINCT
			a.kodebidang,a.kodeprogram,a.kodekegiatan,a.kodesubkegiatan,
			a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek,a.kodesubrincianobjek,
			(
				a.kodeurusan||'.'||
				LPAD(a.kodesuburusan::text,2,'0')||'.'||
				a.kodeorganisasi||'.0.0-'||
				a.kodeakun||'.'||a.kodekelompok||'.'||a.kodejenis||'.'||
				LPAD(a.kodeobjek::text,2,'0')||'.'||LPAD(a.koderincianobjek::text,2,'0')
				||'.'||LPAD(a.kodesubrincianobjek::text,3,'0')
			) as kode_rekening,
			(
				SELECT b.urai as urai_rekening
				FROM master.master_rekening b WHERE b.tahun = a.tahun
				AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis 
				AND b.kodeobjek = a.kodeobjek AND b.koderincianobjek = a.koderincianobjek
				AND b.kodesubrincianobjek = a.kodesubrincianobjek
			),

			a.jumlah_p as anggaran,
			b.{}

			FROM (
					SELECT tahun, kodeurusan, kodesuburusan, kodeorganisasi, kodeunit, kodebidang, kodeprogram, kodekegiatan, kodesubkegiatan, kodeakun, kodekelompok, kodejenis, kodeobjek, koderincianobjek, kodesubrincianobjek, jumlah_p FROM penatausahaan.belanja
					UNION
					SELECT tahun, kodeurusan, kodesuburusan, kodeorganisasi, kodeunit, '5.02' as kodebidang, 0 as kodeprogram, '0.0' as kodekegiatan, 0 as kodesubkegiatan, kodeakun, kodekelompok, kodejenis, kodeobjek, koderincianobjek, kodesubrincianobjek, jumlah_p FROM penatausahaan.pembiayaan
					UNION
					SELECT tahun, kodeurusan, kodesuburusan, kodeorganisasi, kodeunit, '5.02' as kodebidang, 1 as kodeprogram, '0.0' as kodekegiatan, 0 as kodesubkegiatan, kodeakun, kodekelompok, kodejenis, kodeobjek, koderincianobjek, kodesubrincianobjek, jumlah_p FROM penatausahaan.pembiayaan
				) as a 
			JOIN pertanggungjawaban.skpd_bkurincian b ON (b.tahun = a.tahun
				AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan 
				AND b.kodeorganisasi = a.kodeorganisasi AND b.kodeunit = a.kodeunit
				AND b.kodebidang = a.kodebidang AND b.kodeprogram = a.kodeprogram AND b.kodekegiatan = a.kodekegiatan 
				AND b.kodesubkegiatan = a.kodesubkegiatan
				AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis 
				AND b.kodeobjek = a.kodeobjek AND b.koderincianobjek = a.koderincianobjek
				AND b.kodesubrincianobjek = a.kodesubrincianobjek
				AND b.no_bku = %s)

			WHERE a.tahun = %s
			AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s  AND a.kodeunit = %s
			AND a.kodebidang = %s AND a.kodeprogram = %s AND a.kodekegiatan = %s AND a.kodesubkegiatan = %s

			ORDER BY a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek,a.kodesubrincianobjek
		""".format(sekarang), cond)
		qb.result_many(data['rincian'])

	bkupotongan(rq, is_return=False, data=data['potongan'])

	return JsonResponse(data, safe=False)
# 

# OK
def bkupotongan(rq, jenis_bku=None, is_return=True, data=None):
	if data == None: data = []
	if jenis_bku == None: jenis_bku = rq.GET['jenis_bku']

	cond = (
		rq.GET['tahun'],
		rq.GET['kodeurusan'],
		rq.GET['kodesuburusan'],
		rq.GET['kodeorganisasi'],
		rq.GET['kodeunit'],
		rq.GET['no_bku'],
	)

	sekarang = 'pengeluaran';
	if re.search(sekarang_penerimaan_re, jenis_bku): sekarang = 'penerimaan'

	with querybuilder() as qb:
		qb.execute("""
			SELECT 
			a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek,a.kodesubrincianobjek,
			(
				a.kodeakun||'.'||a.kodekelompok||'.'||a.kodejenis||'.'||
				LPAD(a.kodeobjek::text,2,'0')||'.'||LPAD(a.koderincianobjek::text,2,'0')
				||'.'||LPAD(a.kodesubrincianobjek::text,3,'0')
			) AS kode_rekening,
			(
				SELECT b.urai AS urai_rekening FROM master.master_rekening b WHERE b.tahun = a.tahun
				AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis 
				and b.kodeobjek = a.kodeobjek and b.koderincianobjek = a.koderincianobjek
				and b.kodesubrincianobjek = a.kodesubrincianobjek
			),
			a.{0}

			FROM pertanggungjawaban.skpd_bkurincian a WHERE a.tahun = %s
			AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s
			AND a.kodeunit = %s AND a.kodeakun = 2
			AND a.no_bku = %s

			ORDER BY a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek,a.kodesubrincianobjek
		""".format(sekarang), cond)
		qb.result_many(data)

	if is_return: return JsonResponse(data, safe=False)
# 
