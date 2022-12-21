CREATE OR REPLACE FUNCTION __rmfn__(IN fn_name TEXT, OUT fn_dropped INT) AS
$fn$
/* @version: 20190502, 20190705; @author: anovsiradj; */
DECLARE fn_drop_cmd TEXT; i INT;
BEGIN
	fn_dropped = 0;
	FOR i,fn_drop_cmd IN SELECT 1, FORMAT('DROP FUNCTION %s(%s);', a.oid::regproc, pg_get_function_identity_arguments(a.oid))
	FROM pg_catalog.pg_proc a
	LEFT JOIN pg_catalog.pg_namespace b ON (b.oid = a.pronamespace)
	WHERE a.oid::regproc::text = fn_name
	LOOP
		i = COALESCE(i,0);
		fn_dropped = fn_dropped + i;

		IF(i > 0) THEN EXECUTE fn_drop_cmd; END IF;
	END LOOP;
END;
$fn$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION __iif__(yn BOOLEAN, y ANYELEMENT, n ANYELEMENT)
RETURNS ANYELEMENT AS $fn$
	/* @version: 20190703; @author: anovsiradj; */
	/* https://stackoverflow.com/a/53750984 */
	/* https://wiki.postgresql.org/wiki/Simulating_iif_function */
	SELECT CASE WHEN yn THEN y ELSE n END;
$fn$ LANGUAGE SQL IMMUTABLE;

/*
DO $execute$ BEGIN PERFORM __rmfn__('lzero'); END $execute$;
DO $execute$ BEGIN PERFORM __rmfn__('public.lzero'); END $execute$;
CREATE OR REPLACE FUNCTION lzero(TEXT, INT DEFAULT 2, ANYELEMENT DEFAULT 0)
RETURNS TEXT AS $fn$ SELECT LPAD($1::TEXT, $2, $3::TEXT); $fn$ LANGUAGE SQL IMMUTABLE;
CREATE OR REPLACE FUNCTION lzero(INT, INT DEFAULT 2, ANYELEMENT DEFAULT 0)
RETURNS TEXT AS $fn$ SELECT LPAD($1::TEXT, $2, $3::TEXT); $fn$ LANGUAGE SQL IMMUTABLE;
DO $execute$ BEGIN
	PERFORM LZERO(1); PERFORM LZERO(11,1); PERFORM LZERO(1,2,9); PERFORM LZERO(1,9,'A'::TEXT);
	PERFORM LZERO('A'); PERFORM LZERO('AA',1) ; PERFORM LZERO('A',2,9); PERFORM LZERO('A',9,'Z'::TEXT);
END $execute$;
*/
