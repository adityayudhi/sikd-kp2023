from django import template
from support.support_function import encrypt, decrypt

register = template.Library()

monthList = {
    '01': 'Januari',
    '02': 'Februari',
    '03': 'Maret',
    '04': 'April',
    '05': 'Mei',
    '06': 'Juni',
    '07': 'Juli',
    '08': 'Agustus',
    '09': 'September',
    '10': 'Oktober',
    '11': 'November',
    '12': 'Desember'
}
dayList = {
    'Sun' : 'Minggu',
    'Mon' : 'Senin',
    'Tue' : 'Selasa',
    'Wed' : 'Rabu',
    'Thu' : 'Kamis',
    'Fri' : 'Jumat',
    'Sat' : 'Sabtu'
}

def to_tgl_indo_with_time(value):
	tgl__ = ''
	value = value.strftime("%d-%m-%Y %H:%M:%S")
	# 2021-04-12 08:00:00
	try:
		tgl = value.split(' ')[0]
		waktu = value.split(' ')[1]
		bulan = monthList[tgl.split('-')[1]]
		tgl__ = '{} {} {} {}'.format(tgl.split('-')[0],bulan,tgl.split('-')[2],waktu)
	except Exception as e:
		print(e)

	return tgl__

def to_tgl_indo_without_time(value):
    tgl__ = ''
    value = value.strftime("%d-%m-%Y %H:%M:%S")
    # 2021-04-12 08:00:00
    try:
        tgl = value.split(' ')[0]
        bulan = monthList[tgl.split('-')[1]]
        tgl__ = '{} {} {}'.format(tgl.split('-')[0],bulan,tgl.split('-')[2])
    except Exception as e:
        print(e)

    return tgl__

def add_by_one(value):
    return int(value)+1

def get_filename(value):
    return value.split(' - ')[1]

import re

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext
    
def format_duit_spm(value):
    duit = str(f"{value:,}").split('.')
    return f"{duit[0].replace(',', '.')},{duit[1]}"

register.filter('to_tgl_indo_with_time', to_tgl_indo_with_time)
register.filter('to_tgl_indo_without_time', to_tgl_indo_without_time)
register.filter('format_duit_spm', format_duit_spm)

