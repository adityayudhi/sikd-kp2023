from django.db import models
from django.db import connection

class Pengguna(models.Model):
    tahun = models.CharField(max_length=4)
    uname = models.CharField(max_length=50)
    pwd = models.CharField(max_length=50, blank=True, null=True)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=4)
    hakakses = models.CharField(max_length=16)
    is_bendahara_pembantu = models.CharField(max_length=1)
    kegiatan = models.CharField(max_length=1000, blank=True, null=True)
    nama_bendahara_pembantu = models.CharField(max_length=255, blank=True, null=True)
    organisasi = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.uname

      
    class Meta:
        managed = False
        db_table = 'pengguna'


class Masterjabatan(models.Model):
    jenissistem = models.IntegerField(primary_key=True)
    isskpd = models.IntegerField()
    urut = models.IntegerField()
    urai = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'masterjabatan'
        unique_together = (('jenissistem', 'isskpd', 'urut'),)

    def __str__(self):
        return self.isskpd