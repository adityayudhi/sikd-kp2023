import datetime
from django.utils.timezone import utc


now = datetime.datetime.now()
hari = now.strftime("%a")
tanggal = now.strftime("%d")
bulan = now.strftime("%b")
tahun = now.strftime("%Y")
dayList = {
	'Sun' : 'Minggu',
	'Mon' : 'Senin',
	'Tue' : 'Selasa',
	'Wed' : 'Rabu',
	'Thu' : 'Kamis',
	'Fri' : 'Jumat',
	'Sat' : 'Sabtu'
}

monthList = {
	'Jan': 'Januari',
	'Feb': 'Februari',
	'Mar': 'Maret',
	'Apr': 'April',
	'May': 'Mei',
	'Jun': 'Juni',
	'Jul': 'Juli',
	'Aug': 'Agustus',
	'Sep': 'September',
	'Oct': 'Oktober',
	'Nov': 'November',
	'Dec': 'Desember'
}
tgl_lengkap = dayList[hari]+', '+tanggal+' '+monthList[bulan]+' '+tahun

# user = 'admin'
# password = '4dm1nsipkd'
