# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AdvisSp2D(models.Model):
    tahun = models.ForeignKey('Settingtahun', models.DO_NOTHING, db_column='tahun', primary_key=True)
    noadvis = models.CharField(max_length=35)
    nosp2d = models.CharField(max_length=100)
    tanggal = models.DateTimeField()
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)
    pengesah = models.CharField(max_length=50, blank=True, null=True)
    nama = models.CharField(max_length=100, blank=True, null=True)
    nip = models.CharField(max_length=50, blank=True, null=True)
    pangkat = models.CharField(max_length=50, blank=True, null=True)
    cetak = models.CharField(max_length=1)
    urutan = models.IntegerField()
    sumberdana = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'advis_sp2d'
        unique_together = (('tahun', 'noadvis', 'nosp2d'),)


class AkrualBukuJurnal(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    isskpd = models.SmallIntegerField()
    noref = models.CharField(max_length=15)
    nobukti = models.CharField(max_length=50)
    jenisjurnal = models.SmallIntegerField()
    keterangan = models.CharField(max_length=1000)
    posting = models.SmallIntegerField()
    tanggalbukti = models.DateTimeField()
    username = models.CharField(max_length=50)
    no_bku = models.IntegerField(blank=True, null=True)
    ispihakketiga = models.IntegerField()
    jenis_transaksi = models.CharField(max_length=20, blank=True, null=True)
    jenissp2d = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'akrual_buku_jurnal'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'isskpd', 'noref'),)


class AkrualJenisJurnal(models.Model):
    id = models.IntegerField(primary_key=True)
    isskpd = models.IntegerField()
    uraian = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'akrual_jenis_jurnal'
        unique_together = (('id', 'isskpd'),)


class AkrualJurnalRincian(models.Model):
    tahun = models.ForeignKey(AkrualBukuJurnal, models.DO_NOTHING, db_column='tahun', primary_key=True)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    isskpd = models.SmallIntegerField()
    noref = models.CharField(max_length=15)
    kodebidang = models.CharField(max_length=5)
    kodeprogram = models.IntegerField()
    kodekegiatan = models.IntegerField()
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    urut = models.IntegerField()
    debet = models.DecimalField(max_digits=15, decimal_places=2)
    kredit = models.DecimalField(max_digits=15, decimal_places=2)
    posting = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'akrual_jurnal_rincian'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'isskpd', 'noref', 'kodebidang', 'kodeprogram', 'kodekegiatan', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek', 'urut'),)


class AkrualMasterLpe(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kode = models.IntegerField()
    uraian = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'akrual_master_lpe'
        unique_together = (('tahun', 'kode'),)


class AkrualMasterRekening(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    urai = models.CharField(max_length=255, blank=True, null=True)
    keterangan = models.CharField(max_length=255, blank=True, null=True)
    last_update = models.DateTimeField()
    pengguna = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'akrual_master_rekening'
        unique_together = (('tahun', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek'),)


class AnggBelanja(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    kodebidang = models.CharField(max_length=5)
    kodeprogram = models.IntegerField()
    kodekegiatan = models.IntegerField()
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    volume = models.CharField(max_length=30)
    satuan = models.CharField(max_length=30)
    harga = models.DecimalField(max_digits=15, decimal_places=2)
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)
    triwul1 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul2 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul3 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul4 = models.DecimalField(max_digits=15, decimal_places=2)
    volume_p = models.CharField(max_length=30)
    satuan_p = models.CharField(max_length=30)
    harga_p = models.DecimalField(max_digits=15, decimal_places=2)
    jumlah_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul1_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul2_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul3_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul4_p = models.DecimalField(max_digits=15, decimal_places=2)
    jumlah_tahun_depan = models.DecimalField(max_digits=15, decimal_places=2)
    sumberdana = models.IntegerField(blank=True, null=True)
    sumberdana_p = models.IntegerField(blank=True, null=True)
    kodekepentingan = models.IntegerField(blank=True, null=True)
    l_ra = models.DecimalField(max_digits=15, decimal_places=2)
    l_r1 = models.DecimalField(max_digits=15, decimal_places=2)
    l_r2 = models.DecimalField(max_digits=15, decimal_places=2)
    l_rea = models.DecimalField(max_digits=15, decimal_places=2)
    l_re1 = models.DecimalField(max_digits=15, decimal_places=2)
    l_re2 = models.DecimalField(max_digits=15, decimal_places=2)
    pengguna = models.CharField(max_length=50, blank=True, null=True)
    last_update = models.DateTimeField()
    beban = models.CharField(max_length=8, blank=True, null=True)
    jan = models.DecimalField(max_digits=15, decimal_places=2)
    feb = models.DecimalField(max_digits=15, decimal_places=2)
    maret = models.DecimalField(max_digits=15, decimal_places=2)
    april = models.DecimalField(max_digits=15, decimal_places=2)
    mey = models.DecimalField(max_digits=15, decimal_places=2)
    jun = models.DecimalField(max_digits=15, decimal_places=2)
    jul = models.DecimalField(max_digits=15, decimal_places=2)
    agust = models.DecimalField(max_digits=15, decimal_places=2)
    sept = models.DecimalField(max_digits=15, decimal_places=2)
    okto = models.DecimalField(max_digits=15, decimal_places=2)
    nov = models.DecimalField(max_digits=15, decimal_places=2)
    des = models.DecimalField(max_digits=15, decimal_places=2)
    keterangan = models.CharField(max_length=255, blank=True, null=True)
    lock = models.IntegerField()
    lock_p = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'angg_belanja'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'kodebidang', 'kodeprogram', 'kodekegiatan', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek'),)


class AnggBelanjasub1(models.Model):
    tahun = models.ForeignKey(AnggBelanja, models.DO_NOTHING, db_column='tahun', primary_key=True)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    kodebidang = models.CharField(max_length=5)
    kodeprogram = models.IntegerField()
    kodekegiatan = models.IntegerField()
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    kodesub1 = models.IntegerField()
    volume = models.CharField(max_length=30)
    satuan = models.CharField(max_length=30)
    harga = models.DecimalField(max_digits=15, decimal_places=2)
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)
    triwul1 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul2 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul3 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul4 = models.DecimalField(max_digits=15, decimal_places=2)
    volume_p = models.CharField(max_length=30)
    satuan_p = models.CharField(max_length=30)
    harga_p = models.DecimalField(max_digits=15, decimal_places=2)
    jumlah_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul1_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul2_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul3_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul4_p = models.DecimalField(max_digits=15, decimal_places=2)
    urai = models.CharField(max_length=1000, blank=True, null=True)
    jumlah_tahun_depan = models.DecimalField(max_digits=15, decimal_places=2)
    l_ra = models.DecimalField(max_digits=15, decimal_places=2)
    l_r1 = models.DecimalField(max_digits=15, decimal_places=2)
    l_r2 = models.DecimalField(max_digits=15, decimal_places=2)
    l_rea = models.DecimalField(max_digits=15, decimal_places=2)
    l_re1 = models.DecimalField(max_digits=15, decimal_places=2)
    l_re2 = models.DecimalField(max_digits=15, decimal_places=2)
    keterangan = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'angg_belanjasub1'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'kodebidang', 'kodeprogram', 'kodekegiatan', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek', 'kodesub1'),)


class AnggBelanjasub2(models.Model):
    tahun = models.ForeignKey(AnggBelanjasub1, models.DO_NOTHING, db_column='tahun', primary_key=True)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    kodebidang = models.CharField(max_length=5)
    kodeprogram = models.IntegerField()
    kodekegiatan = models.IntegerField()
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    kodesub1 = models.IntegerField()
    kodesub2 = models.IntegerField()
    volume = models.CharField(max_length=30)
    satuan = models.CharField(max_length=30)
    harga = models.DecimalField(max_digits=15, decimal_places=2)
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)
    triwul1 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul2 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul3 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul4 = models.DecimalField(max_digits=15, decimal_places=2)
    volume_p = models.CharField(max_length=30)
    satuan_p = models.CharField(max_length=30)
    harga_p = models.DecimalField(max_digits=15, decimal_places=2)
    jumlah_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul1_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul2_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul3_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul4_p = models.DecimalField(max_digits=15, decimal_places=2)
    urai = models.CharField(max_length=255)
    jumlah_tahun_depan = models.DecimalField(max_digits=15, decimal_places=2)
    l_ra = models.DecimalField(max_digits=15, decimal_places=2)
    l_r1 = models.DecimalField(max_digits=15, decimal_places=2)
    l_r2 = models.DecimalField(max_digits=15, decimal_places=2)
    l_rea = models.DecimalField(max_digits=15, decimal_places=2)
    l_re1 = models.DecimalField(max_digits=15, decimal_places=2)
    l_re2 = models.DecimalField(max_digits=15, decimal_places=2)
    keterangan = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'angg_belanjasub2'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'kodebidang', 'kodeprogram', 'kodekegiatan', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek', 'kodesub1', 'kodesub2'),)


class AnggBelanjasub3(models.Model):
    tahun = models.ForeignKey(AnggBelanjasub2, models.DO_NOTHING, db_column='tahun', primary_key=True)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    kodebidang = models.CharField(max_length=5)
    kodeprogram = models.IntegerField()
    kodekegiatan = models.IntegerField()
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    kodesub1 = models.IntegerField()
    kodesub2 = models.IntegerField()
    kodesub3 = models.IntegerField()
    volume = models.CharField(max_length=30)
    satuan = models.CharField(max_length=30)
    harga = models.DecimalField(max_digits=15, decimal_places=2)
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)
    triwul1 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul2 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul3 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul4 = models.DecimalField(max_digits=15, decimal_places=2)
    volume_p = models.CharField(max_length=30)
    satuan_p = models.CharField(max_length=30)
    urai = models.CharField(max_length=1000)
    harga_p = models.DecimalField(max_digits=15, decimal_places=2)
    jumlah_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul1_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul2_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul3_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul4_p = models.DecimalField(max_digits=15, decimal_places=2)
    jumlah_tahun_depan = models.DecimalField(max_digits=15, decimal_places=2)
    l_ra = models.DecimalField(max_digits=15, decimal_places=2)
    l_r1 = models.DecimalField(max_digits=15, decimal_places=2)
    l_r2 = models.DecimalField(max_digits=15, decimal_places=2)
    l_rea = models.DecimalField(max_digits=15, decimal_places=2)
    l_re1 = models.DecimalField(max_digits=15, decimal_places=2)
    l_re2 = models.DecimalField(max_digits=15, decimal_places=2)
    keterangan = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'angg_belanjasub3'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'kodebidang', 'kodeprogram', 'kodekegiatan', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek', 'kodesub1', 'kodesub2', 'kodesub3'),)


class AnggBidangOrganisasi(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    kodebidang = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'angg_bidang_organisasi'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'kodebidang'),)


class AnggDaftarPenyertaanModal(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    id = models.IntegerField()
    tahunpenyertaan = models.CharField(max_length=4)
    pihakketiga = models.CharField(max_length=255, blank=True, null=True)
    dasarhukum = models.CharField(max_length=255, blank=True, null=True)
    bentukpenyertaan = models.CharField(max_length=100, blank=True, null=True)
    jumlahpenyertaan = models.DecimalField(max_digits=15, decimal_places=2)
    jumlahpenyertaann1 = models.DecimalField(max_digits=15, decimal_places=2)
    jumlahn = models.DecimalField(max_digits=15, decimal_places=2)
    hasil = models.DecimalField(max_digits=15, decimal_places=2)
    jmlterima = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'angg_daftar_penyertaan_modal'
        unique_together = (('tahun', 'id'),)


class AnggDaftarPinjaman(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    id = models.IntegerField()
    dasarhukum = models.CharField(max_length=255, blank=True, null=True)
    tanggalpinjaman = models.DateTimeField()
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)
    jangkawaktu = models.IntegerField()
    bunga = models.DecimalField(max_digits=15, decimal_places=2)
    tujuan = models.CharField(max_length=255, blank=True, null=True)
    bayarpokok = models.DecimalField(max_digits=15, decimal_places=2)
    bayarbunga = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'angg_daftar_pinjaman'
        unique_together = (('tahun', 'id'),)


class AnggDaftarPiutang(models.Model):
    id = models.IntegerField()
    tahun = models.CharField(primary_key=True, max_length=4)
    tahunpengakuan = models.CharField(max_length=4)
    uraian = models.CharField(max_length=255, blank=True, null=True)
    saldotahunn2 = models.DecimalField(max_digits=15, decimal_places=2)
    penambahann1 = models.DecimalField(max_digits=15, decimal_places=2)
    pengurangann1 = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'angg_daftar_piutang'
        unique_together = (('tahun', 'id'),)


class AnggDaftarperkiraanAsetLain(models.Model):
    id = models.IntegerField()
    tahun = models.CharField(primary_key=True, max_length=4)
    jenisasettetap = models.CharField(max_length=255, blank=True, null=True)
    saldotahunn2 = models.DecimalField(max_digits=15, decimal_places=2)
    penambahann1 = models.DecimalField(max_digits=15, decimal_places=2)
    pengurangann1 = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'angg_daftarperkiraan_aset_lain'
        unique_together = (('tahun', 'id'),)


class AnggDaftarperkiraanAsetTetap(models.Model):
    id = models.IntegerField()
    tahun = models.CharField(primary_key=True, max_length=4)
    saldotahunn2 = models.DecimalField(max_digits=15, decimal_places=2)
    penambahann1 = models.DecimalField(max_digits=15, decimal_places=2)
    pengurangann1 = models.DecimalField(max_digits=15, decimal_places=2)
    jenisasettetap = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'angg_daftarperkiraan_aset_tetap'
        unique_together = (('tahun', 'id'),)


class AnggDanaCadangan(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    id = models.IntegerField()
    tujuan = models.CharField(max_length=255)
    dasarhukum = models.CharField(max_length=255)
    jmlrencana = models.DecimalField(max_digits=15, decimal_places=2)
    saldoawal = models.DecimalField(max_digits=15, decimal_places=2)
    transferdarikasda = models.DecimalField(max_digits=15, decimal_places=2)
    transferkekasda = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'angg_dana_cadangan'
        unique_together = (('tahun', 'id'),)


class AnggHakakses(models.Model):
    hakakses = models.CharField(max_length=16)
    modulelist = models.CharField(max_length=1000)
    listpilih = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'angg_hakakses'


class AnggKegiatan(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    kodebidang = models.CharField(max_length=5)
    kodeprogram = models.IntegerField()
    kodekegiatan = models.IntegerField()
    urai = models.CharField(max_length=255)
    pagu = models.DecimalField(max_digits=15, decimal_places=2)
    tahunlalu = models.DecimalField(max_digits=15, decimal_places=2)
    tahundepan = models.DecimalField(max_digits=15, decimal_places=2)
    barulanjutan = models.IntegerField()
    asalkegiatan = models.CharField(max_length=1)
    persen_target = models.FloatField()
    lokasi = models.CharField(max_length=255)
    waktupelaksanaan = models.CharField(max_length=255)
    pagu_p = models.DecimalField(max_digits=15, decimal_places=2)
    persen_target_p = models.FloatField()
    lokasi_p = models.CharField(max_length=255)
    waktupelaksanaan_p = models.CharField(max_length=255)
    latarblk_perubahan = models.CharField(max_length=255, blank=True, null=True)
    l_ta_tahun = models.CharField(max_length=4, blank=True, null=True)
    l_ta_dppa = models.DecimalField(max_digits=15, decimal_places=2)
    l_ta_real = models.DecimalField(max_digits=15, decimal_places=2)
    l_ta_saldo = models.DecimalField(max_digits=15, decimal_places=2)
    l_ta_ket = models.CharField(max_length=1000)
    l_t1_tahun = models.CharField(max_length=4, blank=True, null=True)
    l_t1_dppa = models.DecimalField(max_digits=15, decimal_places=2)
    l_t1_real = models.DecimalField(max_digits=15, decimal_places=2)
    l_t1_saldo = models.DecimalField(max_digits=15, decimal_places=2)
    l_t1_ket = models.CharField(max_length=1000)
    l_t2_tahun = models.CharField(max_length=4, blank=True, null=True)
    l_t2_dppa = models.DecimalField(max_digits=15, decimal_places=2)
    l_t2_real = models.DecimalField(max_digits=15, decimal_places=2)
    l_t2_saldo = models.DecimalField(max_digits=15, decimal_places=2)
    l_t2_ket = models.CharField(max_length=1000)
    sasaran_program = models.CharField(max_length=255, blank=True, null=True)
    sasaran = models.CharField(max_length=1000)
    tolok_capaian = models.CharField(max_length=1000)
    tolok_masukan = models.CharField(max_length=1000)
    tolok_keluaran = models.CharField(max_length=1000)
    tolok_hasil = models.CharField(max_length=1000)
    target_capaian = models.CharField(max_length=1000)
    target_masukan = models.CharField(max_length=1000)
    target_keluaran = models.CharField(max_length=1000)
    target_hasil = models.CharField(max_length=1000)
    tolok_capaian_p = models.CharField(max_length=1000)
    tolok_masukan_p = models.CharField(max_length=1000)
    tolok_keluaran_p = models.CharField(max_length=1000)
    tolok_hasil_p = models.CharField(max_length=1000)
    target_capaian_p = models.CharField(max_length=1000)
    target_masukan_p = models.CharField(max_length=1000)
    target_keluaran_p = models.CharField(max_length=1000)
    target_hasil_p = models.CharField(max_length=1000)
    pengguna = models.CharField(max_length=50, blank=True, null=True)
    last_update = models.DateTimeField()
    sumberdana = models.CharField(max_length=50)
    sumberdana_p = models.CharField(max_length=50)
    lock = models.IntegerField()
    lock_p = models.IntegerField()
    prinsip1 = models.IntegerField(blank=True, null=True)
    prinsip2 = models.IntegerField(blank=True, null=True)
    prinsip3 = models.IntegerField(blank=True, null=True)
    prinsip4 = models.IntegerField(blank=True, null=True)
    prinsip1_p = models.IntegerField(blank=True, null=True)
    prinsip2_p = models.IntegerField(blank=True, null=True)
    prinsip3_p = models.IntegerField(blank=True, null=True)
    prinsip4_p = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'angg_kegiatan'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'kodebidang', 'kodeprogram', 'kodekegiatan'),)


class AnggMasterPrinsip(models.Model):
    id = models.IntegerField(primary_key=True)
    uraian = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'angg_master_prinsip'


class AnggPembiayaan(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    volume = models.CharField(max_length=30)
    satuan = models.CharField(max_length=30)
    harga = models.DecimalField(max_digits=15, decimal_places=2)
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)
    triwul1 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul2 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul3 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul4 = models.DecimalField(max_digits=15, decimal_places=2)
    keterangan = models.CharField(max_length=255)
    volume_p = models.CharField(max_length=30)
    satuan_p = models.CharField(max_length=30)
    harga_p = models.DecimalField(max_digits=15, decimal_places=2)
    jumlah_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul1_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul2_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul3_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul4_p = models.DecimalField(max_digits=15, decimal_places=2)
    pengguna = models.CharField(max_length=50, blank=True, null=True)
    last_update = models.DateTimeField()
    jan = models.DecimalField(max_digits=15, decimal_places=2)
    feb = models.DecimalField(max_digits=15, decimal_places=2)
    maret = models.DecimalField(max_digits=15, decimal_places=2)
    april = models.DecimalField(max_digits=15, decimal_places=2)
    mey = models.DecimalField(max_digits=15, decimal_places=2)
    jun = models.DecimalField(max_digits=15, decimal_places=2)
    jul = models.DecimalField(max_digits=15, decimal_places=2)
    agust = models.DecimalField(max_digits=15, decimal_places=2)
    sept = models.DecimalField(max_digits=15, decimal_places=2)
    okto = models.DecimalField(max_digits=15, decimal_places=2)
    nov = models.DecimalField(max_digits=15, decimal_places=2)
    des = models.DecimalField(max_digits=15, decimal_places=2)
    lock = models.IntegerField()
    lock_p = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'angg_pembiayaan'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek'),)


class AnggPembiayaansub1(models.Model):
    tahun = models.ForeignKey(AnggPembiayaan, models.DO_NOTHING, db_column='tahun', primary_key=True)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    kodesub1 = models.IntegerField()
    volume = models.CharField(max_length=30)
    satuan = models.CharField(max_length=30)
    harga = models.DecimalField(max_digits=15, decimal_places=2)
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)
    triwul1 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul2 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul3 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul4 = models.DecimalField(max_digits=15, decimal_places=2)
    keterangan = models.CharField(max_length=255)
    volume_p = models.CharField(max_length=30)
    satuan_p = models.CharField(max_length=30)
    harga_p = models.DecimalField(max_digits=15, decimal_places=2)
    jumlah_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul1_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul2_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul3_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul4_p = models.DecimalField(max_digits=15, decimal_places=2)
    urai = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'angg_pembiayaansub1'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek', 'kodesub1'),)


class AnggPembiayaansub2(models.Model):
    tahun = models.ForeignKey(AnggPembiayaansub1, models.DO_NOTHING, db_column='tahun', primary_key=True)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    kodesub1 = models.IntegerField()
    kodesub2 = models.IntegerField()
    volume = models.CharField(max_length=30)
    satuan = models.CharField(max_length=30)
    harga = models.DecimalField(max_digits=15, decimal_places=2)
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)
    triwul1 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul2 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul3 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul4 = models.DecimalField(max_digits=15, decimal_places=2)
    keterangan = models.CharField(max_length=255)
    volume_p = models.CharField(max_length=30)
    satuan_p = models.CharField(max_length=30)
    harga_p = models.DecimalField(max_digits=15, decimal_places=2)
    jumlah_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul1_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul2_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul3_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul4_p = models.DecimalField(max_digits=15, decimal_places=2)
    urai = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'angg_pembiayaansub2'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek', 'kodesub1', 'kodesub2'),)


class AnggPembiayaansub3(models.Model):
    tahun = models.ForeignKey(AnggPembiayaansub2, models.DO_NOTHING, db_column='tahun', primary_key=True)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    kodesub1 = models.IntegerField()
    kodesub2 = models.IntegerField()
    kodesub3 = models.IntegerField()
    volume = models.CharField(max_length=30)
    satuan = models.CharField(max_length=30)
    harga = models.DecimalField(max_digits=15, decimal_places=2)
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)
    triwul1 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul2 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul3 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul4 = models.DecimalField(max_digits=15, decimal_places=2)
    keterangan = models.CharField(max_length=255)
    volume_p = models.CharField(max_length=30)
    satuan_p = models.CharField(max_length=30)
    harga_p = models.DecimalField(max_digits=15, decimal_places=2)
    jumlah_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul1_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul2_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul3_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul4_p = models.DecimalField(max_digits=15, decimal_places=2)
    urai = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'angg_pembiayaansub3'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek', 'kodesub1', 'kodesub2', 'kodesub3'),)


class AnggPendapatan(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    volume = models.CharField(max_length=30)
    satuan = models.CharField(max_length=30)
    harga = models.DecimalField(max_digits=15, decimal_places=2)
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)
    triwul1 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul2 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul3 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul4 = models.DecimalField(max_digits=15, decimal_places=2)
    keterangan = models.CharField(max_length=255)
    volume_p = models.CharField(max_length=30)
    satuan_p = models.CharField(max_length=30)
    harga_p = models.DecimalField(max_digits=15, decimal_places=2)
    jumlah_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul1_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul2_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul3_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul4_p = models.DecimalField(max_digits=15, decimal_places=2)
    pengguna = models.CharField(max_length=50, blank=True, null=True)
    last_update = models.DateTimeField()
    jan = models.DecimalField(max_digits=15, decimal_places=2)
    feb = models.DecimalField(max_digits=15, decimal_places=2)
    maret = models.DecimalField(max_digits=15, decimal_places=2)
    april = models.DecimalField(max_digits=15, decimal_places=2)
    mey = models.DecimalField(max_digits=15, decimal_places=2)
    jun = models.DecimalField(max_digits=15, decimal_places=2)
    jul = models.DecimalField(max_digits=15, decimal_places=2)
    agust = models.DecimalField(max_digits=15, decimal_places=2)
    sept = models.DecimalField(max_digits=15, decimal_places=2)
    okto = models.DecimalField(max_digits=15, decimal_places=2)
    nov = models.DecimalField(max_digits=15, decimal_places=2)
    des = models.DecimalField(max_digits=15, decimal_places=2)
    lock = models.IntegerField()
    lock_p = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'angg_pendapatan'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek'),)


class AnggPendapatansub1(models.Model):
    tahun = models.ForeignKey(AnggPendapatan, models.DO_NOTHING, db_column='tahun', primary_key=True)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    kodesub1 = models.IntegerField()
    volume = models.CharField(max_length=30)
    satuan = models.CharField(max_length=30)
    harga = models.DecimalField(max_digits=15, decimal_places=2)
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)
    triwul1 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul2 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul3 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul4 = models.DecimalField(max_digits=15, decimal_places=2)
    volume_p = models.CharField(max_length=30)
    satuan_p = models.CharField(max_length=30)
    harga_p = models.DecimalField(max_digits=15, decimal_places=2)
    jumlah_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul1_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul2_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul3_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul4_p = models.DecimalField(max_digits=15, decimal_places=2)
    urai = models.CharField(max_length=255)
    keterangan = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'angg_pendapatansub1'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek', 'kodesub1'),)


class AnggPendapatansub2(models.Model):
    tahun = models.ForeignKey(AnggPendapatansub1, models.DO_NOTHING, db_column='tahun', primary_key=True)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    kodesub1 = models.IntegerField()
    kodesub2 = models.IntegerField()
    volume = models.CharField(max_length=30)
    satuan = models.CharField(max_length=30)
    harga = models.DecimalField(max_digits=15, decimal_places=2)
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)
    triwul1 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul2 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul3 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul4 = models.DecimalField(max_digits=15, decimal_places=2)
    keterangan = models.CharField(max_length=255)
    volume_p = models.CharField(max_length=30)
    satuan_p = models.CharField(max_length=30)
    harga_p = models.DecimalField(max_digits=15, decimal_places=2)
    jumlah_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul1_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul2_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul3_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul4_p = models.DecimalField(max_digits=15, decimal_places=2)
    urai = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'angg_pendapatansub2'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek', 'kodesub1', 'kodesub2'),)


class AnggPendapatansub3(models.Model):
    tahun = models.ForeignKey(AnggPendapatansub2, models.DO_NOTHING, db_column='tahun', primary_key=True)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    kodesub1 = models.IntegerField()
    kodesub2 = models.IntegerField()
    kodesub3 = models.IntegerField()
    volume = models.CharField(max_length=30)
    satuan = models.CharField(max_length=30)
    harga = models.DecimalField(max_digits=15, decimal_places=2)
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)
    triwul1 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul2 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul3 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul4 = models.DecimalField(max_digits=15, decimal_places=2)
    keterangan = models.CharField(max_length=255)
    volume_p = models.CharField(max_length=30)
    satuan_p = models.CharField(max_length=30)
    harga_p = models.DecimalField(max_digits=15, decimal_places=2)
    jumlah_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul1_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul2_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul3_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul4_p = models.DecimalField(max_digits=15, decimal_places=2)
    urai = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'angg_pendapatansub3'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek', 'kodesub1', 'kodesub2', 'kodesub3'),)


class AnggPengguna(models.Model):
    tahun = models.CharField(max_length=4)
    uname = models.CharField(max_length=50)
    pwd = models.CharField(max_length=50, blank=True, null=True)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    hakakses = models.CharField(max_length=16)
    kegiatan = models.CharField(max_length=1000, blank=True, null=True)
    organisasi = models.CharField(max_length=1000, blank=True, null=True)
    kodeorganisasi = models.CharField(max_length=4, blank=True, null=True)
    is_bendahara_pembantu = models.CharField(max_length=1)
    is_login = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'angg_pengguna'


class AnggPpas(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    kodebidang = models.CharField(max_length=5)
    kodeprogram = models.IntegerField()
    kodekegiatan = models.IntegerField()
    kodeprioritas = models.IntegerField()
    kodesumberdana = models.IntegerField()
    urai = models.CharField(max_length=1000)
    pagu = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    sumberdana = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'angg_ppas'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'kodebidang', 'kodeprogram', 'kodekegiatan', 'kodeprioritas', 'kodesumberdana'),)


class AnggPpasprogram(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeprioritas = models.IntegerField()
    kodesasaran = models.IntegerField()
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    kodebidang = models.CharField(max_length=5)
    kodeprogram = models.IntegerField()
    urai = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'angg_ppasprogram'
        unique_together = (('tahun', 'kodeprioritas', 'kodesasaran', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'kodebidang', 'kodeprogram'),)


class AnggPrioritas(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeprioritas = models.IntegerField()
    uraian = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'angg_prioritas'
        unique_together = (('tahun', 'kodeprioritas'),)


class AnggSasaran(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeprioritas = models.IntegerField()
    kodesasaran = models.IntegerField()
    uraian = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'angg_sasaran'
        unique_together = (('tahun', 'kodeprioritas', 'kodesasaran'),)


class AnggShb(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    id_shb = models.IntegerField()
    jenis_barang = models.CharField(max_length=255)
    merk = models.CharField(max_length=255)
    urai = models.CharField(max_length=1000)
    satuan = models.CharField(max_length=255)
    harga = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'angg_shb'
        unique_together = (('tahun', 'id_shb'),)


class AnggSkpdppas(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeprioritas = models.IntegerField()
    kodesasaran = models.IntegerField()
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'angg_skpdppas'
        unique_together = (('tahun', 'kodeprioritas', 'kodesasaran', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi'),)


class AnggTempDak(models.Model):
    kodedak = models.IntegerField()
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    kodebidang = models.CharField(max_length=5)
    kodeprogram = models.IntegerField()
    kodekegiatan = models.IntegerField()
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)
    kodesumberdana = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'angg_temp_dak'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'kodebidang', 'kodeprogram', 'kodekegiatan', 'kodeakun', 'kodejenis', 'kodeobjek', 'koderincianobjek', 'kodekelompok', 'kodedak'),)


class AnggTempPpas(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    urai = models.CharField(max_length=1000)
    pagu = models.DecimalField(max_digits=15, decimal_places=2)
    pagu_p = models.DecimalField(max_digits=15, decimal_places=2)
    isbold = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'angg_temp_ppas'
        unique_together = (('tahun', 'kodeakun', 'kodekelompok', 'kodejenis'),)


class AruskasKemarin(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kode = models.IntegerField()
    uraian = models.CharField(max_length=255)
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'aruskas_kemarin'
        unique_together = (('tahun', 'kode'),)


class AsetDataAset(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    id = models.IntegerField()
    id_instansi = models.IntegerField()
    golongan = models.IntegerField()
    bidang = models.IntegerField()
    kelompok = models.IntegerField()
    subkelompok = models.IntegerField()
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)
    penyusutan = models.DecimalField(max_digits=15, decimal_places=2)
    id_dhp = models.CharField(max_length=50, blank=True, null=True)
    kondisi = models.CharField(max_length=2, blank=True, null=True)
    asal_usul = models.CharField(max_length=100, blank=True, null=True)
    tanggal = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'aset_data_aset'
        unique_together = (('tahun', 'id', 'id_instansi', 'golongan', 'bidang', 'kelompok', 'subkelompok'),)


class AsetMasterRekening(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    id_kode = models.IntegerField()
    golongan = models.IntegerField()
    bidang = models.IntegerField()
    kelompok = models.IntegerField()
    sub_kelompok = models.IntegerField()
    sub_sub_kelompok = models.IntegerField()
    uraian = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aset_master_rekening'
        unique_together = (('tahun', 'id_kode', 'golongan', 'bidang', 'kelompok', 'sub_kelompok', 'sub_sub_kelompok'),)


class AsetOrganisasi(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    id_instansi = models.IntegerField()
    uraian = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'aset_organisasi'
        unique_together = (('tahun', 'id_instansi'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Belanja(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=4)
    kodebidang = models.CharField(max_length=5)
    kodeprogram = models.IntegerField()
    kodekegiatan = models.IntegerField()
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    volume = models.CharField(max_length=30)
    satuan = models.CharField(max_length=30)
    harga = models.DecimalField(max_digits=15, decimal_places=2)
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)
    triwul1 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul2 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul3 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul4 = models.DecimalField(max_digits=15, decimal_places=2)
    volume_p = models.CharField(max_length=30)
    satuan_p = models.CharField(max_length=30)
    harga_p = models.DecimalField(max_digits=15, decimal_places=2)
    jumlah_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul1_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul2_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul3_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul4_p = models.DecimalField(max_digits=15, decimal_places=2)
    jumlah_tahun_depan = models.DecimalField(max_digits=15, decimal_places=2)
    sumberdana_p = models.IntegerField(blank=True, null=True)
    sumberdana = models.IntegerField(blank=True, null=True)
    kodekepentingan = models.IntegerField(blank=True, null=True)
    l_ra = models.DecimalField(max_digits=15, decimal_places=2)
    l_r1 = models.DecimalField(max_digits=15, decimal_places=2)
    l_r2 = models.DecimalField(max_digits=15, decimal_places=2)
    l_rea = models.DecimalField(max_digits=15, decimal_places=2)
    l_re1 = models.DecimalField(max_digits=15, decimal_places=2)
    l_re2 = models.DecimalField(max_digits=15, decimal_places=2)
    pengguna = models.CharField(max_length=50, blank=True, null=True)
    last_update = models.DateTimeField()
    jan = models.DecimalField(max_digits=15, decimal_places=2)
    feb = models.DecimalField(max_digits=15, decimal_places=2)
    maret = models.DecimalField(max_digits=15, decimal_places=2)
    april = models.DecimalField(max_digits=15, decimal_places=2)
    mey = models.DecimalField(max_digits=15, decimal_places=2)
    jun = models.DecimalField(max_digits=15, decimal_places=2)
    jul = models.DecimalField(max_digits=15, decimal_places=2)
    agust = models.DecimalField(max_digits=15, decimal_places=2)
    sept = models.DecimalField(max_digits=15, decimal_places=2)
    okto = models.DecimalField(max_digits=15, decimal_places=2)
    nov = models.DecimalField(max_digits=15, decimal_places=2)
    des = models.DecimalField(max_digits=15, decimal_places=2)
    lock = models.IntegerField()
    lock_p = models.IntegerField()
    beban = models.CharField(max_length=8, blank=True, null=True)
    keterangan = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'belanja'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'kodebidang', 'kodeprogram', 'kodekegiatan', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek'),)


class BukuJurnal(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    isskpd = models.SmallIntegerField()
    noref = models.CharField(max_length=15)
    nobukti = models.CharField(max_length=50)
    jenisjurnal = models.SmallIntegerField()
    keterangan = models.CharField(max_length=1000)
    posting = models.SmallIntegerField()
    tanggalbukti = models.DateTimeField()
    username = models.CharField(max_length=50)
    no_bku = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'buku_jurnal'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'isskpd', 'noref'),)


class BukuJurnalRincian(models.Model):
    tahun = models.ForeignKey(BukuJurnal, models.DO_NOTHING, db_column='tahun', primary_key=True)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    isskpd = models.SmallIntegerField()
    noref = models.CharField(max_length=15)
    kodebidang = models.CharField(max_length=5)
    kodeprogram = models.IntegerField()
    kodekegiatan = models.IntegerField()
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    urut = models.IntegerField()
    debet = models.DecimalField(max_digits=15, decimal_places=2)
    kredit = models.DecimalField(max_digits=15, decimal_places=2)
    posting = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'buku_jurnal_rincian'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'isskpd', 'noref', 'kodebidang', 'kodeprogram', 'kodekegiatan', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek', 'urut'),)


class ChartMarquee(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    marquee = models.CharField(max_length=1000)
    aktif = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'chart_marquee'


class Contrapos(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    nosts = models.CharField(max_length=100)
    uraian = models.CharField(max_length=1000)
    jenissp2d = models.CharField(max_length=15)
    penyetor = models.CharField(max_length=255)
    bank = models.CharField(max_length=255)
    norekbank = models.CharField(max_length=100)
    tanggal = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'contrapos'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'nosts'),)


class ContraposRincian(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    nosts = models.CharField(max_length=100)
    kodebidang = models.CharField(max_length=5)
    kodeprogram = models.IntegerField()
    kodekegiatan = models.IntegerField()
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'contrapos_rincian'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'nosts', 'kodebidang', 'kodeprogram', 'kodekegiatan', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek'),)


class DaftarDanaCadangan(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    urut = models.IntegerField()
    tujuan = models.CharField(max_length=255)
    dasarhukum = models.CharField(max_length=255)
    jmlrencana = models.DecimalField(max_digits=15, decimal_places=2)
    saldoawal = models.DecimalField(max_digits=15, decimal_places=2)
    transferdarikasda = models.DecimalField(max_digits=15, decimal_places=2)
    transferkekasda = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'daftar_dana_cadangan'
        unique_together = (('tahun', 'urut'),)


class DaftarKorolari(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    posisi = models.CharField(max_length=10)
    a_kodeakun = models.IntegerField()
    a_kodekelompok = models.IntegerField()
    a_kodejenis = models.IntegerField()
    a_kodeobjek = models.IntegerField()
    a_koderincianobjek = models.IntegerField()
    b_kodeakun = models.IntegerField()
    b_kodekelompok = models.IntegerField()
    b_kodejenis = models.IntegerField()
    b_kodeobjek = models.IntegerField()
    b_koderincianobjek = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'daftar_korolari'
        unique_together = (('tahun', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek', 'posisi'),)


class DaftarPegawai(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kelompok = models.IntegerField()
    jenis = models.IntegerField()
    urai = models.CharField(max_length=50, blank=True, null=True)
    eselon1 = models.IntegerField()
    eselon2 = models.IntegerField()
    eselon3 = models.IntegerField()
    eselon4 = models.IntegerField()
    eselon5 = models.IntegerField()
    fungsional = models.IntegerField()
    staff = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'daftar_pegawai'
        unique_together = (('tahun', 'kelompok', 'jenis'),)


class DaftarPenyertaanModal(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    urut = models.IntegerField()
    tahunpenyertaan = models.CharField(max_length=4)
    pihakketiga = models.CharField(max_length=255)
    dasarhukum = models.CharField(max_length=255)
    bentukpenyertaan = models.CharField(max_length=100)
    jmlawal = models.DecimalField(max_digits=15, decimal_places=2)
    jmln = models.DecimalField(max_digits=15, decimal_places=2)
    hasil = models.DecimalField(max_digits=15, decimal_places=2)
    jmlterima = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'daftar_penyertaan_modal'
        unique_together = (('tahun', 'urut'),)


class DaftarPinjamanDaerah(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    urut = models.IntegerField()
    sumberpinjaman = models.CharField(max_length=255)
    tanggalpinjaman = models.DateTimeField()
    jumlahpinjaman = models.DecimalField(max_digits=15, decimal_places=2)
    jangkawaktu = models.CharField(max_length=25)
    persenbunga = models.DecimalField(max_digits=15, decimal_places=2)
    tujuanpinjaman = models.CharField(max_length=255)
    realpokokpinjaman = models.DecimalField(max_digits=15, decimal_places=2)
    realbunga = models.DecimalField(max_digits=15, decimal_places=2)
    sisapokokpinjaman = models.DecimalField(max_digits=15, decimal_places=2)
    sisabunga = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'daftar_pinjaman_daerah'
        unique_together = (('tahun', 'urut'),)


class DaftarPiutang(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    urut = models.IntegerField()
    tahunpengakuan = models.CharField(max_length=4)
    saldoawal = models.DecimalField(max_digits=15, decimal_places=2)
    penambahanpiutang = models.DecimalField(max_digits=15, decimal_places=2)
    penguranganpiutang = models.DecimalField(max_digits=15, decimal_places=2)
    uraianpiutang = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'daftar_piutang'
        unique_together = (('tahun', 'urut'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Dummy(models.Model):
    dummy = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'dummy'


class Dummysp2D(models.Model):
    kode = models.CharField(primary_key=True, max_length=15)
    dummy = models.IntegerField()
    urai = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dummysp2d'


class Hakakses(models.Model):
    hakakses = models.CharField(max_length=16)
    modulelist = models.CharField(max_length=1000)
    listpilih = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'hakakses'


class Jenistransaksijurnal(models.Model):
    id = models.IntegerField(primary_key=True)
    isskpd = models.IntegerField()
    uraian = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'jenistransaksijurnal'
        unique_together = (('id', 'isskpd'),)


class KasdaHakakses(models.Model):
    username = models.CharField(primary_key=True, max_length=50)
    hakakses = models.CharField(max_length=5000)

    class Meta:
        managed = False
        db_table = 'kasda_hakakses'


class KasdaPengguna(models.Model):
    username = models.CharField(primary_key=True, max_length=50)
    pass_field = models.CharField(db_column='pass', max_length=1000)  # Field renamed because it was a Python reserved word.
    nama = models.CharField(max_length=100)
    jenis = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'kasda_pengguna'


class KasdaSumberdanarekening(models.Model):
    urut = models.IntegerField(primary_key=True)
    kodesumberdana = models.IntegerField()
    urai = models.CharField(max_length=25)
    rekening = models.CharField(max_length=100)
    saldoawal = models.DecimalField(max_digits=15, decimal_places=2)
    tanggal = models.DateTimeField()
    bank = models.CharField(max_length=50)
    saldo_tanggal = models.DecimalField(max_digits=15, decimal_places=2)
    pengembalian = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'kasda_sumberdanarekening'


class KasdaTransaksi(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    nobukukas = models.CharField(max_length=10)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=4)
    nobukti = models.CharField(max_length=50)
    tanggal = models.DateTimeField()
    kodesumberdana = models.IntegerField()
    deskripsi = models.CharField(max_length=1000, blank=True, null=True)
    tglbukti = models.DateTimeField()
    jenistransaksi = models.CharField(max_length=13)
    deskripsilengkap = models.CharField(max_length=1000, blank=True, null=True)
    locked = models.CharField(max_length=1)
    kdlokasi = models.IntegerField()
    kodebidang = models.CharField(max_length=5, blank=True, null=True)
    kodeprogram = models.IntegerField(blank=True, null=True)
    kodekegiatan = models.IntegerField(blank=True, null=True)
    username = models.CharField(max_length=50)
    lastupdate = models.DateTimeField()
    jenissp2d = models.CharField(max_length=15, blank=True, null=True)
    contrapost = models.IntegerField(blank=True, null=True)
    upload = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'kasda_transaksi'
        unique_together = (('tahun', 'nobukukas', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi'),)


class KasdaTransaksiDel(models.Model):
    tahun = models.CharField(max_length=4)
    nobukukas = models.CharField(max_length=10)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=4)
    nobukti = models.CharField(max_length=50)
    tanggal = models.DateTimeField()
    kodesumberdana = models.IntegerField()
    lastupdate = models.DateTimeField()
    deskripsi = models.CharField(max_length=1000, blank=True, null=True)
    tglbukti = models.DateTimeField()
    jenistransaksi = models.CharField(max_length=13)
    deskripsilengkap = models.CharField(max_length=1000, blank=True, null=True)
    locked = models.CharField(max_length=1)
    kdlokasi = models.IntegerField()
    kodebidang = models.CharField(max_length=5, blank=True, null=True)
    kodeprogram = models.IntegerField(blank=True, null=True)
    kodekegiatan = models.IntegerField(blank=True, null=True)
    username = models.CharField(max_length=50)
    username_del = models.CharField(max_length=50)
    tgl_del = models.DateTimeField()
    jenissp2d = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kasda_transaksi_del'


class KasdaTransaksiDetil(models.Model):
    tahun = models.ForeignKey(KasdaTransaksi, models.DO_NOTHING, db_column='tahun', primary_key=True)
    nobukukas = models.CharField(max_length=10)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=4)
    kodebidang = models.CharField(max_length=5)
    kodeprogram = models.IntegerField()
    kodekegiatan = models.IntegerField()
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    penerimaan = models.DecimalField(max_digits=15, decimal_places=2)
    pengeluaran = models.DecimalField(max_digits=15, decimal_places=2)
    kd_sumber_dana = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'kasda_transaksi_detil'
        unique_together = (('tahun', 'nobukukas', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'kodebidang', 'kodeprogram', 'kodekegiatan', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek'),)


class KasdaTransaksiDetilDel(models.Model):
    tahun = models.CharField(max_length=4)
    nobukukas = models.CharField(max_length=10)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=4)
    kodebidang = models.CharField(max_length=5)
    kodeprogram = models.IntegerField()
    kodekegiatan = models.IntegerField()
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    penerimaan = models.DecimalField(max_digits=15, decimal_places=2)
    pengeluaran = models.DecimalField(max_digits=15, decimal_places=2)
    username_del = models.CharField(max_length=50)
    tgl_del = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'kasda_transaksi_detil_del'


class Kegiatan(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    kodebidang = models.CharField(max_length=5)
    kodeprogram = models.IntegerField()
    kodekegiatan = models.IntegerField()
    urai = models.CharField(max_length=255)
    sumberdana = models.CharField(max_length=50, blank=True, null=True)
    sumberdana_p = models.CharField(max_length=50, blank=True, null=True)
    baru_lanjutan = models.IntegerField(blank=True, null=True)
    pengguna = models.CharField(max_length=50, blank=True, null=True)
    last_update = models.DateTimeField()
    lock = models.IntegerField()
    lock_p = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'kegiatan'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'kodebidang', 'kodeprogram', 'kodekegiatan'),)


class KonfigTglPenagihan(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    bel_non_fisik = models.DateTimeField()
    bel_fisik = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'konfig_tgl_penagihan'


class Konfigurasi(models.Model):
    id = models.IntegerField(blank=True, null=True)
    namakonfigurasi = models.CharField(max_length=50)
    konfigvalue = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'konfigurasi'


class KonversiAkrual(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    a_kodeakun = models.IntegerField(blank=True, null=True)
    a_kodekelompok = models.IntegerField(blank=True, null=True)
    a_kodejenis = models.IntegerField(blank=True, null=True)
    a_kodeobjek = models.IntegerField(blank=True, null=True)
    a_koderincianobjek = models.IntegerField(blank=True, null=True)
    lob_kodeakun = models.IntegerField(blank=True, null=True)
    lob_kodekelompok = models.IntegerField(blank=True, null=True)
    lob_kodejenis = models.IntegerField(blank=True, null=True)
    lob_kodeobjek = models.IntegerField(blank=True, null=True)
    lob_koderincianobjek = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'konversi_akrual'
        unique_together = (('tahun', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek'),)


class KonversiAkrualPiutang(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    a_kodeakun = models.IntegerField(blank=True, null=True)
    a_kodekelompok = models.IntegerField(blank=True, null=True)
    a_kodejenis = models.IntegerField(blank=True, null=True)
    a_kodeobjek = models.IntegerField(blank=True, null=True)
    a_koderincianobjek = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'konversi_akrual_piutang'
        unique_together = (('tahun', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek'),)


class KonversiRekeningaset(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    golongan = models.IntegerField(blank=True, null=True)
    bidang = models.IntegerField(blank=True, null=True)
    kelompok = models.IntegerField(blank=True, null=True)
    subkelompok = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'konversi_rekeningaset'
        unique_together = (('tahun', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek'),)


class LoKemarin(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    jumlah = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    isskpd = models.IntegerField()
    jumlahn = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'lo_kemarin'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek'),)


class LpeKemarin(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    kode = models.IntegerField()
    jumlah = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    isskpd = models.IntegerField(blank=True, null=True)
    jumlahn = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'lpe_kemarin'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'kode'),)


class LraKemarin(models.Model):
    tahun = models.CharField(max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    jumlah = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    isskpd = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'lra_kemarin'


class MasterBidang(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodebidang = models.CharField(max_length=5)
    urai = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'master_bidang'
        unique_together = (('tahun', 'kodebidang'),)


class MasterDasarhukum(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=4)
    nourut = models.IntegerField()
    nomordasarhukum = models.CharField(max_length=30)
    dasarhukum = models.CharField(max_length=1000)
    tanggal = models.DateTimeField()
    tentang = models.CharField(max_length=1000)
    jenisdpa = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'master_dasarhukum'
        unique_together = (('tahun', 'nomordasarhukum', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'nourut'),)


class MasterFungsi(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodefungsi = models.IntegerField()
    urai = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'master_fungsi'
        unique_together = (('tahun', 'kodefungsi'),)


class MasterKepentingan(models.Model):
    kodekepentingan = models.IntegerField(primary_key=True)
    urai = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'master_kepentingan'


class MasterLokasi(models.Model):
    kdlokasi = models.IntegerField(primary_key=True)
    urut = models.IntegerField()
    urai = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'master_lokasi'


class MasterOrganisasi(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    urai = models.CharField(max_length=255)
    alamat = models.CharField(max_length=255, blank=True, null=True)
    notelp = models.CharField(max_length=30, blank=True, null=True)
    nofax = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    skpkd = models.IntegerField(blank=True, null=True)
    fungsi = models.IntegerField()
    lock = models.IntegerField()
    lock_p = models.IntegerField()
    id_aset = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'master_organisasi'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi'),)


class MasterProgram(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodebidang = models.CharField(max_length=5)
    kodeprogram = models.IntegerField()
    kodekegiatan = models.IntegerField()
    urai = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'master_program'
        unique_together = (('tahun', 'kodebidang', 'kodeprogram', 'kodekegiatan'),)


class MasterRekening(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    urai = models.CharField(max_length=255, blank=True, null=True)
    keterangan = models.CharField(max_length=255, blank=True, null=True)
    last_update = models.DateTimeField()
    pengguna = models.CharField(max_length=50, blank=True, null=True)
    id_aset = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'master_rekening'
        unique_together = (('tahun', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek'),)


class MasterSumberdana(models.Model):
    kodesumberdana = models.IntegerField(primary_key=True)
    urai = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'master_sumberdana'


class Masterjabatan(models.Model):
    jenissistem = models.IntegerField(primary_key=True)
    isskpd = models.IntegerField()
    urut = models.IntegerField()
    urai = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'masterjabatan'
        unique_together = (('jenissistem', 'isskpd', 'urut'),)


class Masterneraca(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    isskpd = models.IntegerField()
    id = models.IntegerField()
    urai = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'masterneraca'
        unique_together = (('tahun', 'id', 'isskpd'),)

class NeracaKemarin(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)
    jumlahn = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'neraca_kemarin'
        unique_together = (('tahun', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek'),)


class OtorisasiAnggaran(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.IntegerField()
    kodebidang = models.CharField(max_length=5)
    kodeprogram = models.IntegerField()
    kodekegiatan = models.IntegerField()
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    uname = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'otorisasi_anggaran'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'kodebidang', 'kodeprogram', 'kodekegiatan', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek'),)


class PejabatSkpd(models.Model):
    tahun = models.CharField(max_length=4)
    kodeurusan = models.IntegerField(primary_key=True)
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=4)
    jenissistem = models.IntegerField()
    id = models.IntegerField()
    pangkat = models.CharField(max_length=255, blank=True, null=True)
    jabatan = models.CharField(max_length=255)
    line1 = models.CharField(max_length=255, blank=True, null=True)
    line2 = models.CharField(max_length=255, blank=True, null=True)
    ub = models.CharField(max_length=1, blank=True, null=True)
    nip = models.CharField(max_length=25, blank=True, null=True)
    norekbank = models.CharField(max_length=50)
    namabank = models.CharField(max_length=50)
    npwp = models.CharField(max_length=50)
    nama = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'pejabat_skpd'
        unique_together = (('kodeurusan', 'tahun', 'kodesuburusan', 'kodeorganisasi', 'id', 'jenissistem'),)


class PejabatSkpkd(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    id = models.IntegerField()
    jenissistem = models.IntegerField()
    nama = models.CharField(max_length=60)
    pangkat = models.CharField(max_length=255, blank=True, null=True)
    nip = models.CharField(max_length=25, blank=True, null=True)
    jabatan = models.CharField(max_length=255)
    line1 = models.CharField(max_length=255, blank=True, null=True)
    line2 = models.CharField(max_length=255, blank=True, null=True)
    ub = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pejabat_skpkd'
        unique_together = (('tahun', 'id', 'jenissistem'),)


class Pembiayaan(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    volume = models.CharField(max_length=30)
    satuan = models.CharField(max_length=30)
    harga = models.DecimalField(max_digits=15, decimal_places=2)
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)
    triwul1 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul2 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul3 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul4 = models.DecimalField(max_digits=15, decimal_places=2)
    volume_p = models.CharField(max_length=30)
    satuan_p = models.CharField(max_length=30)
    harga_p = models.DecimalField(max_digits=15, decimal_places=2)
    jumlah_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul1_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul2_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul3_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul4_p = models.DecimalField(max_digits=15, decimal_places=2)
    pengguna = models.CharField(max_length=50, blank=True, null=True)
    last_update = models.DateTimeField()
    jan = models.DecimalField(max_digits=15, decimal_places=2)
    feb = models.DecimalField(max_digits=15, decimal_places=2)
    maret = models.DecimalField(max_digits=15, decimal_places=2)
    april = models.DecimalField(max_digits=15, decimal_places=2)
    mey = models.DecimalField(max_digits=15, decimal_places=2)
    jun = models.DecimalField(max_digits=15, decimal_places=2)
    jul = models.DecimalField(max_digits=15, decimal_places=2)
    agust = models.DecimalField(max_digits=15, decimal_places=2)
    sept = models.DecimalField(max_digits=15, decimal_places=2)
    okto = models.DecimalField(max_digits=15, decimal_places=2)
    nov = models.DecimalField(max_digits=15, decimal_places=2)
    des = models.DecimalField(max_digits=15, decimal_places=2)
    lock = models.IntegerField()
    lock_p = models.IntegerField()
    keterangan = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pembiayaan'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek'),)


class Pendapatan(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=4)
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    volume = models.CharField(max_length=30)
    satuan = models.CharField(max_length=30)
    harga = models.DecimalField(max_digits=15, decimal_places=2)
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)
    triwul1 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul2 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul3 = models.DecimalField(max_digits=15, decimal_places=2)
    triwul4 = models.DecimalField(max_digits=15, decimal_places=2)
    volume_p = models.CharField(max_length=30)
    satuan_p = models.CharField(max_length=30)
    harga_p = models.DecimalField(max_digits=15, decimal_places=2)
    jumlah_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul1_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul2_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul3_p = models.DecimalField(max_digits=15, decimal_places=2)
    triwul4_p = models.DecimalField(max_digits=15, decimal_places=2)
    pengguna = models.CharField(max_length=50, blank=True, null=True)
    last_update = models.DateTimeField()
    jan = models.DecimalField(max_digits=15, decimal_places=2)
    feb = models.DecimalField(max_digits=15, decimal_places=2)
    maret = models.DecimalField(max_digits=15, decimal_places=2)
    april = models.DecimalField(max_digits=15, decimal_places=2)
    mey = models.DecimalField(max_digits=15, decimal_places=2)
    jun = models.DecimalField(max_digits=15, decimal_places=2)
    jul = models.DecimalField(max_digits=15, decimal_places=2)
    agust = models.DecimalField(max_digits=15, decimal_places=2)
    sept = models.DecimalField(max_digits=15, decimal_places=2)
    okto = models.DecimalField(max_digits=15, decimal_places=2)
    nov = models.DecimalField(max_digits=15, decimal_places=2)
    des = models.DecimalField(max_digits=15, decimal_places=2)
    lock = models.IntegerField()
    lock_p = models.IntegerField()
    keterangan = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pendapatan'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek'),)


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

    class Meta:
        managed = False
        db_table = 'pengguna'


class SalKemarin(models.Model):
    tahun = models.CharField(max_length=4)
    kode = models.IntegerField()
    uraian = models.CharField(max_length=255, blank=True, null=True)
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'sal_kemarin'


class Settingtahun(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    perubahananggaran = models.IntegerField()
    perubahansipkd = models.IntegerField()
    pemda = models.CharField(max_length=255)
    ibukota = models.CharField(max_length=255)
    kepaladaerah = models.CharField(max_length=255)
    namappkd = models.CharField(max_length=255)
    pangkatppkd = models.CharField(max_length=25)
    namasekda = models.CharField(max_length=255)
    pangkatsekda = models.CharField(max_length=25)
    nipppkd = models.CharField(max_length=22)
    nipsekda = models.CharField(max_length=22)
    judulpemda = models.CharField(max_length=100)
    aktif = models.IntegerField()
    jabatansekda = models.CharField(max_length=255, blank=True, null=True)
    jabatanppkd = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'settingtahun'


class SkUp(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=4)
    noskup = models.CharField(max_length=100)
    tanggal = models.DateTimeField(blank=True, null=True)
    jumlah_skup = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'sk_up'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'noskup'),)


class Skp(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    isskpd = models.IntegerField()
    nomor = models.CharField(max_length=100)
    jenis = models.CharField(max_length=15)
    nomorpokok = models.CharField(max_length=100, blank=True, null=True)
    tanggal = models.DateTimeField()
    wajibbayar = models.CharField(max_length=100, blank=True, null=True)
    alamat = models.CharField(max_length=1000, blank=True, null=True)
    uraian = models.CharField(max_length=1000, blank=True, null=True)
    masa = models.IntegerField(blank=True, null=True)
    jatuhtempo = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'skp'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'nomor', 'isskpd'),)


class SkpRincian(models.Model):
    tahun = models.ForeignKey(Skp, models.DO_NOTHING, db_column='tahun', primary_key=True)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    isskpd = models.IntegerField()
    nomor = models.CharField(max_length=100)
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    jumlah = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'skp_rincian'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'isskpd', 'nomor', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek'),)


class SkpdBku(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=4)
    no_bku = models.IntegerField()
    isskpd = models.IntegerField()
    tgl_bku = models.DateTimeField()
    urai = models.CharField(max_length=1000)
    jenis_bku = models.CharField(max_length=20)
    penerimaan = models.DecimalField(max_digits=15, decimal_places=2)
    pengeluaran = models.DecimalField(max_digits=15, decimal_places=2)
    bukti = models.CharField(max_length=100)
    tgl_bukti = models.DateTimeField()
    locked = models.CharField(max_length=1)
    jenis_sp2d = models.CharField(max_length=10)
    nospj = models.CharField(max_length=50, blank=True, null=True)
    status = models.SmallIntegerField()
    simpananbank = models.IntegerField()
    uname = models.CharField(max_length=50, blank=True, null=True)
    is_bendahara_pembantu = models.CharField(max_length=1)
    bendahara_pembantu = models.CharField(max_length=50, blank=True, null=True)
    is_pihak_ketiga = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'skpd_bku'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'no_bku', 'isskpd'),)


class SkpdBkurincian(models.Model):
    tahun = models.ForeignKey(SkpdBku, models.DO_NOTHING, db_column='tahun', primary_key=True)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=4)
    no_bku = models.IntegerField()
    kodebidang = models.CharField(max_length=5)
    kodeprogram = models.IntegerField()
    kodekegiatan = models.IntegerField()
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    isskpd = models.IntegerField()
    penerimaan = models.DecimalField(max_digits=15, decimal_places=2)
    pengeluaran = models.DecimalField(max_digits=15, decimal_places=2)
    nospj = models.CharField(max_length=50, blank=True, null=True)
    nospp = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'skpd_bkurincian'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'no_bku', 'kodebidang', 'kodeprogram', 'kodekegiatan', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek', 'isskpd'),)


class SkpdPenerimaan(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    isskpd = models.IntegerField()
    no_bku = models.IntegerField()
    id_sts = models.IntegerField()
    tgl_bku = models.DateTimeField()
    nobukti = models.CharField(max_length=25)
    tgl_bukti = models.DateTimeField()
    penyetor = models.CharField(max_length=255, blank=True, null=True)
    alamat = models.CharField(max_length=255, blank=True, null=True)
    npwpd = models.CharField(max_length=255, blank=True, null=True)
    sk1 = models.CharField(max_length=255, blank=True, null=True)
    sk2 = models.CharField(max_length=255, blank=True, null=True)
    locked = models.CharField(max_length=1, blank=True, null=True)
    carabayar = models.CharField(max_length=50)
    jumlah = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    urai = models.CharField(max_length=1000)
    bku_sts = models.IntegerField(blank=True, null=True)
    isskp = models.IntegerField()
    jenis_transaksi = models.CharField(max_length=15, blank=True, null=True)
    rekeningbank = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'skpd_penerimaan'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'isskpd', 'no_bku', 'id_sts'),)


class SkpdPengembalian(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    nosts = models.CharField(max_length=100)
    tglsts = models.DateTimeField()
    uraian = models.CharField(max_length=1000, blank=True, null=True)
    nosp2d = models.CharField(max_length=100, blank=True, null=True)
    jenissp2d = models.CharField(max_length=15, blank=True, null=True)
    uname = models.CharField(max_length=100, blank=True, null=True)
    nolpj = models.CharField(max_length=100, blank=True, null=True)
    rekeningbank = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'skpd_pengembalian'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'nosts'),)


class SkpdRincianPenerimaan(models.Model):
    tahun = models.ForeignKey(SkpdPenerimaan, models.DO_NOTHING, db_column='tahun', primary_key=True)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    isskpd = models.IntegerField()
    no_bku = models.IntegerField()
    id_sts = models.IntegerField()
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'skpd_rincian_penerimaan'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'isskpd', 'no_bku', 'id_sts', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek'),)


class SkpdRincianPengembalian(models.Model):
    tahun = models.ForeignKey(SkpdPengembalian, models.DO_NOTHING, db_column='tahun', primary_key=True)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    nosts = models.CharField(max_length=100)
    kodebidang = models.CharField(max_length=5)
    kodeprogram = models.IntegerField()
    kodekegiatan = models.IntegerField()
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'skpd_rincian_pengembalian'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'nosts', 'kodebidang', 'kodeprogram', 'kodekegiatan', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek'),)


class SkpdRincianSetor(models.Model):
    tahun = models.ForeignKey('SkpdSetor', models.DO_NOTHING, db_column='tahun', primary_key=True)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    isskpd = models.IntegerField()
    no_bku = models.IntegerField()
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    jumlah = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    id_sts = models.IntegerField()
    id_penerimaan = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'skpd_rincian_setor'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'isskpd', 'no_bku', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek', 'id_sts'),)


class SkpdSetor(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    isskpd = models.IntegerField()
    no_bku = models.IntegerField()
    tgl_bku = models.DateTimeField()
    nosts = models.CharField(max_length=25)
    tgl_sts = models.DateTimeField()
    penyetor = models.CharField(max_length=255, blank=True, null=True)
    urai = models.CharField(max_length=1000, blank=True, null=True)
    alamat = models.CharField(max_length=255, blank=True, null=True)
    jumlah = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    bank = models.CharField(max_length=255, blank=True, null=True)
    norekbank = models.CharField(max_length=255, blank=True, null=True)
    locked = models.CharField(max_length=1, blank=True, null=True)
    carabayar = models.CharField(max_length=50, blank=True, null=True)
    id_sts = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'skpd_setor'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'isskpd', 'no_bku'),)


class Sp2B(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    nosp2b = models.CharField(max_length=100)
    nosp3b = models.CharField(max_length=100)
    tglsp2b = models.DateTimeField()
    tglsp3b = models.DateTimeField()
    uptdpenerima = models.CharField(max_length=100)
    saldoawal = models.DecimalField(max_digits=15, decimal_places=2)
    pendapatan = models.DecimalField(max_digits=15, decimal_places=2)
    bendaharapenerima = models.CharField(max_length=255)
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    urai = models.CharField(max_length=1000)
    jabatan = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'sp2b'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'nosp2b'),)


class Sp2D(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=4)
    nosp2d = models.CharField(max_length=100)
    tanggal = models.DateTimeField()
    tanggal_draft = models.DateTimeField()
    norekbank = models.CharField(max_length=100)
    bank = models.CharField(max_length=50)
    npwp = models.CharField(max_length=50)
    pemegangkas = models.CharField(max_length=100)
    namayangberhak = models.CharField(max_length=100)
    kodebidang = models.CharField(max_length=5)
    kodeprogram = models.IntegerField(blank=True, null=True)
    kodekegiatan = models.IntegerField(blank=True, null=True)
    triwulan = models.IntegerField()
    sumberdana = models.CharField(max_length=100, blank=True, null=True)
    jumlahppn = models.DecimalField(max_digits=15, decimal_places=2)
    jumlahpph = models.DecimalField(max_digits=15, decimal_places=2)
    jumlahretribusi = models.DecimalField(max_digits=15, decimal_places=2)
    locked = models.CharField(max_length=1)
    lastupdate = models.DateTimeField()
    jenissp2d = models.CharField(max_length=10)
    informasi = models.CharField(max_length=1000, blank=True, null=True)
    perubahan = models.IntegerField()
    nospm = models.CharField(max_length=100)
    tglspm = models.DateTimeField()
    jumlahspm = models.DecimalField(max_digits=15, decimal_places=2)
    deskripsispm = models.CharField(max_length=1000, blank=True, null=True)
    bankasal = models.CharField(max_length=50)
    rekeningpengeluaran = models.CharField(max_length=50)
    statuskeperluan = models.CharField(max_length=1000, blank=True, null=True)
    tglkasda = models.DateTimeField(blank=True, null=True)
    norekbankasal = models.CharField(max_length=255)
    jumlahsp2d = models.DecimalField(max_digits=15, decimal_places=2)
    tolak = models.CharField(max_length=1)
    uname = models.CharField(max_length=50, blank=True, null=True)
    sp2b = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sp2d'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'nosp2d'), ('tahun', 'nosp2d'),)


class Sp2Dhutang(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    nosp2dlama = models.CharField(max_length=100)
    tglsp2dlama = models.DateTimeField()
    jumlahlama = models.DecimalField(max_digits=15, decimal_places=2)
    tahunasal = models.CharField(max_length=4)
    nosp2dbaru = models.CharField(max_length=100, blank=True, null=True)
    tglsp2dbaru = models.DateTimeField(blank=True, null=True)
    jumlahbaru = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    uraian = models.CharField(max_length=1000, blank=True, null=True)
    kepada = models.CharField(max_length=255, blank=True, null=True)
    nospp = models.CharField(max_length=100)
    tglspp = models.DateTimeField(blank=True, null=True)
    nospm = models.CharField(max_length=100)
    tglspm = models.DateTimeField(blank=True, null=True)
    namabank = models.CharField(max_length=100)
    npwp = models.CharField(max_length=100)
    rekeningbankasal = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'sp2dhutang'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'nosp2dlama'),)


class Sp2Dpotongan(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=4)
    nosp2d = models.CharField(max_length=100)
    rekeningpotongan = models.CharField(max_length=20)
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)
    jenispotongan = models.CharField(max_length=10)
    keterangan = models.CharField(max_length=255, blank=True, null=True)
    tanggal = models.DateTimeField()
    tolak = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'sp2dpotongan'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'nosp2d', 'rekeningpotongan'),)


class Sp2Drincian(models.Model):
    tahun = models.ForeignKey(Sp2D, models.DO_NOTHING, db_column='tahun', primary_key=True)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=4)
    nosp2d = models.CharField(max_length=100)
    kodebidang = models.CharField(max_length=5)
    kodeprogram = models.IntegerField()
    kodekegiatan = models.IntegerField()
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)
    tanggal = models.DateTimeField()
    tolak = models.CharField(max_length=1)
    status_aset = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sp2drincian'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'nosp2d', 'kodebidang', 'kodeprogram', 'kodekegiatan', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek'),)


class Sp2Dtolak(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=4)
    notolak = models.CharField(max_length=100)
    nospm = models.CharField(max_length=100)
    tanggal_tolak = models.DateTimeField()
    sebab_tolak = models.CharField(max_length=1000, blank=True, null=True)
    keterangan_tolak = models.CharField(max_length=1000, blank=True, null=True)
    urut = models.IntegerField()
    jumlahtolak = models.DecimalField(max_digits=15, decimal_places=2)
    jenisspm = models.CharField(max_length=15, blank=True, null=True)
    tanggal_spm = models.DateTimeField(blank=True, null=True)
    deskripsispm = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sp2dtolak'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'notolak', 'urut'),)


class Spd(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=4)
    nospd = models.CharField(max_length=100)
    tanggal_draft = models.DateTimeField()
    tanggal = models.DateTimeField()
    tgldpa = models.DateTimeField()
    locked = models.CharField(max_length=1)
    lastupdate = models.DateTimeField()
    bendaharapengeluaran = models.CharField(max_length=100)
    bulan_awal = models.IntegerField()
    bulan_akhir = models.IntegerField()
    jenisdpa = models.CharField(max_length=10)
    nopermohonan = models.CharField(max_length=100, blank=True, null=True)
    jumlahspd = models.DecimalField(max_digits=15, decimal_places=2)
    uname = models.CharField(max_length=50, blank=True, null=True)
    jumlahdpa = models.DecimalField(max_digits=15, decimal_places=2)
    nodpa = models.CharField(max_length=60)
    jenisspd = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spd'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'nospd'), ('tahun', 'nospd'),)


class SpdRincian(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    nospd = models.CharField(max_length=100)
    kodebidang = models.CharField(max_length=5)
    kodeprogram = models.IntegerField()
    kodekegiatan = models.IntegerField()
    jumlah = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    ispembiayaan = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'spd_rincian'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'nospd', 'kodebidang', 'kodeprogram', 'kodekegiatan', 'ispembiayaan'),)


class SpdX(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=4)
    nospd = models.CharField(max_length=100)
    tanggal = models.DateTimeField()
    nodpa = models.CharField(max_length=60)
    tgldpa = models.DateTimeField()
    jumlahdpa = models.DecimalField(max_digits=15, decimal_places=2)
    locked = models.CharField(max_length=1)
    lastupdate = models.DateTimeField()
    bendaharapengeluaran = models.CharField(max_length=100)
    bulan_awal = models.IntegerField()
    bulan_akhir = models.IntegerField()
    jenisdpa = models.CharField(max_length=10)
    nopermohonan = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spd_x'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'nospd'), ('tahun', 'nospd'),)


class SpdrincianX(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=4)
    nospd = models.CharField(max_length=100)
    kodebidang = models.CharField(max_length=5)
    kodeprogram = models.IntegerField()
    kodekegiatan = models.IntegerField()
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)
    tanggal = models.DateTimeField()
    ispembiayaan = models.CharField(max_length=1)
    jenisdpa = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'spdrincian_x'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'nospd', 'kodebidang', 'kodeprogram', 'kodekegiatan', 'ispembiayaan'),)


class SpjPkd(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    nospj = models.CharField(max_length=50)
    tglspj = models.DateTimeField()
    nolpj = models.CharField(max_length=100)
    status = models.IntegerField()
    keperluan = models.CharField(max_length=1000)
    username = models.CharField(max_length=100, blank=True, null=True)
    lastupdate = models.DateTimeField()
    nosp2d = models.CharField(max_length=50, blank=True, null=True)
    jenis = models.CharField(max_length=10)
    jurnal = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'spj_pkd'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'nospj'),)


class SpjPkdRinc(models.Model):
    tahun = models.ForeignKey(SpjPkd, models.DO_NOTHING, db_column='tahun', primary_key=True)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    nospj = models.CharField(max_length=50)
    kodebidang = models.CharField(max_length=5)
    kodeprogram = models.IntegerField()
    kodekegiatan = models.IntegerField()
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'spj_pkd_rinc'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'nospj', 'kodebidang', 'kodeprogram', 'kodekegiatan', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek'),)


class SpjSkpd(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    nospj = models.CharField(max_length=100)
    tglspj = models.DateTimeField()
    keperluan = models.CharField(max_length=1000)
    status = models.SmallIntegerField()
    username = models.CharField(max_length=100, blank=True, null=True)
    lastupdate = models.DateTimeField()
    nosp2d = models.CharField(max_length=100, blank=True, null=True)
    jenis = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'spj_skpd'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'nospj'),)


class SpjSkpdRinc(models.Model):
    tahun = models.ForeignKey(SpjSkpd, models.DO_NOTHING, db_column='tahun', primary_key=True)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    nospj = models.CharField(max_length=100)
    kodebidang = models.CharField(max_length=5)
    kodeprogram = models.IntegerField()
    kodekegiatan = models.IntegerField()
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    jumlah = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spj_skpd_rinc'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'nospj', 'kodebidang', 'kodeprogram', 'kodekegiatan', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek'),)


class SpjSkpdRincSub1(models.Model):
    tahun = models.ForeignKey(SpjSkpdRinc, models.DO_NOTHING, db_column='tahun', primary_key=True)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=5)
    nospj = models.CharField(max_length=100)
    kodebidang = models.CharField(max_length=5)
    kodeprogram = models.IntegerField()
    kodekegiatan = models.IntegerField()
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    kodesub1 = models.IntegerField()
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)
    nobukti = models.CharField(max_length=100, blank=True, null=True)
    tglbukti = models.DateTimeField(blank=True, null=True)
    uraian = models.CharField(max_length=1000, blank=True, null=True)
    kepada = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spj_skpd_rinc_sub1'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'nospj', 'kodebidang', 'kodeprogram', 'kodekegiatan', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek', 'kodesub1'),)


class Spm(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=4)
    nospm = models.CharField(max_length=100)
    jenisspm = models.CharField(max_length=10)
    tanggal = models.DateTimeField()
    tanggal_draft = models.DateTimeField()
    norekbank = models.CharField(max_length=50)
    bank = models.CharField(max_length=50)
    npwp = models.CharField(max_length=50)
    nospp = models.CharField(max_length=100)
    tglspp = models.DateTimeField()
    jumlahspp = models.DecimalField(max_digits=15, decimal_places=2)
    jumlahspm = models.DecimalField(max_digits=15, decimal_places=2)
    pemegangkas = models.CharField(max_length=100)
    namayangberhak = models.CharField(max_length=100)
    kodebidang = models.CharField(max_length=5)
    kodeprogram = models.IntegerField(blank=True, null=True)
    kodekegiatan = models.IntegerField(blank=True, null=True)
    triwulan = models.IntegerField()
    jumlahppn = models.DecimalField(max_digits=15, decimal_places=2)
    jumlahpph = models.DecimalField(max_digits=15, decimal_places=2)
    jumlahretribusi = models.DecimalField(max_digits=15, decimal_places=2)
    locked = models.CharField(max_length=1)
    lastupdate = models.DateTimeField()
    informasi = models.CharField(max_length=1000, blank=True, null=True)
    deskripsispp = models.CharField(max_length=1000, blank=True, null=True)
    perubahan = models.IntegerField()
    rekeningpengeluaran = models.CharField(max_length=100)
    tolak = models.CharField(max_length=1)
    uname = models.CharField(max_length=50, blank=True, null=True)
    statuskeperluan = models.CharField(max_length=1000, blank=True, null=True)
    sumberdana = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spm'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'nospm'),)


class Spmpotongan(models.Model):
    tahun = models.ForeignKey(Spm, models.DO_NOTHING, db_column='tahun', primary_key=True)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=4)
    nospm = models.CharField(max_length=100)
    rekeningpotongan = models.CharField(max_length=20)
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)
    jenispotongan = models.CharField(max_length=10)
    tanggal = models.DateTimeField()
    tolak = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'spmpotongan'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'nospm', 'rekeningpotongan'),)


class Spmrincian(models.Model):
    tahun = models.ForeignKey(Spm, models.DO_NOTHING, db_column='tahun', primary_key=True)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=4)
    nospm = models.CharField(max_length=100)
    kodebidang = models.CharField(max_length=5)
    kodeprogram = models.IntegerField()
    kodekegiatan = models.IntegerField()
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)
    tanggal = models.DateTimeField()
    tolak = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'spmrincian'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'nospm', 'kodebidang', 'kodeprogram', 'kodekegiatan', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek'),)


class Spp(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=4)
    nospp = models.CharField(max_length=100)
    tglspp = models.DateTimeField()
    tglspp_draft = models.DateTimeField()
    kodebidang = models.CharField(max_length=5)
    kodeprogram = models.IntegerField(blank=True, null=True)
    kodekegiatan = models.IntegerField(blank=True, null=True)
    deskripsispp = models.CharField(max_length=1000, blank=True, null=True)
    tglspd = models.DateTimeField(blank=True, null=True)
    nospd = models.CharField(max_length=100, blank=True, null=True)
    sisadanaspd = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    jumlahspp = models.DecimalField(max_digits=15, decimal_places=2)
    locked = models.CharField(max_length=1)
    norekeningbendahara = models.CharField(max_length=50, blank=True, null=True)
    lastupdate = models.DateTimeField()
    keperluanbulan = models.IntegerField(blank=True, null=True)
    tglditeliti = models.DateTimeField(blank=True, null=True)
    namapeneliti = models.CharField(max_length=100, blank=True, null=True)
    nippeneliti = models.CharField(max_length=50, blank=True, null=True)
    namaperusahaan = models.CharField(max_length=100, blank=True, null=True)
    bentukperusahaan = models.CharField(max_length=10, blank=True, null=True)
    alamatperusahaan = models.CharField(max_length=255, blank=True, null=True)
    namapimpinanperusahaan = models.CharField(max_length=100, blank=True, null=True)
    norekperusahaan = models.CharField(max_length=50, blank=True, null=True)
    nokontrak = models.CharField(max_length=100, blank=True, null=True)
    kegiatanlanjutan = models.CharField(max_length=1, blank=True, null=True)
    waktupelaksanaan = models.CharField(max_length=25, blank=True, null=True)
    namabank = models.CharField(max_length=50, blank=True, null=True)
    jenisdpa = models.CharField(max_length=15, blank=True, null=True)
    nodpa = models.CharField(max_length=100, blank=True, null=True)
    tgldpa = models.DateTimeField(blank=True, null=True)
    jenisspp = models.CharField(max_length=10)
    sk_up = models.CharField(max_length=100, blank=True, null=True)
    tgl_sk_up = models.DateTimeField(blank=True, null=True)
    jml_sk_up = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    triwulan = models.IntegerField()
    jmlspd = models.DecimalField(max_digits=15, decimal_places=2)
    perubahan = models.IntegerField()
    tolak = models.CharField(max_length=1)
    nospj = models.CharField(max_length=50, blank=True, null=True)
    npwp = models.CharField(max_length=50, blank=True, null=True)
    uname = models.CharField(max_length=50, blank=True, null=True)
    deskripsipekerjaan = models.CharField(max_length=1000, blank=True, null=True)
    bendaharapengeluaran = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'spp'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'nospp'),)


class Spprincian(models.Model):
    tahun = models.ForeignKey(Spp, models.DO_NOTHING, db_column='tahun', primary_key=True)
    kodeurusan = models.IntegerField()
    kodesuburusan = models.IntegerField()
    kodeorganisasi = models.CharField(max_length=4)
    kodebidang = models.CharField(max_length=5)
    kodeprogram = models.IntegerField()
    kodekegiatan = models.IntegerField()
    nospp = models.CharField(max_length=100)
    kodeakun = models.IntegerField()
    kodekelompok = models.IntegerField()
    kodejenis = models.IntegerField()
    kodeobjek = models.IntegerField()
    koderincianobjek = models.IntegerField()
    kodesub1 = models.IntegerField()
    kodesub2 = models.IntegerField()
    kodesub3 = models.IntegerField()
    tanggal = models.DateTimeField()
    urai = models.CharField(max_length=255)
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)
    tolak = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'spprincian'
        unique_together = (('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'kodebidang', 'kodeprogram', 'kodekegiatan', 'nospp', 'kodeakun', 'kodekelompok', 'kodejenis', 'kodeobjek', 'koderincianobjek', 'kodesub1', 'kodesub2', 'kodesub3'),)


class Sumberdanarekening(models.Model):
    kodesumberdana = models.IntegerField(primary_key=True)
    urai = models.CharField(max_length=25)
    rekening = models.CharField(max_length=100)
    urut = models.IntegerField()
    bank_asal = models.CharField(max_length=100, blank=True, null=True)
    bank = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sumberdanarekening'
        unique_together = (('kodesumberdana', 'urai', 'rekening', 'urut'),)


class TimEksekutif(models.Model):
    tahun = models.CharField(primary_key=True, max_length=4)
    kdtim_eksekutif = models.IntegerField()
    nama = models.CharField(max_length=255)
    jabatan = models.CharField(max_length=255)
    nip = models.CharField(max_length=22)

    class Meta:
        managed = False
        db_table = 'tim_eksekutif'
        unique_together = (('tahun', 'kdtim_eksekutif'),)
