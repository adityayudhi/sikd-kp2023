from django import forms
from .models import MasterOrganisasi

class OrganisasiForm(form.ModelForm):
	class Meta:
		model = MasterOrganisasi
		fields = ('tahun','kodeurusan','kodesuburusan','kodeorganisasi','urai')