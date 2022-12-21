from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from ..config import *
from django.db import connection,connections
from sipkd.config import *

def settingquery(request):
	return render(request, 'konfig/settingquery.html')