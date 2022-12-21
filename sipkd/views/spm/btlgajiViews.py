from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from django.contrib import messages
from support.support_sipkd import *

import json

def btl_gaji(request):
	return render(request, 'spm/btl_gaji.html')
