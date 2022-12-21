var pergeseran = prompts['pergeseran'] = document.getElementById('bku_spjskpd_pergeseran');

forme(pergeseran, 'jenis_bku', function(jenis_bku) {
	$3(jenis_bku).on('change', function() {
		forme(pergeseran, 'simpananbank', function(simpananbank) {
			simpananbank.value = jenis_bku.selectedIndex;
		});
	}).trigger('change');
});

$3(pergeseran).data('prompt', new BootstrapDialog($3.extend(true, {}, window.spjskpd.bs3dialog, {
	title: pergeseran.dataset.promptTitle,
	onshow: function(self) {
		self.getModalBody().parentsUntil('.modal', '.modal-dialog').css('width', '50vw');
	},
	onshown: function(self) {
		self.getModalBody().append(pergeseran);
	},
	onhidden: function(self) { $3(pergeseran).trigger('reset'); },
}))); // data:prompt

$3(pergeseran).on('prompt', function(evnt, type, data) {
	var query = $3.extend({tahun: tahun}, kodeskpd);
	for(var q in query) forme(this, q, function(input) { input.value = query[q]; });

	if (type === 0) {
		$wait.show();
		$3.get(window.spjskpd.href_no_bku_auto, query, function(result) {
			forme(pergeseran,'no_bku', function(input) { input.value = result; });
		}).fail(function() {
			window.alert([
				'gagal ambil NO_BKU terakhir.',
				window.JSON.stringify(arguments),
			].join('\n'));
		}).done(function() {
			$wait.hide();
			$3(pergeseran).data('prompt').open();
		});
	}

	if (type === 1) {
		$3(pergeseran).data('prompt').open();
	}

	forme(this, 'csrfmiddlewaretoken', function(input) {
		input.value = window.spjskpd.kuki('csrftoken');
	});
	$3(this).data('tanggalin').forEach(function(name) {
		$3(forme(pergeseran,name)).trigger('tanggalin', (data && name in data) ? data[name] : dated.current);
	});
	$3(this).data('rupiahin').forEach(function(name) {
		$3(forme(pergeseran,name)).trigger('rupiahin', (data && name in data) ? data[name] : 0);
	});
}); // on:prompt

$3(pergeseran).data('tanggalin', []);
['tgl_bku', 'tgl_bukti'].forEach(function(name) {
	forme(pergeseran, name, function(input) {
		$3(pergeseran).data('tanggalin').push(name);
		jq_tanggalin(input);
	});
});
$3(pergeseran).data('rupiahin', []);
['penerimaan', 'pengeluaran'].forEach(function(name) {
	forme(pergeseran, name, function(input) {
		$3(pergeseran).data('rupiahin').push(name);
		jq_rupiahin(input);
	});
});


$3(pergeseran).on('submit', function(event) {
	event.preventDefault();
	$3.post(this.action, $3(this).serialize(), function() {
		$3(pergeseran).data('prompt').close();
		$3(bku_form).trigger('submit');
	}).fail(function() {
		// window.alert('tidak bisa simpan bku.' + '\n' + window.JSON.stringify(arguments));
		message_ok('error', 'tidak bisa simpan bku.' + '\n' + window.JSON.stringify(arguments));
	});
});

$3(pergeseran).on('reset', function() {
	$3(this).data('prompt').isOpened() && $3(this).data('prompt').close();
}); // on:reset
