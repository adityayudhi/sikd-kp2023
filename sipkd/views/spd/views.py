from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from django.contrib import messages
from support.support_sipkd import *

import json

def spdbtl(request):
	return render(request, 'spd/spdbtl.html')

def spdbl(request):
	return render(request, 'spd/spdbl.html')

def pengeluaranpembiayaan(request):
	return render(request, 'spd/pengeluaranpembiayaan.html')