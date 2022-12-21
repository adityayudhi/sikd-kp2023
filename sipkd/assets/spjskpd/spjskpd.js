/* @copyright: PT. Global Intermedia Nusantara; @version: 20190401,201904,201907; @author: anovsiradj; */
window.unknown = {}.undefined;

($3 || $1 || $)(document).ajaxSuccess(function(event, jqxhr, options, data) {
	var kuki = jqxhr.getResponseHeader('Set-Cookie');
	if (kuki) window.spjskpd.cookies = kuki;
});

window.spjskpd = window.spjskpd || {};
window.spjskpd.anov_csrf_token_init = document.getElementById('anov_csrf_token_init').querySelector('input').value;
window.spjskpd.cookies = '';

$3.extend(true, window.spjskpd, {
	kuki_00: function(k,kv) {
		var v = null;
		var kukies = kv || document.cookie || window.spjskpd.cookies;

		kukies = kukies.split(';').map(kv => kv.trim());
		if (!k) return kukies;

		kukies.forEach(function(kuki) {
			kuki = kuki.split('=');
			if (/csrf/.test(kuki[0])) window.spjskpd.anov_csrf_token_init = kuki[1];
			if (kuki[0] === k) {
				v = kuki[1];
				return;
			}
		});
		return v;
	},
	kuki: function(k) {
		if (/csrf/.test(k)) return window.spjskpd.anov_csrf_token_init;
		return window.spjskpd.kuki_00(k);
	},
	squote: function(str) {
		return ["'",str,"'"].join('');
	},
	dquote: function(str) {
		return ['"',str,'"'].join('');
	},
	kodeskpd_01: function() {
		var elem = document.getElementById('kd_org2');
		if (elem && elem.value.trim() !== '') return elem.value.trim().split('.');
		return null;
	},
	omfg: function() {
		var $ = window.$3 || window.$1 || window.$, _ = [];
		$.each(arguments, function(i,dump) {
			if (typeof (dump) === 'object') _.push(window.JSON.stringify(dump));
			else _.push(dump);
		});
		window.alert(_.join('\n'));
	},
	dump: function() {
		var $ = window.$3 || window.$1 || window.$;
		$.each(arguments, function(i,dump) {
			window.console.log(dump);
		});
	},
	doxce: function(name, attr_prop) {
		var $ = window.$3 || window.$1 || window.$;
		var elem;
		elem = document.createElement(name);
		for (var ap in attr_prop) {
			if (ap in elem) {
				if ($.isPlainObject(attr_prop[ap])) $.extend(true, elem[ap], attr_prop[ap]);
				else elem[ap] = attr_prop[ap];

			} else elem.setAttribute(ap, attr_prop[ap]);
		}
		return elem;
	},
	debounce: function(func, wait, immediate) {
		var timeout;
		return function() {
			var context = this, args = arguments;
			var later = function() {
				timeout = null;
				if (!immediate) func.apply(context, args);
			};
			var callNow = immediate && !timeout;
			clearTimeout(timeout);
			timeout = setTimeout(later, wait);
			if (callNow) func.apply(context, args);
		};
	},
	bs3dialog: {
		size: BootstrapDialog.SIZE_SMALL,
		closeByBackdrop: false,
		closeByKeyboard: false,
		// animate: false,
		draggable: true,
		autodestroy: false,
	},
	alertable_yn: {
		html: true,
		cancelButton: '<button class="alertable-cancel" type="button">Tidak</button>',
		okButton: '<button class="alertable-ok" autofocus>Ya</button>',
	},
	alertable_rm: {
		html: true,
		cancelButton: '<button class="alertable-cancel" type="button">Batal</button>',
		okButton: '<button class="alertable-ok" autofocus>Hapus</button>',
	},
	daterangepicker: {
		singleDatePicker: true,
		calender_style: 'picker_4',
	},
	datatable: {
		paging: false,
		ordering: false, order: [],
		language: {
			search: 'Pencarian: ',
			zeroRecords: '<div class="text-muted text-center">(kosong)</div>',
			emptyTable: '<div class="text-muted text-center">(kosong)</div>',
		},
		dom: 't',
	},
	jq_datatable: (table, params) => {
		return $1(table).DataTable( $3.extend(true, {}, window.spjskpd.datatable, params) );
	},
	jq_daterangepicker: (input, params_0) => {
		var params_1 = {};
		var callback_1 = $3.noop;
		var callback_0 = (moment_0,moment_1,label) => {
			var moment = moment_0 || moment_1 || null;
			callback_1( moment.toDate(), moment.format('YYYY-MM-DD'), label );
		};

		if (params_0 === window.unknown) params_0 = {};

		if ($3.isFunction(params_0)) {
			callback_1 = params_0;
			params_0 = { date: new window.Date, };
		}

		if ($3.isPlainObject(params_0)) {
			if (params_0.date) {
				if (typeof params_0.date) params_0.date = new window.Date(params_0.date);
				params_0.startDate = params_0.endDate = params_0.date;
				delete params_0.date;
			}
			if (params_0.min) { params_0.minDate = params_0.min; delete params_0.min; }
			if (params_0.max) { params_0.maxDate = params_0.max; delete params_0.max; }
			if (params_0.callback) { callback_1 = params_0.callback; delete params_0.callback; }

			$3.extend(true , params_1, params_0);
		}
		$3.extend(true , params_1, window.spjskpd.daterangepicker);

		$1(input).daterangepicker( params_1, callback_0 );
	},
	jq_bs3dialog: params => {
		/* $1 */ return new BootstrapDialog($3.extend(true, {}, window.spjskpd.bs3dialog, params || {}));
	},
	forme: function(form, name_one_many, fn_key_prop, value) {
		var $ = window.$3 || window.$1 || window.$;
		if ($.isArray(name_one_many)) {
			name_one_many.forEach(name => {
				var elem = form.elements.namedItem(name);
				if (elem) {
					;;;; if ($.isFunction(fn_key_prop)) fn_key_prop(elem, name);
					else if (fn_key_prop in elem && value !== window.unknown) elem[fn_key_prop] = value;
				}
			});
			return null;

		} else {
			var elem = form.elements.namedItem(name_one_many);
			if (elem) {
				if (value !== window.unknown && fn_key_prop !== window.unknown) { // f,n,k,v
					;;;; if ($.isFunction(value) && fn_key_prop in elem) return value(elem[fn_key_prop], elem, fn_key_prop);
					else if (fn_key_prop in elem) elem[fn_key_prop] = value;
					return;

				} else if (fn_key_prop !== window.unknown) { // f,n,k
					;;;; if ($.isFunction(fn_key_prop)) return fn_key_prop(elem, name_one_many);
					else if (fn_key_prop in elem) return elem[fn_key_prop];
					return null;
				}

				return elem;
			}
		}
		return null;
	},
	rupiahin_koma: 2,
	rupiahin_parse: function(numeral,koma) {
		koma = Number(koma || 2);
		numeral = String(numeral);
		var batas_akhir = numeral.lastIndexOf(',');
		if(batas_akhir < 0) batas_akhir = numeral.lastIndexOf('.');
		if(batas_akhir < 0) batas_akhir = numeral.length;
		var asli = Number(numeral.substring(0, batas_akhir).replace(/[^0-9]/g,''));
		var desi = Number('0.' + numeral.substring(batas_akhir + 1).replace(/[^0-9]/g,''));
		return (asli+desi).toFixed(koma);
	},
	rupiahin: function(numeral,koma) {
		koma = Number(koma || 2);
		numeral = numeral.toString().split('.');
		numeral[1] = numeral[1] || 0;
		return [
			Number(numeral[0]).toLocaleString().replace(/\./g, '.').replace(/\,/g, '.'),
			Number('0.' + numeral[1]).toFixed(koma).toString().substr(-1*koma),
		].join(',');
	},
	tanggalin_iso: function(dt) {
		if (typeof dt === 'string') dt = new window.Date(dt);
		if (dt instanceof window.Date) {
			var m = dt.getMonth()+1, d = dt.getDate();
			if (m < 10) m = ['0',m].join('');
			if (d < 10) d = ['0',d].join('');
			return [dt.getFullYear(), m, d, ].join('-');
		}
		return dt;
	},
	tanggalin_id: function(dt) {
		if (typeof dt === 'string') dt = new window.Date(dt);
		if (dt instanceof window.Date) {
			return dt.toLocaleDateString('id', {
				year: 'numeric',
				month: 'long',
				day: 'numeric',
			});
		}
		return dt;
	},
	datatable_parse: function(struct) {
		var $ = window.$3 || window.$1 || window.$;
		function parse(table_footer,tfoot) {
			var row,cel;
			row = table_footer.insertRow();
			for (var i = 0; i < tfoot.length; i++) {
				cel = row.insertCell();
				for (var n in tfoot[i]) if (n in cel) {
					if ($.isFunction(tfoot[i][n])) tfoot[i][n](cel,n);
					else cel[n] = tfoot[i][n];
				}
			}
		} //fn

		struct.tbody = struct.tbody || [];
		if ($.isArray(struct.tbody)) {
			for (var i = 0; i < struct.tbody.length; i++) {
				if (!struct.tbody[i].title && struct.tbody[i].data) struct.tbody[i].title = struct.tbody[i].data.toUpperCase();
			}
		} else struct.tbody = [];

		struct.tbody_defs = struct.tbody_defs || [];

		struct.tfoot = struct.tfoot || [];
		if (struct.element && struct.tfoot && $.isArray(struct.tfoot) && struct.tfoot.length > 0) {
			var table_footer = struct.element.createTFoot();
			if ($.isArray(struct.tfoot[0])) struct.tfoot.forEach(function(tfoot) { parse(table_footer, tfoot); });
			else parse(table_footer, struct.tfoot);
		}

		return struct;
	},
});

if ('tahun' in window.spjskpd) {
	window.spjskpd.tahun = Number(window.spjskpd.tahun);
	window.spjskpd.min = new Date(window.spjskpd.tahun, 0, 1);
	window.spjskpd.max = new Date(window.spjskpd.tahun, 11, 31);
	window.spjskpd.current = new Date;
	window.spjskpd.current.setYear(window.spjskpd.tahun);

	var date = new Date(), y = window.spjskpd.tahun, m = date.getMonth();
	window.spjskpd.firstDay = new Date(y, m, 1);
	window.spjskpd.lastDay = new Date(y, m + 1, 0);
}
