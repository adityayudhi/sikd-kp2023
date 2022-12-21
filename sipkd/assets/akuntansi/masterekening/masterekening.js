/* @copyright: PT. Global Intermedia Nusantara; @author: anovsiradj; @version: 20190523,20190527; */
(function(unknown) {
var $ = $3;
var $wait = $3('#container').children('.cover:first');

var extra = {
	prompt_title_prefix: '',
	prompt_title_suffix: '',
	entry: null, /* on:prompt() entry yang sedang aktif, pada form */
	type: null, /* on:prompt() */
};
var helper = window.spjskpd;
var forme = window.spjskpd.forme;
var dump = window.spjskpd.dump;
var omfg = window.spjskpd.omfg;

function parse(data) {
	if ($3.isPlainObject(data)) {
		var kode_rekening_short = data.kode_rekening.replace(/\.0.*/, '');

		data.kode_rekening_short = kode_rekening_short;
		data.id = data.kode_rekening;
		data.name = `${kode_rekening_short} - ${data.urai_rekening}`;

		/* supaya tree auto ajax, ketika expanded/dibutuhkankan */
		data.load_on_demand = !(data.__last__ && data.__last__ == 1);

		if (data.children && data.children.length > 0) parse(data.children);
	} else if ($3.isArray(data)) {
		data.forEach(entry => parse(entry));
	}
}

var root = document.getElementById('akuntansi_masterekening');
$(root).on('create', function(event) {
	if (tree.tree('getSelectedNodes').length === 0) { /* harus pilih node dulu */
		message_ok('error', 'belum pilih rekening (tree)');
		return;
	}
	var entry_parent = tree.tree('getSelectedNodes')[0];
	if ('__last__' in entry_parent && entry_parent.__last__ == 1) { /* kalo node terdalam, tidak bisa */
		message_ok('error', 'tidak bisa tambah rekening (tree)');
		return;
	}

	extra.prompt_title_prefix = 'Tambah';
	extra.prompt_title_suffix = `(${entry_parent.kode_rekening_short} - ${entry_parent.urai_rekening})`;
	var entry = {};
	var field = null;

	for (var i = 0; i < window.akuntansi_masterekening.fields.length; i++) {
		field = window.akuntansi_masterekening.fields[i];
		entry[field] = entry_parent[field];

		/* kalo != pk pertama && pk dari parent == nol */
		if (i > 0 && entry_parent[field] == 0) {
			entry['__field__'] = field;
			break;
		}
	}

	$wait.show();
	$.get(window.akuntansi_masterekening.href_browse, {node: entry_parent.kode_rekening}, function(result) {
		entry[field] = 0;
		for (var i = 0; i < result.length; i++) {
			if (result[i][field] > entry[field]) entry[field] = result[i][field];
		}
		entry[field] += 1;

		$wait.hide();
		$(form).trigger('prompt', [0, entry, ]);
	});
});
$(root).on('update', function(event) {
	extra.prompt_title_prefix = 'Ubah';
	var entry;

	;;;; if (table.row('.selected').length > 0) entry = table.row('.selected').data();
	else if(tree.tree('getSelectedNodes').length > 0) entry = tree.tree('getSelectedNodes')[0];

	if (entry) $(form).trigger('prompt', [1, entry, ]);
	else message_ok('error', 'belum pilih rekening');
});
$(root).on('delete', function(event) {
	if (tree.tree('getSelectedNodes').length === 0) { /* harus pilih node dulu */
		message_ok('error', 'belum pilih rekening (tree)');
		return;
	}
	var entry = {csrfmiddlewaretoken: helper.kuki('csrftoken'),};
	for (var e in tree.tree('getSelectedNodes')[0]) {
		if (typeof tree.tree('getSelectedNodes')[0][e] === 'object') continue;
		if (typeof tree.tree('getSelectedNodes')[0][e] === 'function') continue;
		entry[e] = tree.tree('getSelectedNodes')[0][e];
	}

	$1.alertable.confirm(`yakin hapus rekening <b>${entry.kode_rekening_short}</b> ?`, window.spjskpd.alertable_rm).then(function(result) {
		$wait.show();
		$3.post(form.dataset.hrefRm, entry, function() {
			tree.tree('selectNode', null);
			tree.tree('reload', () => tree_reload_table());
		})
		.fail(function() { omfg('tidak bisa hapus rekening.', arguments); })
		.always(() => $wait.hide());
	});
});
$(root).on('report', event => report.open());

var treeelm = document.getElementById('akuntansi_masterekening_tree');
var tree = $1(treeelm).tree({
	dataUrl: window.akuntansi_masterekening.href_browse,
	keyboardSupport: false,
	selectable: true,
	dragAndDrop: false,
	saveState: false,
	dataFilter: data => { parse(data); return data; },
});

var form_extra = {
	once: true,
	type: null, /* 0:create,1:update */
};
var form = document.getElementById('akuntansi_masterekening_form');

$3(form).data('prompt', new BootstrapDialog({
	title: form.dataset.promptTitle,
	size: BootstrapDialog.SIZE_SMALL,
	autodestroy: false,
	draggable: true,
	// animate: false,
	closeByBackdrop: false,
	closeByKeyboard: false,
	onshow: function($self) {
		forme(form, 'csrfmiddlewaretoken', 'value', helper.kuki('csrftoken'));

		$self.setTitle(`${extra.prompt_title_prefix} ${form.dataset.promptTitle} ${extra.prompt_title_suffix}`);
		if (form_extra.once) {
			$self.getModalDialog().css({ width: form.dataset.promptWidth });
			$self.getModalBody().append(form);
		}
	},
	onhidden: function() {
		form_extra.once = false;
		extra.prompt_title_prefix = extra.prompt_title_suffix = '';

		$3(form).trigger('reset');
	},
}));

$3(form).on('prompt', function(event, __type__, entry) {
	entry = entry || {};
	forme(form, '__type__', 'value', __type__);

	var hide = false, kode;
	for (var i = 0; i < window.akuntansi_masterekening.fields.length; i++) {
		kode = window.akuntansi_masterekening.fields[i];
		forme(form, kode, function(elem) {
			elem.value = 0;
			elem.readOnly = false;
			$(elem).parents('.kode').show();

			if (__type__ === 0) {
				elem.readOnly = true;
				if (hide) $(elem).parents('.kode').hide();
				if (entry['__field__'] === kode) { elem.readOnly = false; hide = true; }
			}

			if (__type__ === 1) {
				elem.readOnly = true;
				if (i > 0 && entry[kode] == 0) hide = true;
				if (hide) $(elem).parents('.kode').hide();
			}
		});
	}

	for(var n in entry) forme(form, n, 'value', entry[n]);
	$(form).data('prompt').open();
});

$(form).on('submit', function(event) {
	event.preventDefault();
	$.post(form.action, $(form).serialize(), function(result) {
		$(form).data('prompt').close();

		/* saya inginnya tidak refresh secara keseluruhan, hanya yg berubah saja.
		   tapi saya males untuk nulis skripnya. [TODO] */
		tree.tree('selectNode', null);
		tree.tree('reload', () => tree_reload_table());
	});
});

$(form).on('reset', function() {
	$(form).data('prompt').isOpened() && $(form).data('prompt').close();
});

$1(treeelm).on('tree.select', event => tree_reload_table());

function tree_reload_table(node) {
	node = node || tree.tree('getSelectedNodes')[0] || null;
	/* yang tampil pada table hanya children dari parent-node.
	   jadi node yg paling dalam, ketika di klik,
	   table akan selalu kosong, karena memang tidak punya children. */
	table.clear().draw();
	if (node && (node.__last__ || 0) == 0) {
		$.get(window.akuntansi_masterekening.href_browse, {node: node.kode_rekening}, function(result) {
			parse(result);
			table.rows.add(result);
			table.columns.adjust().draw();
		});
	}
}

var tableelm = document.getElementById('akuntansi_masterekening_table');
$(tableelm).data('selected', null);
$(tableelm).data('columns', []);
$(tableelm).children('thead').children('tr').children('th').each(function() {
	if (this.innerText.trim() === '') this.innerText = this.dataset.field;
	$(tableelm).data('columns').push({ data: this.dataset.field, });
});

var table = $1(tableelm).DataTable({
	dom: 't',
	columns: $(tableelm).data('columns'),
	ordering: false, searching: false, paging: false,
	language: {
		zeroRecords: '<div class="text-muted text-center">(kosong)</div>',
		emptyTable: '<div class="text-muted text-center">(kosong)</div>',
	},
	createdRow: function(tbrow, entry) {
		$(tbrow).on('click', function() {
			if ($(tbrow).hasClass('selected')) {
				$(tbrow).removeClass('selected');
				return;
			}

			table.row('.selected').nodes().to$().removeClass('selected');
			$(tbrow).addClass('selected'); // table.row(tbrow).nodes().to$().addClass('selected');
		});
	},
});

$('#akuntansi_masterekening_action').find('button[data-action]').each(function() {
	$(this).on('click', event => $(root).trigger(event.target.dataset.action));
});

var report_extra = $.extend({ once: true, }, window.akuntansi_masterekening.report);
var report = new BootstrapDialog($3.extend(true, {}, window.spjskpd.bs3dialog, {
	title: report_extra.title,
	onshow: function(iframe) {
		if (report_extra.once) {
			iframe.getModalDialog().css({width: report_extra.width, height: report_extra.height});
			iframe.getModalContent().css({height: '100%'});
			iframe.getModalBody().css({margin: 0, padding: 0, height: report_extra.height});
		}
	},
	onshown: function(iframe) {
		var elem = window.spjskpd.doxce('iframe', {
			style: {
				width: '100%',
				height: '100%',
			}
		});
		elem.setAttribute('frameborder', 0);
		elem.setAttribute('src', report_extra.href);
		iframe.getModalBody().append(elem);
	},
	onhide: function(iframe) {
		iframe.getModalBody().children().remove();
	},
	onhidden: function() {
		report_extra.once = false;
	},
}));

$(document).ready(() => tree.tree('setOption', 'saveState', treeelm.id));
})();
