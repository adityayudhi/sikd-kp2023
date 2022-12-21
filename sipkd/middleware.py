from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.db import connection,connections
from sipkd.config import *
import datetime
from sipkd.config import *

def cek_user(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        response = get_response(request)
        if request.path == '/':
            return HttpResponseRedirect(reverse('sipkd:index'))
        else:
            if not request.session.get('sipkd_username','') and request.path != '/sipkd/login/':
                return HttpResponseRedirect(reverse('sipkd:login'))
            else:
                now = datetime.datetime.now().strftime('%H:%M:%S')
                last_activity = request.session.get('sipkd_last_login_timestamp','00:00:00')
                # for x in range(len(connection.queries)):
                #     if 'update' in connection.queries[x]['sql']:
                #         print(connection.queries[x]['sql'])

                pecah1 = now.split(':')
                pecah2 = last_activity.split(':')

                waktu_sekarang = int(pecah1[1]) + 60*int(pecah1[0])
                waktu_terakhir = int(pecah2[1]) + 60*int(pecah2[0])

                if(request.session.get('sipkd_username')):
                    menus = ['/sipkd/','/sipkd/index/','/sipkd/logout/']
                    arank = set_menu(request)
                    for mn in arank["anak1"]:
                        if(mn["link_page"]!="#"):
                            menus.append(mn["link"]+'/')
                        else:
                            for mx in arank["anak2"]:
                                menus.extend(mx["link"]+'/')

                    if(request.path == '/sipkd/login/'):
                        return HttpResponseRedirect(reverse('sipkd:index'))
                    # else:
                    #     x = menus.count(request.path)
                    #     if(x == 0):
                    #         return HttpResponseRedirect(reverse('sipkd:index'))
                    
                    # return HttpResponse(urlpatterns)


                selisih = ((waktu_sekarang-waktu_terakhir)**2)**0.5        	
                if selisih>=100 and request.path != '/sipkd/login/':        		
                    request.session.flush()
                    messages.success(request, "Sesi anda sudah habis, silahkan Login kembali.")
                    return HttpResponseRedirect(reverse('sipkd:login'))
                else:
                    request.session['sipkd_last_login_timestamp'] = now        
                    return response

    return middleware