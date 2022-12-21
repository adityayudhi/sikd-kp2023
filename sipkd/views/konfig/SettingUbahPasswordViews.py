from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.db import connection,connections
from sipkd.config import *
from django.contrib import messages

def ubahpassword(request):
	return render(request, 'konfig/ubahpassword.html')

def ubahpwd(request):
	uname = request.session.get('sipkd_username').upper()
	view_uname = '' 
	view_password = ''
	hasil = ''
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT uname, pwd FROM penatausahaan.pengguna WHERE uname = %s",[uname])
		hasil = dictfetchall(cursor)
		for hasilnya in hasil:
				view_uname = hasilnya['uname']
				view_password = decrypt(hasilnya['pwd'])
		
	data = {
		'view_uname':view_uname,
		'view_pwd':view_password
	}
	return render(request,'konfig/ubahpassword.html',data)

def save_ubahpwd(request):
	pesan = ''
	view_uname = ''
	view_password = ''
	close=''
	hasil = ''
	if request.method == 'POST':
		uname = request.POST.get('uname', None)
		pwd_lama = request.POST.get('pwd_lama', None).upper()
		pwd_baru = encrypt(request.POST.get('pwd_baru', None).upper())

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT uname, pwd FROM penatausahaan.pengguna WHERE uname = %s",[uname])
			hasil = dictfetchall(cursor)
			for hasilnya in hasil:
					view_uname = hasilnya['uname']
					view_password = decrypt(hasilnya['pwd'])

		if pwd_lama!=view_password:
			pesan = 'Password Lama Tidak Cocok'
		else:
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("UPDATE penatausahaan.pengguna SET pwd = %s WHERE uname=%s",[pwd_baru,uname])
				pesan = 'Password Berhasil Diganti'
				close = 'yes'
			messages.success(request, "Data berhasil Diubah!")
	data = {
        'pesan': pesan,
        'close': close
    }
	return JsonResponse(data)
