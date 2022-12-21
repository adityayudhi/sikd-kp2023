/* @copyright: PT. Global Intermedia Nusantara; @version: 20190703-origin, 20190730, 20190708; @author: anovsiradj; */
(function(unknown) {
var $ = $3 || $1 || $;

var omfg = window.spjskpd.omfg, dump = window.spjskpd.dump, forme = window.spjskpd.forme;
var tanggalin_id = window.spjskpd.tanggalin_id, tanggalin_iso = window.spjskpd.tanggalin_iso, rupiahin = window.spjskpd.rupiahin, rupiahin_parse = window.spjskpd.rupiahin_parse;
var $wait = $3('#container').children('.cover:first');
var dated = { min: window.spjskpd.min, max: window.spjskpd.max, current: window.spjskpd.current, firstDay: window.spjskpd.firstDay, lastDay: window.spjskpd.lastDay, };

var tahun = window.spjskpd.tahun;
var jq_daterangepicker = window.spjskpd.jq_daterangepicker;

var bulan = dated.current.getMonth() + 1 || 1;
// var bulan = 3; window.console.warn(`bulan(${bulan}):hardcoded;`);

var rupiahin_koma = window.spjskpd.rupiahin_koma || 2;
var isskpd = window.spjskpd.isskpd || 0;

var akrual = document.getElementById('spjskpd-akrual');
var akrual_form = document.getElementById('spjskpd-akrual-form');
var akrual_extra = {
	delay: 500,
	istilah: 'Jurnal',
	search_delay: 500, /* [DEPRECATED] */
	errors: {
		skpd_required: 'SKPD belum dipilih.',
		undef_action: 'tidak bisa, aksi belum ada.',
		reload: 'tidak bisa ambil jurnal.',
	},
	h: (function() {
		var h = {
			wix: window.innerHeight,
			navbar: document.body.querySelector('.navbar').offsetHeight,
			header: document.getElementById('container').querySelector('.header-konten').offsetHeight,
			form: akrual_form.offsetHeight,
			thead: akrual.querySelector('thead').offsetHeight,
			tfoot: akrual.querySelector('tfoot').offsetHeight,
		};
		return (h.wix -
			(
				h.navbar + h.header +
				h.thead + h.tfoot +
				h.form +
				0
			)
		);
	})(),
};

/* const skpd ppkd */
var kodeskpd = {}, kodeskpd_index = [];
['kodeurusan','kodesuburusan','kodeorganisasi','kodeunit'].forEach(pk => {
	kodeskpd[pk] = kodeskpd_index[kodeskpd_index.length] = window.spjskpd.skpkd[pk];
});

/* copas ~/assets/spjskpd/spjpengeluaranskpd/main.js */
function jq_tanggalin(input,fn) {
	var exput = input.nextElementSibling;
	if (input.nextElementSibling && input.nextElementSibling.nodeName === 'INPUT') {
		$1(exput).daterangepicker({
			minDate: window.spjskpd.min, maxDate: window.spjskpd.max,
			singleDatePicker: true, calender_style: "picker_4",
		}, function(moment) {
			$(input).prop('value', moment.format('YYYY-MM-DD')).trigger('change');
			if (fn) fn(moment.toDate(), input.value);
		});
		$3(input).on('tanggalin', function(evt, dt) {
			if (typeof dt === 'string') dt = new Date(dt);
			var picker = $1(exput).data('daterangepicker');
			picker.setStartDate(dt); picker.setEndDate(dt);
			picker.updateInputText(); picker.notify(); picker.updateCalendars();
			$3(input).prop('value', tanggalin_iso(dt)).trigger('change'); // paksa
		});
	} // fi
} // fn

$([
	document.getElementById('spjskpd-akrual-action-1'),
	document.getElementById('spjskpd-akrual-action-2'),
]).find('button[data-action]').on('click', event => $(akrual).trigger('action', [event.currentTarget,]));

$(akrual).on('action', function(event, elem) {
	var tmp, action = elem.dataset.action || '';

	if (!kodeskpd) return message_ok('error', akrual_extra.errors.skpd_required);

	if (/form/.test(action)) return $(xformx).trigger('prompt', [0,]);

	if (/laporan/.test(action)) {
		tmp = action.match(/\[(.+)\]/);
		if (tmp) return $(laporan).trigger('prompt', [tmp[1].trim(),]);
	}

	var i = $(akrual).data('index')['__action_delete__'];
	if (/destroy|posting/.test(action) && i) {
		var t = $(akrual).data('table'), e = [];

		t.column(i).nodes().to$().each((i,tbrcel) => {
			if (tbrcel.querySelector('input[type=checkbox]').checked) {
				e.push(t.row(tbrcel.parentElement).data());
			}
		});

		if (e.length > 0) {
			if (/destroy/.test(action)) destroy(e);
			if (/posting/.test(action)) posting(e,elem);
		} else message_ok('error', 'belum ada jurnal yang dicentang.');

		return;
	}

	return message_ok('error', akrual_extra.errors.undef_action);
});

$(akrual).data('index', {});
$(akrual).data('action', {});
$(akrual).data('columns', []);
$(akrual).children('thead').each(function() {
	var thead = this;
	$(this).children('tr').each(function() {
		var thr0w = this;
		$(this).children('th').each(function() {
			var thrcel = this, thrcel_action = this.querySelector('[hidden]');
			var styleObject = this.dataset.styleObject ? eval(`(${this.dataset.styleObject})`) : null;
			var styleClass = this.dataset.styleClass ? this.dataset.styleClass : null;
			var column = this.dataset.column, nullable = column === unknown || /_action_/.test(column);

			if (thrcel.innerHTML.trim() === '') thrcel.innerText = column;

			$(akrual).data('columns').push({
				data: (nullable ? null : column),
				createdCell: function(tbrcel, data, entry) {
					if (styleObject) $(tbrcel).css(styleObject);
					if (styleClass) $(tbrcel).addClass(styleClass);

					if (/_action_/.test(column)) {
						$(thrcel_action.cloneNode(true)).removeAttr('hidden').appendTo(tbrcel);
						if (/_update_/.test(column)) {
							if (entry.posting == 0) {
								$(tbrcel).find('button').on('click', () => $(xformx).trigger('prompt', [1,entry,]));
							}
							if (entry.posting == 1) {
								$(tbrcel).find('button').prop('disabled', true);
							}
						}
					}
				},
				render: function(data,type,entry) {
					if (nullable) return null;
					if (/display/.test(type) && thrcel.dataset.type) {
						if (/rp/.test(thrcel.dataset.type)) return rupiahin(data, rupiahin_koma);
						if (/dt/.test(thrcel.dataset.type)) return tanggalin_id(data);
					}
					return data;
				},
			});

			// acuan (column) index
			$(akrual).data('index')[column] = thrcel.cellIndex;

			if (/_action_/.test(column)) {
				$(akrual).data('action')[column] = thrcel;

				if (/_delete_/.test(column)) {
					$(thrcel).find('[type=checkbox]:first').each((i,xbox0) => {
						$(xbox0).on('change', (event) => {
							$(akrual).data('table')
							.column(thrcel.cellIndex).nodes()
							.to$().each((i,xbox1) => {
								$(xbox1).find('input[type=checkbox]:first').prop('checked', xbox0.checked);
							});
						});
					});
				}
			}
		}); // thrcel
	}); // thr0w
}); // thead
$3(akrual).data('table', $1(akrual).DataTable($.extend(true, {}, window.spjskpd.datatable, {
	data: [],
	scrollY: (akrual_extra.h + Number(akrual.dataset.hPlus) - Number(akrual.dataset.hMinus)) || akrual.dataset.h,
	columns: $(akrual).data('columns'),
	footerCallback: function(tfrow,data) {
		var tfoot = tfrow.parentElement;
		var summary = {
			__init__: function(column) {
				if (!(column in summary)) {
					summary[column] = data.length > 0 ? data.map(n => n[column]).reduce((a,b) => (Number(a)+Number(b))) : 0;
				}
				return summary[column];
			},
		};

		$(tfoot).find('[data-summary]').each(function() {
			$(this).text( rupiahin(summary.__init__(this.dataset.summary), rupiahin_koma) );
		});
	}, //footerCallback
})));
$(akrual).on('reload', (event, data) => {
	var table = $(akrual).data('table'), data = data || [];

	table.clear();

	/* hilangkan centang pada xbox0 */
	var xbox0 = $(akrual).data('action')['__action_delete__'];
	if (xbox0) $(xbox0).find('[type=checkbox]:first').prop('checked', false);

	table.search(''); /* reset pencarian table */
	table.rows.add(data);
	table.columns.adjust().draw();
});

/* [DONE] akrual_form@submit */
$3(akrual_form).on('submit', function(event) {
	event.preventDefault();

	// clear
	$3(akrual).trigger('reload', [[],]);
	forme(this, 'search', search => $(search).prop('value', '').trigger('change'));
	forme(this, 'jenis', jenis => $(jenis).prop('selectedIndex', 0).trigger('change'));

	// skip
	if (!kodeskpd || !bulan) return;

	// ajax
	var params = $.extend(true, {
		tahun: tahun,
		bulan: Number(bulan),
		jenis: forme(this, 'jenis', 'value'),
	}, kodeskpd);
	$wait.show();
	$3.get(this.action, params, data => $3(akrual).trigger('reload', [data,]))
	.fail(() => omfg(akrual_extra.errors.reload, arguments))
	.always(() => $wait.hide());
});

/* [DONE] akrual_form.jenis@change */
forme(akrual_form, 'jenis', jenis => {
	$(jenis).on('change', () => {
		var table = $(akrual).data('table'),
		jenis_column_index = $3(akrual).data('index')[jenis.dataset.column];

		if (jenis_column_index) {
			if (jenis.selectedIndex !== 0) {
				forme(akrual_form, 'search', 'value', '');

				table
				.columns( jenis_column_index )
				.search( jenis.children[jenis.selectedIndex].innerText.trim() )
				.draw();
			} else {
				table
				.columns( jenis_column_index )
				.search( '' )
				.draw();
			}
		}
	}).trigger('change');
});

/* [DONE] akrual_form.search@input */
forme(akrual_form, 'search', search => {
	$(search).on('input', window.spjskpd.debounce(() => {
		var term = String(forme(akrual_form, 'search', 'value') || '').trim();
		if (term !== '') forme(akrual_form, 'jenis', 'selectedIndex', 0);

		$(akrual).data('table').search( term ).draw();
	}, akrual_extra.search_delay));
});

/* [DONE] akrual_form.month@change */
forme(akrual_form, 'month', month => {
	month.value = bulan;
	$(month).on('change', () => {
		bulan = Number(month.value);

		$(akrual_form).trigger('submit');
	}).trigger('change');
});

/* [DONE] */
forme(akrual_form, 'skpkd', 'value', `${kodeskpd_index.join('.')} - ${window.spjskpd.skpkd.urai}`);

/* [DONE] TIDAK BOLEH PINDAH LOKASI BARIS! */
$3(akrual_form).trigger('submit');

function destroy(entry_entries) {
	var uuid_k = 'noref', uuid_v, text;

	if ($3.isArray(entry_entries) && entry_entries.length === 1) entry_entries = entry_entries[0];
	if ($3.isArray(entry_entries))
	     uuid_v = entry_entries.map(entry => entry[uuid_k]).join(',');
	else uuid_v = entry_entries[uuid_k];

	if ($3.isArray(entry_entries))
	     text = 'yakin hapus jurnal ?';
	else text = `yakin hapus jurnal <b>${uuid_v}</b> ?`;

	var para = $3.extend({
		csrfmiddlewaretoken: window.spjskpd.kuki('csrftoken'),
	}, kodeskpd);
	para[uuid_k] = uuid_v;

	$1.alertable.confirm(text, window.spjskpd.alertable_rm).then(function(result) {
		$wait.show();
		$3.post(window.spjskpd.href_destroy, para, result => {
			$wait.hide();
			$(akrual_form).trigger('submit');
		}).fail(function() { $wait.hide(); omfg('tidak bisa hapus jurnal.', arguments); });
	});
}

function posting(entry_entries,elem) {
	var uuid_k = 'noref', uuid_v, text, yn = elem.dataset.action.replace(/[^0-1]+/, '');

	if ($3.isArray(entry_entries) && entry_entries.length === 1) entry_entries = entry_entries[0];
	if ($3.isArray(entry_entries))
	     uuid_v = entry_entries.map(entry => entry[uuid_k]).join(',');
	else uuid_v = entry_entries[uuid_k];

	if ($3.isArray(entry_entries))
	     text = `yakin ${elem.innerText.trim()} jurnal ?`;
	else text = `yakin ${elem.innerText.trim()} jurnal <b>${uuid_v}</b> ?`;

	var para = $3.extend({
		csrfmiddlewaretoken: window.spjskpd.kuki('csrftoken'),
		posting: yn,
	}, kodeskpd);
	para[uuid_k] = uuid_v;

	$1.alertable.confirm(text, window.spjskpd.alertable_yn).then(function(result) {
		$wait.show();
		$3.post(window.spjskpd.href_posting, para, result => {
			$wait.hide();
			$(akrual_form).trigger('submit');
		}).fail(function() { $wait.hide(); omfg('tidak bisa posting jurnal.', arguments); });
	});
}

// MODAL TAMBAH ================================================================
var xformx = document.getElementById('spjskpd-akrual-xformx');
var xformx_rincian = document.getElementById('spjskpd-akrual-xformx-rincian');
var xformx_rekening = document.getElementById('spjppkd-akrual-rekening');
var xformx_extra = {
	once: true,
	rekening_once: true,
	rekening_load: true,
	errors: {
		hmm_noref: 'Gagal ambil "No. Ref" terakhir.',
	},

	/*
	$FLEX/sipkd_AKUNTANSI_PEMDA/src/spjAkuntansiPemda/views/Akrual/VInputJurnalAkrualPPKD.mxml:cbJenisChange();

	selain "tanggalbukti", tiap elem harus dituliskan.

	k(__0__):v(() => {}) = construct (awal);
	K(__1__):v(() => {}) = destruct (akhir);
	*/
	defaults_by_pk: {
		NA: {
			nobukti: 'Buku Besar',
			keterangan: 'Neraca Awal',
			tanggalbukti: tanggalbukti => $(tanggalbukti).trigger('tanggalin', dated.min),
		},
		JU: {
			nobukti: '',
			keterangan: '',
		},
		JS: {
			nobukti: '',
			keterangan: 'Penyesuaian',
			tanggalbukti: tanggalbukti => $(tanggalbukti).trigger('tanggalin', dated.min),
		},
		JPLRA: {
			nobukti: 'Penutup LRA',
			keterangan: 'Jurnal Penutup LRA',
			tanggalbukti: tanggalbukti => $(tanggalbukti).trigger('tanggalin', dated.lastDay),
			__1__: opts => {
				$wait.show();
				$3.get(xformx.dataset.rekeningDefaultHref, opts, result => $(xformx_rekening).trigger('browsed', [result,]))
				.fail(function() { omfg(`tidak bisa ambil rincian ${opts.jenis_pk}`, arguments); })
				.always(() => $wait.hide());
			},
		},
		JPLO: {
			nobukti: 'Penutup LO',
			keterangan: 'Jurnal Penutup LO',
			tanggalbukti: tanggalbukti => $(tanggalbukti).trigger('tanggalin', dated.lastDay),
			__1__: opts => {
				$wait.show();
				$3.get(xformx.dataset.rekeningDefaultHref, opts, result => $(xformx_rekening).trigger('browsed', [result,]))
				.fail(function() { omfg(`tidak bisa ambil rincian ${opts.jenis_pk}`, arguments); })
				.always(() => $wait.hide());
			},
		},
	},
};

$3(xformx).data('tanggalin', ['tanggalbukti']);
$3(xformx).data('tanggalin').forEach(name => forme(xformx, name, elem => jq_tanggalin(elem)));

forme(xformx, 'jenisjurnal', jenisjurnal => {
	var jenisjenis = window.spjskpd.jenisjenis;
	$(jenisjurnal).on('change', () => {
		var __type__ = Number(forme(xformx, '__type__', 'value') || 0);
		var jenis_id = jenisjurnal.value;
		var jenis_pk = jenisjenis[jenis_id].pk;

		forme(xformx, 'jenis_transaksi', elem => $(elem).prop('value', jenis_pk));
		$(xbrowsex).trigger('jenisjurnal', [__type__,jenis_pk,]);

		forme(xformx, 'tanggalbukti', tanggalbukti => {
			$(tanggalbukti).trigger('tanggalin', dated.current);
			// $(tanggalbukti).trigger('tanggalin', `${tahun}-03-01`); window.console.warn(`tanggalbukti(${tanggalbukti.value}):hardcoded;`);
		});

		if (__type__ === 0) {
			$(xformx_rincian).trigger('reload', [[],]);
			var default_pk = xformx_extra.defaults_by_pk[jenis_pk];
			if (default_pk) for (pk in default_pk) {
				if (/__\d__/.test(pk)) {
					default_pk[pk]({ __type__: __type__, jenis_id:jenis_id, jenis_pk: jenis_pk, });
					continue;
				}
				if ($.isFunction(default_pk[pk])) forme(xformx, pk, default_pk[pk]);
				else forme(xformx, pk, 'value', default_pk[pk]);
			}
		}

		/* [TODO] */
		if (__type__ === 1) {}
	});
});

/* untuk reset form */
forme(xformx, 'noref_trigger', noref_trigger => {
	$(noref_trigger).on('click', () => $(noref_trigger).trigger('auto', []));
	$(noref_trigger).on('auto', function(event, cb) {
		$wait.show();
		$.get(xformx.dataset.hrefNorefauto, {tahun: tahun}, result => {
			$wait.hide();

			if (cb) cb(result);
			else forme(xformx, 'jenisjurnal', jenisjurnal => $(jenisjurnal).trigger('change'));

			forme(xformx, 'noref', 'value', result);
		}).fail(function() {
			$wait.hide();
			omfg(xformx_extra.errors.hmm_noref, arguments);
		});
	});
});

$(xformx).on('assigned', function(event, __type__, entry) {
	for (var n in entry) {
		if ($(this).data('tanggalin').indexOf(n) > -1) continue;
		forme(this, n, 'value', entry[n]);
	}

	$(this).data('tanggalin').forEach(name => forme(this, name,
		elem => $(elem).trigger('tanggalin', (entry && name in entry) ? entry[name] : dated.current)
	));
});

$(xformx).on('prompt', function(event, __type__, entry) {
	forme(this, '__type__', 'value', __type__);
	forme(this, 'csrfmiddlewaretoken', 'value', window.spjskpd.kuki('csrftoken'));
	forme(this, 'tahun', 'value', tahun);
	if (kodeskpd) for (var name in kodeskpd) forme(this, name, 'value', kodeskpd[name]);

	forme(this, 'noref', 'readOnly', __type__ === 1);
	forme(this, 'noref_trigger', 'disabled', __type__ === 1);

	forme(this, 'jenisjurnal', jenisjurnal => {
		$(jenisjurnal).children().each((i,elem) => $(elem).prop('disabled', false));
		$(jenisjurnal).prop('selectedIndex', 0);

		forme(akrual_form, 'jenis', jenis => {
			$(jenisjurnal).children().each((i,elem) => {
				if (
					(__type__ === 0 && elem.value == jenis.value) ||
					(__type__ === 1 && entry && entry.jenisjurnal && entry.jenisjurnal == elem.value)
				) $(jenisjurnal).prop('selectedIndex', i);
			});
		});

		if (__type__ === 1) {
			$(jenisjurnal).children().each((i,elem) => {
				if (jenisjurnal.value != elem.value) $(elem).prop('disabled', true);
			});
		}

		$(jenisjurnal).trigger('change');
	});

	if (__type__ === 0) {
		forme(xformx, 'noref_trigger', noref_trigger => $(noref_trigger).trigger('auto',[() => $(xformx).data('prompt').open(),]));
	}

	if (__type__ === 1) {
		var params = $.extend({noref: entry.noref}, kodeskpd);
		$wait.show();
		$.get(xformx.dataset.hrefRincianUpdate, params, result => {
			$(xformx).trigger('assigned', [__type__,entry,]);
			$(xformx_rincian).trigger('reload', [result,]);
			$wait.hide();
			$(xformx).data('prompt').open();
		}).fail(function() { $wait.hide(); omfg('tidak bisa ambil rincian jurnal', arguments); });
	}
});

$(xformx).data('prompt', new BootstrapDialog($3.extend(true, {}, window.spjskpd.bs3dialog, {
	title: xformx.dataset.promptTitle,
	onshow: function($prompt) {
		$prompt.getModalDialog().css('width', xformx.dataset.promptWidth);
		if (xformx_extra.once) $prompt.getModalBody().append(xformx);
	},
	onshown:function() {
		$(xformx_rincian).data('table').columns.adjust().draw();
		// /* [TEST] */ $3(xformx_rekening).data('prompt').open();
	},
	onhide: function() {
		$(xformx_rincian).data('table').clear().draw();
	},
	onhidden: function() {
		xformx_extra.once = false;
		$(xformx).trigger('reset');
	},
})));

$(xformx).on('submit', function(event) {
	event.preventDefault();

	var tanggalbukti = Number(forme(xformx, 'tanggalbukti', 'value', value => value.split('-')[1]) || 1);

	var data = $(xformx_rincian).data('table').data().toArray();
	var empty = data.map(n => n['debet'] + n['kredit']).reduce((a,b) => (Number(a) + Number(b)), 0);
	if (data.length === 0 || empty < 1) {
		return message_ok('error','rincian masih kosong.');
	}

	var balance = { debet: 0, kredit: 0, };
	for (var i = 0; i < data.length; i++) {
		balance.debet = balance.debet + Number(data[i].debet);
		balance.kredit = balance.kredit + Number(data[i].kredit);
	}
	if (balance.debet !== balance.kredit) {
		return message_ok('error', 'jumlah "debet" dan "kredit" harus sama.');
	}

	$wait.show();
	$.post(xformx.action, $(xformx).serialize(), function() {
		$wait.hide();

		forme(akrual_form, 'month', 'value', tanggalbukti); /* ganti bulan sesuai tanggalbukti */

		$(xformx).trigger('reset'); /* tutup prompt */
		setTimeout(() => $(akrual_form).trigger('submit'), 100); /* reload table data */
	}).fail(function() { $wait.hide(); omfg('tidak bisa simpan jurnal', arguments); });
});

/* [DONE] */
$3(xformx).on('reset', function() {
	$3(xformx).data('prompt').isOpened() && $3(xformx).data('prompt').close();
});

// /* [TEST] */ $3(document).ready(() => $(xformx).trigger('prompt', [0,]));

$(xformx_rincian).data('index', {});
$(xformx_rincian).data('columns', []);

$(xformx_rincian).children('thead').children('tr').children('th').each(function() {
	var thrcel = this;
	var styleObject = this.dataset.styleObject ? eval(`(${this.dataset.styleObject})`) : null;
	var styleClass = this.dataset.styleClass ? this.dataset.styleClass : null;
	var column = this.dataset.column, nullable = column === unknown || /_action_|debet|kredit/.test(column);

	if (thrcel.innerHTML.trim() === '') thrcel.innerText = column;

	// definisi tiap column pada table
	$(xformx_rincian).data('columns').push({
		data: (nullable ? null : column),
		createdCell: function(tbrcel, data, entry) {
			if (styleObject) $(tbrcel).css(styleObject);
			if (styleClass) $(tbrcel).addClass(styleClass);

			/* primarykeys untuk kode* rincian */
			if (/kode_rekening/.test(column)) {
				for(var n in entry) {
					if (/rekening/.test(n)) continue;
					if (/kode/.test(n) === false) continue;
					tbrcel.appendChild(window.spjskpd.doxce('input', {
						type: 'hidden', name: `__rincian__[${n}][]`, value: entry[n],
					}));
				}
			}

			/* freetext rincian */
			if (/debet|kredit/.test(column)) {
				tbrcel.appendChild(window.spjskpd.doxce('div', {
					clasName: 'freetext', contentEditable: true,
					innerText: rupiahin(entry[column], rupiahin_koma),
				}));
				tbrcel.appendChild(window.spjskpd.doxce('input', {
					type: 'hidden', name: `__rincian__[${column}][]`, value: entry[column],
				}));

				$(tbrcel).children(':first')
				.on('keypress', function(event) {
					if (/Enter/.test(event.key)) event.preventDefault() || $(this).trigger('blur');
				})
				.on('input', function() {
					var rp = rupiahin_parse(this.innerText, rupiahin_koma);
					$(this).next().prop('value', rp);
					entry[column] = rp;
				})
				.on('blur', function() {
					this.innerText = rupiahin(entry[column], rupiahin_koma);
					$(xformx_rincian).data('table').columns.adjust().draw();
				});
			}

			if (/_action_/.test(column)) {
				$(thrcel.children[1].cloneNode(true))
				.appendTo(tbrcel).removeAttr('hidden')
				.find('button').on('click',function() {
					var table = $(xformx_rincian).data('table');

					table.row( $(this).parents('tr') ).remove();
					table.columns.adjust().draw();
				});
			}
		},
		render: function(data,type,entry) {
			if (nullable) return null;
			if (/display/.test(type) && thrcel.dataset.type) {
				if (/rp/.test(thrcel.dataset.type)) return rupiahin(data, rupiahin_koma);
				if (/dt/.test(thrcel.dataset.type)) return tanggalin_id(data);
			}
			return data;
		},
	});

	// definisi kolom index
	$(xformx_rincian).data('index')[column] = thrcel.cellIndex;

	// handle untuk aksi create|delete
	if (/_action_/.test(column)) {
		$(thrcel.children[0]).find('button').on('click', () => $3(xformx_rekening).data('prompt').open());
	}
});

$3(xformx_rincian).data('table', $1(xformx_rincian).DataTable($.extend(true, {}, window.spjskpd.datatable, {
	data: [],
	scrollY: xformx_rincian.dataset.height,
	columns: $(xformx_rincian).data('columns'),
	footerCallback: function(tfrow,data) {
		var tfoot = tfrow.parentElement;
		var summary = {
			__init__: function(column) {
				if (!(column in summary)) {
					summary[column] = data.length > 0 ? data.map(n => n[column]).reduce((a,b) => (Number(a)+Number(b))) : 0;
				}
				return summary[column];
			},
		};
		$(tfoot).find('[data-summary]').each(function() {
			$(this).text( rupiahin(summary.__init__(this.dataset.summary), rupiahin_koma) );
		});
	},
})));

$(xformx_rincian).on('reload', (event, data) => {
	var table = $(xformx_rincian).data('table'), data = data || [];

	table.clear();
	table.rows.add(data);

	/* redraw ketika prompt terbuka saja */
	if ($(xformx).data('prompt').isOpened()) {
		if (data.length > 0) table.columns.adjust().draw(); else table.draw();
	}
});

$(xformx_rekening).data('index', {});
$(xformx_rekening).data('columns', []);

$(xformx_rekening).children('table').children('thead').children('tr').children('th').each(function() {
	var thrcel = this;
	var styleObject = this.dataset.styleObject ? eval(`(${this.dataset.styleObject})`) : null;
	var styleClass = this.dataset.styleClass ? this.dataset.styleClass : null;
	var column = this.dataset.column, nullable = column === unknown || /_action_/.test(column);

	if (thrcel.innerHTML.trim() === '') thrcel.innerText = column;

	// definisi tiap column pada table
	$(xformx_rekening).data('columns').push({
		data: (nullable ? null : column),
		createdCell: function(tbrcel, data, entry) {
			if (styleObject) $(tbrcel).css(styleObject);
			if (styleClass) $(tbrcel).addClass(styleClass);
		},
		render: function(data,type,entry) {
			if (nullable) return null;
			if (/display/.test(type) && thrcel.dataset.type) {
				if (/rp/.test(thrcel.dataset.type)) return rupiahin(data, rupiahin_koma);
				if (/dt/.test(thrcel.dataset.type)) return tanggalin_id(data);
			}
			return data;
		},
	});
});

$3(xformx_rekening).data('table', $1(xformx_rekening.querySelector('table')).DataTable($.extend(true, {}, window.spjskpd.datatable, {
	data: [], dom: 'ft',
	scrollY: xformx_rincian.dataset.height.replace(/[0-9]+/, height => height * 1.5),
	columns: $(xformx_rekening).data('columns'),
	createdRow: function(tbrow, data) {
		$(tbrow).on('dblclick', () => $(xformx_rekening).trigger('browsed', [data,]));
	}
})));

$(xformx_rekening).data('prompt', new BootstrapDialog($3.extend(true, {}, window.spjskpd.bs3dialog, {
	title: xformx.dataset.rekeningTitle,
	onshow: function($prompt) {
		$prompt.getModalDialog().css('width', xformx.dataset.promptWidth);
		if (xformx_extra.rekening_once) $prompt.getModalBody().append(xformx_rekening);
	},
	onshown:function() {
		var table = $(xformx_rekening).data('table');

		if (xformx_extra.rekening_load) {
			table.clear();
			table.columns.adjust().draw();

			$wait.show();
			$3.get(xformx.dataset.rekeningHref, function(result) {
				table.rows.add(result);
				table.columns.adjust().draw();
			})
			.fail(function() { omfg('tidak bisa ambil rekening', arguments); })
			.always(() => $wait.hide());
		} else {
			/* jangan draw ulang, karena datanya banyak */
			if (xformx_extra.rekening_once) setTimeout(() => table.columns.adjust().draw(), 500);
		}
	},
	onhidden: function() {
		xformx_extra.rekening_once = false;
		xformx_extra.rekening_load = false;
	},
})));

$(xformx_rekening).on('browsed', function(event, data) {
	if (! $3.isArray(data)) data = [data,];
	var table = $(xformx_rincian).data('table');

	table.rows.add(data.map(elem => {
		elem = $3.extend(true, {}, elem);
		if (!('debet' in elem) || !('kredit' in elem)) $3.extend(elem, { debet:0, kredit:0, });
		return elem;
	}));
	table.columns.adjust().draw();

	$(xformx_rekening).data('prompt').close();
});

var xbrowsex = document.getElementById('spjppkd-akrual-xbrowsex');
var xbrowsex_extra = {
	jenis_pk: [],
	jenis_id_fn: () => forme(xformx, 'jenisjurnal', 'value'),
	jenis_pk_fn: () => {
		var jenis_pk;
		jenis_pk = forme(xformx, 'jenisjurnal', 'value');
		jenis_pk = window.spjskpd.jenisjenis[jenis_pk].pk;
		return jenis_pk;
	},
	bulan_fn:(name) => {
		name = name || false;
		var bulan = (
			forme(xformx, 'tanggalbukti', 'value', value => value.split('-')[1]) ||
			forme(akrual_form, 'bulan', 'value') ||
			0
		);
		bulan = Number(bulan);
		if (name) {
			name = bulan;
			forme(akrual_form, 'month', month => {
				$(month).children().each(function() {
					if (this.value == bulan) name = this.innerText;
				});
			});
			return name;
		}
		return bulan;
	},
	once: true,
};

/* aksi [nobukti_browse] klik */
forme(xformx, 'nobukti_browse', nobukti_browse => {
	$(nobukti_browse).on('click', () => $(xbrowsex).data('prompt').open());
});

/* apakah [nobukti_browse] bisa klik atau tidak? */
$(xbrowsex).on('jenisjurnal', function(event, __type__, jenis_pk) {
	__type__ = __type__ || Number(forme(xformx, '__type__', 'value') || 0);
	jenis_pk = jenis_pk || xbrowsex_extra.jenis_pk_fn();

	forme(xformx, 'nobukti_browse', 'disabled', (__type__ === 0 && xbrowsex_extra.jenis_pk.indexOf(jenis_pk) >= 0) === false);
});

$(xbrowsex).data('prompt', new BootstrapDialog($3.extend(true, {}, window.spjskpd.bs3dialog, {
	onshow: function($prompt) {
		var promptWidth = xbrowsex.dataset.width || xformx.dataset.promptWidth.replace(/[0-9]+/, width => width * 1.2);
		$prompt.getModalDialog().css('width', promptWidth);
		$prompt.setTitle(xbrowsex.dataset.title.replace('{bulan}', xbrowsex_extra.bulan_fn(true)));

		if (xbrowsex_extra.once) $prompt.getModalBody().append(xbrowsex);

		var jenis_pk = xbrowsex_extra.jenis_pk_fn();
		$(xbrowsex).children('[data-content]').hide();
		$(xbrowsex).children(`[data-content=${jenis_pk}]`).show();
	},
	onshown:function() {
		var
		jenis_pk = xbrowsex_extra.jenis_pk_fn(),
		table = $(xbrowsex).data(`table:${jenis_pk}`);

		table.draw();

		var params = {
			jenis_id: xbrowsex_extra.jenis_id_fn(),
			jenis_pk: jenis_pk,
			bulan: xbrowsex_extra.bulan_fn(),
		};

		$wait.show();
		$.get(window.spjskpd.href_browse, params, function(result) {
			$wait.hide();
			table.rows.add(result);
			table.columns.adjust().draw();
		}).fail(function() {
			$wait.hide();
			omfg('tidak bisa ambil transaksi jurnal', arguments);
		});
	},
	onhide: function() {
		var
		jenis_pk = xbrowsex_extra.jenis_pk_fn(),
		table = $(xbrowsex).data(`table:${jenis_pk}`);

		table.clear().draw();
	},
	onhidden: function() {
		xbrowsex_extra.once = false;
	},
})));

$(xbrowsex).children('[data-content]').each((i,elem) => {
	var jenis_pk = elem.dataset.content;
	xbrowsex_extra.jenis_pk.push(jenis_pk);

	var columns = [];
	$(elem).children('table').children('thead').children('tr').children('th').each(function() {
		var thrcel = this;
		var styleObject = this.dataset.styleObject ? eval(`(${this.dataset.styleObject})`) : null;
		var styleClass = this.dataset.styleClass ? this.dataset.styleClass : null;
		var column = this.dataset.column;

		if (thrcel.innerHTML.trim() === '') thrcel.innerText = column;

		columns.push({
			data: column,
			createdCell: function(tbrcel, data, entry) {
				if (styleObject) $(tbrcel).css(styleObject);
				if (styleClass) $(tbrcel).addClass(styleClass);
			},
			render: function(data,type,entry) {
				if (entry[column] === unknown || entry[column] === null || entry[column] === '') {
					if (thrcel.dataset.coalesce) return thrcel.dataset.coalesce;
					return null;
				}
				if (/display/.test(type) && thrcel.dataset.type) {
					if (/rp/.test(thrcel.dataset.type)) return rupiahin(data, rupiahin_koma);
					if (/dt/.test(thrcel.dataset.type)) return tanggalin_id(data);
				}
				return data;
			},
		});
	});

	$3(xbrowsex).data(`table:${jenis_pk}`, $1(elem).children('table').DataTable($.extend(true, {}, window.spjskpd.datatable, {
		data: [], dom: 'ft',
		scrollY: xbrowsex.dataset.height || xformx_rincian.dataset.height.replace(/[0-9]+/, height => height * 1.5),
		columns: columns,
		createdRow: function(tbrow, entry) {
			$(tbrow).on('dblclick', event => {
				$(xbrowsex).data('prompt').close();
				setTimeout(() => $(xbrowsex).trigger('assigned', [entry,]), akrual_extra.delay);
			});
		}
	})));
});

$(xbrowsex).on('assigned', function(event, entry) {
	$(xformx).trigger('assigned', [0, entry]);

	var params = $.extend({}, kodeskpd);
	for (var e in entry) if (/^(tgl|tanggal|no|jenis|kode)/.test(e)) params[e] = entry[e];

	$wait.show();
	$.get(xformx.dataset.hrefRincianCreate, params, result => {

		$wait.hide();
		$(xformx_rincian).trigger('reload', [result,]);

	}).fail(function() { $wait.hide(); omfg('tidak bisa ambil rincian jurnal', arguments); });
});

var laporan = document.querySelector('#spjskpd-akrual-laporan');
var laporan_jenisakun = document.querySelector('#spjskpd-akrual-laporan-jenisakun');
var laporan_pejabat = document.querySelector('#spjskpd-akrual-laporan-pejabat');
var laporan_cfg = {
	jenis: window.spjskpd.laporan_jenisjenis,
	pejabat: window.spjskpd.laporan_pejabat,
	jenis0: null,
	jenis1: null,
	prompt_once: true,
	iframe_once: true,
};

forme(laporan, '__jenis__', __jenis__ => {
	$(__jenis__).on('change', () => {
		var jenis0, jenis1, yn;

		jenis0 = laporan_cfg.jenis0;
		laporan_cfg.jenis1 = jenis1 = __jenis__.value;

		if (laporan_cfg.jenis[jenis0][jenis1]) {
			if (laporan_jenisakun) {
				yn = laporan_cfg.jenis[jenis0][jenis1].jenisakun === true ? 'show' : 'hide';
				$(laporan_jenisakun)[yn]();
			}

			forme(laporan, 'file', 'value', laporan_cfg.jenis[jenis0][jenis1].fr3);
		}
	});
});

forme(laporan, 'idpa', idpa => {
	$(idpa).on('change', () => {
		forme(laporan,'pejabat_skpkd_id', 'value', idpa.value);

		if (laporan_pejabat && laporan_cfg.pejabat[idpa.value]) {
			$(laporan_pejabat).find('input[data-field]').each((i,elem) => {
				$(elem).prop('value', laporan_cfg.pejabat[idpa.value][elem.dataset.field]);
			});
		}
	});
});

forme(laporan, 'tglawal', tglawal => {
	jq_tanggalin(tglawal, (date) => {
		date.setDate(date.getDate() - 1);
		forme(laporan, 'tglkemarin', 'value', tanggalin_iso(date));
	});
});
forme(laporan, 'tglakhir', tglakhir => jq_tanggalin(tglakhir));
forme(laporan, 'TGLCETAK', TGLCETAK => {
	var params = $3.extend({}, window.spjskpd.daterangepicker);
	$1(TGLCETAK).daterangepicker(params, function(moment) {
		//...
	});
});

forme(laporan, 'TGLCETAK', TGLCETAK => jq_tanggalin(TGLCETAK));

$(laporan).on('prompt', function(event,jenis0) {
	laporan_cfg.jenis0 = jenis0;
	var elem;

	forme(laporan, 'tahun', 'value', tahun);
	forme(laporan, 'isskpd', 'value', isskpd);
	if (kodeskpd) for (var e in kodeskpd) forme(this, e, 'value', kodeskpd[e]);

	forme(laporan, 'tglawal', tglawal => $(tglawal).trigger('tanggalin', dated.min));
	forme(laporan, 'tglakhir', tglakhir => $(tglakhir).trigger('tanggalin', dated.max));
	forme(laporan, 'TGLCETAK', TGLCETAK => $(TGLCETAK).trigger('tanggalin', dated.current));

	/* generate */
	forme(laporan, '__jenis__', __jenis__ => {
		$(__jenis__.children).remove();

		if (laporan_cfg.jenis[jenis0]) {
			for (var jenis1 in laporan_cfg.jenis[jenis0]) {
				elem = window.spjskpd.doxce('option', {
					value: jenis1,
					innerText: laporan_cfg.jenis[jenis0][jenis1].teks,
				});
				__jenis__.appendChild(elem);
			}
		}

		$(__jenis__).trigger('change');
	});

	forme(laporan, 'idpa', idpa => $(idpa).trigger('change'));

	$(laporan).data('prompt').open();
});

$(laporan).data('prompt', new BootstrapDialog($3.extend(true, {}, window.spjskpd.bs3dialog, {
	onshow: ($prompt) => {
		$prompt.setTitle(laporan.dataset.promptTitle.replace('{jenis0}', laporan_cfg.jenis0));

		$prompt.getModalDialog().css('width', laporan.dataset.promptWidth);
		if (laporan_cfg.prompt_once) {
			$prompt.getModalBody().append(laporan);
		}
	},

	onhide: () => {
		laporan_cfg.prompt_once = false;
	},

	onhidden: () => {
		$(laporan).trigger('reset');
	},
})));

/* [DONE] */
$(laporan).on('reset', function() {
	$(laporan).data('prompt').isOpened() && $(laporan).data('prompt').close();
});

$(laporan).on('submit', function(event) {
	var iframe_title;

	event.preventDefault();

	iframe_title = laporan_cfg.jenis[laporan_cfg.jenis0][laporan_cfg.jenis1].teks;
	iframe_title = laporan.dataset.iframeTitle.replace('{jenis1}', iframe_title).trim();
	if ((iframe_title.match(/laporan/ig) || []).length > 1) {
		iframe_title = iframe_title.replace(/^laporan\s{0,}/ig, '');
	}

	$(laporan).data('iframe').setTitle(iframe_title);
	$(laporan).data('iframe').open();
});

$(laporan).data('iframe', new BootstrapDialog($3.extend(true, {}, window.spjskpd.bs3dialog, {
	onshow: function($prompt) {
		$prompt.getModalDialog().css({width: laporan.dataset.iframeWidth, height: laporan.dataset.iframeHeight});
		$prompt.getModalBody().css({margin: 0, padding: 0, height: laporan.dataset.iframeHeight});
		$prompt.getModalContent().css({height: '100%'});
	},
	onshown: function($prompt) {
		var iframe = window.spjskpd.doxce('iframe', {
			src: (laporan.dataset.iframeHref + '?' + $(laporan).serialize()),
			style: { width: '100%', height: '100%', },
			frameborder: 0,
		});
		$prompt.getModalBody().append(iframe);
	},
	onhide: $prompt => {
		$prompt.getModalBody().children().remove();
	},
})));

/* [TEST] */
/*
$(document).ready(() => {
	var jenis0 = Object.keys(laporan_cfg.jenis)[0];
	$(laporan).trigger('prompt', [jenis0],);
});
*/
})();
