var forme = window.spjskpd.forme;
var tanggalin_iso = window.spjskpd.tanggalin_iso;
var rupiahin = window.spjskpd.rupiahin;
var rupiahin_parse = window.spjskpd.rupiahin_parse;
var $wait = $3('#container').children('.cover:first');

var rupiahin_koma = 2;
var prompts = {};
var dated = {
	min: window.spjskpd.min,
	max: window.spjskpd.max,
	current: window.spjskpd.current,
};

var tahun = window.spjskpd.tahun;
var bulan = null;

var bku = document.getElementById('bku_spjskpd_table');
var bku_form = document.getElementById('bku_spjskpd_form');
var bku_struct = window.spjskpd.datatable_parse({
	element: bku,
	tbody: [
		{data: 'no_bku'},
		{data: 'tgl_bku'},
		{data: 'urai'},
		{data: 'penerimaan'},
		{data: 'pengeluaran'},
		{data: 'jenis_bku'},
		{data: 'bukti'},
	],
	tfoot: [
		[
			{
				innerText: 'Jumlah Bulan Ini',
				colSpan: 3,
			},
			{innerText: 0, 'column-summary-data': 'penerimaan'},
			{innerText: 0, 'column-summary-data': 'pengeluaran'},
			{innerText: 0, colSpan: 2, 'column-summary-data': 'selisih'},
		],
		[
			{innerText: 'Kas Bulan Lalu', colSpan: 5},
			{innerText: 0, colSpan: 2},
		],
		[
			{innerText: 'Kas pada Bendahara Pengeluaran', colSpan: 5},
			{innerText: 0, colSpan: 2},
		],
	],
});

function dump() {
	$3.each(arguments, function(i,dump) {
		window.console.log(dump);
	});
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
			input.value = moment.format('YYYY-MM-DD');
		});

		$3(input).on('tanggalin', function(evt, dt) {
			// library KONTOL. method-e raono sing mlaku kabeh, iseh wae dinggo.
			// $(input.nextElementSibling).trigger('change'); $picker.updateView(); $picker.updateCalendars(); $picker.updateInputText(); $picker.updateFormInputs();
			if (typeof dt === 'string') dt = new Date(dt);
			$1(exput).data('daterangepicker').setStartDate(dt);
			$1(exput).prop('value', $1(exput).data('daterangepicker').startDate.format($1(exput).data('daterangepicker').format));
			$1(exput).data('daterangepicker').updateFromControl();

			$3(input).prop('value', tanggalin_iso(dt)); // paksa
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

$3(bku).data('table', $1(bku).DataTable($3.extend(true, {}, window.spjskpd.datatable, {
	scrollY: '50vh',
	columns: bku_struct.tbody,
	footerCallback: function(tfrow,data) {
		var tfoot = tfrow.parentElement;
		var summary = {};
		summary.penerimaan  = data.length > 0 ? data.map(function (item) { return item.penerimaan; }).reduce(function(a,b) { return Number(a)+Number(b); }) : 0;
		summary.pengeluaran = data.length > 0 ? data.map(function (item) { return item.pengeluaran; }).reduce(function(a,b) { return Number(a)+Number(b); }) : 0;
		summary.selisih     = summary.penerimaan - summary.pengeluaran;

		$3.each(tfoot.children, function(i,tfrow) {
			var tfrcel;
			if (bku_struct.tfoot[tfrow.rowIndex]) for (var i = 0; i < bku_struct.tfoot[tfrow.rowIndex].length; i++) {
				tfrcel = tfrow.children[i];
				if ('column-summary-data' in bku_struct.tfoot[tfrow.rowIndex][i]) {
					tfrcel.innerText = rupiahin(summary[bku_struct.tfoot[tfrow.rowIndex][i]['column-summary-data']], rupiahin_koma);
				} //fi
			} //fi
		});
	}, //footerCallback
})));
$3(bku).on('reload', function(evt, data) {
	var table = $3(this).data('table');

	table.clear()
	for (var i = 0; i < data.length; i++) table.row.add(data[i]);
	table.draw();
});

$3(bku_form).on('submit', function(evt) {
	evt.preventDefault();
	$3(bku).trigger('reload', [[],]);

	if (!kodeskpd || !bulan) return;

	$wait.show();
	$3.get(this.action, $3.extend({}, kodeskpd, {tahun: tahun, bulan: bulan }), function(data) {
		$3(bku).trigger('reload', [data,]);
	}).fail(function() {
		window.alert('tidak bisa ambil bku.' + '\n' + window.JSON.stringify(arguments));
	}).always(function() {
		$wait.hide();
	});
});

forme(bku_form, 'month', function(input) {
	$3(input).on('change', function() {
		bulan = Number(this.value);

		$3(bku_form).trigger('submit');
	}).trigger('change');
});

var kodeskpd = null;
var kodeskpd_index = null;
$1('#kd_org2').on('change', function() {
	var temp = this.value.trim();
	if (temp === '') kodeskpd = kodeskpd_index = null;
	else {
		kodeskpd_index = temp.split('.');
		kodeskpd = {
			kodeurusan: kodeskpd_index[0],
			kodesuburusan: kodeskpd_index[1],
			kodeorganisasi: kodeskpd_index[2], 
		};

		$3(bku_form).trigger('submit');
	}
}).trigger('change'); // kodeskpd

$3('#bku_spjskpd_prompts_trigger').find('button').each(function() {
	$3(this).on('click', function() {
		if (this.dataset.prompt && prompts[this.dataset.prompt]) {
			if (kodeskpd) $3(prompts[this.dataset.prompt]).trigger('prompt',0);
			else message_ok('error', 'SKPD belum dipilih.');
		}
	});
});

$3(document).ready(function() {
	window.tmp = bku;
});
