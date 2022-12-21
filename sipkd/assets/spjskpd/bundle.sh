# @author: anovsiradj
# @version: 20190411

( \
	echo '/* @copyright: PT. Global Intermedia Nusantara; @author: anovsiradj; @version: 20190411, 201904; */';
	echo '(function(unknown) {'; \
	echo 'var $ = unknown;';
	cat $(dirname $0)/spjpengeluaranskpd/main.js; \
	cat $(dirname $0)/spjpengeluaranskpd/pergeseran.js; \
	echo '})();'; \
) \
> $(dirname $0)/spjpengeluaranskpd.dist.js \
