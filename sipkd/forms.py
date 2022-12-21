from django import forms
from .models import *

class LocationChoiceField(forms.form)
	
	location = forms.ModelChoiceField(
		queryset=masterjabatan.objects.values_list("isspkd", flat=True).distinct(),
		)