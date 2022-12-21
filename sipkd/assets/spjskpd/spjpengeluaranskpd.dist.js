/* @copyright: PT. Global Intermedia Nusantara; @author: anovsiradj; @version: 20190411, 201904, 201905, 201906; */
(function(unknown) {
// var $ = unknown;
var $ = $3 || $1 || $;
var omfg = window.spjskpd.omfg, dump = window.spjskpd.dump;
var forme = window.spjskpd.forme;
var debounce = window.spjskpd.debounce;
var tanggalin_id = window.spjskpd.tanggalin_id,tanggalin_iso = window.spjskpd.tanggalin_iso;
var rupiahin = window.spjskpd.rupiahin,rupiahin_parse = window.spjskpd.rupiahin_parse;

var jq_datatable = window.spjskpd.jq_datatable;
var jq_daterangepicker = window.spjskpd.jq_daterangepicker;

var $wait = $3('#container').children('.cover:first');

var prompts = {};
var dated = {
	min: window.spjskpd.min,
	max: window.spjskpd.max,
	current: window.spjskpd.current,
};

var tahun = window.spjskpd.tahun || null;
var bulan = (dated.current.getMonth() || 0) + 1; // bulan = bulan < 10 ? ['0',bulan].join('') : bulan;
// var bulan = 3; window.console.warn(`bulan(${bulan}):hardcoded;`);

var rupiahin_koma = window.spjskpd.rupiahin_koma || 2;
var isskpd = window.spjskpd.isskpd || 0;

var bku = document.getElementById('bku_spjskpd_table');
var bku_form = document.getElementById('bku_spjskpd_form');
var bku_extra = {
	delay: 300,
	height: (function() {
		var height = {
			w: window.innerHeight,
			navbar: document.body.querySelector('.navbar').offsetHeight,
			header: document.getElementById('container').querySelector('.header-konten').offsetHeight,
			form: bku_form.offsetHeight,
			thead: bku.querySelector('thead').offsetHeight,
			tfoot: bku.querySelector('tfoot').offsetHeight,
		};
		return (height.w -
			(
				height.navbar + height.header +
				height.thead + height.tfoot +
				height.form + 0
			)
		);
	})(),
	summary: {},
};

function jq_promptin(para) {
	return new BootstrapDialog($3.extend(true, {}, window.spjskpd.bs3dialog, para || {}));
}
function jq_tabelin(table, para) {
	return $1(table).DataTable($3.extend(true, {data: []}, window.spjskpd.datatable, para));
}

function jq_tanggalin(input,fn) {
	var exput = input.nextElementSibling;
	if (input.nextElementSibling && input.nextElementSibling.nodeName === 'INPUT') {
		$1(exput).daterangepicker({
			minDate: window.spjskpd.min,
			maxDate: window.spjskpd.max,
			singleDatePicker: true,
			calender_style: "picker_4",
		}, function(moment) {
			$(input).prop('value', moment.format('YYYY-MM-DD')).trigger('change');
		});

		$3(input).on('tanggalin', function(evt, dt) {
			// library KONTOL. method-e raono sing mlaku kabeh, iseh wae dinggo.
			// $(input.nextElementSibling).trigger('change'); $picker.updateView(); $picker.updateCalendars(); $picker.updateInputText(); $picker.updateFormInputs();
			if (typeof dt === 'string') dt = new Date(dt);
			// $1(exput).data('daterangepicker').setStartDate(dt);
			// $1(exput).data('daterangepicker').setEndDate(dt);
			// $1(exput).prop('value', $1(exput).data('daterangepicker').startDate.format($1(exput).data('daterangepicker').format));
			// $1(exput).data('daterangepicker').updateFromControl();
			var picker = $1(exput).data('daterangepicker');
			picker.setStartDate(dt);
			picker.setEndDate(dt);
			picker.updateInputText();
			picker.notify();
			picker.updateCalendars();
			$3(input).prop('value', tanggalin_iso(dt)).trigger('change'); // paksa
		});
	} //fi
} //fn
function jq_rupiahin(input) {
	var exput = input.nextElementSibling;
	if (input.nextElementSibling && input.nextElementSibling.nodeName === 'INPUT') {
		$3(exput).on('input', function() {
			input.value = rupiahin_parse(exput.value, rupiahin_koma);
		});
		$3(exput).on('focus', function() {
			exput.value = input.value;
			exput.setSelectionRange(0, input.value.length);
		});
		$3(exput).on('blur', function() {
			exput.value = rupiahin(Number(input.value), rupiahin_koma);
		});
		$3(input).on('rupiahin', function(evt, uang) {
			input.value = uang;
			exput.value = rupiahin(uang, rupiahin_koma); // .blur()
		});
	} //fi
} //fn

function jq_datatable_thead2columns(segments) {
	/*
	action_1 untuk update,delete,checkbox dan updown (update+delete)
	action_2 untuk kode_rekening,urai_rekening.
	action_3 untuk freetext rupiahin
	(canceled) action_4 untuk update+delete
	*/
	var tmp = {columns:[],actions:{},indexes:{}};
	for (var n in tmp) {
		if (segments[n] === unknown) {
			if ($(segments.table).data(n) === unknown) $(segments.table).data(n, tmp[n]);
			segments[n] = $(segments.table).data(n);
		}
	}
	segments.fn_init = segments.fn_init || $.noop;
	segments.fn_render = segments.fn_render || $.noop;
	segments.fn_callback = segments.fn_callback || $.noop;

	$(segments.table).children('thead').children('tr').children('th').each(function(i,thrcel) {
		var column = thrcel.dataset.column ? thrcel.dataset.column : null;

		var nullable = false;
		if (thrcel.dataset.nope == 1) nullable = true;
		if (segments.nullable_regex && segments.nullable_regex.test(column)) nullable = true;

		var styleClass = this.dataset.styleClass ? this.dataset.styleClass : '';
		var styleObject = this.dataset.styleObject ? eval(`(${this.dataset.styleObject})`) : {};
		if (column && thrcel.innerHTML.trim() === '') thrcel.innerText = column;

		var action_1 = null;
		if (segments.is_action_1) {
			if (/_action_/.test(column)) nullable = true;
			$(thrcel).children('[hidden]').each((i,action) => { if (action_1 === null) action_1 = action; });
		}

		if (segments.is_action_2) {
			segments.is_action_2_prefix = segments.is_action_2_prefix || segments.form_prefix || '__rincian__';
		}

		var action_3 = false;
		if (segments.is_action_3) {
			if (
				(segments.is_action_3_names && segments.is_action_3_names.indexOf(column) >= 0) ||
				(segments.is_action_3_regex && segments.is_action_3_regex.test(column)) ||
				false
			) action_3 = nullable = true;

			segments.is_action_3_prefix = segments.is_action_3_prefix || segments.form_prefix || '__rincian__';
			segments.is_action_3_editable = segments.is_action_3_editable || false;
		}

		segments.actions[column] = thrcel;
		segments.indexes[column] = thrcel.cellIndex;
		segments.columns.push({
			data: (nullable ? null : column),
			createdCell: (tbrcel, data, entry) => {
				segments.fn_init(column,tbrcel,data,entry);

				$(tbrcel).addClass(styleClass);
				$(tbrcel).css(styleObject);

				if (segments.is_action_1 && action_1 && /_action_/.test(column)) {
					$(action_1.cloneNode(true)).appendTo(tbrcel).removeAttr('hidden');
					if (/_update_/.test(column)) {
						$(tbrcel).find('button').on('click', event => segments.fn_action_1_update(entry));
					}
					if (/_updown_/.test(column)) {
						$(tbrcel).find('button').on('click', event => {
							var override;
							if (segments.fn_action_1_updown_rm) override = segments.fn_action_1_updown_rm(entry);
							if (override) return;

							var table = $(segments.table).data('table');
							table.row( $(event.currentTarget).parents('tr') ).remove();
							table.columns.adjust().draw();
						});
					}
				}
				if (segments.is_action_2 && /kode_rekening/.test(column) && !/urai_rekening/.test(column)) {
					for(var e in entry) {
						if (/rekening/.test(e) || !/kode/.test(e)) continue;
						tbrcel.appendChild(window.spjskpd.doxce('input', {
							type: 'hidden', name: `${segments.is_action_2_prefix}[${e}][]`, value: entry[e],
						}));
					}
				}
				if (segments.is_action_3 && action_3) {
					var colas;
					     if ($.isFunction(segments.is_action_3_alias)) colas = segments.is_action_3_alias(column,segments) || column;
					else if ($.isPlainObject(segments.is_action_3_alias)) {
						if ($.isFunction(segments.is_action_3_alias[column])) colas = segments.is_action_3_alias[column](segments,column);
						else colas = segments.is_action_3_alias[column] || column;
					}

					tbrcel.appendChild(window.spjskpd.doxce('span', {
						innerText: (window.spjskpd.rupiahin(entry[colas], window.spjskpd.rupiahin_koma)),
						contentEditable: segments.is_action_3_editable, className: 'freetext',
					}));
					tbrcel.appendChild(window.spjskpd.doxce('input', {
						type: 'hidden', name: `${segments.is_action_3_prefix}[${colas}][]`, value: entry[colas],
					}));

					if (segments.is_action_3_editable) {
						$(tbrcel).children('span.freetext:first')
						.on('keypress', function(event) {
							if (/Enter/.test(event.key)) event.preventDefault() || $(this).trigger('blur');
						})
						.on('input', function(event) {
							let rp = window.spjskpd.rupiahin_parse(this.innerText, window.spjskpd.rupiahin_koma);
							$(this).next().prop('value', rp);
							entry[colas] = rp;
						})
						.on('blur', function() {
							$(this).prop('innerText', window.spjskpd.rupiahin(entry[colas]), window.spjskpd.rupiahin_koma);
							$(this).next().prop('value', entry[colas]);

							var override;
							if (segments.fn_action_3_editable) override = segments.fn_action_3_editable(segments);
							if (override) return;

							$(segments.table).data('table').draw(false);
						});
					}
				}
			},
			render: (data,type,entry) => {
				var override = segments.fn_render(column,data,type,entry);
				if (override !== unknown) return override;

				if (nullable) return null;
				if (thrcel.dataset.coalesce && (data === unknown || data === null || String(data).trim() === '')) return thrcel.dataset.coalesce;
				if (/display/.test(type) && thrcel.dataset.type) {
					if (thrcel.dataset.type === 'rp') return window.spjskpd.rupiahin(data, rupiahin_koma);
					if (thrcel.dataset.type === 'dt') return window.spjskpd.tanggalin_id(data);
				}
				return data;
			},
		});

		if (segments.is_action_1 && /_action_/.test(column) && /_delete_|_checkbox_/.test(column)) {
			$(thrcel).children().each((i,action) => {
				if (action.hasAttribute('hidden')) return;
				$(action).find('input[type=checkbox]').each((i,xbox0) => {
					$(xbox0).on('change', event => {
						$(segments.table).data('table').column(thrcel.cellIndex).nodes()
						.to$().each((i,xbox1) => $(xbox1).find('input[type=checkbox]').prop('checked', xbox0.checked));
					});
				});
			});
		}
		if (segments.is_action_1 && /_action_/.test(column) && /_updown_/.test(column) && segments.fn_action_1_updown_mk) {
			$(thrcel).children().each((i,action) => {
				if (action.hasAttribute('hidden')) return;
				$(action).find('button').on('click', () => segments.fn_action_1_updown_mk(segments));
			});
		}
		segments.fn_callback(column,thrcel,segments);
	});
}
function jq_datatable_summaries(segments) {
	if(segments.data === unknown) segments.data = [];
	if(segments.tfoot === unknown && segments.tfrow) segments.tfoot = segments.tfrow.parentElement;
	if(segments.summaries === unknown) segments.summaries = {};
	if(segments.summaries.__main__ === unknown) {
		segments.summaries.__main__ = column => {
			if (segments.summaries[column] === unknown) {
				segments.summaries[column] = segments.data.map(n => (n[column] || 0)).reduce((a,b) => (Number(a) + Number(b)), 0);
			} else if ($.isFunction(segments.summaries[column])) {
				return segments.summaries[column](segments.summaries);
			}
			return (segments.summaries[column] || 0);
		};
	}

	$(segments.tfoot).find('[data-summary]').each((i,elem) => {
		$(elem).text( window.spjskpd.rupiahin(segments.summaries.__main__(elem.dataset.summary), window.spjskpd.rupiahin_koma) );
	});
}

jq_datatable_thead2columns({
	table: bku,
	is_action_1: true,
	fn_action_1_update: entry => $(bku).trigger('update', [entry,]),
});
$3(bku).data('table', $1(bku).DataTable($3.extend(true, {}, window.spjskpd.datatable, {
	data: [],
	scrollY: ((bku_extra.height + Number(bku.dataset.heightPlus)) - Number(bku.dataset.heightMinus)) || bku.dataset.height,
	columns: $3(bku).data('columns'),
	footerCallback: function(tfrow,data) {
		/*
		kalo saya liat di mxml nya, ada banyak fields pada result footer,
		kalo sekarang, saya liat, pada storproc, cuma ada saldolalu,tunaiini,bankini,berhargaini.
		jadi saya tidak tau, ini isi apa ...
		*/
		// bku_struct.summary.saldoini = (bku_struct.summary.tunaiini || 0) + (bku_struct.summary.bankini || 0) + (bku_struct.summary.berhargaini || 0);
		// bku_struct.summary.kaslalu = (bku_struct.summary.saldolalu || 0) + bku_struct.summary.selisih; // !?

		var summaries = {
			selisih: self => ( self.__main__('penerimaan') - self.__main__('pengeluaran') ),
		};
		for(var n in bku_extra.summary)
			if(summaries[n] === unknown)
				summaries[n] = Number(bku_extra.summary[n]) || 0;
		// 

		jq_datatable_summaries({
			data: data,
			tfoot: tfrow.parentElement,
			summaries: summaries,
		});
	},
})));

$3(bku).on('reload', function(event, data) {
	var table = $3(this).data('table');
	data = data || {}; data.tbody = data.tbody || []; data.tfoot = data.tfoot || {};

	for(var n in data.tfoot) bku_extra.summary[n] = Number(data.tfoot[n]) || 0;

	// hilang centang checkbox //
	var elem = $(bku).data('actions')['__action_delete__'];
	if (elem) $(elem).find('input[type=checkbox]').prop('checked', false);

	table.clear();
	table.rows.add(data.tbody);

	var search = (forme(bku_form, 'search', 'value') || '').trim();
	// var search = 'gu'; window.console.warn(`search(${search}):hardcoded;`);

	table.search(search).columns.adjust().draw();
});

$(bku_form).on('submit', function(event) {
	event.preventDefault();

	$3(bku).trigger('reload', []);
	forme(bku_form, 'search', 'value', '');

	if (!kodeskpd || !bulan) return;

	$wait.show();
	$.get(bku_form.action, $.extend({}, kodeskpd, {tahun: tahun, bulan: bulan, }), function(data) {
		$3(bku).trigger('reload', [data,]);
	}).fail(function() {
		omfg('tidak bisa ambil bku.', arguments);
	}).always(() => $wait.hide());
});
forme(bku_form, 'search', search => {
	$(search).on('input', debounce(() => {
		$(bku).data('table').search( search.value.trim() ).draw();
	}, bku_extra.delay));
});
forme(bku_form, 'month', month => {
	month.value = bulan;

	$(month).on('change', event => {
		bulan = Number(month.value);
		// [DEPRECATED] jangan rubah bulan, karena membuat dated.current tidak consistent. //
		// supaya semua tanggal pada module berada pada bulan yang sama //
		/*
		dated.current.setMonth(bulan-1);
		if (dated.current.getFullYear() != tahun) {
			dated.current.setFullYear(tahun);
			dated.current.setMonth(bulan-1);
		}
		*/
		$(bku_form).trigger('submit');
	}).trigger('change');
});

$3(bku).on('update', function(evt, entry) {
	if (pergeseran_extra.jenisjenis.indexOf(entry.jenis_bku) >= 0)
		$3(pergeseran).trigger('prompt', [1,entry,]);

	else if(/SP(2|J)/.test(entry.jenis_bku) && /UP|GU/.test(entry.jenis_sp2d))
		$3(xupgux).trigger('prompt', [1,entry,]);

	else if(/SP(2|J)/.test(entry.jenis_bku) && /TU/.test(entry.jenis_sp2d))
		$3(xtux).trigger('prompt', [1,entry,]);

	else if(/SP(2|J)/.test(entry.jenis_bku) && /LS/.test(entry.jenis_sp2d))
		$(barjas).trigger('prompt', [1,entry,]);

	else if(/SP2D|BAYAR/.test(entry.jenis_bku) && /GJ/.test(entry.jenis_sp2d))
		$3(xlsgjx).trigger('prompt', [1,entry,]);

	else if(/PUNGUT|SETOR/.test(entry.jenis_bku) && /PAJAK/.test(entry.jenis_bku) && /GU|TU|LS|GJ/.test(entry.jenis_sp2d))
		$3(pajak).trigger('prompt', [1,entry,]);

	else if(entry.jenis_bku === rkppkd_extra.jenis_bku) $(rkppkd).trigger('prompt', [1,entry,]);
	else if(entry.jenis_bku === 'SALDOAWAL') $(saldoawal).trigger('prompt', [1,entry,]);
	else if(entry.jenis_bku === 'PANJAR') $(panjar).trigger('prompt', [1,entry,]);

	else if(false) return;

	else message_ok('error', 'tidak bisa ubah, form belum ada.');
});
$3(bku).on('delete', () => console.warn('bku@delete() deprecated.'));

var kodeskpd = null;
var kodeskpd_index = null;
$1('#kd_org2').on('change', function() {
	var temp = this.value.trim();
	// var temp = '4.1.04'; window.console.warn(`kodeskpd(${temp}):hardcoded;`);
	// var temp = '4.4.05'; window.console.warn(`kodeskpd(${temp}):hardcoded;`); // upgu create
	// var temp = '4.1.03'; window.console.warn(`kodeskpd(${temp}):hardcoded;`); // upgu update
	// var temp = '1.2.01'; window.console.warn(`kodeskpd(${temp}):hardcoded;`); // lsgj create
	// var temp = '1.1.01'; window.console.warn(`kodeskpd(${temp}):hardcoded;`); // lsgj update
	// var temp = '2.5.01'; window.console.warn(`kodeskpd(${temp}):hardcoded;`); // barjas create
	// var temp = '1.5.02'; window.console.warn(`kodeskpd(${temp}):hardcoded;`); // tu create

	if (temp === '') kodeskpd = kodeskpd_index = null;
	else {
		kodeskpd_index = temp.split('.');
		kodeskpd = { kodeurusan: kodeskpd_index[0], kodesuburusan: kodeskpd_index[1], kodeorganisasi: kodeskpd_index[2], kodeunit: kodeskpd_index[3]};
		$3(bku_form).trigger('submit');
	}
}).trigger('change'); // kodeskpd

$3('#bku_spjskpd_prompts_trigger').find('button[data-prompt]').each(function() {
	$3(this).on('click', function() {
		if (!kodeskpd) return message_ok('error', 'SKPD belum dipilih.');

		if (/destroy/.test(this.dataset.prompt)) {
			var i = $(bku).data('indexes')['__action_delete__'];
			var t = $(bku).data('table');
			var e = [];
			t.column(i).nodes().to$().each((i,elem) => {
				if ($(elem).find('input[type=checkbox]').prop('checked')) e.push(t.row(elem.parentElement).data());
			});
			if (e.length > 0) rm(e);
			else message_ok('error', 'belum ada BKU yang di centang');
			return;
		}

		if (prompts[this.dataset.prompt])$3(prompts[this.dataset.prompt]).trigger('prompt', [0,]);
		else message_ok('error', 'tidak bisa, belum ada.');
	});
});

function rm(entry_entries) {
	var no_bku, text;

	if ($3.isArray(entry_entries) && entry_entries.length === 1) entry_entries = entry_entries[0];

	if ($3.isArray(entry_entries))
	     no_bku = entry_entries.map(entry => entry.no_bku).join(',');
	else no_bku = entry_entries.no_bku;

	if ($3.isArray(entry_entries))
	     text = 'Anda yakin hapus BKU yang dicentang ?';
	else text = `Anda yakin hapus BKU nomor <b>${entry_entries.no_bku}</b> ?`;

	var para = $3.extend({
		tahun: tahun,
		isskpd: isskpd,
		no_bku: no_bku,
		csrfmiddlewaretoken: window.spjskpd.kuki('csrftoken'),
	}, kodeskpd);

	$1.alertable.confirm(text, window.spjskpd.alertable_rm).then(function(result) {
		$wait.show();
		$3.post(window.spjskpd.href_rm, para, () => $(bku_form).trigger('submit'))
		.fail(function() { omfg('tidak bisa hapus bku.', arguments); })
		.always(() => $wait.hide());
	});
}

function nobkuauto(ye,na,hmm) {
	$wait.show();
	$3.get(window.spjskpd.href_nobkuauto, $3.extend({tahun: tahun, isskpd: isskpd}, kodeskpd), function(no_bku) {
		$wait.hide(); if (ye) ye(no_bku);
	})
	.fail(function() {
		$wait.hide(); omfg('tidak bisa ambil no_bku terakhir.', arguments); if(na) na();
	})
	.always(function() { if(hmm) hmm(); });
}

var potongan = document.getElementById('spjskpd_pengeluaran_potongan');
var potongan_extra = {
	once: true,
	reload: true,
	params: {},
	callback: [],
	'z-index': null,
};

$(potongan).data('columns', []);
$(potongan).find('table:first').children('thead').children('tr').children('th').each(function() {
	$(potongan).data('columns').push({ data: this.dataset.field, });
});

$(potongan).data('prompt', jq_promptin({
	title: potongan.dataset.promptTitle,
	onshow: function($self) {

		/* commit:aaaf6f9fe47836e15c8a7e460e2b457d52ca25b7; */
		for (var i in window.BootstrapDialog.dialogs)
			if (window.BootstrapDialog.dialogs[i].opened)
				potongan_extra['z-index'] = Number(window.BootstrapDialog.dialogs[i].$modal.css('z-index') || 0);

		$self.getModalDialog().css({ width: potongan.dataset.promptWidth });

		if (potongan_extra.once) {
			$self.getModalBody().append(potongan);

			$(potongan).data('table', jq_tabelin(potongan.querySelector('table'), {
				dom: 'ft',
				columns: $(potongan).data('columns'),
				scrollY: potongan.dataset.tableHeight,
				createdRow: function(tbrow, entry) {
					$(tbrow).on('dblclick', function() {
						$(potongan).data('prompt').close();
						potongan_extra.callback.forEach(callback => callback(entry));
					});
				},
			}));
		}
	},
	onshown: function($self) {
		// commit:aaaf6f9fe47836e15c8a7e460e2b457d52ca25b7; //
		var a = potongan_extra['z-index'], b = Number($self.getModal().css('z-index') || 0);
		if (b <= a) $self.getModal().css('z-index', a+1);

		if (potongan_extra.reload) {
			$(potongan).data('table').clear().draw();

			$wait.show();
			$.get(potongan.dataset.href, $.extend(true, {tahun:tahun}, potongan_extra.params), result => {
				$wait.hide();
				$(potongan).data('table').rows.add(result);
				$(potongan).data('table').columns.adjust().draw();
			}).fail(function() {
				$wait.hide(); omfg('tidak bisa ambil rekening.', arguments);
			});
		}
	},
	onhidden: function() {
		potongan_extra.once = false;
		potongan_extra.reload = false;
		potongan_extra.params = {};
		potongan_extra.callback.splice(0,potongan_extra.callback.length);
	},
}));

$(potongan).on('prompt', function(event) {
	for (var i = 1; i < arguments.length; i++) {
		if ($.isFunction(arguments[i])) potongan_extra.callback.push(arguments[i]);
		if ($.isPlainObject(arguments[i])) $.extend(true, potongan_extra.params, arguments[i]);
	}
	$(potongan).data('prompt').open();
});
var laporan = prompts['laporan'] = document.getElementById('sipkd_spjskpd_laporan');
var laporan_bulan;
var laporan_pejabatpejabat = {};
var laporan_jenisjenis = window.spjskpd.laporan_jenisjenis;
var laporan_cfg = {
	prompt_once: true,
	iframe_once: true,
};

forme(laporan, 'username', 'value', window.spjskpd.squote(window.spjskpd.username));

forme(laporan, 'TGLCETAK', TGLCETAK => jq_daterangepicker(TGLCETAK));
forme(laporan, 'PERIODEAWAL', PERIODEAWAL => jq_daterangepicker(PERIODEAWAL));
forme(laporan, 'PERIODEAKHIR', PERIODEAKHIR => jq_daterangepicker(PERIODEAKHIR));

forme(laporan, 'bulan', function(input) {
	$3(input).on('change', function() {
		laporan_bulan = Number(this.value);

		// MAKSUDNYA TANGGAL AKHIR PADA BULAN, DALAM FORMAT:ID //
		forme(laporan, 'tglakhir', function(tglakhir) {
			tglakhir.value = tanggalin_id(new Date(tahun, laporan_bulan+0, 0));
		});
	});
});

forme(laporan, '__jenis__', function(__jenis__) {
	$3(__jenis__).on('change', function() {
		forme(laporan, 'file', function(file) {
			file.value = laporan_jenisjenis[__jenis__.value].fr3;
		});

		if (laporan_jenisjenis[__jenis__.value].jenis)
			$3(laporan).find('.idspj:first').show();
		else
			$3(laporan).find('.idspj:first').hide();
	}).trigger('change');
});


$3(laporan).data('pejabatin', ['idpa','id']);
$3(laporan).data('pejabatin').forEach(function(nama) {
	forme(laporan, nama, function(input) {
		$3(input).on('change', function() {
			$3(this).parentsUntil('.row', '.' + input.name).find('input').each(function() {
				if (this.dataset.source) {
					this.value = laporan_pejabatpejabat[String(kodeskpd_index)][Number(input.value)][this.dataset.source];
				}
			});
		});
	});
});

$3(laporan).data('prompt', new BootstrapDialog($3.extend(true, {}, window.spjskpd.bs3dialog, {
	title: laporan.dataset.promptTitle,
	onshow: function(self) {
		self.getModalBody().parents('.modal-dialog').css('width', laporan.dataset.promptWidth);
		if (laporan_cfg.prompt_once) {
			self.getModalBody().append(laporan);
		}

		forme(laporan, 'bulan', function(input) {
			$3(input).prop('value', bulan).trigger('change');
		});

		forme(laporan, 'TGLCETAK', function(input) {
			var picker = $1(input).data('daterangepicker');
			// picker.setStartDate(new Date);
			// picker.setEndDate(new Date);
			// picker.startDate.set('month', laporan_bulan-1); // 0:index
			// picker.endDate.set('month', laporan_bulan-1); // 0:index
			picker.updateInputText();
			picker.notify();
			picker.updateCalendars();
			// input.value = picker.startDate.format(picker.format);
		});
		forme(laporan, 'PERIODEAWAL', function(input) {
			var picker = $1(input).data('daterangepicker');
			// picker.setStartDate(new Date);
			// picker.setEndDate(new Date);
			// picker.startDate.set('month', laporan_bulan-1); // 0:index
			// picker.endDate.set('month', laporan_bulan-1); // 0:index
			picker.updateInputText();
			picker.notify();
			picker.updateCalendars();
			// input.value = picker.startDate.format(picker.format);
		});
		forme(laporan, 'PERIODEAKHIR', function(input) {
			var picker = $1(input).data('daterangepicker');
			// picker.setStartDate(new Date);
			// picker.setEndDate(new Date);
			// picker.startDate.set('month', laporan_bulan-1); // 0:index
			// picker.endDate.set('month', laporan_bulan-1); // 0:index
			picker.updateInputText();
			picker.notify();
			picker.updateCalendars();
			// input.value = picker.startDate.format(picker.format);
		});
	},
	onhide: function() {
		forme(laporan, '__jenis__', function(input) {
			input.selectedIndex = 0;
			$3(input).trigger('change');
		});
	},

	onhidden: function() {
		laporan_cfg.prompt_once = false;
	},
}))); // data:prompt

$3(laporan).on('prompt', function() {
	$3(laporan).data('pejabatin').forEach(function(name) {
		forme(laporan, name, function(input) {
			$3(input).children().remove();
		});
	});

	function pejabatin(name) {
		forme(laporan, name, function(input) {
			laporan_pejabatpejabat[String(kodeskpd_index)].forEach(function(entry) {
				var bend = /BENDAHARA/.test(entry.jabatan.toUpperCase());
				if (/idpa/.test(name)) { if(bend) return; }
				else if (bend === false) return;

				var element = document.createElement('option');
				element.innerText = [entry.jabatan,entry.nama].join(' / ');
				element.value = entry.id;
				input.appendChild(element);
			});
			$3(input).trigger('change');
		});
	}

	if (kodeskpd) {
		for(var k in kodeskpd) {
			forme(laporan, k, function(input) {
				if (k === 'kodeorganisasi' || k === 'kodeunit') input.value = window.spjskpd.squote(kodeskpd[k]);
				else input.value = kodeskpd[k];
			});
		}
		if (!laporan_pejabatpejabat[String(kodeskpd_index)]) {
			$3.get(window.spjskpd.href_pejabat, $3.extend({}, kodeskpd, {tahun:tahun}), function(result) {
				laporan_pejabatpejabat[String(kodeskpd_index)] = [];
				for (var i = 0; i < result.length; i++) laporan_pejabatpejabat[String(kodeskpd_index)][Number(result[i].id)] = result[i];
				$3(laporan).data('pejabatin').forEach(pejabatin);
			}).fail(function() {
				window.alert('tidak bisa ambil data pejabat.\n' + window.JSON.stringify(arguments));
			});
		} else $3(laporan).data('pejabatin').forEach(pejabatin);
	}

	$3(laporan).data('prompt').open();
}); // on:prompt

$3(laporan).data('iframe', jq_promptin({
	title: laporan.dataset.iframeTitle,
	onshow: function(iframe) {
		if (laporan_cfg.iframe_once) {
			iframe.getModalDialog().css({width: laporan.dataset.iframeWidth, height: laporan.dataset.iframeHeight});
			iframe.getModalContent().css({height: '100%'});
			iframe.getModalBody().css({margin: 0, padding: 0, height: laporan.dataset.iframeHeight});
		}
	},
	onshown: function(iframe) {
		var elem;
		elem = document.createElement('iframe');
		elem.setAttribute("frameborder", 0);
		elem.style.width  = '100%';
		elem.style.height = '100%';
		elem.setAttribute('src', laporan_cfg.href);
		iframe.getModalBody().append(elem);
	},
	onhide: function(iframe) {
		iframe.getModalBody().children().remove();
	},
	onhidden: function() {
		laporan_cfg.iframe_once = false;
	},
}));

$3(laporan).on('submit', function(event) {
	laporan_cfg.href = laporan.dataset.iframeHref + '&' + $3(laporan).serialize();

	event.preventDefault();

	var title;
	forme(laporan, '__jenis__', function(__jenis__) {
		if (__jenis__.children[__jenis__.selectedIndex]) {
			title = __jenis__.children[__jenis__.selectedIndex].innerText;
		}
	});

	$3(laporan).data('iframe').setTitle(title);
	$3(laporan).data('iframe').open();
});
var pergeseran_extra = {
	once: true,
	jenisjenis: [],
	required: ['no_bku', 'bukti','urai'],
	bukti_suggest: document.getElementById('spjskpd_pengeluaran_pergeseran_bukti_suggest'),
};
var pergeseran = prompts['pergeseran'] = document.getElementById('bku_spjskpd_pergeseran');

$(pergeseran).data('tanggalin', ['tgl_bku', 'tgl_bukti']);
$(pergeseran).data('tanggalin').forEach(name => forme(pergeseran, name, elem => jq_tanggalin(elem)));

$(pergeseran).data('rupiahin', ['penerimaan', 'pengeluaran']);
$(pergeseran).data('rupiahin').forEach(name => forme(pergeseran, name, elem => {
	$(elem).next().on('keypress', event => {
		if (/Enter/.test(event.key)) { event.preventDefault(); $(event.currentTarget).trigger('blur'); }
	});
	jq_rupiahin(elem);
}));

forme(pergeseran, 'jenis_bku', jenis_bku => {
	$(jenis_bku.children).each((i,elem) => {
		pergeseran_extra.jenisjenis.push(elem.value.trim());
	});
	forme(pergeseran, 'simpananbank', simpananbank => {
		$(jenis_bku).on('change', () => {
			simpananbank.value = jenis_bku.selectedIndex; /* sesuai flex, pakai index */
		}).trigger('change');
	});
});

$(pergeseran).data('prompt', new BootstrapDialog($3.extend(true, {}, window.spjskpd.bs3dialog, {
	title: pergeseran.dataset.promptTitle,
	onshow: self => {
		if (pergeseran_extra.once) self.getModalBody().append(pergeseran);
		self.getModalDialog().css('width', pergeseran.dataset.promptWidth);

		if (pergeseran_extra.bukti_suggest) {
			$(pergeseran_extra.bukti_suggest).children().remove();
			$(bku).data('table').data()
			.toArray().map(e => e.bukti)
			.filter((e,i,a) => ( a.indexOf(e) === i ))
			.forEach(bukti => pergeseran_extra.bukti_suggest.appendChild(window.spjskpd.doxce('option', {'value': bukti})));
		}
	},
	onhidden: self => {
		if (pergeseran_extra.bukti_suggest) $(pergeseran_extra.bukti_suggest).children().remove();

		pergeseran_extra.once = false;
		$(pergeseran).trigger('reset');
	},
}))); // data:prompt

$3(pergeseran).on('prompt', function(event, __type__, entry) {
	var query = $3.extend({tahun: tahun, isskpd: isskpd}, kodeskpd);
	for(var q in query) forme(this, q, function(input) { input.value = query[q]; });

	forme(pergeseran, '__type__', 'value', __type__);
	forme(pergeseran, 'csrfmiddlewaretoken', 'value', window.spjskpd.kuki('csrftoken'));

	forme(pergeseran, 'no_bku', 'readOnly', __type__ === 1);

	if (__type__ === 0) {
		$wait.show();
		$3.get(window.spjskpd.href_nobkuauto, query, function(result) {
			forme(pergeseran,'no_bku', 'value', result);
		}).fail(function() {
			omfg('gagal ambil no_bku terakhir.', arguments);
		}).always(() => {
			$wait.hide();
			$3(pergeseran).data('prompt').open();
		});
	}

	if (__type__ === 1) {
		for(var e in entry) {
			if ($3.inArray(e, $3(this).data('tanggalin')) >= 0 || $3.inArray(e, $3(this).data('rupiahin')) >= 0) continue;
			forme(pergeseran, e, elem => $(elem).prop('value', entry[e]));
		}
		$3(pergeseran).data('prompt').open();
	}

	$3(this).data('tanggalin').forEach(function(name) {
		forme(pergeseran,name, function(input) {
			$3(input).trigger('tanggalin', (entry && name in entry) ? entry[name] : dated.current);
		});
	});
	$3(this).data('rupiahin').forEach(function(name) {
		forme(pergeseran,name, function(input) {
			$3(input).trigger('rupiahin', (entry && name in entry) ? entry[name] : 0);
		});
	});
}); // on:prompt

$3(pergeseran).on('submit', function(event) {
	// return;
	event.preventDefault();

	var yn = false;
	pergeseran_extra.required.forEach(name => {
		if (yn) return;
		var value = forme(pergeseran, name, 'value');
		if (!value || value.trim() === '') {
			yn = true;
			message_ok('error', `Isian ${name.toUpperCase()} Tidak Boleh Kosong.`);
		}
	});
	if (yn) return;

	if (
		Number(forme(pergeseran, 'tgl_bku', 'value', v => v.replace(/[^0-9]/g, ''))) <
		Number(forme(pergeseran, 'tgl_bukti', 'value', v => v.replace(/[^0-9]/g, '')))
	) {
		return message_ok('error', 'TGL_BKU tidak boleh kurang dari TGL_BUKTI.');
	}

	$3.post(this.action, $3(this).serialize(), function() {
		$3(pergeseran).data('prompt').close();
		$3(bku_form).trigger('submit');
	}).fail(function() {
		omfg('tidak bisa simpan bku.', arguments);
	});
});

$3(pergeseran).on('reset', () => {
	$(pergeseran).data('prompt').isOpened() && $(pergeseran).data('prompt').close();
}); // on:reset

// $(document).ready(() => $(pergeseran).trigger('prompt', [0,])); // [LINT] //
var saldoawal = prompts['saldoawal'] = document.getElementById('spjskpd_pengeluaran_saldoawal');
var saldoawal_extra = {
	required: ['no_bku', 'bukti', 'urai'],
	jenis_bku: forme(saldoawal, 'jenis_bku', 'value'),
	force: {
		jenis_bku: forme(saldoawal, 'jenis_bku', 'value'),
		jenis_sp2d: forme(saldoawal, 'jenis_sp2d', 'value'),
	},
	once: true,
};

forme(saldoawal, '__money__', function(__money__) {
	$3(__money__).on( 'change', event => forme(saldoawal, 'simpananbank', 'value', __money__.value) ).trigger('change');
});

$(saldoawal).data('tanggalin', ['tgl_bku', 'tgl_bukti']);
$(saldoawal).data('tanggalin').forEach(name => forme(saldoawal, name, elem => jq_tanggalin(elem)));

$(saldoawal).data('rupiahin', ['penerimaan', 'pengeluaran']);
$(saldoawal).data('rupiahin').forEach(name => forme(saldoawal, name, elem => {
	jq_rupiahin(elem);
	$(elem).next().on('keypress', event => {
		if (/Enter/.test(event.key)) { event.preventDefault(); $(event.currentTarget).trigger('blur'); }
	});
}));

$3(saldoawal).data('prompt', new BootstrapDialog($3.extend(true, {}, window.spjskpd.bs3dialog, {
	title: saldoawal.dataset.promptTitle,
	onshow: function(self) {
		if (saldoawal_extra.once) self.getModalBody().append(saldoawal);
		self.getModalDialog().css('width', saldoawal.dataset.promptWidth);
	},
	onhidden: function(self) {
		$(saldoawal).trigger('reset');
		saldoawal_extra.once = false;
	},
})));

$3(saldoawal).on('prompt', function(event, __type__, entry) {
	var query = $3.extend({tahun: tahun, isskpd: isskpd}, kodeskpd);
	for(var n in query) forme(saldoawal, n, 'value', query[n]);

	forme(saldoawal, 'no_bku', 'readOnly', __type__ === 1);

	if (__type__ === 0) {
		nobkuauto(
			function(no_bku) {
				forme(saldoawal, 'no_bku', 'value', no_bku);
				$3(saldoawal).data('prompt').open();
			},
			function() {
				$3(saldoawal).data('prompt').open();
			}
		);
	}

	if (__type__ === 1) {
		for(var e in entry) {
			if ($(this).data('tanggalin').indexOf(e) > -1) continue;
			if ($(this).data('rupiahin').indexOf(e) > -1) continue;
			forme(saldoawal, e, 'value', entry[e]);
		}
		forme(saldoawal, '__money__', 'value', forme(saldoawal, 'simpananbank', 'value'));

		$3(saldoawal).data('prompt').open();
	}

	forme(this, 'csrfmiddlewaretoken', 'value', window.spjskpd.kuki('csrftoken'));

	$3(this).data('tanggalin').forEach(function(name) {
		forme(saldoawal,name, function(input) {
			$3(input).trigger('tanggalin', (entry && name in entry) ? entry[name] : dated.current);
		});
	});
	$3(this).data('rupiahin').forEach(function(name) {
		forme(saldoawal,name, function(input) {
			$3(input).trigger('rupiahin', (entry && name in entry) ? entry[name] : 0);
		});
	});

	forme(saldoawal, '__type__', 'value', __type__);
});
$3(saldoawal).on('submit', function(event) {
	// return;
	event.preventDefault();

	var yeet = false;
	saldoawal_extra.required.forEach(name => forme(saldoawal, name, function(elem) {
		if (yeet) return;
		if (elem.value.trim() === '') {
			yeet = true;
			message_ok('error', `Isian ${name.toUpperCase()} Tidak Boleh Kosong.`);
		}
	}));
	if (yeet) return;

	if (Number(forme(saldoawal, 'tgl_bku', 'value', v => v.replace(/[^0-9]/g, ''))) < Number(forme(saldoawal, 'tgl_bukti', 'value', v => v.replace(/[^0-9]/g, '')))) {
		return message_ok('error', 'TGL_BKU tidak boleh kurang dari TGL_BUKTI.');
	}

	$.post(saldoawal.action, $3(this).serialize(), function() {
		$(saldoawal).data('prompt').close();
		forme(bku_form, 'month', function(month) {
			$(month)
			.prop('value', forme(saldoawal,'tgl_bku','value', v => Number( v.split('-')[1] )))
			.trigger('change');
		});
	}).fail(function() {
		omfg(`terjadi error saat simpan ${saldoawal_extra.jenis_bku}.`, arguments);
	});
});
$3(saldoawal).on('reset', function() {
	$3(this).data('prompt').isOpened() && $3(this).data('prompt').close();
});

// $(document).ready(() => ( kodeskpd && $(saldoawal).trigger('prompt', [0,]) )); // [TEST] //
var xupgux_extra = {
	jenis_bku_label: document.getElementById('spjskpd_upgu_jenis_bku_label'),
	jenis_bku_create_clear: ['bukti','urai','tgl_bku','tgl_bukti'],
	required: ['no_bku', 'bukti','urai'],
	tjumlahf: null,
	is_penerimaan_re: /SP2D/, 
	is_penerimaan: null,

	/* [TODO][REWRITE][FUTURE]: JS => HTML; */
	browse: {
		SP2D: window.spjskpd.datatable_parse({
			tbody: [
				{
					data: 'nosp2d',
					createdCell: function(tbrcel) { $3.extend(tbrcel.style, {'white-space': 'nowrap'}); },
				},
				{
					data: 'tanggal',
					createdCell: function(tbrcel) { $3.extend(tbrcel.style, {'white-space': 'nowrap'}); },
					render: function(data,type) { return (/display|filter/.test(type) ? tanggalin_id(data) : data); },
				},
				{
					data: 'tglkasda',
					render: function(data,type) {
						if (/display/.test(type) && data === null) return '<div class="text-muted text-center">(belum cair)</div>';
						return data;
					},
				},
				{data: 'namayangberhak'},
				{data: 'informasi'},
				{
					data: 'nospm',
					createdCell: function(tbrcel) { $3.extend(tbrcel.style, {'white-space': 'nowrap'}); },
				},
				{
					data: 'jumlah',
					createdCell: function(tbrcel) { $3.extend(tbrcel.style, {'text-align': 'right'}); },
					render: function(data,type) { return (/display/.test(type) ? rupiahin(Number(data), rupiahin_koma) : Number(data)); },
				},
			],
		}),
		SPJ: window.spjskpd.datatable_parse({
			tbody: [
				{data: 'nospj'},
				{
					data: 'tglspj',
					createdCell: function(tbrcel) { $3.extend(tbrcel.style, {'white-space': 'nowrap'}); },
					render: function(data,type) { return (/display|filter/.test(type) ? tanggalin_id(data) : data); },
				},
				{data: 'keperluan'},
				{
					data: 'jumlah',
					createdCell: function(tbrcel) { $3.extend(tbrcel.style, {'text-align': 'right'}); },
					render: function(data,type) { return (/display/.test(type) ? rupiahin(Number(data), rupiahin_koma) : Number(data)); },
				},
			],
		}),
	},
};

var xupgux = prompts['xupgux'] = document.getElementById('spjskpd_pengeluaran_upgu');
var xupgux_rincian = document.getElementById('spjskpd_pengeluaran_upgu_rincian');
var xupgux_potongan = document.getElementById('spjskpd_pengeluaran_upgu_potongan');

$3(xupgux).data('tanggalin', ['tgl_bku', 'tgl_bukti']);
$3(xupgux).data('tanggalin').forEach(name => forme(xupgux, name, elem => jq_tanggalin(elem)));

$(xupgux).data('centangin', ['simpananbank','is_pihak_ketiga']);
$(xupgux).data('centangin').forEach(name => {
	forme(xupgux, name, a => {
		if (a.dataset.against) {
			forme(xupgux, a.dataset.against, b => {
				$(a).on('change', () => {
					if (a.checked) $(b).prop('checked', false).trigger('change');
				});
			});
		}
	});
});

forme(xupgux, 'jenis_bku', function(jenis_bku) {
	$3(jenis_bku).on('change', function() {
		xupgux_extra.jenis_bku = jenis_bku.value;
		xupgux_extra.is_penerimaan = xupgux_extra.is_penerimaan_re.test(xupgux_extra.jenis_bku);
		xupgux_extra.tjumlahf = xupgux_extra.is_penerimaan ? 'penerimaan' : 'pengeluaran';

		if (xupgux_extra.jenis_bku_label) {
			var tmp = xupgux_extra.jenis_bku_label;
			tmp.innerText = jenis_bku.value || tmp.dataset.default;
		}

		$(xupgux_rincian).trigger('reload', [[],]);
		$(xupgux_potongan).trigger('reload', [[],]);

		forme(xupgux, '__type__', function(__type__) {
			if (__type__.value == 0) {
				xupgux_extra.jenis_bku_create_clear.forEach(function(name) {
					if ($(xupgux).data('tanggalin').indexOf(name) > -1)
						forme(xupgux, name, elem => $(elem).trigger('tanggalin', dated.current));
					else
						forme(xupgux, name, elem => $(elem).prop('value','').trigger('change'));
				});
			}
		}); // __type__
	}); // on:change
}); // jenis_bku

forme(xupgux, 'bukti_trigger', function(bukti_trigger) {
	$3(bukti_trigger).on('click', function() {
		var
		table,
		jenis_bku = forme(xupgux, 'jenis_bku', 'value'),
		para = $3.extend(true, {
			tahun: tahun,
			jenis_bku: jenis_bku,
		}, kodeskpd);

		table = document.createElement('table');
		table.setAttribute('id', xupgux.id + '_bukti_trigger_table_' + jenis_bku);
		table.setAttribute('class', 'display responsive nowrap select_tabel sipkd-spjskpd sipkd-spjskpd-prompt');

		jq_promptin({
			autodestroy: true,
			onshow: function(self) {
				if (bukti_trigger.dataset.promptWidth) self.getModalDialog().css('width', bukti_trigger.dataset.promptWidth);
				if (xupgux_extra.jenis_bku_label) self.setTitle(xupgux_extra.jenis_bku_label.parentElement.innerText);

				self.getModalBody().append(table);
			},
			onshown: function(self) {
				var $prompt = self, browse_trigger, browse_columns;
				browse_columns = $3.extend(true, {} ,xupgux_extra.browse[jenis_bku]).tbody;

				$3(table).data('table', jq_tabelin(table, {
					dom: 'ft',
					ordering: true,
					scrollY: bukti_trigger.dataset.tableHeight,
					columns: browse_columns,
					createdRow: function(tbrow,entry) {
						$(tbrow).css('cursor','pointer');
						$(tbrow).on('dblclick', function() {
							$3(xupgux).trigger('browsed', [entry,]);
							$prompt.close();
						});
					},
				}));

				$wait.show();
				$3.get(bukti_trigger.dataset.href, para, function(result) {
					for (var i = 0; i < result.length; i++) $3(table).data('table').row.add(result[i]);
				}).fail(function() {
					window.alert('tidak bisa ambil bukti.' + '\n' + window.JSON.stringify(arguments));
				}).always(function() {
					$wait.hide();
					$3(table).data('table').draw().columns.adjust().draw();
				});
			},
			onhidden: function() {
				$3(table).data('table').destroy();
				$3(table).remove();
			},
		}).open(); // jq_promptin
	}); // on:click
}); // bukti_trigger

$3(xupgux).data('prompt', new BootstrapDialog($3.extend(true, {}, window.spjskpd.bs3dialog, {
	title: xupgux.dataset.promptTitle,
	onshow: function(self) {
		self.getModalBody().parentsUntil('.modal', '.modal-dialog').css('width', xupgux.dataset.promptSize);
		self.getModalBody().append(xupgux);
	},
	onshown: function(self) {
		$3(xupgux_rincian).data('table').draw();
		$3(xupgux_potongan).data('table').draw();
	},
	onhidden: function(self) {
		$3(xupgux).trigger('reset');
	},
	onhide: function() {
		$(xupgux_rincian).trigger('reload', [[],]);
		$(xupgux_potongan).trigger('reload', [[],]);
	},
}))); // :data:prompt

$3(xupgux).on('prompt', function(event, __type__, entry) {
	forme(xupgux, '__type__', 'value', __type__);
	forme(xupgux, 'csrfmiddlewaretoken', 'value', window.spjskpd.kuki('csrftoken'));
	forme(xupgux, 'tahun', 'value', tahun);
	for(var n in kodeskpd) forme(xupgux, n, 'value', kodeskpd[n]);

	forme(xupgux, 'no_bku', 'readOnly', __type__ === 1);
	forme(xupgux, 'bukti_trigger', 'disabled', __type__ === 1);
	forme(xupgux, 'jenis_bku', function(jenis_bku) {
		$3(jenis_bku).children().prop('disabled', false);
		jenis_bku.selectedIndex = 0;
		if (__type__ === 1) {
			jenis_bku.value = entry.jenis_bku;
			$3(jenis_bku).children().each(function(i,elem) {
				if (elem.value !== entry.jenis_bku) elem.disabled = true;
			});
		}
		$3(jenis_bku).trigger('change');
	});

	$(xupgux).data('tanggalin').forEach(name => forme(xupgux, name, elem => $(elem).trigger('tanggalin', dated.current)));
	forme(xupgux, 'simpananbank', simpananbank => $(simpananbank).prop('checked', true).trigger('change'));

	if (__type__ === 0) {
		$wait.show();
		$3.get(window.spjskpd.href_nobkuauto, $3.extend({tahun: tahun, isskpd: isskpd}, kodeskpd), function(no_bku) {
			forme(xupgux, 'no_bku', 'value', no_bku);
		}).fail(function() {
			omfg('tidak bisa ambil no_bku terakhir.', arguments);
		}).always(function() {
			$wait.hide(); $3(xupgux).data('prompt').open();
		});
	}

	if (__type__ === 1) {
		$3(xupgux).trigger('formated', [__type__,entry,]);
		$wait.show();
		$3.get(xupgux_rincian.dataset.hrefBkurincian, $3.extend({
			tahun: tahun,
			no_bku: entry.no_bku,
			jenis_bku: entry.jenis_bku,
			jenis_sp2d: entry.jenis_sp2d,
			bukti: entry.bukti,
		}, kodeskpd), function(result) {
			$3(xupgux_rincian).trigger('reload', [result.rincian,]);
			$3(xupgux_potongan).trigger('reload', [result.potongan,]); //INI YANG BUAT MUNCUL
			$3(xupgux).data('prompt').open();
		}).fail(function() {
			omfg('tidak bisa ambil rincian BKU.', arguments);
		}).always(() => $wait.hide());
	}
}); // on:prompt

$3(xupgux).on('formated', function(event, __type__, entry) {
	for (var n in entry) {
		if ($3(xupgux).data('tanggalin').indexOf(n) > -1) continue;
		if ($3(xupgux).data('centangin').indexOf(n) > -1) continue;
		forme(xupgux, n, 'value', entry[n]);
	}

	$3(xupgux).data('tanggalin').forEach(function(name) {
		forme(xupgux, name, function(input) {
			$3(input).trigger('tanggalin', (entry && name in entry) ? entry[name] : dated.current);
		});
	});
	$3(xupgux).data('centangin').forEach(function(n) {
		forme(xupgux, n, function(input) {
			if (entry && n in entry && entry[n] == 1) $3(input).prop('checked', true).trigger('change');
		});
	});
});

$3(xupgux).on('browsed', function(event, entry) {
	var __type__ = 0;
	var jenis_bku = xupgux_extra.jenis_bku;

	// jika `current < tgl_bukti ? tgl_bukti : tgl_bku` maka `tgl_bku = tgl_bukti` //
	if (entry.tgl_bukti && entry.tgl_bku === unknown && dated.current < (new Date(entry.tgl_bukti))) entry.tgl_bku = entry.tgl_bukti;

	$3(xupgux).trigger('formated', [__type__,entry,]);

	if (jenis_bku === 'SP2D') {
		$wait.show();
		$3.get(xupgux_rincian.dataset.hrefSp2drincian, $3.extend({
			tahun: tahun,
			nosp2d: entry.nosp2d,
			jenissp2d: entry.jenissp2d,
		}, kodeskpd), function(result) {
			$3(xupgux_rincian).trigger('reload', [result.rincian,]);
			$3(xupgux_potongan).trigger('reload', [result.potongan,]);
		}).fail(function() {
			omfg('tidak bisa ambil rincian SP2D.', arguments);
		}).always(() => $wait.hide());

	} else if (jenis_bku === 'SPJ') {
		$wait.show();
		$3.get(xupgux_rincian.dataset.hrefSpjrincian, $3.extend({
			tahun: tahun,
			nospj: entry.bukti,
		}, kodeskpd), function(result) {
			$3(xupgux_rincian).trigger('reload', [result.rincian,]);
			$3(xupgux_potongan).trigger('reload', [result.potongan,]);
		}).fail(function() {
			omfg('tidak bisa ambil rincian SPJ.', arguments);
		}).always(() => $wait.hide());

	} else omfg(`tidak bisa ambil rincian ${jenis_bku}.`, arguments);
});

jq_datatable_thead2columns({ table: xupgux_rincian,
	is_action_2: true,
	is_action_3: true,
	is_action_3_names: ['jumlah'],
	is_action_3_alias: column => ( column === 'jumlah' ? xupgux_extra.tjumlahf : column ),
});
$(xupgux_rincian).data('table', jq_tabelin(xupgux_rincian, {
	columns: $(xupgux_rincian).data('columns'),
	scrollY: xupgux_rincian.dataset.height,
	footerCallback: function(tfrow,data) {
		jq_datatable_summaries({
			data: data,
			tfoot: tfrow.parentElement,
			summaries: { jumlah: self => ( self.__main__(xupgux_extra.tjumlahf) ), },
		});
	},
}));
$(xupgux_rincian).on('reload',function(event, data) {
	data = data || [];
	var table = $(xupgux_rincian).data('table');

	table.clear();
	table.rows.add(data);

	/* redraw ketika prompt opened saja */
	$(xupgux).data('prompt').isOpened() && ((data.length > 0 && table.columns.adjust().draw()) || table.draw());
});

jq_datatable_thead2columns({ table: xupgux_potongan, form_prefix: '__potongan__',
	is_action_2: true,
	is_action_1: true,
	fn_action_1_updown_mk: () => {
		$(potongan).trigger('prompt', entry => {
			var data = $.extend(true, {}, entry); data[xupgux_extra.tjumlahf] = 0;
			var table = $(xupgux_potongan).data('table');

			var kode_rekening = table.data().toArray().map(n => n.kode_rekening);
			if (kode_rekening.indexOf(data.kode_rekening) === -1) {
				table.row.add(data) && table.columns.adjust().draw();
			}
		});
	},
	is_action_3: true,
	is_action_3_names: ['jumlah'],
	is_action_3_alias: column => ( column === 'jumlah' ? xupgux_extra.tjumlahf : column ),
	is_action_3_editable: true,
});
$(xupgux_potongan).data('table', jq_tabelin(xupgux_potongan, {
	scrollY: xupgux_potongan.dataset.height,
	columns: $(xupgux_potongan).data('columns'),
	footerCallback: function(tfrow,data) {
		jq_datatable_summaries({
			data: data,
			tfoot: tfrow.parentElement,
			summaries: {
				jumlah: self => ( self.__main__(xupgux_extra.tjumlahf) ),
			},
		});
	},
}));
$3(xupgux_potongan).on('reload',function(event, data) {
	data = data || [];
	var table = $3(this).data('table');

	table.clear();
	table.rows.add(data);

	/* redraw ketika prompt opened saja */
	$(xupgux).data('prompt').isOpened() && ((data.length > 0 && table.columns.adjust().draw()) || table.draw());
});

$3(xupgux).on('rm', function(event, entry) { rm(entry); });

$3(xupgux).on('submit', function(event) {
	// if (true) return; // [LINT] //
	event.preventDefault();

	var yn = false;
	xupgux_extra.required.forEach(function(name) {
		if (yn) return;
		var value = forme(xupgux, name, 'value');
		if (!value || String(value).trim() === '') {
			yn = true;
			message_ok('error', `Isian ${name.toUpperCase()} Tidak Boleh Kosong.`);
		}
	});
	if (yn) return;

	if (
		forme(xupgux, 'tgl_bku', 'value', value => Number(value.replace(/[^0-9]/g, '') || 0)) <
		forme(xupgux, 'tgl_bukti', 'value', value => Number(value.replace(/[^0-9]/g, '') || 0))
	) return message_ok('error', 'TGL_BKU tidak boleh kurang dari TGL_BUKTI.');

	if ((forme(xupgux, 'simpananbank', 'checked') || forme(xupgux, 'is_pihak_ketiga', 'checked')) === false) {
		return message_ok('error', 'Cara Belum Pilih Pencairan.');
	}

	if (forme(xupgux, 'simpananbank', 'checked') && forme(xupgux, 'is_pihak_ketiga', 'checked')) {
		return message_ok('error', 'Cara Pencairan tidak boleh pilih keduanya.');
	}

	$wait.show();
	$3.post(xupgux.action, $3(xupgux).serialize(), function() {
		$wait.hide();
		$3(xupgux).data('prompt').close();

		forme(bku_form, 'month', function(month) {
			month.value = Number(forme(xupgux, 'tgl_bku', 'value').split('-')[1]);
			$3(month).trigger('change');
		});
	}).fail(function() {
		$wait.hide();
		omfg('terjadi errors saat simpan bku.', arguments);
	});
});
$(xupgux).on('reset', function(event) {
	$(xupgux).data('prompt').isOpened() && $(xupgux).data('prompt').close();
});

/* [LINT] */
// $(document).ready(() => ( kodeskpd && $(xupgux).trigger('prompt', [0,]) )); //
var xlsgjx_extra = {
	once: true,
	jenis_bku_title: document.getElementById('spjskpd_lsgj_jenis_bku_title'),
	is_penerimaan: null,
	is_penerimaan_re: /SP2D-GJ/,
	is_penerimaan_fi: null,
	jenis_bku: null,
	tjumlahf: null,
	required: ['no_bku', 'bukti','urai','tgl_bku','tgl_bukti'],
	reset_create: ['bukti','urai','tgl_bku','tgl_bukti'],
};
var xlsgjx = prompts['xlsgjx'] = document.getElementById('spjskpd_pengeluaran_lsgj');
var xlsgjx_rincian = document.getElementById('sipkd_spjskpd_pengeluaran_lsgj_rincian');
var xlsgjx_potongan = document.getElementById('sipkd_spjskpd_pengeluaran_lsgj_potongan');

$(xlsgjx).data('centangin', ['simpananbank','is_pihak_ketiga']);
$(xlsgjx).data('centangin').forEach(name => {
	forme(xlsgjx, name, a => {
		if (a.dataset.against) {
			$(a).on('change', function() {
				forme(xlsgjx, a.dataset.against, b => {
					if (a.checked) $(b).prop('checked', false).trigger('change');
				});
			});
		}
	});
});

$(xlsgjx).data('tanggalin', ['tgl_bku', 'tgl_bukti']);
$(xlsgjx).data('tanggalin').forEach(name => forme(xlsgjx, name, elem => jq_tanggalin(elem)));

forme(xlsgjx, 'jenis_bku', function(jenis_bku) {
	$3(jenis_bku).on('change', function() {
		xlsgjx_extra.jenis_bku = jenis_bku.value;
		xlsgjx_extra.is_penerimaan = xlsgjx_extra.is_penerimaan_re.test(jenis_bku.value);
		xlsgjx_extra.tjumlahf = xlsgjx_extra.is_penerimaan ? 'penerimaan' : 'pengeluaran';

		$3(xlsgjx_rincian).trigger('reload', [[],]);
		$3(xlsgjx_potongan).trigger('reload', [[],]);

		if (xlsgjx_extra.jenis_bku_title) {
			var tmp = xlsgjx_extra.jenis_bku_title.dataset;
			xlsgjx_extra.jenis_bku_title.innerText = tmp[xlsgjx_extra.tjumlahf] || tmp.default;
		}

		forme(xlsgjx, '__type__', function(__type__) {
			if (__type__.value == 0) {
				xlsgjx_extra.reset_create.forEach(function(name) {
					if ($(xlsgjx).data('tanggalin').indexOf(name) > -1)
						forme(xlsgjx, name, elem => $(elem).trigger('tanggalin', dated.current));
					else
						forme(xlsgjx, name, elem => $(elem).val('').trigger('change'));
				});
			}
		}); // __type__
	});
});

$3(xlsgjx).data('prompt', jq_promptin({
	title: xlsgjx.dataset.promptTitle,
	onshow: function($prompt) {
		$prompt.getModalDialog().css('width', xlsgjx.dataset.promptWidth);
		if (xlsgjx_extra.once) {
			$prompt.getModalBody().append(xlsgjx);
		}
	},
	onshown:function() {
		$(xlsgjx_rincian).data('table').columns.adjust().draw();
		$(xlsgjx_potongan).data('table').columns.adjust().draw();
	},
	onhide: function() {
		$3(xlsgjx_rincian).data('table').clear().draw();
		$3(xlsgjx_potongan).data('table').clear().draw();
	},
	onhidden: function() {
		xlsgjx_extra.once = false;
		$3(xlsgjx).trigger('reset');
	},
}));

$3(xlsgjx).on('prompt', function(event, __type__, entry) {
	forme(xlsgjx, '__type__', 'value', __type__);
	forme(xlsgjx, 'csrfmiddlewaretoken', 'value', window.spjskpd.kuki('csrftoken'));

	forme(xlsgjx, 'tahun', 'value', tahun);
	if (kodeskpd) for (var n in kodeskpd) forme(xlsgjx, n, 'value', kodeskpd[n]);

	forme(xlsgjx, 'no_bku', 'readOnly', __type__ === 1);
	forme(xlsgjx, 'bukti_browse', 'disabled', __type__ === 1);
	forme(xlsgjx, 'jenis_bku', function(jenis_bku) {
		$3(jenis_bku).children().prop('disabled', false);
		jenis_bku.selectedIndex = 0;
		if (__type__ === 1 && entry && entry.jenis_bku) {
			jenis_bku.value = entry.jenis_bku;
			$3(jenis_bku.children).each(function(i,elem) {
				if (elem.value !== entry.jenis_bku) elem.disabled = true;
			});
		}
		$3(jenis_bku).trigger('change');
	});

	$3(xlsgjx).data('tanggalin').forEach(name => forme(xlsgjx, name, elem => $(elem).trigger('tanggalin', dated.current)));
	forme(xlsgjx, 'simpananbank', simpananbank => $(simpananbank).prop('checked', true).trigger('change'));

	if (__type__ === 0) {
		nobkuauto(
			function(no_bku) {
				forme(xlsgjx, 'no_bku', 'value', no_bku);
				$3(xlsgjx).data('prompt').open();
			},
			function() {
				$3(xlsgjx).data('prompt').open();
			}
		);
	}

	if (__type__ === 1) {
		$wait.show();
		$.get(xlsgjx_rincian.dataset.hrefBkurincian, $.extend({
			tahun: tahun,
			no_bku: entry.no_bku,
			jenis_bku: entry.jenis_bku,
		}, kodeskpd), function(result) {
			$wait.hide();
			$3(xlsgjx_rincian).trigger('reload', [result.rincian,]);
			$3(xlsgjx_potongan).trigger('reload', [result.potongan,]);
			$3(xlsgjx).trigger('assigned', [__type__, entry, ]);
			$3(xlsgjx).data('prompt').open();
		}).fail(function() {
			omfg('tidak bisa ambil rincian BKU.', arguments);
			$wait.hide();
		});
	}
});

/* a.k.a upgu:format(t)ed */
$3(xlsgjx).on('assigned', function(event, __type__, entry) {
	for (var n in entry) {
		if ($3(xlsgjx).data('tanggalin').indexOf(n) > -1) continue;
		if ($3(xlsgjx).data('centangin').indexOf(n) > -1) continue;
		forme(xlsgjx, n, 'value', entry[n]);
	}

	$3(xlsgjx).data('tanggalin').forEach(function(name) {
		forme(xlsgjx, name,
			elem => $(elem).trigger('tanggalin', (entry && name in entry) ? entry[name] : dated.current)
		);
	});

	$3(xlsgjx).data('centangin').forEach(function(name) {
		forme(xlsgjx, name, function(elem) {
			if (entry && name in entry && entry[name] == 1) $3(elem).prop('checked', true).trigger('change');
		});
	});
});

forme(xlsgjx, 'bukti_browse', function(bukti_browse) {
	var once = true;
	var contents = document.getElementById(bukti_browse.dataset.content);
	var tables = {};
	var columns = {};
	$(bukti_browse).on('click', function() {
		var params = $.extend({
			tahun: tahun,
			jenis_bku: xlsgjx_extra.jenis_bku,
		}, kodeskpd);

		$wait.show();
		$.get(bukti_browse.dataset.href, params, function(result) {
			$(tables[xlsgjx_extra.jenis_bku]).data('table').rows.add(result);
			$wait.hide();
			$(bukti_browse).data('prompt').open();
		})
		.fail(function() {
			$wait.hide();
			omfg('tidak bisa ambil bukti.', arguments);
			$(bukti_browse).data('prompt').open();
		});
	});

	$(contents).children('[data-content]').each((i,content) => {
		$(content).children('table').each((i,table) => {
			tables[content.dataset.content] = table;

			jq_datatable_thead2columns({ table: table, });
			$(table).data('table', jq_tabelin(table, {
				dom: 'ft',
				scrollY: bukti_browse.dataset.tableHeight,
				columns: $(table).data('columns'),
				createdRow: (tbrow,entry) => {
					$(tbrow).on('dblclick', () => {
						$3(xlsgjx).trigger('browsed', [entry,]);
						$(bukti_browse).data('prompt').close();
					});
				},
			}));
		});
	});

	$(bukti_browse).data('prompt', jq_promptin({
		onshow: function(self) {
			if (once) self.getModalBody().append(contents);

			self.getModalDialog().css({width: bukti_browse.dataset.promptWidth});

			forme(xlsgjx, 'jenis_bku', jenis_bku => self.setTitle(jenis_bku.children[jenis_bku.selectedIndex].innerText));

			$(contents).children('[data-content]').each((i,elem) => {
				$(elem)[elem.dataset.content === xlsgjx_extra.jenis_bku ? 'show' : 'hide']();
			});
		},
		onshown: function() {
			$(tables[xlsgjx_extra.jenis_bku]).data('table').columns.adjust().draw();
		},
		onhide: function() {
			$(tables[xlsgjx_extra.jenis_bku]).data('table').clear().draw();
		},
		onhidden: function($self) {
			once = false;
		},
	}));
});

$3(xlsgjx).on('browsed', function(event, entry) {
	var __type__ = 0;
	var jenis_bku = xlsgjx_extra.jenis_bku;

	// hapus `no_bku` karena sudah auto, untuk `no_bku` muncul ketika browse spj //
	var no_bku = entry.no_bku || null;
	entry.no_bku && (delete entry.no_bku);

	// supaya `tgl_bku` auto menyesuaikan `tgl_bukti` //
	// jika `current < tgl_bukti ? tgl_bukti : tgl_bku` maka `tgl_bku = tgl_bukti` //
	if (entry.tgl_bukti && entry.tgl_bku === unknown && dated.current < (new Date(entry.tgl_bukti))) entry.tgl_bku = entry.tgl_bukti;

	$3(xlsgjx).trigger('assigned', [__type__,entry,]);

	if (jenis_bku === 'SP2D-GJ') {
		$wait.show();
		$3.get(xlsgjx_rincian.dataset.hrefRinciansp2d, $3.extend({
			tahun: tahun,
			nosp2d: entry.nosp2d,
			jenissp2d: entry.jenissp2d,
		}, kodeskpd), function(result) {
			$wait.hide();
			$3(xlsgjx_rincian).trigger('reload', [result.rincian,]);
			$3(xlsgjx_potongan).trigger('reload', [result.potongan,]);
		}).fail(function() {
			$wait.hide();
			omfg(`tidak bisa ambil rincian ${jenis_bku}`, arguments);
		});

	} else if (jenis_bku === 'BAYAR-GJ') {
		$wait.show();
		$3.get(xlsgjx_rincian.dataset.hrefRincianbayar, $3.extend({
			tahun: tahun,
			no_bku: no_bku,
			jenis_bku: jenis_bku,
		}, kodeskpd), function(result) {
			$wait.hide();
			$3(xlsgjx_rincian).trigger('reload', [result.rincian,]);
			$3(xlsgjx_potongan).trigger('reload', [result.potongan,]);
		}).fail(function() {
			$wait.hide();
			omfg(`tidak bisa ambil rincian ${jenis_bku}`, arguments);
		});

	} else omfg(`tidak bisa ambil rincian ${jenis_bku}.`, arguments);
});

jq_datatable_thead2columns({ table: xlsgjx_rincian,
	is_action_2: true,
	is_action_3: true,
	is_action_3_names: ['jumlah'],
	is_action_3_alias: column => (column === 'jumlah' ? xlsgjx_extra.tjumlahf : column),
});
$(xlsgjx_rincian).data('table', jq_tabelin(xlsgjx_rincian, {
	scrollY: xlsgjx_rincian.dataset.height,
	columns: $3(xlsgjx_rincian).data('columns'),
	footerCallback: function(tfrow,data) {
		jq_datatable_summaries({
			data: data,
			tfoot: tfrow.parentElement,
			summaries: {
				jumlah: self => ( self.__main__(xlsgjx_extra.tjumlahf) ),
			},
		});
	},
}));
$(xlsgjx_rincian).on('reload', (event,data) => {
	var table = $(xlsgjx_rincian).data('table');
	data = data || [];

	table.clear();
	table.rows.add(data);

	/* redraw ketika prompt shown saja */
	$(xlsgjx).data('prompt').isOpened() && ((data.length > 0 && table.columns.adjust().draw()) || table.draw());
});

jq_datatable_thead2columns({ table: xlsgjx_potongan,
	form_prefix: '__potongan__',
	is_action_2: true,
	is_action_1: true,
	fn_action_1_updown_mk: self => {
		$(potongan).trigger('prompt', entry_0 => {
			var table = $(self.table).data('table');
			var entry_1 = $.extend(true, {[xlsgjx_extra.tjumlahf]:0}, entry_0);

			var kode_rekening = table.data().toArray().map(n => n.kode_rekening);
			if (kode_rekening.indexOf(entry_1.kode_rekening) === -1) {
				table.row.add(entry_1);
				table.columns.adjust().draw();
			}
		});
	},
	is_action_3: true,
	is_action_3_names: ['jumlah'],
	is_action_3_alias: column => (column === 'jumlah' ? xlsgjx_extra.tjumlahf : column),
	is_action_3_editable: true,
});
$(xlsgjx_potongan).data('table', jq_tabelin(xlsgjx_potongan, {
	scrollY: xlsgjx_potongan.dataset.height,
	columns: $(xlsgjx_potongan).data('columns'),
	footerCallback: function(tfrow,data) {
		jq_datatable_summaries({
			data: data,
			tfoot: tfrow.parentElement,
			summaries: {
				jumlah: self => ( self.__main__(xlsgjx_extra.tjumlahf) ),
			},
		});
	},
}));
$(xlsgjx_potongan).on('reload', (event,data) => {
	var table = $(xlsgjx_potongan).data('table');
	data = data || [];

	table.clear();
	table.rows.add(data);

	/* redraw ketika prompt shown saja */
	$(xlsgjx).data('prompt').isOpened() && ((data.length > 0 && table.columns.adjust().draw()) || table.draw());
});

$3(xlsgjx).on('rm', (event, entry) => rm(entry));
$3(xlsgjx).on('submit', function(event) {
	// return; // [LINT] //
	event.preventDefault();

	var jenis = xlsgjx_extra.tjumlahf;
	var yeet = false;

	xlsgjx_extra.required.forEach(function(name) {
		if (yeet) return;
		var value = forme(xlsgjx, name, 'value');
		if (!value || String(value).trim() === '') {
			yeet = true;
			message_ok('error', `Isian ${name.toUpperCase()} Tidak Boleh Kosong.`);
		}
	});
	if (yeet) return;

	if (Number(forme(xlsgjx, 'tgl_bku', 'value').replace(/[^0-9]/g, '')) < Number(forme(xlsgjx, 'tgl_bukti', 'value').replace(/[^0-9]/g, ''))) {
		return message_ok('error', 'TGL_BKU tidak boleh kurang dari TGL_BUKTI.');
	}

	if ((forme(xlsgjx, 'simpananbank', 'checked') || forme(xlsgjx, 'is_pihak_ketiga', 'checked')) === false) {
		return message_ok('error', 'Cara Pencairan Belum di Pilih.');
	}

	if (forme(xlsgjx, 'simpananbank', 'checked') && forme(xlsgjx, 'is_pihak_ketiga', 'checked')) {
		return message_ok('error', 'Cara Pencairan tidak boleh pilih keduanya.');
	}

	var data = $(xlsgjx_rincian).data('table').data().toArray();
	var empty = data.map(n => n[jenis]).reduce((a,b) => (Number(a) + Number(b)));
	if (data.length === 0 || empty < 1) {
		return message_ok('error','rincian gaji masih kosong.');
	}

	$wait.show();
	$3.post(xlsgjx.action, $3(xlsgjx).serialize(), function() {
		$wait.hide();
		$3(xlsgjx).data('prompt').close();
		forme(bku_form, 'month', function(month) {
			month.value = Number(forme(xlsgjx, 'tgl_bku', 'value').split('-')[1]);
			$3(month).trigger('change');
		});
	}).fail(function() {
		$wait.hide();
		omfg('terjadi errors saat simpan bku.', arguments);
	});
});

$(xlsgjx).on('reset', function() {
	$(xlsgjx).data('prompt').isOpened() && $(xlsgjx).data('prompt').close();
});

// [LINT] //
// $(document).ready(() => ( kodeskpd && $(xlsgjx).trigger('prompt', [0,]) )); //
var xtux_extra = {
	required: ['no_bku', 'bukti','urai', 'tgl_bku', 'tgl_bukti'],
	jenis_bku_create_clear: ['bukti','urai','tgl_bku','tgl_bukti'],
	once: true,
	tjumlahf: null,
	jenis_bku: null,
	is_penerimaan: null,
	is_penerimaan_re: /SP2D/,
	jenis_bku_title: document.getElementById('spjskpd_pengeluaran_tu_jenis_bku_title'),
};
var xtux = prompts['xtux'] = document.getElementById('spjskpd_pengeluaran_tu');
var xtux_rincian = document.getElementById('spjskpd_pengeluaran_tu_rincian');
var xtux_potongan = document.getElementById('spjskpd_pengeluaran_tu_potongan');

$(xtux).data('centangin', ['simpananbank','is_pihak_ketiga']);
$(xtux).data('centangin').forEach(function(name) {
	forme(xtux, name, a => {
		if (a.dataset.against) {
			forme(xtux, a.dataset.against, b => {
				$(a).on('change', () => {
					if (a.checked) $(b).prop('checked', false).trigger('change');
				});
			});
		}
	});
});

$(xtux).data('tanggalin', ['tgl_bku', 'tgl_bukti']);
$(xtux).data('tanggalin').forEach(name => forme(xtux, name, elem => jq_tanggalin(elem)));

forme(xtux, 'jenis_bku', function(jenis_bku) {
	$(jenis_bku).on('change', function() {
		xtux_extra.jenis_bku = jenis_bku.value;
		xtux_extra.is_penerimaan = xtux_extra.is_penerimaan_re.test(xtux_extra.jenis_bku);
		xtux_extra.tjumlahf = xtux_extra.is_penerimaan ? 'penerimaan' : 'pengeluaran';

		if (xtux_extra.jenis_bku_title) {
			var tmp = xtux_extra.jenis_bku_title.dataset;
			xtux_extra.jenis_bku_title.innerText = tmp[xtux_extra.tjumlahf] || tmp.default;
		}

		$(xtux_rincian).trigger('reload', [[],]);
		$(xtux_potongan).trigger('reload', [[],]);

		forme(xtux, '__type__', function(__type__) {
			if (__type__.value == 0) {
				xtux_extra.jenis_bku_create_clear.forEach(function(name) {
					if ($(xtux).data('tanggalin').indexOf(name) > -1)
						forme(xtux, name, elem => $(elem).trigger('tanggalin', dated.current));
					else
						forme(xtux, name, elem => $(elem).prop('value','').trigger('change'));
				});
			}
		}); // :forme:__type__
	}); // :on:change
});

$(xtux).data('prompt', jq_promptin({
	title: xtux.dataset.promptTitle,
	onshow: function($prompt) {
		$prompt.getModalDialog().css('width', xtux.dataset.promptWidth);
		if (xtux_extra.once) {
			$prompt.getModalBody().append(xtux);
		}
	},
	onshown:function() {
		$(xtux_rincian).data('table').columns.adjust().draw();
		$(xtux_potongan).data('table').columns.adjust().draw();
	},
	onhide: function() {
		$(xtux_rincian).data('table').clear().draw();
		$(xtux_potongan).data('table').clear().draw();
	},
	onhidden: function() {
		xtux_extra.once = false;
		$(xtux).trigger('reset');
	},
}));

$(xtux).on('prompt', function(event, __type__, entry) {
	forme(xtux, '__type__', 'value', __type__);
	forme(xtux, 'csrfmiddlewaretoken', 'value', window.spjskpd.kuki('csrftoken'));

	forme(xtux, 'tahun', 'value', tahun);
	if (kodeskpd) for (var k in kodeskpd) forme(xtux, k, 'value', kodeskpd[k]);

	forme(xtux, 'no_bku', 'readOnly', __type__ === 1);
	forme(xtux, 'bukti_browse', 'disabled', __type__ === 1);
	forme(xtux, 'jenis_bku', function(jenis_bku) {
		$(jenis_bku).children().prop('disabled', false);
		jenis_bku.selectedIndex = 0;
		if (__type__ === 1 && entry && entry.jenis_bku) {
			jenis_bku.value = entry.jenis_bku;
			$(jenis_bku.children).each(function(i,elem) {
				if (elem.value !== entry.jenis_bku) elem.disabled = true;
			});
		}
		$(jenis_bku).trigger('change');
	});

	$(xtux).data('tanggalin').forEach(name => forme(xtux, name, elem => $(elem).trigger('tanggalin', dated.current)));
	forme(xtux, 'simpananbank', simpananbank => $(simpananbank).prop('checked', true).trigger('change'));

	if (__type__ === 0) {
		nobkuauto(
			function(no_bku) {
				forme(xtux, 'no_bku', 'value', no_bku);
				$(xtux).data('prompt').open();
			},
			function() {
				$(xtux).data('prompt').open();
			}
		);
	}

	if (__type__ === 1) {
		$wait.show();
		$.get(xtux_rincian.dataset.hrefBkurincian, $.extend({
			tahun: tahun,
			no_bku: entry.no_bku, jenis_bku: entry.jenis_bku,
			jenis_sp2d: entry.jenis_sp2d, nospj:entry.bukti,
		}, kodeskpd), function(result) {
			$wait.hide();
			$3(xtux_rincian).trigger('reload', [result.rincian,]);
			$3(xtux_potongan).trigger('reload', [result.potongan,]);

			$3(xtux).trigger('assigned', [__type__, entry, ]);
			$3(xtux).data('prompt').open();
		}).fail(function() {
			$wait.hide();
			omfg('tidak bisa ambil rincian bku.', arguments);
		});
	}
});

$(xtux).on('assigned', function(event, __type__, entry) {
	for (var n in entry) {
		if ($(xtux).data('tanggalin').indexOf(n) > -1) continue;
		if ($(xtux).data('centangin').indexOf(n) > -1) continue;
		forme(xtux, n, 'value', entry[n]);
	}

	$(xtux).data('tanggalin').forEach(name => forme(xtux, name, elem =>
		$(elem).trigger('tanggalin', (entry && entry[name]) ? entry[name] : dated.current)
	));
	$(xtux).data('centangin').forEach(name => forme(xtux, name, elem => {
		if (entry && name in entry && entry[name] == 1) $(elem).prop('checked', true).trigger('change'); 
	}));
});

forme(xtux, 'bukti_browse', function(bukti_browse) {
	var once = true, tables = {}, columns = {};
	var contents = document.getElementById(bukti_browse.dataset.content);

	$(bukti_browse).on('click', function() {
		var params = $.extend({tahun: tahun, jenis_bku: xtux_extra.jenis_bku}, kodeskpd);

		$wait.show();
		$.get(bukti_browse.dataset.href, params, function(result) {
			$wait.hide();
			$(tables[xtux_extra.jenis_bku]).data('table').rows.add(result);
			$(bukti_browse).data('prompt').open();
		})
		.fail(function() {
			omfg('tidak bisa ambil bukti.', arguments); $wait.hide(); $(bukti_browse).data('prompt').open();
		});
	});

	$(contents).children('[data-content]').each((i,content) => {
		$(content).children('table').each((i,table) => {
			tables[content.dataset.content] = table;

			jq_datatable_thead2columns({ table: table, });
			$(table).data('table', jq_tabelin(table, {
				dom: 'ft',
				scrollY: bukti_browse.dataset.tableHeight,
				columns: $(table).data('columns'),
				createdRow: (tbrow,entry) => {
					$(tbrow).on('dblclick', () => {
						$(xtux).trigger('browsed', [entry,]);
						$(bukti_browse).data('prompt').close();
					});
				},
			}));
		});
	});

	$(bukti_browse).data('prompt', jq_promptin({
		onshow: function(self) {
			if (once) self.getModalBody().append(contents);
			self.getModalDialog().css({width: bukti_browse.dataset.promptWidth});

			forme(bukti_browse.form, 'jenis_bku', jenis_bku => self.setTitle(jenis_bku.children[jenis_bku.selectedIndex].innerText));

			$(contents).children('[data-content]').each((i,elem) => {
				$(elem)[elem.dataset.content === xtux_extra.jenis_bku ? 'show' : 'hide']();
			});
		},
		onshown: function() {
			$(tables[xtux_extra.jenis_bku]).data('table').columns.adjust().draw();
		},
		onhide: function() {
			$(tables[xtux_extra.jenis_bku]).data('table').clear().draw();
		},
		onhidden: function($self) {
			once = false;
		},
	}));
});

$3(xtux).on('browsed', function(event, entry) {
	var __type__ = 0;
	var jenis_bku = xtux_extra.jenis_bku;

	$(xtux).trigger('assigned', [__type__, entry,]);

	if (jenis_bku === 'SP2D') {
		$wait.show();
		$.get(xtux_rincian.dataset.hrefSp2drincian, $.extend({
			tahun: tahun,
			nosp2d: entry.nosp2d, jenissp2d: entry.jenissp2d,
		}, kodeskpd), function(result) {
			$wait.hide();
			$(xtux_rincian).trigger('reload', [result.rincian,]);
			$(xtux_potongan).trigger('reload', [result.potongan,]);
		}).fail(function() {
			$wait.hide();
			omfg('tidak bisa ambil rincian SP2D.', arguments);
		});

	} else if (jenis_bku === 'SPJ') {
		$wait.show();
		$3.get(xtux_rincian.dataset.hrefSpjrincian, $3.extend({
			tahun: tahun,
			nospj: entry.bukti,
		}, kodeskpd), function(result) {
			$3(xtux_rincian).trigger('reload', [result,]);
			$3(xtux_potongan).trigger('reload', [[],]);
		}).fail(function() {
			omfg('tidak bisa ambil rincian SPJ.', arguments);
		}).always(function() {
			$wait.hide();
		});

	} else omfg(`tidak bisa ambil rincian "${jenis_bku}" (unknown).`);
});

jq_datatable_thead2columns({ table: xtux_rincian,
	is_action_2: true,
	is_action_3: true,
	is_action_3_names: ['jumlah'],
	is_action_3_alias: column => (column === 'jumlah' ? xtux_extra.tjumlahf : column),
});
$(xtux_rincian).data('table', jq_tabelin(xtux_rincian, {
	columns: $(xtux_rincian).data('columns'),
	scrollY: xtux_rincian.dataset.height,
	footerCallback: function(tfrow,data) {
		jq_datatable_summaries({
			data: data,
			tfoot: tfrow.parentElement,
			summaries: {
				jumlah: self => ( self.__main__(xtux_extra.tjumlahf) ),
			},
		});
	},
}));
$(xtux_rincian).on('reload', function(event,data) {
	data = data || [];
	var table = $(this).data('table');

	table.clear();
	table.rows.add(data);

	/* redraw ketika prompt shown saja */
	$(xtux).data('prompt').isOpened() && ((data.length > 0 && table.columns.adjust().draw()) || table.draw());
});

jq_datatable_thead2columns({ table: xtux_potongan,
	form_prefix: '__potongan__',
	is_action_3: true,
	is_action_3_editable: true,
	is_action_3_names: ['jumlah'],
	is_action_3_alias: column => (column === 'jumlah' ? xtux_extra.tjumlahf : column),
	is_action_2: true,
	is_action_1: true,
	fn_action_1_updown_mk: self => {
		$(potongan).trigger('prompt', function(entry_0) {
			var table = $(xtux_potongan).data('table');
			var entry_1 = $.extend(true, {[xtux_extra.tjumlahf]:0}, entry_0);

			var kode_rekening = table.data().toArray().map(n => n.kode_rekening);
			if (kode_rekening.indexOf(entry_1.kode_rekening) === -1) {
				table.row.add(entry_1); table.columns.adjust().draw();
			}
		});
	},
});
$(xtux_potongan).data('table', jq_tabelin(xtux_potongan, {
	scrollY: xtux_potongan.dataset.height,
	columns: $(xtux_potongan).data('columns'),
	footerCallback: function(tfrow,data) {
		jq_datatable_summaries({
			data: data,
			tfoot: tfrow.parentElement,
			summaries: {
				jumlah: self => ( self.__main__(xtux_extra.tjumlahf) ),
			},
		});
	},
}));
$(xtux_potongan).on('reload',function(event,data) {
	data = data || [];
	var table = $(this).data('table');

	table.clear();
	table.rows.add(data);

	/* redraw ketika prompt shown saja */
	$(xtux).data('prompt').isOpened() && ((data.length > 0 && table.columns.adjust().draw()) || table.draw());
});

$3(xtux).on('submit', function(event) {
	// return;
	event.preventDefault();

	var yn = false;
	xtux_extra.required.forEach(function(name) {
		if (yn) return;
		var value = forme(xtux, name, 'value');
		if (!value || String(value).trim() === '') {
			message_ok('error', `Isian ${name.toUpperCase()} Tidak Boleh Kosong.`);
			yn = true;
		}
	});
	if (yn) return;

	if (
		forme(xtux, 'tgl_bku', 'value', v => Number(v.replace(/[^0-9]/g, ''))) <
		forme(xtux, 'tgl_bukti', 'value', v => Number(v.replace(/[^0-9]/g, '')))
	) {
		return message_ok('error', 'TGL_BKU tidak boleh kurang dari TGL_BUKTI.');
	}

	if ((forme(xtux, 'simpananbank', 'checked') || forme(xtux, 'is_pihak_ketiga', 'checked')) === false) {
		return message_ok('error', 'Cara Pencairan Belum di Pilih.');
	}

	if (forme(xtux, 'simpananbank', 'checked') && forme(xtux, 'is_pihak_ketiga', 'checked')) {
		return message_ok('error', 'Cara Pencairan tidak boleh pilih keduanya.');
	}

	var data = $(xtux_rincian).data('table').data().toArray();
	var empty = data.map(n => n[xtux_extra.tjumlahf]).reduce((a,b) => (Number(a) + Number(b)), 0);
	if (data.length === 0 || empty < 1) {
		return message_ok('error','Rincian Masih Kosong.');
	}

	$wait.show();
	$.post(xtux.action, $(xtux).serialize(), function() {
		$wait.hide();
		$(xtux).data('prompt').close();

		forme(bku_form, 'month', month => {
				$(month).prop('value', forme(xtux,'tgl_bku','value',
					v => Number(v.split('-')[1])
				)).trigger('change');
		});
	}).fail(function() {
		$wait.hide();
		omfg('terjadi errors saat simpan BKU.', arguments);
	});
});

$(xtux).on('reset', function() {
	$(xtux).data('prompt').isOpened() && $(xtux).data('prompt').close();
});

// $(document).ready(() => ( kodeskpd && $(xtux).trigger('prompt', [0,]) )); // [LINT] //
/*

	TODO|UNTESTED. KARENA BELUM ADA DATA SAMA SEKALI. 20190701.

*/

var rkppkd = prompts['rkppkd'] = document.getElementById('spjskpd_pengeluaran_rkppkd');
var rkppkd_rincian = document.getElementById('spjskpd_pengeluaran_rkppkd_rincian');
var rkppkd_extra = {
	once: true,
	save_required: ['no_bku','bukti','tgl_bku','tgl_bukti','jenis_sp2d','jenis_sp2d_alt','urai',],
	jenis_bku: forme(rkppkd, 'jenis_bku', 'value'),
	jenis_sp2d_alt_rgx: /UP|GU/,
	__type__: null,
};

$(rkppkd).data('tanggalin', ['tgl_bku', 'tgl_bukti']);
$(rkppkd).data('tanggalin').forEach( name => forme(rkppkd, name, elem => jq_tanggalin(elem)) );

forme(rkppkd, 'jenis_sp2d_alt', function(jenis_sp2d_alt) {
	forme(rkppkd, 'jenis_sp2d', function(jenis_sp2d) {
		$(jenis_sp2d_alt).on('change', function(event) {
			forme(rkppkd, 'bukti_browse', 'disabled', rkppkd_extra.__type__ === 1);

			var rgx = rkppkd_extra.jenis_sp2d_alt_rgx;
			if ((rgx.test(jenis_sp2d_alt.value) && rgx.test(jenis_sp2d.value)) === false) {
				jenis_sp2d.value = jenis_sp2d_alt.value;
			}
			if (rkppkd_extra.__type__ === 0) {
				forme(rkppkd, 'bukti', 'value', '');
				forme(rkppkd, 'bukti_browse', 'disabled', jenis_sp2d_alt.value === '');
				$(rkppkd_rincian).trigger('reload', [[],]);
			} // __type__
		});
	});
});

$(rkppkd).on('assigned', function(event, __type__, entry) {
	for (var n in entry) {
		if ($(rkppkd).data('tanggalin').indexOf(n) > -1) continue;
		forme(rkppkd, n, 'value', entry[n]);
	}

	$(rkppkd).data('tanggalin').forEach(name => forme(rkppkd, name,
		elem => $(elem).trigger('tanggalin', (entry && name in entry) ? entry[name] : dated.current)
	));
});

$(rkppkd).data('prompt', jq_promptin({
	title: rkppkd.dataset.promptTitle,
	onshow: function($prompt) {
		$prompt.getModalDialog().css('width', rkppkd.dataset.promptWidth);
		if (rkppkd_extra.once) {
			$prompt.getModalBody().append(rkppkd);
		}
	},
	onshown:function() {
		$(rkppkd_rincian).data('table').draw();
	},
	onhide: function() {
		$(rkppkd_rincian).data('table').clear().draw();
	},
	onhidden: function() {
		rkppkd_extra.once = false;
		$(rkppkd).trigger('reset');
	},
}));

$(rkppkd).on('prompt', function(event, __type__, entry) {
	rkppkd_extra.__type__ = __type__;
	forme(this, '__type__', 'value', __type__);
	forme(this, 'csrfmiddlewaretoken', 'value', window.spjskpd.kuki('csrftoken'));

	forme(rkppkd, 'tahun', 'value', tahun);
	if (kodeskpd) for (var k in kodeskpd) forme(rkppkd, k, 'value', kodeskpd[k]);

	forme(this, 'no_bku', 'readOnly', __type__ === 1);
	forme(this, 'bukti', 'readOnly', __type__ === 1);
	forme(this, 'jenis_sp2d_alt', jenis_sp2d_alt => {
		var has = false;
		$(jenis_sp2d_alt).each((i,elem) => {
			$(elem).prop('checked', false).prop('disabled', __type__ === 1);
			if (entry && (entry.jenis_sp2d === elem.value || (
				rkppkd_extra.jenis_sp2d_alt_rgx.test(entry.jenis_sp2d) &&
				rkppkd_extra.jenis_sp2d_alt_rgx.test(elem.value) &&
				true
			))) elem.checked = true;
		});
		$(jenis_sp2d_alt).trigger('change');
	});

	$(this).data('tanggalin').forEach(name => forme(this, name, elem => $(elem).trigger('tanggalin', dated.current)));

	if (__type__ === 0) {
		nobkuauto(
			no_bku => {
				forme(rkppkd, 'no_bku', 'value', no_bku);
				$(rkppkd).data('prompt').open();
			},
			function() { $3(rkppkd).data('prompt').open(); }
		);
	}


	if (__type__ === 1) {
		$wait.show();
		$.get(rkppkd_rincian.dataset.hrefBkurincian, $.extend({
			tahun: tahun,
			no_bku: entry.no_bku, jenis_bku: entry.jenis_bku,
			jenis_sp2d: entry.jenis_sp2d,
		}, kodeskpd), function(result) {
			$wait.hide();
			$3(rkppkd_rincian).trigger('reload', [result.rincian,]);
			$3(rkppkd).trigger('assigned', [__type__,entry,]);
			$3(rkppkd).data('prompt').open();
		}).fail(function() {
			$wait.hide();
			omfg('tidak bisa ambil rincian.', arguments);
		});
	}
});


jq_datatable_thead2columns({ table: rkppkd_rincian,
	form_prefix: '__rincian__',
	is_action_3: true,
	is_action_3_editable: true,
	is_action_3_names: ['penerimaan', 'pengeluaran'],
	is_action_3_alias: column => (column === 'jumlah' ? rkppkd_extra.tjumlahf : column),
	is_action_2: true,
	is_action_1: true,
	fn_action_1_updown_mk: self => {
		$(potongan).trigger('prompt', function(entry_0) {
			var table = $(self.table).data('table');
			var entry_1 = $.extend(true, {[rkppkd_extra.tjumlahf]:0}, entry_0,);

			var kode_rekening = table.data().toArray().map(n => n.kode_rekening);
			if (kode_rekening.indexOf(entry_1.kode_rekening) === -1) {
				table.row.add(entry_1) && table.columns.adjust().draw();
			}
		});
	},
});

// jq_datatable_thead2columns({ table: rkppkd_rincian,
// 	is_action_2: true,
// 	is_action_3: true,
// 	is_action_3_editable: true,
// 	is_action_3_regex: /terima|keluar/,
// });
$(rkppkd_rincian).data('table', jq_tabelin(rkppkd_rincian, {
	columns: $(rkppkd_rincian).data('columns'),
	scrollY: rkppkd_rincian.dataset.height,
	footerCallback: function(tfrow,data) {
		jq_datatable_summaries({
			data: data,
			tfoot: tfrow.parentElement,
		});
	},
}));
$(rkppkd_rincian).on('reload', function(event, data) {
	var table = $(rkppkd_rincian).data('table'), data = data || [];

	table.clear();
	table.rows.add(data);

	/* redraw ketika prompt opened saja */
	if ($(rkppkd).data('prompt').isOpened()) {
		if (data.length > 0) table.columns.adjust().draw();
		else table.draw();
	}
});

forme(rkppkd, 'bukti_browse', function(bukti_browse) {
	var once = true;
	var contents = document.getElementById(bukti_browse.dataset.content);
	var tables = {};
	var columns = {};

	$(bukti_browse).on('click', function() {
		var params = $.extend({
			tahun: tahun,
			jenis_bku: rkppkd_extra.jenis_bku,
			jenis_sp2d: forme(rkppkd, 'jenis_sp2d', 'value'),
		}, kodeskpd);

		$wait.show();
		$.get(bukti_browse.dataset.href, params, result => {
			$wait.hide();
			$(tables[rkppkd_extra.jenis_bku]).data('table').rows.add(result);
			$(bukti_browse).data('prompt').open();
		})
		.fail(function() {
			$wait.hide();
			omfg('tidak bisa ambil bukti.', arguments);
		});
	});

	$(contents).children('[data-content]').each((i,content) => {
		$(content).children('table').each((i,table) => {
			tables[content.dataset.content] = table;

			jq_datatable_thead2columns({ table: table, });
			$(table).data('table', jq_tabelin(table, {
				dom: 'ft',
				scrollY: bukti_browse.dataset.tableHeight,
				columns: $(table).data('columns'),
				createdRow: function(tbrow, entry) {
					$(tbrow).on('dblclick', function() {
						$(rkppkd).trigger('browsed', [entry,]);
						$(bukti_browse).data('prompt').close();
					});
				},
			}));
		});
	});

	$(bukti_browse).data('prompt', jq_promptin({
		onshow: function(self) {
			if (once) self.getModalBody().append(contents);
			self.getModalDialog().css({width: bukti_browse.dataset.promptWidth});

			$(contents).children('[data-content]').each((i,elem) => {
				$(elem).hide();
				if (elem.dataset.content === rkppkd_extra.jenis_bku) {
					$(elem).show();
					self.setTitle(elem.dataset.title || elem.dataset.content);
				}
			});
		},
		onshown: function() {
			$(tables[rkppkd_extra.jenis_bku]).data('table').columns.adjust().draw();
		},
		onhide: function() {
			$(tables[rkppkd_extra.jenis_bku]).data('table').clear().draw();
		},
		onhidden: function() {
			once = false;
		},
	}));
});

$3(rkppkd).on('browsed', function(event, entry) {
	var __type__ = 0;
	$3(rkppkd).trigger('assigned', [__type__, entry, ]);
	
	var jenis_bku = entry.jenissp2d
	var params = $.extend({
			tahun: tahun,
			nosts: entry.nosts,
			jenis_bku: rkppkd_extra.jenis_bku,
			jenis_sp2d: forme(rkppkd, 'jenis_sp2d', 'value'),
		}, kodeskpd);

	$wait.show();
	$.get(rkppkd_rincian.dataset.hrefStsrincian, params, function(result) {
		$3(rkppkd_rincian).trigger('reload', [result.rincian,]);
		$wait.hide();
	}).fail(function() {
		$wait.hide();
		omfg(`tidak bisa ambil rincian ${entry.jenis_sp2d}`, arguments);
	});

	if (jenis_bku === 'SP2D-GJ') {
		$wait.show();
		$3.get(xlsgjx_rincian.dataset.hrefRinciansp2d, $3.extend({
			tahun: tahun,
			nosp2d: entry.nosp2d,
			jenissp2d: entry.jenissp2d,
		}, kodeskpd), function(result) {
			$wait.hide();
			$3(xlsgjx_rincian).trigger('reload', [result.rincian,]);

		}).fail(function() {
			$wait.hide();
			omfg(`tidak bisa ambil rincian ${jenis_bku}`, arguments);
		});
	}
});

$(rkppkd).on('submit', function(event) {
	event.preventDefault();

	var yeet = false;
	rkppkd_extra.save_required.forEach(function(name) {
		forme(rkppkd, name, 'value', value => {
			if (!yeet && value === '') {
				message_ok('error', `Isian ${name.toUpperCase()} Tidak Boleh Kosong.`);
				yeet = true;
			}
		});
	});
	if (yeet) return;

	if (
		forme(rkppkd, 'tgl_bku', 'value', v => Number(v.replace(/[^0-9]/g, ''))) <
		forme(rkppkd, 'tgl_bukti', 'value', v => Number(v.replace(/[^0-9]/g, '')))
	) return message_ok('error', 'TGL_BKU tidak boleh kurang dari TGL_BUKTI.');

	var data = $(rkppkd_rincian).data('table').data().toArray();
	var empty = data.map(n => n['penerimaan'] + n['pengeluaran']).reduce((a,b) => (Number(a) + Number(b)), 0);
	if (data.length < 1 || empty < 1) return message_ok('error','Rincian Masih Kosong.');
	
	$wait.show();
	$.post(rkppkd.action, $(rkppkd).serialize(), function() {
		$wait.hide();
		$(rkppkd).data('prompt').close();
		forme(bku_form, 'month', month => {
			$(month)
			.prop('value', forme(rkppkd,'tgl_bku','value', v => Number(v.split('-')[1]) ))
			.trigger('change');
		});
	}).fail(function() {
		$wait.hide();
		omfg('terjadi errors saat simpan BKU.', arguments);
	});
});

$(rkppkd).on('reset', function() {
	$(this).data('prompt').isOpened() && $(this).data('prompt').close();
});

// $(document).ready(() => ( kodeskpd && $(rkppkd).trigger('prompt', [0,]) )); // [TEST] //
var barjas_extra = {
	jenis_bku_create_clear: ['bukti','tgl_bku','tgl_bukti','__kegiatan__','urai',],
	required_0: ['no_bku', 'bukti','urai', 'tgl_bku', 'tgl_bukti',],
	once: true,
	tjumlahf: null,
	jenis_bku: null,
	is_penerimaan: null,
	is_penerimaan_re: /SP2D/,
	jenis_bku_title: document.querySelector('#spjskpd_pengeluaran_barjas_jenis_bku_title'),
};
var barjas = prompts['barjas'] = document.querySelector('#spjskpd_pengeluaran_barjas');
var barjas_rincian = document.querySelector('#spjskpd_pengeluaran_barjas_rincian');
var barjas_potongan = document.querySelector('#spjskpd_pengeluaran_barjas_potongan');

$(barjas).data('centangin', ['simpananbank','is_pihak_ketiga']);
$(barjas).data('centangin').forEach(name => {
	forme(barjas, name, a => {
		if (a.dataset.against) {
			forme(barjas, a.dataset.against, b => {
				$3(a).on('change', () => {
					if (a.checked) $(b).prop('checked', false).trigger('change');
				});
			});
		}
	});
});

$3(barjas).data('tanggalin', ['tgl_bku', 'tgl_bukti']);
$3(barjas).data('tanggalin').forEach(name => forme(barjas, name, elem => jq_tanggalin(elem)));

forme(barjas, 'jenis_bku', function(jenis_bku) {
	$(jenis_bku).on('change', function() {
		barjas_extra.jenis_bku = jenis_bku.value;
		barjas_extra.is_penerimaan = barjas_extra.is_penerimaan_re.test(barjas_extra.jenis_bku);
		barjas_extra.tjumlahf = barjas_extra.is_penerimaan ? 'penerimaan' : 'pengeluaran';

		if (barjas_extra.jenis_bku_title) {
			var tmp = barjas_extra.jenis_bku_title.dataset;
			barjas_extra.jenis_bku_title.innerText = tmp[barjas_extra.tjumlahf] || tmp.default;
		}

		$(barjas_rincian).trigger('reload', [[],]);
		$(barjas_potongan).trigger('reload', [[],]);

		forme(barjas, '__type__', function(__type__) {
			if (__type__.value == 0) {
				barjas_extra.jenis_bku_create_clear.forEach(function(name) {
					if ($(barjas).data('tanggalin').indexOf(name) > -1)
						forme(barjas, name, elem => $(elem).trigger('tanggalin', dated.current));
					else
						forme(barjas, name, elem => $(elem).val('').trigger('change'));
				});
			}
		}); // :forme:__type__
	}); // :on:change
});

$(barjas).data('prompt', jq_promptin({
	title: barjas.dataset.promptTitle,
	onshow: function(self) {
		if (barjas_extra.once) self.getModalBody().append(barjas);
		self.getModalDialog().css('width', barjas.dataset.promptWidth);
	},
	onshown:function() {
		$(barjas_rincian).data('table').columns.adjust().draw();
		$(barjas_potongan).data('table').columns.adjust().draw();
	},
	onhide: function() {
		$(barjas_rincian).data('table').clear().draw();
		$(barjas_potongan).data('table').clear().draw();
	},
	onhidden: function() {
		barjas_extra.once = false;
		$(barjas).trigger('reset');
	},
}));

$(barjas).on('prompt', function(event, __type__, entry) {
	forme(barjas, '__type__', 'value', __type__);
	forme(barjas, 'csrfmiddlewaretoken', 'value', window.spjskpd.kuki('csrftoken'));

	forme(barjas, 'tahun', 'value', tahun);
	if (kodeskpd) for (var k in kodeskpd) forme(barjas, k, 'value', kodeskpd[k]);

	forme(barjas, 'no_bku', 'readOnly', __type__ === 1);
	forme(barjas, 'bukti_browse', 'disabled', __type__ === 1);
	forme(barjas, 'jenis_bku', function(jenis_bku) {
		$(jenis_bku).children().prop('disabled', false);
		jenis_bku.selectedIndex = 0;
		if (__type__ === 1 && entry && entry.jenis_bku) {
			jenis_bku.value = entry.jenis_bku;
			$(jenis_bku.children).each(function(i,elem) {
				if (elem.value !== entry.jenis_bku) elem.disabled = true;
			});
		}
		$(jenis_bku).trigger('change');
	});

	$(barjas).data('tanggalin').forEach(name => forme(barjas, name, elem => $(elem).trigger('tanggalin', dated.current)));
	$(barjas).data('centangin').forEach(name => forme(barjas, name, elem => $(elem).prop('checked', false).trigger('change')));

	if (__type__ === 0) {
		nobkuauto(
			function(no_bku) {
				forme(barjas, 'no_bku', 'value', no_bku);
				$(barjas).data('prompt').open();
			},
			function() {
				$(barjas).data('prompt').open();
			}
		);
	}

	if (__type__ === 1) {
		$wait.show();
		$.get(barjas_rincian.dataset.hrefBkurincian, $.extend({
			tahun: tahun,
			no_bku: entry.no_bku, jenis_bku: entry.jenis_bku,
		}, kodeskpd), function(result) {
			$wait.hide();
			result.entry && $.extend(true, entry, result.entry);

			$3(barjas_rincian).trigger('reload', [result.rincian,]);
			$3(barjas_potongan).trigger('reload', [result.potongan,]);

			$3(barjas).trigger('assigned', [__type__, entry, ]);
			$3(barjas).data('prompt').open();

		}).fail(function() {
			omfg('tidak bisa ambil rincian BKU.', arguments);
			$wait.hide();
		});
	}
});

$(barjas).on('assigned', function(event, __type__, entry) {
	for (var n in entry) {
		if ($(barjas).data('tanggalin').indexOf(n) > -1) continue;
		if ($(barjas).data('centangin').indexOf(n) > -1) continue;
		forme(barjas, n, 'value', entry[n]);
	}

	forme(barjas,'__kegiatan__', 'value', ( (entry.kegiatan_kode || '?') + ' ― ' + (entry.kegiatan_urai || '?') ));

	$(barjas).data('tanggalin').forEach(name => forme(barjas, name,
		elem => $(elem).trigger('tanggalin', (entry && entry[name]) ? entry[name] : dated.current)
	));
	$(barjas).data('centangin').forEach(name => forme(barjas, name, elem => {
		if (entry && name in entry && entry[name] == 1) $(elem).prop('checked', true).trigger('change');
	}));
});

forme(barjas, 'bukti_browse', function(bukti_browse) {
	var once = true;
	var contents = document.getElementById(bukti_browse.dataset.content);
	var tables = {};
	var columns = {};

	$(contents).children('[data-content]').each((i,content) => {
		$(content).children('table').each((i,table) => {
			tables[content.dataset.content] = table;

			jq_datatable_thead2columns({ table: table, });
			$(table).data('table', jq_tabelin(table, {
				dom: 'ft',
				scrollY: bukti_browse.dataset.tableHeight,
				columns: $(table).data('columns'),
				createdRow: (tbrow,entry) => {
					$(tbrow).on('dblclick', () => {
						$(barjas).trigger('browsed', [entry,]);
						$(bukti_browse).data('prompt').close();
					});
				},
			}));
		});
	});

	$(bukti_browse).data('prompt', jq_promptin({
		onshow: function(self) {
			if (once) self.getModalBody().append(contents);
			self.getModalDialog().css({width: bukti_browse.dataset.promptWidth});

			forme(bukti_browse.form, 'jenis_bku', jenis_bku => self.setTitle(jenis_bku.children[jenis_bku.selectedIndex].innerText));

			$(contents).children('[data-content]').each((i,elem) => {
				$(elem)[elem.dataset.content === barjas_extra.jenis_bku ? 'show' : 'hide']();
			});
		},
		onshown: function() {
			$(tables[barjas_extra.jenis_bku]).data('table').columns.adjust().draw();
		},
		onhide: function() {
			$(tables[barjas_extra.jenis_bku]).data('table').clear().draw();
		},
		onhidden: function($self) {
			once = false;
		},
	}));

	$(bukti_browse).on('click', function() {
		var params = $.extend({
			tahun: tahun,
			jenis_bku: barjas_extra.jenis_bku,
		}, kodeskpd);

		$wait.show();
		$.get(bukti_browse.dataset.href, params, result => {
			$(tables[barjas_extra.jenis_bku]).data('table').rows.add(result);
			$wait.hide();
			$(bukti_browse).data('prompt').open();
		})
		.fail(function() {
			$wait.hide();
			omfg('tidak bisa ambil bukti.', arguments);
			$(bukti_browse).data('prompt').open();
		});
	});
});

$(barjas).on('browsed', function(event, entry_0) {
	var entry = $.extend(true, {}, entry_0);
	var __type__ = 0;
	var jenis_bku = barjas_extra.jenis_bku;
	var no_bku = entry.no_bku || null;

	/* hapus no_bku, supaya tidak override input:no_bku.value (spj). */
	if (entry.no_bku) delete entry.no_bku;

	if (jenis_bku === 'SP2D') {
		$wait.show();
		$3.get(barjas_rincian.dataset.hrefRinciansp2d, $3.extend({
			tahun: tahun,
			nosp2d: entry.nosp2d, jenissp2d: entry.jenissp2d,
			kodebidang: entry.kodebidang, kodeprogram: entry.kodeprogram, kodekegiatan: entry.kodekegiatan,
			kodesubkegiatan: entry.kodesubkegiatan,
		}, kodeskpd), function(result) {
			$wait.hide();
			$(barjas).trigger('assigned', [__type__, entry, ]);

			$3(barjas_rincian).trigger('reload', [result.rincian,]);
			$3(barjas_potongan).trigger('reload', [result.potongan,]);
		}).fail(function() {
			$wait.hide();
			omfg(`tidak bisa ambil rincian ${jenis_bku}`, arguments);
		});

	} else if (jenis_bku === 'SPJ') {
		$wait.show();
		$3.get(barjas_rincian.dataset.hrefRincianspj, $3.extend({
			tahun: tahun,
			no_bku: no_bku, jenis_bku: jenis_bku,
			kodebidang: entry.kodebidang, kodeprogram: entry.kodeprogram, kodekegiatan: entry.kodekegiatan,
			kodesubkegiatan: entry.kodesubkegiatan,
		}, kodeskpd), function(result) {
			$wait.hide();
			$(barjas).trigger('assigned', [__type__, entry, ]);

			$3(barjas_rincian).trigger('reload', [result.rincian,]);
			$3(barjas_potongan).trigger('reload', [result.potongan,]);
		}).fail(function() {
			$wait.hide();
			omfg(`tidak bisa ambil rincian ${jenis_bku}`, arguments);
		});

	} else omfg(`tidak bisa ambil rincian. unknown:jenis_bku(${jenis_bku});`);
});

jq_datatable_thead2columns({ table: barjas_rincian,
	is_action_2: true,
	is_action_3: true,
	is_action_3_names: ['jumlah'],
	is_action_3_alias: column => (column === 'jumlah' ? barjas_extra.tjumlahf : column),
});
$(barjas_rincian).data('table', jq_tabelin(barjas_rincian, {
	scrollY: barjas_rincian.dataset.height,
	columns: $(barjas_rincian).data('columns'),
	footerCallback: function(tfrow,data) {
		jq_datatable_summaries({
			data: data,
			tfoot: tfrow.parentElement,
			summaries: {
				jumlah: self => ( self.__main__(barjas_extra.tjumlahf) ),
			},
		});
	},
}));
$(barjas_rincian).on('reload', function(event, data) {
	data = data || [];
	var table = $(this).data('table');

	table.clear();
	table.rows.add(data);

	/* redraw ketika prompt shown saja */
	$(barjas).data('prompt').isOpened() && ((data.length > 0 && table.columns.adjust().draw()) || table.draw());
});

jq_datatable_thead2columns({ table: barjas_potongan,
	form_prefix: '__potongan__',
	is_action_3: true,
	is_action_3_editable: true,
	is_action_3_names: ['jumlah'],
	is_action_3_alias: column => (column === 'jumlah' ? barjas_extra.tjumlahf : column),
	is_action_2: true,
	is_action_1: true,
	fn_action_1_updown_mk: self => {
		$(potongan).trigger('prompt', function(entry_0) {
			var table = $(self.table).data('table');
			var entry_1 = $.extend(true, {[barjas_extra.tjumlahf]:0}, entry_0,);

			var kode_rekening = table.data().toArray().map(n => n.kode_rekening);
			if (kode_rekening.indexOf(entry_1.kode_rekening) === -1) {
				table.row.add(entry_1) && table.columns.adjust().draw();
			}
		});
	},
});
$(barjas_potongan).data('table', jq_tabelin(barjas_potongan, {
	scrollY: barjas_potongan.dataset.height,
	columns: $(barjas_potongan).data('columns'),
	footerCallback: function(tfrow,data) {
		jq_datatable_summaries({
			data: data,
			tfoot: tfrow.parentElement,
			summaries: {
				jumlah: self => ( self.__main__(barjas_extra.tjumlahf) ),
			},
		});
	},
}));
$3(barjas_potongan).on('reload',function(event, data) {
	data = data || [];
	var table = $(this).data('table');

	table.clear();
	table.rows.add(data);

	/* redraw ketika prompt shown saja */
	$(barjas).data('prompt').isOpened() && ((data.length > 0 && table.columns.adjust().draw()) || table.draw());
});

$3(barjas).on('submit', function(event) {
	var jenis = barjas_extra.tjumlahf;
	var yeet = false;
	event.preventDefault();

	barjas_extra.required_0.forEach(function(name) {
		var value = forme(barjas, name, 'value');
		if (!value || String(value).trim() === '') {
			if (yeet) return;
			yeet = true;
			message_ok('error', `Isian ${name.toUpperCase()} Tidak Boleh Kosong.`);
		}
	});
	if (yeet) return;

	if (Number(forme(barjas, 'tgl_bku', 'value').replace(/[^0-9]/g, '')) < Number(forme(barjas, 'tgl_bukti', 'value').replace(/[^0-9]/g, ''))) {
		message_ok('error', 'TGL_BKU tidak boleh kurang dari TGL_BUKTI.');
		return;
	}

	if ((forme(barjas, 'simpananbank', 'checked') || forme(barjas, 'is_pihak_ketiga', 'checked')) === false) {
		message_ok('error', 'Cara Pencairan Belum di Pilih.');
		return;
	}

	if (forme(barjas, 'simpananbank', 'checked') && forme(barjas, 'is_pihak_ketiga', 'checked')) {
		event.preventDefault();
		message_ok('error', 'Cara Pencairan tidak boleh pilih keduanya.');
		return;
	}

	var data = $(barjas_rincian).data('table').data().toArray();
	var empty = data.map(n => n[jenis]).reduce((a,b) => (Number(a) + Number(b)));
	if (data.length === 0 || empty < 1) {
		message_ok('error','Rincian Masih Kosong.');
		return;
	}

	$wait.show();
	$3.post(barjas.action, $3(barjas).serialize(), function() {
		$wait.hide();
		$3(barjas).data('prompt').close();
		forme(bku_form, 'month', function(month) {
			month.value = Number(forme(barjas, 'tgl_bku', 'value').split('-')[1]);
			$3(month).trigger('change');
		});
	}).fail(function() {
		$wait.hide();
		omfg('terjadi errors saat simpan bku.', arguments);
	});
});

$(barjas).on('reset', () => ( $(barjas).data('prompt').isOpened() && $(barjas).data('prompt').close() ));

// $(document).ready(() => ( kodeskpd && $(barjas).trigger('prompt', [0,]) )); // [LINT] //

/*
	untuk panjar, saya bingung.
	opsi simpananbank|is_pihak_ketiga saya matikan, (simpananbank=1, is_pihak_ketiga=0).
*/

var panjar = prompts['panjar'] = document.getElementById('spjskpd_pengeluaran_panjar');
var panjar_rincian = null;
var panjar_potongan = null;
var panjar_extra = {
	jenis_bku_create_clear: [
		'urai',
		'bukti',
		'tgl_bku', 'tgl_bukti',
		'penerimaan', 'pengeluaran',
	],
	required: [,'no_bku', 'bukti','urai', 'tgl_bku', 'tgl_bukti', 'penerimaan', 'pengeluaran'],
	loaded_create_rm: ['jenis_bku'],
	loaded_update_rm: ['jenis_bku'],
	once: true,
	tjumlahf: null,
	jenis_bku_update_fn: e => ((e.penerimaan == 0 && e.pengeluaran != 0) ? 'KELUAR' : 'TERIMA'),
	jenis_bku: null,
	jenis_bku_defs: {}, /* html2object */
	v0: {
		jenis_bku: forme(panjar, 'jenis_bku', 'value'),
	},
};

$(panjar).data('tanggalin', ['tgl_bku', 'tgl_bukti']);
$(panjar).data('tanggalin').forEach(name => forme(panjar, name, elem => jq_tanggalin(elem)));

$(panjar).data('rupiahin', ['penerimaan', 'pengeluaran']);
$(panjar).data('rupiahin').forEach(name => forme(panjar, name, elem => {
	jq_rupiahin(elem);
	$(elem).next().on('keypress', event => {
		if (/Enter/.test(event.key)) { event.preventDefault(); $(event.currentTarget).trigger('blur'); }
	});
}));

$(panjar).data('centangin', ['simpananbank','is_pihak_ketiga']);
$(panjar).data('centangin').forEach(function(name) {
	forme(panjar, name, function(a) {
		$(a).on('change', function() {
			if (a.dataset.centanginReverse) {
				forme(panjar, a.dataset.centanginReverse, function(b) {
					if (a.checked) $(b).prop('checked', false).trigger('change');
				});
			}
		}); // :on:change:a
	}); // :forme:a
});

forme(panjar, 'jenis_bku_alt', function(jenis_bku_alt) {
	$(jenis_bku_alt).children().each((i,elem) => {
		panjar_extra.jenis_bku_defs[elem.value] = elem.innerText;
	});

	$(jenis_bku_alt).on('change', function() {
		panjar_extra.jenis_bku = jenis_bku_alt.value;

		forme(panjar, '__type__', function(__type__) {
			if (__type__.value == 0) {

				// disabled browse, jika prompt tidak ada. //
				forme(panjar, 'bukti_browse', bukti_browse => {
					var yn = true;

					$(document.getElementById(bukti_browse.dataset.content)).children('[data-content]').each((i,elem) => {
						if (elem.dataset.content === panjar_extra.jenis_bku) yn = false;
					});
					$(bukti_browse).prop('disabled', yn);
				});

				panjar_extra.jenis_bku_create_clear.forEach(function(name) {
					if ($(panjar).data('tanggalin').indexOf(name) > -1)
						forme(panjar, name, elem => $(elem).trigger('tanggalin', dated.current));
					else if ($(panjar).data('rupiahin').indexOf(name) > -1)
						forme(panjar, name, elem => $(elem).trigger('rupiahin', 0));
					else
						forme(panjar, name, elem => $(elem).prop('value','').trigger('change'));
				});

				forme(panjar, 'urai', 'value', panjar_extra.jenis_bku_defs[panjar_extra.jenis_bku]);
			}
		}); // :forme:__type__
	}); // :on:change
});

forme(panjar, 'bukti_browse', function(bukti_browse) {
	var contents = document.getElementById(bukti_browse.dataset.content);
	var once = true, tables = {};
	$(bukti_browse).data('prompt', jq_promptin({
		onshow: function(self) {
			if (once) self.getModalBody().append(contents);
			self.getModalDialog().css({ width: bukti_browse.dataset.promptWidth });

			forme(panjar, 'jenis_bku_alt', function(jenis_bku_alt) {
				self.setTitle(panjar_extra.jenis_bku_defs[panjar_extra.jenis_bku]);
			});

			$(contents).children('[data-content]').each((i,elem) => {
				$(elem)[elem.dataset.content === panjar_extra.jenis_bku ? 'show' : 'hide']();
			});
		},
		onshown: function() {
			$(tables[panjar_extra.jenis_bku]).data('table').columns.adjust().draw();
		},
		onhide: function() {
			$(tables[panjar_extra.jenis_bku]).data('table').clear().draw();
		},
		onhidden: () => { once = false; },
	}));

	$(bukti_browse).on('click', () => {
		var para = $.extend({
			tahun: tahun,
			jenis_bku: panjar_extra.v0.jenis_bku, // origin
		}, kodeskpd);
		$wait.show();
		$.get(bukti_browse.dataset.href, para, result => {
			$wait.hide();
			$(tables[panjar_extra.jenis_bku]).data('table').rows.add(result);
			$(bukti_browse).data('prompt').open();
		})
		.fail(function() { $wait.hide(); omfg('tidak bisa ambil bukti.', arguments); });
	});

	$(contents).children('[data-content]').each((i,content) => {
		$(content).children('table').each((i,table) => {
			tables[content.dataset.content] = table;
			jq_datatable_thead2columns({ table: table, });
			$(table).data('table', jq_tabelin(table, {
				dom: 'ft',
				scrollY: bukti_browse.dataset.tableHeight,
				columns: $(table).data('columns'),
				createdRow: (tbrow,entry) => {
					$(tbrow).on('dblclick', () => {
						$(panjar).trigger('browsed', [entry,]);
						$(bukti_browse).data('prompt').close();
					});
				},
			}));
		});
	});
});

$3(panjar).on('browsed', function(event, entry) {
	var __type__ = 0;
	var jenis_bku = panjar_extra.jenis_bku;
	var no_bku = entry.no_bku || null; if (entry.no_bku) delete entry.no_bku;

	if (jenis_bku === 'TERIMA') {
		var para = $.extend({
			tahun: tahun,
			jenis_bku: jenis_bku, no_bku: no_bku,
		}, kodeskpd);

		$wait.show();
		$.get(panjar.dataset.href, para, function(result) {
			$wait.hide();
			if (result.entry) {
				for (var i = 0; i < panjar_extra.loaded_create_rm.length; i++) {
					result.entry[panjar_extra.loaded_create_rm[i]] && delete result.entry[panjar_extra.loaded_create_rm[i]];
				}
				$.extend(true, entry, result.entry);
			}

			if (entry.urai) entry.urai = 'Pertanggung Jawaban ' + entry.urai;

			$(panjar).trigger('assigned', [__type__, entry, ]);
			$(panjar).data('prompt').open();
		}).fail(function() {
			$wait.hide();
			omfg(`tidak bisa ambil rincian "${jenis_bku}" (unknown).`, arguments);
		});

	} else omfg(`tidak bisa ambil rincian. unknown jenis_bku(${jenis_bku}).`);
});

$(panjar).data('prompt', jq_promptin({
	title: panjar.dataset.promptTitle,
	onshow: function($prompt) {
		if (panjar_extra.once) {
			$prompt.getModalBody().append(panjar);
			$prompt.getModalDialog().css('width', panjar.dataset.promptWidth);
		}
	},
	onshown:function() {},
	onhide: function() {},
	onhidden: function() {
		panjar_extra.once = false;
		$(panjar).trigger('reset');
	},
}));

$(panjar).on('prompt', function(event, __type__, entry) {
	forme(panjar, '__type__', 'value', __type__);
	forme(panjar, 'csrfmiddlewaretoken', 'value', window.spjskpd.kuki('csrftoken'));

	forme(panjar, 'tahun', 'value', tahun);
	if (kodeskpd) for (var k in kodeskpd) forme(panjar, k, 'value', kodeskpd[k]);

	forme(panjar, 'no_bku', 'readOnly', __type__ === 1);
	forme(panjar, 'bukti', 'readOnly', __type__ === 1); /* kata mbamad, ketika create, boleh manual. */
	forme(panjar, 'bukti_browse', 'disabled', __type__ === 1);

	forme(panjar, 'jenis_bku_alt', function(jenis_bku_alt) {
		jenis_bku_alt.selectedIndex = 0;
		var selected = entry ? panjar_extra.jenis_bku_update_fn(entry) : null;

		/* disabled dan selected secara bersamaan */
		$(jenis_bku_alt).children().each((i,elem) => {
			$(elem).prop('disabled', (__type__ === 1 && elem.value !== selected));
			$(elem).prop('selected', (__type__ === 1 && elem.value === selected));
		});

		$(jenis_bku_alt).trigger('change');
	});

	$(panjar).data('tanggalin').forEach(name => forme(panjar, name, elem => $(elem).trigger('tanggalin', dated.current)));
	$(panjar).data('rupiahin').forEach(name => forme(panjar, name, elem => $(elem).trigger('rupiahin', (entry && name in entry) ? entry[name] : 0)));
	$(panjar).data('centangin').forEach(name => forme(panjar, name, elem => $(elem).prop('checked', false).trigger('change')));

	if (__type__ === 0) {
		nobkuauto(
			function(no_bku) {
				forme(panjar, 'no_bku', 'value', no_bku);
				$(panjar).data('prompt').open();
			},
			function() {
				$(panjar).data('prompt').open();
			}
		);
	}

	if (__type__ === 1) {
		$wait.show();
		$.get(panjar.dataset.href, $.extend({
			tahun: tahun,
			no_bku: entry.no_bku,
			jenis_bku: entry.jenis_bku,
		}, kodeskpd), function(result) {
			$wait.hide();
			if (result.entry) {
				for (var i = 0; i < panjar_extra.loaded_update_rm.length; i++) {
					result.entry[panjar_extra.loaded_update_rm[i]] && delete result.entry[panjar_extra.loaded_update_rm[i]];
				}
				$.extend(true, entry, result.entry);
			}

			$(panjar).trigger('assigned', [__type__, entry, ]);
			$(panjar).data('prompt').open();

		}).fail(function() {
			$wait.hide();
			omfg('tidak bisa ambil rincian.', arguments);
		});
	}
});

$(panjar).on('assigned', function(event, __type__, entry) {
	for (var n in entry) {
		if ($(panjar).data('tanggalin').indexOf(n) > -1) continue;
		if ($(panjar).data('rupiahin').indexOf(n) > -1) continue;
		if ($(panjar).data('centangin').indexOf(n) > -1) continue;
		forme(panjar, n, 'value', entry[n]);
	}

	$(panjar).data('tanggalin').forEach(name => forme(panjar, name,
		elem => $(elem).trigger('tanggalin', (entry && entry[name]) ? entry[name] : dated.current)
	));
	$(panjar).data('rupiahin').forEach(name => forme(panjar, name,
		elem => $(elem).trigger('rupiahin', (entry && entry[name]) ? entry[name] : 0)
	));
	$(panjar).data('centangin').forEach(
		name => forme(panjar, name, elem => {
			if (entry && name in entry && entry[name] == 1) $(elem).prop('checked', true).trigger('change'); 
		})
	);
});

$(panjar).on('submit', function(event) {
	// return;
	event.preventDefault();
	var yeet = false;

	for (var v in panjar_extra.v0) forme(panjar, v, 'value', panjar_extra.v0[v]);

	panjar_extra.required.forEach(function(name) {
		if (yeet) return;
		var value = forme(panjar, name, 'value');
		if (!value || String(value).trim() === '') {
			yeet = true;
			message_ok('error', `Isian ${name.toUpperCase()} Tidak Boleh Kosong.`);
		}
	});
	if (yeet) return;

	if (
		forme(panjar, 'tgl_bku', 'value', v => Number(v.replace(/[^0-9]/g, ''))) <
		forme(panjar, 'tgl_bukti', 'value', v => Number(v.replace(/[^0-9]/g, '')))
	) {
		message_ok('error', 'TGL_BKU tidak boleh kurang dari TGL_BUKTI.'); return;
	}

	if ((forme(panjar, 'simpananbank', 'checked') || forme(panjar, 'is_pihak_ketiga', 'checked')) === false) {
		return message_ok('error', 'Belum Pilih Cara Pencairan.');
	}

	if (forme(panjar, 'simpananbank', 'checked') && forme(panjar, 'is_pihak_ketiga', 'checked')) {
		return message_ok('error', 'Cara Pencairan tidak boleh pilih keduanya.');
	}

	if (forme(panjar, 'penerimaan', 'value', v => Number(v)) === 0 && forme(panjar, 'pengeluaran', 'value', v => Number(v)) === 0) {
		message_ok('error', 'Jumlah Panjar Masih Kosong'); return;
	}

	$wait.show();
	$.post(panjar.action, $(panjar).serialize(), function() {
		$wait.hide();
		$(panjar).data('prompt').close();

		forme(bku_form, 'month', month => {
				$(month).prop('value', forme(panjar,'tgl_bku','value',
					v => Number(v.split('-')[1])
				)).trigger('change');
		});
	}).fail(function() {
		$wait.hide();
		omfg('terjadi errors saat simpan panjar.', arguments);
	});
});
$(panjar).on('reset', () => ( $(panjar).data('prompt').isOpened() && $(panjar).data('prompt').close() ));

// $(document).ready(() => ( kodeskpd && $(panjar).trigger('prompt', [0,]) )); // [TEST] //

// PELIMPAHAN
var pelimpahan = prompts['pelimpahan'] = document.getElementById('spjskpd_pengeluaran_pelimpahan');
var pelimpahan_rincian = null;
var pelimpahan_potongan = null;
var pelimpahan_extra = {
	jenis_bku_create_clear: [
		'urai',
		'bukti',
		'tgl_bku', 'tgl_bukti',
		'penerimaan', 'frm_benda_bantu', 'frm_benda_bantu_uname'
	],
	required: ['frm_benda_bantu' ,'no_bku', 'bukti','urai', 'tgl_bku', 'tgl_bukti', 'penerimaan', ],
	loaded_create_rm: ['jenis_bku'],
	loaded_update_rm: ['jenis_bku'],
	once: true,
	tjumlahf: null,
	jenis_bku_update_fn: e => ((e.penerimaan == 0 && e.pengeluaran != 0) ? 'KELUAR' : 'TERIMA'),
	jenis_bku: null,
	jenis_bku_defs: {}, /* html2object */
	v0: {
		jenis_bku: forme(pelimpahan, 'jenis_bku', 'value'),
	},
};

$(pelimpahan).data('tanggalin', ['tgl_bku', 'tgl_bukti']);
$(pelimpahan).data('tanggalin').forEach(name => forme(pelimpahan, name, elem => jq_tanggalin(elem)));

$(pelimpahan).data('rupiahin', ['penerimaan']);
$(pelimpahan).data('rupiahin').forEach(name => forme(pelimpahan, name, elem => {
	jq_rupiahin(elem);
	$(elem).next().on('keypress', event => {
		if (/Enter/.test(event.key)) { event.preventDefault(); $(event.currentTarget).trigger('blur'); }
	});
}));

forme(pelimpahan, 'jenis_bku_alt', function(jenis_bku_alt) {
	$(jenis_bku_alt).children().each((i,elem) => {
		pelimpahan_extra.jenis_bku_defs[elem.value] = elem.innerText;
	});

	$(jenis_bku_alt).on('change', function() {
		pelimpahan_extra.jenis_bku = jenis_bku_alt.value;

		forme(pelimpahan, '__type__', function(__type__) {
			if (__type__.value == 0) {

				// disabled browse, jika prompt tidak ada. //
				forme(pelimpahan, 'bukti_browse', bukti_browse => {
					var yn = true;
					
					$(document.getElementById(bukti_browse.dataset.content)).children('[data-content]').each((i,elem) => {
						if (elem.dataset.content === pelimpahan_extra.jenis_bku) yn = false;
					});
					$(bukti_browse).prop('disabled', yn);
				});

				if (pelimpahan_extra.jenis_bku == 'TERIMA') {
					$('#sec_benda_bantu').css('display', 'none')
				}else{
					$('#sec_benda_bantu').css('display', '');
				}

				pelimpahan_extra.jenis_bku_create_clear.forEach(function(name) {
					if ($(pelimpahan).data('tanggalin').indexOf(name) > -1)
						forme(pelimpahan, name, elem => $(elem).trigger('tanggalin', dated.current));
					else if ($(pelimpahan).data('rupiahin').indexOf(name) > -1)
						forme(pelimpahan, name, elem => $(elem).trigger('rupiahin', 0));
					else
						forme(pelimpahan, name, elem => $(elem).prop('value','').trigger('change'));
				});

				forme(pelimpahan, 'urai', 'value', pelimpahan_extra.jenis_bku_defs[pelimpahan_extra.jenis_bku]);
			}
		}); // :forme:__type__
	}); // :on:change
});

forme(pelimpahan, 'bukti_browse', function(bukti_browse) {
	var contents = document.getElementById(bukti_browse.dataset.content);
	var once = true, tables = {};
	$(bukti_browse).data('prompt', jq_promptin({
		onshow: function(self) {
			if (once) self.getModalBody().append(contents);
			self.getModalDialog().css({ width: bukti_browse.dataset.promptWidth });

			forme(pelimpahan, 'jenis_bku_alt', function(jenis_bku_alt) {
				self.setTitle(pelimpahan_extra.jenis_bku_defs[pelimpahan_extra.jenis_bku]);
			});

			$(contents).children('[data-content]').each((i,elem) => {
				$(elem)[elem.dataset.content === pelimpahan_extra.jenis_bku ? 'show' : 'hide']();
			});
		},
		onshown: function() {
			$(tables[pelimpahan_extra.jenis_bku]).data('table').columns.adjust().draw();
		},
		onhide: function() {
			$(tables[pelimpahan_extra.jenis_bku]).data('table').clear().draw();
		},
		onhidden: () => { once = false; },
	}));

	$(bukti_browse).on('click', () => {
		var para = $.extend({
			tahun: tahun,
			jenis_bku: pelimpahan_extra.v0.jenis_bku, // origin
		}, kodeskpd);

		$wait.show();
		$.get(bukti_browse.dataset.href, para, result => {
			$wait.hide();
			$(tables[pelimpahan_extra.jenis_bku]).data('table').rows.add(result);
			$(bukti_browse).data('prompt').open();
		})
		.fail(function() { $wait.hide(); omfg('tidak bisa ambil bukti.', arguments); });
	});

	$(contents).children('[data-content]').each((i,content) => {
		$(content).children('table').each((i,table) => {
			tables[content.dataset.content] = table;
			jq_datatable_thead2columns({ table: table, });
			$(table).data('table', jq_tabelin(table, {
				dom: 'ft',
				scrollY: bukti_browse.dataset.tableHeight,
				columns: $(table).data('columns'),
				createdRow: (tbrow,entry) => {
					$(tbrow).on('dblclick', () => {
						// $(pelimpahan).trigger('browsed', [entry,]);
						
						$('#frm_benda_bantu').val(entry['nama_bendahara_pembantu']);
						$('#frm_benda_bantu_uname').val(entry['uname']);
						$(bukti_browse).data('prompt').close();
					});
				},
			}));
		});
	});
});

$3(pelimpahan).on('browsed', function(event, entry) {
	var __type__ = 0;
	var jenis_bku = pelimpahan_extra.jenis_bku;
	var no_bku = entry.no_bku || null; if (entry.no_bku) delete entry.no_bku;

	if (jenis_bku === 'KELUAR') {
		var para = $.extend({
			tahun: tahun,
			jenis_bku: jenis_bku, no_bku: no_bku,
		}, kodeskpd);

		$wait.show();
		$.get(pelimpahan.dataset.href, para, function(result) {
			$wait.hide();
			if (result.entry) {
				for (var i = 0; i < pelimpahan_extra.loaded_create_rm.length; i++) {
					result.entry[pelimpahan_extra.loaded_create_rm[i]] && delete result.entry[pelimpahan_extra.loaded_create_rm[i]];
				}
				$.extend(true, entry, result.entry);
			}

			if (entry.urai) entry.urai = 'Pertanggung Jawaban ' + entry.urai;

			$(pelimpahan).trigger('assigned', [__type__, entry, ]);
			$(pelimpahan).data('prompt').open();
		}).fail(function() {
			$wait.hide();
			omfg(`tidak bisa ambil rincian "${jenis_bku}" (unknown).`, arguments);
		});

	} else omfg(`tidak bisa ambil rincian. unknown jenis_bku(${jenis_bku}).`);
});

$(pelimpahan).data('prompt', jq_promptin({
	title: pelimpahan.dataset.promptTitle,
	onshow: function($prompt) {
		if (pelimpahan_extra.once) {
			$prompt.getModalBody().append(pelimpahan);
			$prompt.getModalDialog().css('width', pelimpahan.dataset.promptWidth);
		}
	},
	onshown:function() {},
	onhide: function() {},
	onhidden: function() {
		pelimpahan_extra.once = false;
		$(pelimpahan).trigger('reset');
	},
}));

$(pelimpahan).on('prompt', function(event, __type__, entry) {
	forme(pelimpahan, '__type__', 'value', __type__);
	forme(pelimpahan, 'csrfmiddlewaretoken', 'value', window.spjskpd.kuki('csrftoken'));

	forme(pelimpahan, 'tahun', 'value', tahun);
	if (kodeskpd) for (var k in kodeskpd) forme(pelimpahan, k, 'value', kodeskpd[k]);

	forme(pelimpahan, 'no_bku', 'readOnly', __type__ === 0);
	forme(pelimpahan, 'bukti', 'readOnly', __type__ === 1); /* kata mbamad, ketika create, boleh manual. */
	forme(pelimpahan, 'bukti_browse', 'disabled', __type__ === 1);

	forme(pelimpahan, 'jenis_bku_alt', function(jenis_bku_alt) {
		jenis_bku_alt.selectedIndex = 0;
		var selected = entry ? pelimpahan_extra.jenis_bku_update_fn(entry) : null;

		/* disabled dan selected secara bersamaan */
		$(jenis_bku_alt).children().each((i,elem) => {
			$(elem).prop('disabled', (__type__ === 1 && elem.value !== selected));
			$(elem).prop('selected', (__type__ === 1 && elem.value === selected));
		});

		$(jenis_bku_alt).trigger('change');
	});

	$(pelimpahan).data('tanggalin').forEach(name => forme(pelimpahan, name, elem => $(elem).trigger('tanggalin', dated.current)));
	$(pelimpahan).data('rupiahin').forEach(name => forme(pelimpahan, name, elem => $(elem).trigger('rupiahin', (entry && name in entry) ? entry[name] : 0)));

	if (__type__ === 0) {
		nobkuauto(
			function(no_bku) {
				forme(pelimpahan, 'no_bku', 'value', no_bku);
				$(pelimpahan).data('prompt').open();
			},
			function() {
				$(pelimpahan).data('prompt').open();
			}
		);
	}

	if (__type__ === 1) {
		$wait.show();
		$.get(pelimpahan.dataset.href, $.extend({
			tahun: tahun,
			no_bku: entry.no_bku,
			jenis_bku: entry.jenis_bku,
		}, kodeskpd), function(result) {
			$wait.hide();
			if (result.entry) {
				for (var i = 0; i < pelimpahan_extra.loaded_update_rm.length; i++) {
					result.entry[pelimpahan_extra.loaded_update_rm[i]] && delete result.entry[pelimpahan_extra.loaded_update_rm[i]];
				}
				$.extend(true, entry, result.entry);
			}

			$(pelimpahan).trigger('assigned', [__type__, entry, ]);
			$(pelimpahan).data('prompt').open();

		}).fail(function() {
			$wait.hide();
			omfg('tidak bisa ambil rincian.', arguments);
		});
	}
});

$(pelimpahan).on('assigned', function(event, __type__, entry) {
	for (var n in entry) {
		if ($(pelimpahan).data('tanggalin').indexOf(n) > -1) continue;
		if ($(pelimpahan).data('rupiahin').indexOf(n) > -1) continue;
		forme(pelimpahan, n, 'value', entry[n]);
	}

	$(pelimpahan).data('tanggalin').forEach(name => forme(pelimpahan, name,
		elem => $(elem).trigger('tanggalin', (entry && entry[name]) ? entry[name] : dated.current)
	));
	$(pelimpahan).data('rupiahin').forEach(name => forme(pelimpahan, name,
		elem => $(elem).trigger('rupiahin', (entry && entry[name]) ? entry[name] : 0)
	));
});

$(pelimpahan).on('submit', function(event) {
	// return;
	event.preventDefault();
	var yeet = false;

	for (var v in pelimpahan_extra.v0) forme(pelimpahan, v, 'value', pelimpahan_extra.v0[v]);
		if (pelimpahan_extra.jenis_bku == 'TERIMA') {
			pelimpahan_extra.required.splice( $.inArray( 'frm_benda_bantu', pelimpahan_extra.required), 1 );
		}else{
			if(jQuery.inArray("frm_benda_bantu", pelimpahan_extra.required) === -1) {
			    pelimpahan_extra.required.unshift('frm_benda_bantu')
			}
		}
		
	pelimpahan_extra.required.forEach(function(name) {
		if (yeet) return;
		var value = forme(pelimpahan, name, 'value');

		if (!value || String(value).trim() === '') {
			yeet = true;

			if (name == 'frm_benda_bantu') {
				name = 'Bendahara Pembantu'
			}
			message_ok('error', `Isian ${name.toUpperCase()} Tidak Boleh Kosong.`);
		}
	});
	if (yeet) return;

	if (
		forme(pelimpahan, 'tgl_bku', 'value', v => Number(v.replace(/[^0-9]/g, ''))) <
		forme(pelimpahan, 'tgl_bukti', 'value', v => Number(v.replace(/[^0-9]/g, '')))
	) {
		message_ok('error', 'TGL_BKU tidak boleh kurang dari TGL_BUKTI.'); return;
	}

	if (forme(pelimpahan, 'penerimaan', 'value', v => Number(v)) === 0 && forme(pelimpahan, 'pengeluaran', 'value', v => Number(v)) === 0) {
		message_ok('error', 'Jumlah pelimpahan Masih Kosong'); return;
	}

	$wait.show();
	$.post(pelimpahan.action, $(pelimpahan).serialize(), function() {
		$wait.hide();
		$(pelimpahan).data('prompt').close();

		forme(bku_form, 'month', month => {
				$(month).prop('value', forme(pelimpahan,'tgl_bku','value',
					v => Number(v.split('-')[1])
				)).trigger('change');
		});
	}).fail(function() {
		$wait.hide();
		omfg('terjadi errors saat simpan pelimpahan.', arguments);
	});
});
$(pelimpahan).on('reset', () => ( $(pelimpahan).data('prompt').isOpened() && $(pelimpahan).data('prompt').close() ));


var pajak_extra = {
	jenis_bku_create_clear: ['bukti','urai','tgl_bku','tgl_bukti'],
	required: [,'no_bku', 'bukti','urai','jenis_sp2d', 'tgl_bku', 'tgl_bukti'],
	once: true,
	tjumlahf: null,
	jenis_bku: null,
	is_penerimaan: null,
	is_penerimaan_re: /PUNGUT/,
	potongan_params: [{ kodejenis: 1 },{ kodejenis: 3 }],
	nosspauto: entry => eval(pajak.dataset.nosspformat),
};
var pajak = prompts['pajak'] = document.getElementById('spjskpd_pengeluaran_pajak');
var pajak_rincian = null;
var pajak_potongan = document.getElementById('spjskpd_pengeluaran_pajak_potongan');

$(pajak).data('tanggalin', ['tgl_bku', 'tgl_bukti']);
$(pajak).data('tanggalin').forEach(name => forme(pajak, name, elem => {
	jq_tanggalin(elem);
	if (name === 'tgl_bku') {
		$(elem).on('change', event => {
			if (pajak_extra.is_penerimaan && $(pajak).data('prompt').isOpened()) {
				$(pajak).trigger('noauto', { params:{ nosspauto:1 } });
			}
		});
	}
}));

$(pajak).data('centangin', ['simpananbank','is_pihak_ketiga']);
$(pajak).data('centangin').forEach(function(name) {
	forme(pajak, name, function(a) {
		$(a).on('change', function() {
			if (a.dataset.centanginReverse) {
				forme(pajak, a.dataset.centanginReverse, function(b) {
					if (a.checked) $(b).prop('checked', false).trigger('change');
				});
			}
		}); // :on:change:a
	}); // :forme:a
});

forme(pajak, 'jenis_bku', function(jenis_bku) {
	$(jenis_bku).on('change', function() {
		pajak_extra.jenis_bku = jenis_bku.value;
		pajak_extra.is_penerimaan = pajak_extra.is_penerimaan_re.test(pajak_extra.jenis_bku);
		pajak_extra.tjumlahf = pajak_extra.is_penerimaan ? 'penerimaan' : 'pengeluaran';

		$(pajak_potongan).trigger('reload', [[],]);

		/* pungut === manual */
		forme(pajak, 'bukti', 'readOnly', false);
		forme(pajak, 'bukti_browse', 'disabled', pajak_extra.is_penerimaan);

		forme(pajak, '__type__', function(__type__) {
			if (__type__.value == 0) {
				pajak_extra.jenis_bku_create_clear.forEach(function(name) {
					if ($(pajak).data('tanggalin').indexOf(name) > -1)
						forme(pajak, name, elem => $(elem).trigger('tanggalin', dated.current));
					else
						forme(pajak, name, elem => $(elem).prop('value','').trigger('change'));
				});

				if (pajak_extra.is_penerimaan && $(pajak).data('prompt').isOpened()) {
					$(pajak).trigger('noauto', { params:{ nosspauto:1 } });
				}
			}
		}); // :forme:__type__
	}); // :on:change
});

$(pajak).data('prompt', jq_promptin({
	title: pajak.dataset.promptTitle,
	onshow: function($prompt) {
		potongan_extra.reload = true; /* [IMPORTANT] ./main.js#potongan:prompt():shown() */

		$prompt.getModalDialog().css('width', pajak.dataset.promptWidth);
		if (pajak_extra.once) {
			$prompt.getModalBody().append(pajak);
		}
	},
	onshown:function() {
		$(pajak_potongan).data('table').columns.adjust().draw();
	},
	onhide: function() {
		$(pajak_potongan).data('table').clear().draw();
	},
	onhidden: function() {
		potongan_extra.reload = true; /* [IMPORTANT] ./main.js#potongan:prompt():shown() */
		pajak_extra.once = false;
		$(pajak).trigger('reset');
	},
}));

$(pajak).on('prompt', function(event, __type__, entry) {
	forme(pajak, '__type__', 'value', __type__);
	forme(pajak, 'csrfmiddlewaretoken', 'value', window.spjskpd.kuki('csrftoken'));

	forme(pajak, 'tahun', 'value', tahun);
	if (kodeskpd) for (var k in kodeskpd) forme(pajak, k, 'value', kodeskpd[k]);

	forme(pajak, 'jenis_sp2d', elem => $(elem).each(i => { elem[i].checked = false }));
	forme(pajak, 'no_bku', 'readOnly', __type__ === 1);
	forme(pajak, 'jenis_bku', function(jenis_bku) {
		$(jenis_bku).children().prop('disabled', false);
		jenis_bku.selectedIndex = 0;
		if (__type__ === 1 && entry && entry.jenis_bku) {
			jenis_bku.value = entry.jenis_bku;
			$(jenis_bku.children).each(function(i,elem) {
				if (elem.value !== entry.jenis_bku) elem.disabled = true;
			});
		}
		$(jenis_bku).trigger('change');
	});

	$(pajak).data('tanggalin').forEach(name => forme(pajak, name, elem => $(elem).trigger('tanggalin', dated.current)));
	$(pajak).data('centangin').forEach(name => forme(pajak, name, elem => $(elem).prop('checked', false).trigger('change')));

	if (__type__ === 0) {
		$(pajak).trigger('noauto', {
			params: { nobkuauto: 1, nosspauto: Number(pajak_extra.is_penerimaan), },
			y: () => $(pajak).data('prompt').open(),
			n: () => $(pajak).data('prompt').open(),
		});
	}

	if (__type__ === 1) {
		/* jenis_bku:__type__:0 */
		forme(pajak, 'bukti', 'readOnly', true);
		forme(pajak, 'bukti_browse', 'disabled', true);

		$wait.show();
		$.get(pajak_potongan.dataset.hrefBkurincian, $.extend({
			tahun: tahun,
			no_bku: entry.no_bku, jenis_bku: entry.jenis_bku,
			jenis_sp2d: entry.jenis_sp2d,
		}, kodeskpd), function(result) {
			$wait.hide();
			result.entry && $.extend(true, entry, result.entry);

			$3(pajak_potongan).trigger('reload', [result.potongan,]);

			$3(pajak).trigger('assigned', [__type__, entry, ]);
			$3(pajak).data('prompt').open();

		}).fail(function() {
			$wait.hide();
			omfg('tidak bisa ambil rincian.', arguments);
		});
	}
});

$(pajak).on('noauto', function(event, args) {
	var params = $.extend(true, {
		tahun: tahun,
		isskpd: isskpd,
		jenis_bku: pajak_extra.jenis_bku,
		bulan: forme(pajak, 'tgl_bku', 'value', v => Number( v.split('-')[1] )),
	}, kodeskpd, args.params);
	params.nosspauto = Number(pajak.dataset.nosspauto);

	$wait.show();
	$.get(pajak.dataset.noauto, params, function(result) {
		$wait.hide();
		if (result.nobkuauto) forme(pajak, 'no_bku', 'value', result.nobkuauto);
		if (result.nosspauto) {
			forme(pajak, 'bukti', bukti => {
				bukti.value = pajak_extra.nosspauto({
					kodeskpd: kodeskpd_index.join('.'),
					month: params.bulan,
					total: result.nosspauto,
				});
			});
		}

		if (args.y) args.y(result);
	})
	.fail(function() {
		$wait.hide();
		if (args.n) args.n();
		omfg('tidak bisa ambil NOAUTO terakhir.', arguments);
	});
});

$(pajak).on('assigned', function(event, __type__, entry) {
	for (var n in entry) {
		if ($(pajak).data('tanggalin').indexOf(n) > -1) continue;
		if ($(pajak).data('centangin').indexOf(n) > -1) continue;
		forme(pajak, n, 'value', entry[n]);
	}

	$(pajak).data('tanggalin').forEach(
		name => forme(pajak, name,
			elem => $(elem).trigger('tanggalin', (entry && name in entry) ? entry[name] : dated.current)
		)
	);
	$(pajak).data('centangin').forEach(
		name => forme(pajak, name, elem => {
			if (entry && name in entry && entry[name] == 1) $(elem).prop('checked', true).trigger('change'); 
		})
	);
});

jq_datatable_thead2columns({ table: pajak_potongan, form_prefix: '__rincian__',
	is_action_2: true,
	is_action_3: true,
	is_action_3_names: ['jumlah'],
	is_action_3_alias: { jumlah: () => pajak_extra.tjumlahf, },
	is_action_3_editable: true,
	is_action_1: true,
	fn_action_1_updown_mk: self => {
		$(potongan).trigger('prompt', [
			pajak_extra.potongan_params,
			entry_0 => {
				var entry_1 = $.extend(true, {[pajak_extra.tjumlahf]:0}, entry_0);
				var table = $(pajak_potongan).data('table');
				var kode_rekening = table.data().toArray().map(n => n.kode_rekening);
				if (kode_rekening.indexOf(entry_1.kode_rekening) === -1) {
					table.row.add(entry_1); table.columns.adjust().draw();
				}
			},
		]);
	},
});
$(pajak_potongan).data('table', jq_tabelin(pajak_potongan, {
	scrollY: pajak_potongan.dataset.height,
	columns: $(pajak_potongan).data('columns'),
	footerCallback: function(tfrow,data) {
		jq_datatable_summaries({
			data: data,
			tfoot: tfrow.parentElement,
			summaries: { jumlah: self => self.__main__(pajak_extra.tjumlahf), },
		});
	},
}));
$(pajak_potongan).on('reload',(event,data) => {
	var table = $(pajak_potongan).data('table');
	data = data || [];

	table.clear();
	table.rows.add(data);

	/* redraw ketika prompt shown saja */
	$(pajak).data('prompt').isOpened() && ((data.length > 0 && table.columns.adjust().draw()) || table.draw());
});

forme(pajak, 'bukti_browse', function(bukti_browse) {
	var contents = document.getElementById(bukti_browse.dataset.content);
	var once = true, tables = {};

	$(bukti_browse).on('click', () => {
		$wait.show();
		var para = $.extend({tahun: tahun, jenis_bku: pajak_extra.jenis_bku}, kodeskpd);
		$.get(bukti_browse.dataset.href, para, result => {
			$wait.hide();
			$(tables[pajak_extra.jenis_bku]).data('table').rows.add(result);
			$(bukti_browse).data('prompt').open();
		})
		.fail(function() {
			$wait.hide(); omfg('tidak bisa ambil bukti.', arguments);
		});
	});

	$(contents).children('[data-content]').each((i,content) => {
		$(content).children('table').each((i,table) => {
			tables[content.dataset.content] = table;

			jq_datatable_thead2columns({ table: table, });
			$(table).data('table', jq_tabelin(table, {
				dom: 'ft',
				scrollY: bukti_browse.dataset.tableHeight,
				columns: $(table).data('columns'),
				createdRow: (tbrow,entry) => $(tbrow).on('dblclick', () => {
					$(pajak).trigger('browsed', [entry,]); $(bukti_browse).data('prompt').close();
				}),
			}));
		});
	});

	$(bukti_browse).data('prompt', jq_promptin({
		onshow: function(self) {
			if (once) self.getModalBody().append(contents);
			self.getModalDialog().css({width: bukti_browse.dataset.promptWidth});

			forme(pajak, 'jenis_bku', jenis_bku => {
				self.setTitle(jenis_bku.children[jenis_bku.selectedIndex].innerText);
			});

			$(contents).children('[data-content]').each((i,elem) => $(elem)[elem.dataset.content === pajak_extra.jenis_bku ? 'show' : 'hide']());
		},
		onshown: function() {
			$(tables[pajak_extra.jenis_bku]).data('table').columns.adjust().draw();
		},
		onhide: function() {
			$(tables[pajak_extra.jenis_bku]).data('table').clear().draw();
		},
		onhidden: () => { once = false; },
	}));
});

$3(pajak).on('browsed', function(event, entry) {
	var __type__ = 0;
	var jenis_bku = pajak_extra.jenis_bku;
	var no_bku = entry.no_bku || null; if (entry.no_bku) delete entry.no_bku;

	if (jenis_bku === 'SETOR-PAJAK') {
		var para = $.extend({
			tahun: tahun,
			jenis_bku: jenis_bku, no_bku: no_bku,
			jenis_sp2d: entry.jenis_sp2d,
			keluar_eq_terima: 1,
		}, kodeskpd);

		$wait.show();
		$.get(pajak_potongan.dataset.hrefBkurincian, para, function(result) {
			$wait.hide();
			$(pajak_potongan).trigger('reload', [result.potongan,]);
			$3(pajak).trigger('assigned', [__type__, entry, ]);

		}).fail(function() {
			$wait.hide();
			omfg(`tidak bisa ambil rincian "${jenis_bku}" (unknown).`, arguments);
		});

	} else omfg(`tidak bisa ambil rincian. unknown jenis_bku(${jenis_bku}).`);
});

$3(pajak).on('submit', function(event) {
	// return;
	event.preventDefault();
	var jenis = pajak_extra.tjumlahf;
	var yeet = false;

	pajak_extra.required.forEach(function(name) {
		if (yeet) return;
		var value = forme(pajak, name, 'value');
		if (!value || String(value).trim() === '') {
			message_ok('error', `Isian ${name.toUpperCase()} Tidak Boleh Kosong.`);
			yeet = true;
		}
	});
	if (yeet) return;

	if (
		forme(pajak, 'tgl_bku', 'value', v => Number(v.replace(/[^0-9]/g, ''))) <
		forme(pajak, 'tgl_bukti', 'value', v => Number(v.replace(/[^0-9]/g, '')))
	) {
		return message_ok('error', 'TGL_BKU tidak boleh kurang dari TGL_BUKTI.');
	}

	if ((forme(pajak, 'simpananbank', 'checked') || forme(pajak, 'is_pihak_ketiga', 'checked')) === false) {
		return message_ok('error', 'Belum Pilih Cara Pencairan.');
	}

	if (forme(pajak, 'simpananbank', 'checked') && forme(pajak, 'is_pihak_ketiga', 'checked')) {
		return message_ok('error', 'Cara Pencairan tidak boleh pilih keduanya.');
	}

	var data = $(pajak_potongan).data('table').data().toArray();
	var empty = data.map(n => n[jenis]).reduce((a,b) => (Number(a) + Number(b)),0);
	if (data.length < 0 || empty < 1) {
		return message_ok('error','Rincian Masih Kosong.');
	}

	$wait.show();
	$.post(pajak.action, $(pajak).serialize(), function() {
		$wait.hide();
		$(pajak).data('prompt').close();
		forme(bku_form, 'month', month => {
				$(month)
				.prop('value', forme(pajak,'tgl_bku','value', v => Number(v.split('-')[1]) ))
				.trigger('change');
		});
	}).fail(function() {
		$wait.hide();
		omfg('terjadi errors saat simpan BKU.', arguments);
	});
});

$(pajak).on('reset', function() {
	$(pajak).data('prompt').isOpened() && $(pajak).data('prompt').close();
});

// Pelimpahan


// $(document).ready(() => ( kodeskpd && $(pajak).trigger('prompt', [0,]) )); // [TEST] //
})();
