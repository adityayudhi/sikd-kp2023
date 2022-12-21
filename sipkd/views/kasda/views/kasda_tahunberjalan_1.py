from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render, redirect

def index(request):
	return render(request, 'kasda/kasda_tahunberjalan.html')