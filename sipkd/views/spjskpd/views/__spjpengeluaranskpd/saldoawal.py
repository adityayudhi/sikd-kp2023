from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseServerError
from .. import main
from ...anov import *

isskpd = 0

@require_POST
def save(request):
	sess = dict(request.session.items())
	post = {k:v for k,v in request.POST.items()}

	if '__type__' not in post: return HttpResponseServerError(None, content_type='text/plain')
	__type__ = int(post['__type__']);

	data_default = {
		'isskpd': isskpd,
		'tahun': sess['sipkd_tahun'],
		'uname': sess['sipkd_username'],
		'is_bendahara_pembantu': sess['sipkd_is_bendahara_pembantu'],
	}
	data = {}
	for k,v in post.items():
		if k in main.bku_fields:
			data[k] = v
	for k,v in data_default.items():
		if k in main.bku_fields: # and k not in data:
			data[k] = v

	if __type__ == 0:
		with querybuilder('pertanggungjawaban.skpd_bku', **data) as qb:
			try: qb.create()
			except Exception as err: return HttpResponseServerError(err, content_type='text/plain')

	elif __type__ == 1:
		with querybuilder('pertanggungjawaban.skpd_bku', *main.bku_primarykeys, **data) as qb:
			try: qb.update()
			except Exception as err: return HttpResponseServerError(err, content_type='text/plain')

	else: return HttpResponseServerError('__type__ ?? "%s"' % __type__, content_type='text/plain')

	# return HttpResponse('ok', content_type='text/plain')
	return JsonResponse({
		'data': data,
		'sess': sess,
		'post': post,
	}, safe=False)
# fed
