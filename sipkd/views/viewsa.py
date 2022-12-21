from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from .config import *
from django.db import connection,connections
from django.contrib import messages
from sipkd.config import *
from django.contrib.auth import update_session_auth_hash
import datetime, pprint


def error_404_view(request, exception):
	data = {"name": "ThePythonDjango.com"}
	return render(request, 'base/error_404.html', data)

def index(request):	
	return render(request, 'base/main.html')

def login(request):
	with connection.cursor() as cursor:
		cursor.execute("SELECT tahun FROM master.settingtahun WHERE aktif = 3 ORDER BY tahun DESC")
		setting_tahun = dictfetchall(cursor)
	data = {'setting_tahun': setting_tahun}
	return render(request, 'base/login.html',data)

def proseslogin(request):

	if request.method == 'POST':
		tahun = request.POST.get('listtahun')
		user_name = request.POST.get('username').upper()
		pwd = request.POST.get('password').upper()
		enkrip_pass = encrypt(pwd);

		with connections[tahun].cursor() as cursor:
			cursor.execute("SELECT * FROM penatausahaan.fc_sipkd_do_login (%s,%s,%s)",[tahun.strip(),user_name.strip(),enkrip_pass.strip()])
			setting_pengguna = dictfetchall(cursor)
		data = {'setting_pengguna': setting_pengguna}
		
		for result in setting_pengguna:
			username = result['uname']
			password = result['pwd']

			if ((user_name.strip() == username) and (enkrip_pass.strip() == password)):				
				request.session['sipkd_tahun'] = result['tahun']
				request.session['sipkd_username'] = result['uname']
				request.session['sipkd_hakakses'] = result['hakakses']
				request.session['sipkd_modulelist'] = result['modulelist']
				request.session['sipkd_listpilih'] = result['listpilih']
				request.session['sipkd_listsub'] = result['listsub']
				request.session['sipkd_is_bendahara_pembantu'] = result['is_bendahara_pembantu']
				request.session['sipkd_perubahan'] = result['perubahan']
				request.session['sipkd_perubahananggaran'] = result['perubahananggaran']
				request.session['sipkd_listorganisasi'] = str(result['kodeurusan'])+'.'+str(result['kodesuburusan'])+'.'+str(result['kodeorganisasi'])+'.'+str(result['kodeunit'])
				request.session['sipkd_last_login_timestamp'] = datetime.datetime.now().strftime('%H:%M:%S')
				# session expire in 5 minutes.
				# request.session.set_expiry(300) 
				# redirect success
				messages.success(request, "Selamat Datang "+result['uname']+", Anda berhasil login.")
				return redirect('sipkd:index')

		# redirect gagal
		messages.success(request, "Login Anda Gagal !!!")
		return redirect('sipkd:login')

	else:
		return redirect('sipkd:login')

def logout(request):
	request.session.flush()
	messages.success(request, "Anda telah berhasil Log out.")
	return redirect('sipkd:index')