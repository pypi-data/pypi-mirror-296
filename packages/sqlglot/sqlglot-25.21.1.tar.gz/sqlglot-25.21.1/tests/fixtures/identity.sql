SUM(1)
SUM(CASE WHEN x > 1 THEN 1 ELSE 0 END) / y
1
(1)
1.
(1.)
1.0
(1.0)
1E2
1E+2
1E-2
1.1E10
1.12e-10
-11.023E7 * 3
0.2
(1 * 2) / (3 - 5)
((TRUE))
''
''''
'x'
'\x'
"x"
'\z'
'\\z'
'\\\z'
'\\\\z'
'\\\\\z'
'\\\\\\z'
'\n'
'\\n'
'\\\n'
'\\\\n'
'\\\\\n'
'\\\\\\n'
""
"""x"""
N'abc'
x
x % 1
x < 1
x <= 1
x > 1
x >= 1
x <> 1
x = y OR x > 1
x & 1
x | 1
x ^ 1
~x
x << 1
x >> 1
x >> 1 | 1 & 1 ^ 1
x || y
x[ : ]
x[1 : ]
x[ : 2]
x[1 : 2]
x[-4 : -1]
1 - -1
- -5
dec.x + y
a.filter
a.b.c
a.b.c.d
a.b.c.d.e
a.b.c.d.e[0]
a.b.c.d.e[0].f
a[0][0].b.c[1].d.e.f[1][1]
a[0].b[1]
a[0].b.c['d']
a.b.C()
a['x'].b.C()
a.B()
a['x'].C()
int.x
map.x
SELECT update
SELECT x.update
SELECT call.x
SELECT end
a.b.INT(1.234)
INT(x / 100)
time * 100
int * 100
dec + 1
x IN (-1, 1)
x IN ('a', 'a''a')
x IN ((1))
x BETWEEN -1 AND 1
x BETWEEN 'a' || b AND 'c' || d
((a, b) AS c)
NOT x IS NULL
x IS TRUE
x IS FALSE
x IS TRUE IS TRUE
x LIKE y IS TRUE
TRIM('a' || 'b')
MAP()
GREATEST(x)
LEAST(y)
MAX(a, b)
MIN(a, b)
time
zone
ARRAY<TEXT>
CURRENT_DATE
CURRENT_DATE('UTC')
CURRENT_DATE AT TIME ZONE 'UTC'
CURRENT_DATE AT TIME ZONE zone_column
CURRENT_DATE AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Tokio'
f1 AT TIME ZONE INTERVAL '-10:00' AS f1
ARRAY()
ARRAY(1, 2)
ARRAY(time, foo)
ARRAY(foo, time)
ARRAY(LENGTH(waiter_name) > 0)
ARRAY_CONTAINS(x, 1)
x.EXTRACT(1)
EXTRACT(X FROM y)
EXTRACT(DATE FROM y)
EXTRACT(WEEK(monday) FROM created_at)
CONCAT_WS('-', 'a', 'b')
CONCAT_WS('-', 'a', 'b', 'c')
POSEXPLODE("x") AS ("a", "b")
POSEXPLODE("x") AS ("a", "b", "c")
STR_POSITION(haystack, needle)
STR_POSITION(haystack, needle, pos)
LEVENSHTEIN('gumbo', 'gambol', 2, 1, 1)
SPLIT(SPLIT(referrer, 'utm_source=')[OFFSET(1)], "&")[OFFSET(0)]
x[ORDINAL(1)][SAFE_OFFSET(2)]
x GLOB '??-*'
x GLOB y
ILIKE(x, 'z')
x LIKE SUBSTR('abc', 1, 1)
x LIKE y
x LIKE a.y
x LIKE '%y%'
x ILIKE '%y%'
x LIKE '%y%' ESCAPE '\'
x ILIKE '%y%' ESCAPE '\'
1 AS escape
INTERVAL '1' DAY
INTERVAL '1' MONTH
INTERVAL '1' YEAR
INTERVAL '1' HOUR TO SECOND
INTERVAL '-1' CURRENT_DATE
INTERVAL '-31' CAST(GETDATE() AS DATE)
INTERVAL (1 + 3) DAYS
INTERVAL '1' DAY * 5
5 * INTERVAL '1' DAY
CASE WHEN TRUE THEN INTERVAL '15' DAYS END
CASE WHEN TRUE THEN 1 ELSE interval END
CASE WHEN TRUE THEN 1 ELSE "INTERVAL" END
SELECT asof FROM x
SELECT * WHERE interval IS NULL
SELECT * WHERE NOT interval IS NULL
SELECT * WHERE INTERVAL "is" > 1
SELECT * WHERE INTERVAL x.is > 1
CAST('45' AS INTERVAL DAYS)
CAST(x AS UUID)
FILTER(a, x -> x.a.b.c.d.e.f.g)
FILTER(a, x -> FOO(x.a.b.c.d.e.f.g) + x.a.b.c.d.e.f.g)
TIMESTAMP_FROM_PARTS(2019, 1, 10, 2, 3, 4, 123456789, 'America/Los_Angeles')
TIMESTAMPDIFF(CURRENT_TIMESTAMP(), 1, DAY)
DATETIME_DIFF(CURRENT_DATE, 1, DAY)
QUANTILE(x, 0.5)
REGEXP_REPLACE('new york', '(\w)(\w*)', x -> UPPER(x[1]) || LOWER(x[2]))
REGEXP_LIKE('new york', '.')
REGEXP_SPLIT('new york', '.')
SPLIT('new york', '.')
X((y AS z)).1
X(a.b = 1)
(x AS y, y AS z)
REPLACE(1)
DATE(x) = DATE(y)
TIMESTAMP(DATE(x))
TIMESTAMP_TRUNC(COALESCE(time_field, CURRENT_TIMESTAMP()), DAY)
COUNT(DISTINCT CASE WHEN DATE_TRUNC('ISOWEEK', DATE(time_field)) = DATE_TRUNC('ISOWEEK', DATE(time_field2)) THEN report_id ELSE NULL END)
COUNT(a, b)
x[y - 1]
CASE WHEN SUM(x) > 3 THEN 1 END OVER (PARTITION BY x)
ANY(x) OVER (PARTITION BY x)
SUM(ROW() OVER (PARTITION BY x))
SUM(ROW() OVER (PARTITION BY x + 1))
SUM(ROW() OVER (PARTITION BY x AND y))
SUM(x) OVER (w ORDER BY y)
(ROW() OVER ())
CASE WHEN (x > 1) THEN 1 ELSE 0 END
CASE (1) WHEN 1 THEN 1 ELSE 0 END
CASE 1 WHEN 1 THEN 1 ELSE 0 END
CASE 1 WHEN 1 THEN timestamp ELSE date END
x AT TIME ZONE 'UTC'
CAST('2025-11-20 00:00:00+00' AS TIMESTAMP) AT TIME ZONE 'Africa/Cairo'
SET x = 1
SET x = ';'
SET variable = value
SET GLOBAL variable = value
SET LOCAL variable = value
@x
@"x"
COMMIT
USE db
USE ROLE x
USE WAREHOUSE x
USE DATABASE x
USE SCHEMA x.y
USE CATALOG abc
NOT 1
NOT NOT 1
SELECT * FROM test
SELECT * FROM db.FOO()
SELECT *, 1 FROM test
SELECT * FROM a.b
SELECT * FROM a.b.c
SELECT * FROM table
SELECT 1
SELECT 1 FROM test
SELECT * FROM a, b, (SELECT 1) AS c
SELECT a FROM test
SELECT 1 AS filter
SELECT 1 AS "quoted alias"
SELECT SUM(x) AS filter
SELECT 1 AS range FROM test
SELECT 1 AS count FROM test
SELECT 1 AS comment FROM test
SELECT 1 AS numeric FROM test
SELECT 1 AS number FROM test
SELECT COALESCE(offset, 1)
SELECT t.count
SELECT DISTINCT x FROM test
SELECT DISTINCT x, y FROM test
SELECT DISTINCT TIMESTAMP_TRUNC(time_field, MONTH) AS time_value FROM "table"
SELECT DISTINCT ON (x) x, y FROM z
SELECT DISTINCT ON (x, y + 1) * FROM z
SELECT DISTINCT ON (x.y) * FROM z
SELECT DISTINCT FROM_SOMETHING
SELECT top.x
SELECT TIMESTAMP(DATE_TRUNC('MONTH', DATE(time_field))) AS time_value FROM "table"
SELECT GREATEST((3 + 1), LEAST(3, 4))
SELECT TRANSFORM(a, b -> b) AS x
SELECT AGGREGATE(a, (a, b) -> a + b) AS x
SELECT COUNT(DISTINCT a, b)
SELECT COUNT(DISTINCT a, b + 1)
SELECT SUM(DISTINCT x)
SELECT TRUNCATE(a, b)
SELECT ARRAY_AGG(STRUCT(x, x AS y) ORDER BY z DESC) AS x
SELECT LAG(x) OVER (ORDER BY y) AS x
SELECT LEAD(a) OVER (ORDER BY b) AS a
SELECT LEAD(a, 1) OVER (PARTITION BY a ORDER BY a) AS x
SELECT LEAD(a, 1, b) OVER (PARTITION BY a ORDER BY a) AS x
SELECT X((a, b) -> a + b, z -> z) AS x
SELECT X(a -> a + ("z" - 1))
SELECT EXISTS(ARRAY(2, 3), x -> x % 2 = 0)
SELECT test.* FROM test
SELECT a AS b FROM test
SELECT "a"."b" FROM "a"
SELECT "a".b FROM a
SELECT a.b FROM "a"
SELECT a.b FROM a
SELECT '"hi' AS x FROM x
SELECT 1 AS "|sum" FROM x
SELECT '\"hi' AS x FROM x
SELECT 1 AS b FROM test
SELECT 1 AS "b" FROM test
SELECT 1 + 1 FROM test
SELECT 1 - 1 FROM test
SELECT 1 * 1 FROM test
SELECT 1 % 1 FROM test
SELECT 1 / 1 FROM test
SELECT 1 < 2 FROM test
SELECT 1 <= 2 FROM test
SELECT 1 > 2 FROM test
SELECT 1 >= 2 FROM test
SELECT 1 <> 2 FROM test
SELECT JSON_EXTRACT(x, '$.name')
SELECT JSON_EXTRACT_SCALAR(x, '$.name')
SELECT x LIKE '%x%' FROM test
SELECT * FROM test LIMIT 100
SELECT * FROM test LIMIT 1 + 1
SELECT * FROM test LIMIT 100 OFFSET 200
SELECT * FROM test LIMIT (SELECT 1)
SELECT * FROM test LIMIT (SELECT 1) OFFSET (SELECT 1)
SELECT * FROM test FETCH FIRST ROWS ONLY
SELECT * FROM test FETCH FIRST 1 ROWS ONLY
SELECT * FROM test ORDER BY id DESC FETCH FIRST 10 ROWS WITH TIES
SELECT * FROM test ORDER BY id DESC FETCH FIRST 10 PERCENT ROWS WITH TIES
SELECT * FROM test FETCH NEXT 1 ROWS ONLY
SELECT (1 > 2) AS x FROM test
SELECT NOT (1 > 2) FROM test
SELECT 1 + 2 AS x FROM test
SELECT a, b, 1 < 1 FROM test
SELECT a FROM test WHERE NOT FALSE
SELECT a FROM test WHERE a = 1
SELECT a FROM test WHERE a = 1 AND b = 2
SELECT a FROM test WHERE a IN (SELECT b FROM z)
SELECT a FROM test WHERE a IN ((SELECT 1), 2)
SELECT * FROM x WHERE y IN ((SELECT 1) EXCEPT (SELECT 2))
SELECT * FROM x WHERE y IN (SELECT 1 UNION SELECT 2)
SELECT * FROM x WHERE y IN ((SELECT 1 UNION SELECT 2))
SELECT * FROM x WHERE y IN (WITH z AS (SELECT 1) SELECT * FROM z)
SELECT a FROM test WHERE (a > 1)
SELECT a FROM test WHERE a > (SELECT 1 FROM x GROUP BY y)
SELECT a FROM test WHERE EXISTS(SELECT 1)
SELECT a FROM test WHERE EXISTS(SELECT * FROM x UNION SELECT * FROM Y) OR TRUE
SELECT a FROM test WHERE TRUE OR NOT EXISTS(SELECT * FROM x)
SELECT a AS any, b AS some, c AS all, d AS exists FROM test WHERE a = ANY (SELECT 1)
SELECT a FROM test WHERE a > ALL (SELECT 1)
SELECT a FROM test WHERE (a, b) IN (SELECT 1, 2)
SELECT X((SELECT 1) UNION (SELECT 2))
SELECT a FROM test ORDER BY a
SELECT a FROM test ORDER BY a, b
SELECT x FROM tests ORDER BY a DESC, b DESC, c
SELECT a FROM test ORDER BY a > 1
SELECT * FROM test ORDER BY DATE DESC, TIMESTAMP DESC
SELECT a, b FROM test GROUP BY 1
SELECT a, b FROM test GROUP BY a
SELECT a, b FROM test WHERE a = 1 GROUP BY a HAVING a = 2
SELECT a, b FROM test WHERE a = 1 GROUP BY a HAVING a = 2 ORDER BY a
SELECT a, b FROM test WHERE a = 1 GROUP BY CASE 1 WHEN 1 THEN 1 END
SELECT a FROM test GROUP BY GROUPING SETS (())
SELECT a FROM test GROUP BY GROUPING SETS (x, ())
SELECT a FROM test GROUP BY GROUPING SETS (x, (x, y), (x, y, z), q)
SELECT a FROM test GROUP BY CUBE (x)
SELECT a FROM test GROUP BY ROLLUP (x)
SELECT t.a FROM test AS t GROUP BY ROLLUP (t.x)
SELECT a FROM test GROUP BY GROUPING SETS ((x, y)), ROLLUP (b)
SELECT a FROM test GROUP BY CUBE (x), ROLLUP (x, y, z)
SELECT CASE WHEN a < b THEN 1 WHEN a < c THEN 2 ELSE 3 END FROM test
SELECT CASE 1 WHEN 1 THEN 1 ELSE 2 END
SELECT CASE 1 WHEN 1 THEN MAP('a', 'b') ELSE MAP('b', 'c') END['a']
SELECT CASE 1 + 2 WHEN 1 THEN 1 ELSE 2 END
SELECT CASE TEST(1) + x[0] WHEN 1 THEN 1 ELSE 2 END
SELECT CASE x[0] WHEN 1 THEN 1 ELSE 2 END
SELECT CASE a.b WHEN 1 THEN 1 ELSE 2 END
SELECT CASE CASE x > 1 WHEN TRUE THEN 1 END WHEN 1 THEN 1 ELSE 2 END
SELECT a FROM (SELECT a FROM test) AS x
SELECT a FROM (SELECT a FROM (SELECT a FROM test) AS y) AS x
SELECT a FROM test WHERE a IN (1, 2, 3) OR b BETWEEN 1 AND 4
SELECT a FROM test AS x TABLESAMPLE (BUCKET 1 OUT OF 5)
SELECT a FROM test TABLESAMPLE (BUCKET 1 OUT OF 5)
SELECT a FROM test TABLESAMPLE (BUCKET 1 OUT OF 5 ON x)
SELECT a FROM test TABLESAMPLE (BUCKET 1 OUT OF 5 ON RAND())
SELECT a FROM test TABLESAMPLE (0.1 PERCENT)
SELECT a FROM test TABLESAMPLE (100 ROWS)
SELECT a FROM test PIVOT(SUM(x) FOR y IN ('z', 'q'))
SELECT 1 FROM a.b.table1 AS t UNPIVOT((c3) FOR c4 IN (a, b))
SELECT a FROM test PIVOT(SOMEAGG(x, y, z) FOR q IN (1))
SELECT a FROM test PIVOT(SUM(x) FOR y IN ('z', 'q')) PIVOT(MAX(b) FOR c IN ('d'))
SELECT a FROM (SELECT a, b FROM test) PIVOT(SUM(x) FOR y IN ('z', 'q'))
SELECT a FROM test UNPIVOT(x FOR y IN (z, q)) AS x
SELECT a FROM test PIVOT(SUM(x) FOR y IN ('z', 'q')) UNPIVOT(x FOR y IN (z, q)) AS x
SELECT ABS(a) FROM test
SELECT AVG(a) FROM test
SELECT CEIL(a) FROM test
SELECT CEIL(a, b) FROM test
SELECT COUNT(a) FROM test
SELECT COUNT(1) FROM test
SELECT COUNT(*) FROM test
SELECT COUNT() FROM test
SELECT COUNT(DISTINCT a) FROM test
SELECT EXP(a) FROM test
SELECT FLOOR(a) FROM test
SELECT FLOOR(a, b) FROM test
SELECT FIRST_VALUE(a) FROM test
SELECT GREATEST(a, b, c) FROM test
SELECT LAST_VALUE(a) FROM test
SELECT LAST_VALUE(a) IGNORE NULLS OVER () + 1
SELECT LN(a) FROM test
SELECT MAX(a) FROM test
SELECT MIN(a) FROM test
SELECT POWER(a, 2) FROM test
SELECT QUANTILE(a, 0.95) FROM test
SELECT ROUND(a) FROM test
SELECT ROUND(a, 2) FROM test
SELECT SUM(a) FROM test
SELECT SQRT(a) FROM test
SELECT STDDEV(a) FROM test
SELECT STDDEV_POP(a) FROM test
SELECT STDDEV_SAMP(a) FROM test
SELECT VARIANCE(a) FROM test
SELECT VARIANCE_POP(a) FROM test
SELECT CAST(a AS INT) FROM test
SELECT CAST(a AS DATETIME) FROM test
SELECT CAST(a AS VARCHAR) FROM test
SELECT CAST(a < 1 AS INT) FROM test
SELECT CAST(a IS NULL AS INT) FROM test
SELECT COUNT(CAST(1 < 2 AS INT)) FROM test
SELECT COUNT(CASE WHEN CAST(1 < 2 AS BOOLEAN) THEN 1 END) FROM test
SELECT CAST(a AS DECIMAL) FROM test
SELECT CAST(a AS DECIMAL(1)) FROM test
SELECT CAST(a AS DECIMAL(1, 2)) FROM test
SELECT CAST(a AS MAP<INT, INT>) FROM test
SELECT CAST(a AS TIMESTAMP) FROM test
SELECT CAST(a AS DATE) FROM test
SELECT CAST(a AS ARRAY<INT>) FROM test
SELECT CAST(a AS VARIANT) FROM test
SELECT TRY_CAST(a AS INT) FROM test
SELECT COALESCE(a, b, c) FROM test
SELECT ANY_VALUE(a) FROM test
SELECT 1 FROM a JOIN b ON a.x = b.x
SELECT 1 FROM a JOIN b AS c ON a.x = b.x
SELECT 1 FROM a INNER JOIN b ON a.x = b.x
SELECT 1 FROM a LEFT JOIN b ON a.x = b.x
SELECT 1 FROM a RIGHT JOIN b ON a.x = b.x
SELECT 1 FROM a CROSS JOIN b ON a.x = b.x
SELECT 1 FROM a SEMI JOIN b ON a.x = b.x
SELECT 1 FROM a LEFT SEMI JOIN b ON a.x = b.x
SELECT 1 FROM a LEFT ANTI JOIN b ON a.x = b.x
SELECT 1 FROM a RIGHT SEMI JOIN b ON a.x = b.x
SELECT 1 FROM a RIGHT ANTI JOIN b ON a.x = b.x
SELECT 1 FROM a JOIN b USING (x)
SELECT 1 FROM a JOIN b USING (x, y, z)
SELECT 1 FROM a JOIN (SELECT a FROM c) AS b ON a.x = b.x AND a.x < 2
SELECT 1 FROM a UNION SELECT 2 FROM b
SELECT 1 FROM a UNION ALL SELECT 2 FROM b
SELECT 1 FROM a JOIN b ON a.foo = b.bar JOIN c ON a.foo = c.bar
SELECT 1 FROM a LEFT JOIN b ON a.foo = b.bar JOIN c ON a.foo = c.bar
SELECT 1 FROM a LEFT INNER JOIN b ON a.foo = b.bar
SELECT 1 FROM a LEFT OUTER JOIN b ON a.foo = b.bar
SELECT 1 FROM a NATURAL JOIN b
SELECT 1 FROM a NATURAL LEFT JOIN b
SELECT 1 FROM a NATURAL LEFT OUTER JOIN b
SELECT 1 FROM a OUTER JOIN b ON a.foo = b.bar
SELECT 1 FROM a FULL JOIN b ON a.foo = b.bar
SELECT 1 FROM a JOIN b JOIN c ON b.id = c.id ON a.id = b.id
SELECT * FROM a JOIN b JOIN c USING (id) USING (id)
SELECT 1 UNION ALL SELECT 2
SELECT 1 EXCEPT SELECT 2
SELECT 1 EXCEPT SELECT 2
SELECT 1 INTERSECT SELECT 2
SELECT 1 INTERSECT SELECT 2
SELECT 1 AS delete, 2 AS alter
SELECT * FROM (x)
SELECT * FROM ((x))
SELECT * FROM (((x)))
SELECT * FROM ((SELECT 1))
SELECT * FROM (x CROSS JOIN foo LATERAL VIEW EXPLODE(y))
SELECT * FROM (SELECT 1) AS x
SELECT * FROM (SELECT 1 UNION SELECT 2) AS x
SELECT * FROM (SELECT 1 UNION ALL SELECT 2) AS x
SELECT * FROM (SELECT 1 UNION ALL SELECT 2)
SELECT * FROM ((SELECT 1) AS a UNION ALL (SELECT 2) AS b)
SELECT * FROM ((SELECT 1) AS a(b))
SELECT * FROM ((SELECT 1) UNION (SELECT 2) UNION (SELECT 3))
SELECT * FROM (table1 AS t1 LEFT JOIN table2 AS t2 ON 1 = 1)
SELECT * FROM (tbl1 LEFT JOIN tbl2 ON 1 = 1)
SELECT * FROM (tbl1, tbl2 JOIN tbl3 ON TRUE)
SELECT * FROM (tbl1 CROSS JOIN tbl2)
SELECT * FROM (tbl1 CROSS JOIN tbl2) AS t
SELECT * FROM (tbl AS tbl) AS t
SELECT * FROM (tbl1 JOIN (tbl2 CROSS JOIN tbl3) ON bla = foo)
SELECT * FROM (tbl1, LATERAL (SELECT * FROM bla) AS tbl)
SELECT * FROM x AS y(a, b)
SELECT * EXCEPT (a, b)
SELECT * EXCEPT (a, b) FROM y
SELECT * REPLACE (a AS b, b AS C)
SELECT * REPLACE (a + 1 AS b, b AS C)
SELECT * EXCEPT (a, b) REPLACE (a AS b, b AS C)
SELECT * EXCEPT (a, b) REPLACE (a AS b, b AS C) FROM y
SELECT a.* EXCEPT (a, b), b.* REPLACE (a AS b, b AS C)
SELECT a.* EXCEPT (a, b), b.* REPLACE (a AS b, b AS C) FROM x
SELECT A.* EXCEPT (A.COL_1) FROM TABLE_1 AS A
SELECT zoo, animals FROM (VALUES ('oakland', ARRAY('a', 'b')), ('sf', ARRAY('b', 'c'))) AS t(zoo, animals)
SELECT zoo, animals FROM UNNEST(ARRAY(STRUCT('oakland' AS zoo, ARRAY('a', 'b') AS animals), STRUCT('sf' AS zoo, ARRAY('b', 'c') AS animals))) AS t(zoo, animals)
WITH a AS (SELECT 1) SELECT 1 UNION ALL SELECT 2
WITH a AS (SELECT 1) SELECT 1 UNION SELECT 2
WITH a AS (SELECT 1) SELECT 1 INTERSECT SELECT 2
WITH a AS (SELECT 1) SELECT 1 EXCEPT SELECT 2
WITH a AS (SELECT 1) SELECT 1 EXCEPT SELECT 2
WITH sub_query AS (SELECT a FROM table) (SELECT a FROM sub_query)
WITH sub_query AS (SELECT a FROM table) ((((SELECT a FROM sub_query))))
(SELECT 1) UNION (SELECT 2)
(SELECT 1) UNION SELECT 2
SELECT 1 UNION (SELECT 2)
(SELECT 1) ORDER BY x LIMIT 1 OFFSET 1
(SELECT 1 UNION SELECT 2) UNION (SELECT 2 UNION ALL SELECT 3)
(SELECT 1 UNION SELECT 2) ORDER BY x LIMIT 1 OFFSET 1
SELECT 1 UNION (SELECT 2) ORDER BY x
(SELECT 1) UNION SELECT 2 ORDER BY x
SELECT * FROM (((SELECT 1) UNION SELECT 2) ORDER BY x LIMIT 1 OFFSET 1)
SELECT * FROM ((SELECT 1 AS x) CROSS JOIN (SELECT 2 AS y)) AS z
((SELECT 1) EXCEPT (SELECT 2))
((SELECT 1)) LIMIT 1
VALUES (1) UNION SELECT * FROM x
WITH a AS (SELECT 1) SELECT a.* FROM a
WITH a AS (SELECT 1), b AS (SELECT 2) SELECT a.*, b.* FROM a CROSS JOIN b
WITH a AS (WITH b AS (SELECT 1 AS x) SELECT b.x FROM b) SELECT a.x FROM a
WITH RECURSIVE T(n) AS (VALUES (1) UNION ALL SELECT n + 1 FROM t WHERE n < 100) SELECT SUM(n) FROM t
WITH RECURSIVE T(n, m) AS (VALUES (1, 2) UNION ALL SELECT n + 1, n + 2 FROM t) SELECT SUM(n) FROM t
WITH baz AS (SELECT 1 AS col) UPDATE bar SET cid = baz.col1 FROM baz
SELECT * FROM (WITH y AS (SELECT 1 AS z) SELECT z FROM y) AS x
SELECT RANK() OVER () FROM x
SELECT RANK() OVER () AS y FROM x
SELECT RANK() OVER (PARTITION BY a) FROM x
SELECT RANK() OVER (PARTITION BY a, b) FROM x
SELECT RANK() OVER (ORDER BY a) FROM x
SELECT RANK() OVER (ORDER BY a, b) FROM x
SELECT RANK() OVER (PARTITION BY a ORDER BY a) FROM x
SELECT RANK() OVER (PARTITION BY a, b ORDER BY a, b DESC) FROM x
SELECT SUM(x) OVER (PARTITION BY a) AS y FROM x
SELECT SUM(x) OVER (PARTITION BY a ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
SELECT SUM(x) OVER (PARTITION BY a ORDER BY b ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
SELECT SUM(x) OVER (PARTITION BY a ORDER BY b ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
SELECT SUM(x) OVER (PARTITION BY a ORDER BY b RANGE BETWEEN INTERVAL '1' DAY PRECEDING AND CURRENT ROW)
SELECT SUM(x) OVER (PARTITION BY a ORDER BY b RANGE BETWEEN INTERVAL '1' DAY PRECEDING AND INTERVAL '2' DAYS FOLLOWING)
SELECT SUM(x) OVER (PARTITION BY a ORDER BY b RANGE BETWEEN INTERVAL '1' DAY PRECEDING AND UNBOUNDED FOLLOWING)
SELECT SUM(x) OVER (PARTITION BY a ROWS BETWEEN UNBOUNDED PRECEDING AND PRECEDING)
SELECT SUM(x) OVER (PARTITION BY a ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
SELECT SUM(x) OVER (PARTITION BY a ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING)
SELECT SUM(x) OVER (PARTITION BY a RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
SELECT SUM(x) OVER (PARTITION BY a RANGE BETWEEN 1 AND 3)
SELECT SUM(x) OVER (PARTITION BY a RANGE BETWEEN 1 FOLLOWING AND 3)
SELECT SUM(x) OVER (PARTITION BY a RANGE BETWEEN 1 FOLLOWING AND UNBOUNDED FOLLOWING)
SELECT AVG(x) OVER (ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) FROM t
SELECT SUM(x) OVER (PARTITION BY a ORDER BY date ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING)
SELECT LISTAGG(x) WITHIN GROUP (ORDER BY x) AS y
SELECT LISTAGG(x) WITHIN GROUP (ORDER BY x DESC)
SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY x)
SELECT PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY x)
SELECT SUM(x) FILTER(WHERE x > 1)
SELECT SUM(x) FILTER(WHERE x > 1) OVER (ORDER BY y)
SELECT COUNT(DISTINCT a) OVER (PARTITION BY c ORDER BY d ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING)
SELECT a['1'], b[0], x.c[0], "x".d['1'] FROM x
SELECT ARRAY(1, 2, 3) FROM x
SELECT ARRAY(ARRAY(1), ARRAY(2)) FROM x
SELECT MAP[ARRAY(1), ARRAY(2)] FROM x
SELECT MAP(ARRAY(1), ARRAY(2)) FROM x
SELECT MAX(ARRAY(1, 2, 3)) FROM x
SELECT ARRAY(ARRAY(0))[0][0] FROM x
SELECT MAP[ARRAY('x'), ARRAY(0)]['x'] FROM x
SELECT student, score FROM tests LATERAL VIEW EXPLODE(scores)
SELECT student, score FROM tests LATERAL VIEW EXPLODE(scores) AS score
SELECT student, score FROM tests LATERAL VIEW EXPLODE(scores) t AS score
SELECT student, score FROM tests LATERAL VIEW EXPLODE(scores) t AS score, name
SELECT student, score FROM tests LATERAL VIEW OUTER EXPLODE(scores) t AS score, name
SELECT tf.* FROM (SELECT 0) AS t LATERAL VIEW STACK(1, 2) tf
SELECT tf.* FROM (SELECT 0) AS t LATERAL VIEW STACK(1, 2) tf AS col0, col1, col2
SELECT student, score FROM tests CROSS JOIN UNNEST(scores) AS t(score)
SELECT student, score FROM tests CROSS JOIN UNNEST(scores) AS t(a, b)
SELECT student, score FROM tests CROSS JOIN UNNEST(scores) WITH ORDINALITY AS t(a, b)
SELECT student, score FROM tests CROSS JOIN UNNEST(x.scores) AS t(score)
SELECT student, score FROM tests CROSS JOIN UNNEST(ARRAY(x.scores)) AS t(score)
CREATE TABLE foo AS (SELECT 1) UNION ALL (SELECT 2)
CREATE TABLE foo (id INT PRIMARY KEY ASC)
CREATE TABLE a.b AS SELECT 1
CREATE TABLE a.b AS SELECT 1 WITH DATA AND STATISTICS
CREATE TABLE a.b AS SELECT 1 WITH NO DATA AND NO STATISTICS
CREATE TABLE a.b AS (SELECT 1) NO PRIMARY INDEX
CREATE TABLE a.b AS (SELECT 1) UNIQUE PRIMARY INDEX index1 (a) UNIQUE INDEX index2 (b)
CREATE TABLE a.b AS (SELECT 1) PRIMARY AMP INDEX index1 (a) UNIQUE INDEX index2 (b)
CREATE TABLE a.b AS SELECT a FROM a.c
CREATE TABLE IF NOT EXISTS x AS SELECT a FROM d
CREATE TABLE z (a INT, b VARCHAR, c VARCHAR(100), d DECIMAL(5, 3))
CREATE TABLE z (end INT)
CREATE TABLE z (a ARRAY<TEXT>, b MAP<TEXT, DOUBLE>, c DECIMAL(5, 3))
CREATE TABLE z (a INT, b VARCHAR COMMENT 'z', c VARCHAR(100) COMMENT 'z', d DECIMAL(5, 3))
CREATE TABLE z (a INT(11) DEFAULT UUID())
CREATE TABLE z (n INT DEFAULT 0 NOT NULL)
CREATE TABLE z (a INT(11) DEFAULT NULL COMMENT '客户id')
CREATE TABLE z (a INT(11) NOT NULL DEFAULT 1)
CREATE TABLE z (a INT(11) NOT NULL DEFAULT -1)
CREATE TABLE z (a INT(11) NOT NULL COLLATE utf8_bin AUTO_INCREMENT)
CREATE TABLE z (a INT, PRIMARY KEY (a))
CREATE TABLE z WITH (FORMAT='parquet') AS SELECT 1
CREATE TABLE z WITH (FORMAT='ORC', x='2') AS SELECT 1
CREATE TABLE z WITH (TABLE_FORMAT='iceberg', FORMAT='parquet') AS SELECT 1
CREATE TABLE z WITH (TABLE_FORMAT='iceberg', FORMAT='ORC', x='2') AS SELECT 1
CREATE TABLE z (z INT) WITH (PARTITIONED_BY=(x INT, y INT))
CREATE TABLE z (z INT) WITH (PARTITIONED_BY=(x INT)) AS SELECT 1
CREATE TABLE z AS (WITH cte AS (SELECT 1) SELECT * FROM cte)
CREATE TABLE z AS ((WITH cte AS (SELECT 1) SELECT * FROM cte))
CREATE TABLE z (a INT UNIQUE)
CREATE TABLE z (a INT AUTO_INCREMENT)
CREATE TABLE z (a INT UNIQUE AUTO_INCREMENT)
CREATE TABLE z (a INT REFERENCES parent (b, c))
CREATE TABLE z (a INT PRIMARY KEY, b INT REFERENCES foo (id))
CREATE TABLE z (a INT, FOREIGN KEY (a) REFERENCES parent (b, c))
CREATE TABLE foo (bar INT REFERENCES baz (baz_id) ON DELETE NO ACTION)
CREATE TABLE foo (bar INT REFERENCES baz (baz_id) ON DELETE CASCADE)
CREATE TABLE foo (bar INT REFERENCES baz (baz_id) ON DELETE SET NULL)
CREATE TABLE foo (bar INT REFERENCES baz (baz_id) ON DELETE SET DEFAULT)
CREATE TABLE foo (bar INT REFERENCES baz (baz_id) ON UPDATE NO ACTION)
CREATE TABLE foo (bar INT REFERENCES baz (baz_id) ON UPDATE CASCADE)
CREATE TABLE foo (bar INT REFERENCES baz (baz_id) ON UPDATE SET NULL)
CREATE TABLE foo (bar INT REFERENCES baz (baz_id) ON UPDATE SET DEFAULT)
CREATE TABLE asd AS SELECT asd FROM asd WITH NO DATA
CREATE TABLE asd AS SELECT asd FROM asd WITH DATA
CREATE TABLE products (x INT GENERATED BY DEFAULT AS IDENTITY)
CREATE TABLE products (x INT GENERATED BY DEFAULT ON NULL AS IDENTITY)
CREATE TABLE products (x INT GENERATED ALWAYS AS IDENTITY)
CREATE TABLE konyvszerzo (szerzo_azon INT CONSTRAINT konyvszerzo_szerzo_fk REFERENCES szerzo)
CREATE TABLE IF NOT EXISTS customer (pk BIGINT NOT NULL GENERATED ALWAYS AS IDENTITY (INCREMENT BY 1))
CREATE TABLE customer (pk BIGINT NOT NULL GENERATED ALWAYS AS IDENTITY (START WITH 10 INCREMENT BY 1 MINVALUE -1 MAXVALUE 1 NO CYCLE))
CREATE TABLE customer (pk BIGINT NOT NULL GENERATED ALWAYS AS IDENTITY (START WITH 10))
CREATE TABLE customer (pk BIGINT NOT NULL GENERATED ALWAYS AS IDENTITY (CYCLE))
CREATE TABLE customer (period INT NOT NULL)
CREATE TABLE foo (baz_id INT REFERENCES baz (id) DEFERRABLE)
CREATE TABLE foo (baz CHAR(4) CHARACTER SET LATIN UPPERCASE NOT CASESPECIFIC COMPRESS 'a')
CREATE TABLE db.foo (id INT NOT NULL, valid_date DATE FORMAT 'YYYY-MM-DD', measurement INT COMPRESS)
CREATE TABLE foo (baz DATE FORMAT 'YYYY/MM/DD' TITLE 'title' INLINE LENGTH 1 COMPRESS ('a', 'b'))
CREATE TABLE t (title TEXT)
CREATE TABLE foo (baz INT, inline TEXT)
CREATE ALGORITHM=UNDEFINED DEFINER=foo@% SQL SECURITY DEFINER VIEW a AS (SELECT a FROM b)
CREATE TEMPORARY TABLE x AS SELECT a FROM d
CREATE TEMPORARY TABLE IF NOT EXISTS x AS SELECT a FROM d
CREATE TABLE a (b INT) ON COMMIT PRESERVE ROWS
CREATE VIEW x AS SELECT a FROM b
CREATE VIEW IF NOT EXISTS x AS SELECT a FROM b
CREATE VIEW z (a, b COMMENT 'b', c COMMENT 'c') AS SELECT a, b, c FROM d
CREATE VIEW IF NOT EXISTS z (a, b COMMENT 'b', c COMMENT 'c') AS SELECT a, b, c FROM d
CREATE OR REPLACE VIEW x AS SELECT *
CREATE OR REPLACE TEMPORARY VIEW x AS SELECT *
CREATE TEMPORARY VIEW x AS SELECT a FROM d
CREATE TEMPORARY VIEW IF NOT EXISTS x AS SELECT a FROM d
CREATE TEMPORARY VIEW x AS WITH y AS (SELECT 1) SELECT * FROM y
CREATE MATERIALIZED VIEW x.y.z AS SELECT a FROM b
CREATE VIEW z (a, b)
CREATE VIEW z (a, b COMMENT 'b', c COMMENT 'c')
CREATE VIEW z AS LOCKING ROW FOR ACCESS SELECT a FROM b
CREATE TEMPORARY FUNCTION f
CREATE TEMPORARY FUNCTION f AS 'g'
CREATE FUNCTION f
CREATE FUNCTION f AS 'g'
CREATE FUNCTION a(b INT, c VARCHAR) AS 'SELECT 1'
CREATE FUNCTION a() LANGUAGE sql
CREATE FUNCTION a() LANGUAGE sql RETURNS INT
CREATE FUNCTION a.b(x INT) RETURNS INT AS RETURN x + 1
CREATE FUNCTION a.b(x TEXT) RETURNS TEXT CONTAINS SQL AS RETURN x
CREATE FUNCTION a.b(x TEXT) RETURNS TEXT LANGUAGE SQL MODIFIES SQL DATA AS RETURN x
CREATE FUNCTION a.b(x TEXT) LANGUAGE SQL READS SQL DATA RETURNS TEXT AS RETURN x
CREATE FUNCTION a.b.c()
CREATE INDEX abc ON t(a)
CREATE INDEX "abc" ON t(a)
CREATE INDEX abc ON t(a, b, b)
CREATE INDEX abc ON t(a NULLS LAST)
CREATE INDEX pointloc ON points USING GIST(BOX(location, location))
CREATE UNIQUE INDEX abc ON t(a, b, b)
CREATE UNIQUE INDEX IF NOT EXISTS my_idx ON tbl(a, b)
CREATE SCHEMA x
CREATE SCHEMA IF NOT EXISTS y
CREATE DATABASE x
CREATE DATABASE IF NOT EXISTS y
CREATE PROCEDURE IF NOT EXISTS a.b.c() AS 'DECLARE BEGIN; END'
CREATE TABLE T3 AS (SELECT DISTINCT A FROM T1 EXCEPT (SELECT A FROM T2) LIMIT 1)
DESCRIBE x
DESCRIBE EXTENDED a.b
DESCRIBE FORMATTED a.b
DESCRIBE SELECT 1
DROP INDEX a.b.c
DROP FUNCTION a.b.c (INT)
DROP MATERIALIZED VIEW x.y.z
CACHE TABLE x
CACHE LAZY TABLE x
CACHE LAZY TABLE x OPTIONS('storageLevel' = 'value')
CACHE LAZY TABLE x OPTIONS(N'storageLevel' = 'value')
CACHE LAZY TABLE x OPTIONS('storageLevel' = 'value') AS SELECT 1
CACHE LAZY TABLE x OPTIONS('storageLevel' = 'value') AS WITH a AS (SELECT 1) SELECT a.* FROM a
CACHE LAZY TABLE x AS WITH a AS (SELECT 1) SELECT a.* FROM a
CACHE TABLE x AS WITH a AS (SELECT 1) SELECT a.* FROM a
CACHE TABLE x AS (SELECT 1 AS y)
DROP PROCEDURE a.b.c (INT)
INSERT OVERWRITE TABLE a.b PARTITION(ds) SELECT x FROM y
INSERT OVERWRITE TABLE a.b PARTITION(ds = 'YYYY-MM-DD') SELECT x FROM y
INSERT OVERWRITE TABLE a.b PARTITION(ds, hour) SELECT x FROM y
INSERT OVERWRITE TABLE a.b PARTITION(ds = 'YYYY-MM-DD', hour = 'hh') SELECT x FROM y
INSERT INTO a.b PARTITION(DAY = '2024-04-14') (col1, col2) SELECT x FROM y
DELETE FROM x WHERE y > 1
DELETE FROM y
DELETE FROM event USING sales WHERE event.eventid = sales.eventid
DELETE FROM event USING sales, bla WHERE event.eventid = sales.eventid
DELETE FROM event USING sales AS s WHERE event.eventid = s.eventid
DELETE FROM event AS event USING sales AS s WHERE event.eventid = s.eventid
DROP TABLE a
DROP TABLE a.b
DROP TABLE IF EXISTS a
DROP TABLE IF EXISTS a.b
DROP TABLE a CASCADE
DROP TABLE s_hajo CASCADE CONSTRAINTS
DROP TABLE a PURGE
DROP VIEW a
DROP VIEW a.b
DROP VIEW IF EXISTS a
DROP VIEW IF EXISTS a.b
USE db
BEGIN
ROLLBACK
ROLLBACK TO b
INSERT INTO x SELECT * FROM y
INSERT INTO x (SELECT * FROM y)
INSERT INTO x WITH y AS (SELECT 1) SELECT * FROM y
INSERT INTO x.z IF EXISTS SELECT * FROM y
INSERT INTO x VALUES (1, 'a', 2.0)
INSERT INTO x VALUES (1, 'a', 2.0), (1, 'a', 3.0), (X(), y[1], z.x)
INSERT INTO y (a, b, c) SELECT a, b, c FROM x
INSERT INTO y (SELECT 1) UNION (SELECT 2)
INSERT INTO result_table (WITH test AS (SELECT * FROM source_table) SELECT * FROM test)
INSERT INTO "tests_user" ("username", "first_name", "last_name") VALUES ('fiara', 'Fiara', 'Ironhide') RETURNING "tests_user"."id"
INSERT INTO t1 (tc1 /* tc1 */, tc2 /* tc2 */) SELECT c1 /* sc1 */, c2 /* sc2 */ FROM t
INSERT INTO t1 ("tc1" /* tc1 */, "tc2" /* tc2 */) SELECT "c1" /* sc1 */, "c2" /* sc2 */ FROM t
INSERT OVERWRITE TABLE x IF EXISTS SELECT * FROM y
INSERT OVERWRITE TABLE a.b IF EXISTS SELECT * FROM y
INSERT OVERWRITE DIRECTORY 'x' SELECT 1
INSERT OVERWRITE LOCAL DIRECTORY 'x' SELECT 1
INSERT OVERWRITE LOCAL DIRECTORY 'x' ROW FORMAT DELIMITED FIELDS TERMINATED BY '1' COLLECTION ITEMS TERMINATED BY '2' MAP KEYS TERMINATED BY '3' LINES TERMINATED BY '4' NULL DEFINED AS '5' SELECT 1
LOAD DATA INPATH 'x' INTO TABLE y PARTITION(ds = 'yyyy')
LOAD DATA LOCAL INPATH 'x' INTO TABLE y PARTITION(ds = 'yyyy')
LOAD DATA LOCAL INPATH 'x' INTO TABLE y PARTITION(ds = 'yyyy') INPUTFORMAT 'y'
LOAD DATA LOCAL INPATH 'x' INTO TABLE y PARTITION(ds = 'yyyy') INPUTFORMAT 'y' SERDE 'z'
LOAD DATA INPATH 'x' INTO TABLE y INPUTFORMAT 'y' SERDE 'z'
LOAD DATA INPATH 'x' INTO TABLE y.b INPUTFORMAT 'y' SERDE 'z'
SELECT 1 FROM PARQUET_SCAN('/x/y/*') AS y
UNCACHE TABLE x
UNCACHE TABLE IF EXISTS x
UPDATE tbl_name SET foo = 123
UPDATE tbl_name SET foo = 123, bar = 345
UPDATE db.tbl_name SET foo = 123 WHERE tbl_name.bar = 234
UPDATE db.tbl_name SET foo = 123, foo_1 = 234 WHERE tbl_name.bar = 234
UPDATE products SET price = price * 1.10 WHERE price <= 99.99 RETURNING name, price AS new_price
UPDATE t1 AS a, t2 AS b, t3 AS c LEFT JOIN t4 AS d ON c.id = d.id SET a.id = 1
COMMENT ON COLUMN my_schema.my_table.my_column IS 'Employee ID number'
COMMENT ON DATABASE my_database IS 'Development Database'
COMMENT ON PROCEDURE my_proc(integer, integer) IS 'Runs a report'
COMMENT ON TABLE my_schema.my_table IS 'Employee Information'
COMMENT ON TABLE my_schema.my_table IS N'National String'
WITH a AS (SELECT 1) INSERT INTO b SELECT * FROM a
WITH a AS (SELECT * FROM b) UPDATE a SET col = 1
WITH a AS (SELECT * FROM b) CREATE TABLE b AS SELECT * FROM a
WITH a AS (SELECT * FROM b) DELETE FROM a
SELECT ? AS ? FROM x WHERE b BETWEEN ? AND ? GROUP BY ?, 1 LIMIT ?
SELECT :hello, ? FROM x LIMIT :my_limit
SELECT a FROM b WHERE c IS ?
SELECT * FROM x OFFSET @skip FETCH NEXT @take ROWS ONLY
WITH a AS ((SELECT b.foo AS foo, b.bar AS bar FROM b) UNION ALL (SELECT c.foo AS foo, c.bar AS bar FROM c)) SELECT * FROM a
WITH a AS ((SELECT 1 AS b) UNION ALL (SELECT 1 AS b)) SELECT * FROM a
SELECT (WITH x AS (SELECT 1 AS y) SELECT * FROM x) AS z
SELECT ((SELECT 1) + 1)
SELECT * FROM project.dataset.INFORMATION_SCHEMA.TABLES
SELECT CAST(x AS INT) /* comment */ FROM foo
SELECT c /* c1 /* c2 */ c3 */
SELECT c /* c1 /* c2 /* c3 */ */ */
SELECT c /* c1 */ AS alias /* c2 */
SELECT a /* x */, b /* x */
SELECT a /* x */ /* y */ /* z */, b /* k */ /* m */
SELECT * FROM foo /* x */, bla /* x */
SELECT 1 /* comment */ + 1
SELECT 1 /* c1 */ + 2 /* c2 */
SELECT 1 /* c1 */ + /* c2 */ 2 /* c3 */
SELECT 1 /* c1 */ + 2 /* c2 */ + 3 /* c3 */
SELECT 1 /* c1 */ + 2 /* c2 */, 3 /* c3 */
SELECT x FROM a.b.c /* x */, e.f.g /* x */
SELECT FOO(x /* c */) /* FOO */, b /* b */
SELECT FOO(x /* c1 */ + y /* c2 */ + BLA(5 /* c3 */)) FROM (VALUES (1 /* c4 */, "test" /* c5 */)) /* c6 */
INSERT INTO foo SELECT * FROM bar /* comment */
/* c */ WITH x AS (SELECT 1) SELECT * FROM x
SELECT a FROM x WHERE a COLLATE 'utf8_general_ci' = 'b'
SELECT x AS INTO FROM bla
ALTER TABLE integers ADD COLUMN k INT
ALTER TABLE integers ADD COLUMN k INT FIRST
ALTER TABLE integers ADD COLUMN k INT AFTER m
ALTER TABLE integers ADD COLUMN IF NOT EXISTS k INT
ALTER TABLE IF EXISTS integers ADD COLUMN k INT
ALTER TABLE integers ADD COLUMN l INT DEFAULT 10
ALTER TABLE measurements ADD COLUMN mtime TIMESTAMPTZ DEFAULT NOW()
ALTER TABLE integers DROP COLUMN k
ALTER TABLE integers DROP COLUMN IF EXISTS k
ALTER TABLE integers DROP COLUMN k CASCADE
ALTER TABLE integers ALTER COLUMN i SET DATA TYPE VARCHAR
ALTER TABLE integers ALTER COLUMN i SET DATA TYPE VARCHAR USING CONCAT(i, '_', j)
ALTER TABLE integers ALTER COLUMN i SET DEFAULT 10
ALTER TABLE integers ALTER COLUMN i DROP DEFAULT
ALTER TABLE ingredients ALTER COLUMN amount COMMENT 'tablespoons'
ALTER TABLE mydataset.mytable DROP COLUMN A, DROP COLUMN IF EXISTS B
ALTER TABLE mydataset.mytable ADD COLUMN A TEXT, ADD COLUMN IF NOT EXISTS B INT
ALTER TABLE orders DROP PARTITION(dt = '2014-05-14', country = 'IN')
ALTER TABLE orders DROP IF EXISTS PARTITION(dt = '2014-05-14', country = 'IN')
ALTER TABLE orders DROP PARTITION(dt = '2014-05-14', country = 'IN'), PARTITION(dt = '2014-05-15', country = 'IN')
ALTER TABLE mydataset.mytable DELETE WHERE x = 1
ALTER TABLE table1 RENAME COLUMN c1 TO c2
ALTER TABLE table1 RENAME COLUMN IF EXISTS c1 TO c2
ALTER TABLE table1 RENAME TO table2
ALTER VIEW view1 AS SELECT a, b, c FROM table1
ALTER VIEW view1 AS SELECT a, b, c FROM table1 UNION ALL SELECT a, b, c FROM table2
ALTER VIEW view1 AS SELECT a, b, c FROM table1 UNION ALL SELECT a, b, c FROM table2 LIMIT 100
SELECT div.a FROM test_table AS div
WITH view AS (SELECT 1 AS x) SELECT * FROM view
ARRAY<STRUCT<INT, DOUBLE, ARRAY<INT>>>
STRUCT<int INT>
SELECT CAST(NULL AS ARRAY<INT>) IS NULL AS array_is_null
ALTER TABLE "schema"."tablename" ADD CONSTRAINT "CHK_Name" CHECK (NOT "IdDwh" IS NULL AND "IdDwh" <> (0))
ALTER TABLE persons ADD CONSTRAINT persons_pk PRIMARY KEY (first_name, last_name)
ALTER TABLE pets ADD CONSTRAINT pets_persons_fk FOREIGN KEY (owner_first_name, owner_last_name) REFERENCES persons
ALTER TABLE pets ADD CONSTRAINT pets_name_not_cute_chk CHECK (LENGTH(name) < 20)
ALTER TABLE people10m ADD CONSTRAINT dateWithinRange CHECK (birthDate > '1900-01-01')
ALTER TABLE people10m ADD CONSTRAINT validIds CHECK (id > 1 AND id < 99999999) ENFORCED
ALTER TABLE baa ADD CONSTRAINT boo PRIMARY KEY (x, y) NOT ENFORCED DEFERRABLE INITIALLY DEFERRED NORELY
ALTER TABLE baa ADD CONSTRAINT boo PRIMARY KEY (x, y) NOT ENFORCED DEFERRABLE INITIALLY DEFERRED NORELY
ALTER TABLE baa ADD CONSTRAINT boo FOREIGN KEY (x, y) REFERENCES persons ON UPDATE NO ACTION ON DELETE NO ACTION MATCH FULL
ALTER TABLE a ADD PRIMARY KEY (x, y) NOT ENFORCED
ALTER TABLE a ADD FOREIGN KEY (x, y) REFERENCES bla
ALTER TABLE s_ut ADD CONSTRAINT s_ut_uq UNIQUE hajo
SELECT partition FROM a
SELECT end FROM a
SELECT id FROM b.a AS a QUALIFY ROW_NUMBER() OVER (PARTITION BY br ORDER BY sadf DESC) = 1
SELECT * FROM x WHERE a GROUP BY a HAVING b SORT BY s ORDER BY c LIMIT d
SELECT LEFT.FOO FROM BLA AS LEFT
SELECT RIGHT.FOO FROM BLA AS RIGHT
SELECT LEFT FROM LEFT LEFT JOIN RIGHT RIGHT JOIN LEFT
SELECT * FROM x WHERE name ILIKE ANY XXX('a', 'b')
SELECT * FROM x WHERE name LIKE ANY XXX('a', 'b')
a OVERLAPS b
PRAGMA quick_check
PRAGMA QUICK_CHECK(0)
PRAGMA QUICK_CHECK('sqlite_master')
PRAGMA schema.quick_check
PRAGMA schema.QUICK_CHECK(0)
PRAGMA schema.QUICK_CHECK('sqlite_master')
PRAGMA synchronous = 2
PRAGMA synchronous = FULL
PRAGMA memory_limit = '1GB'
PRAGMA schema.synchronous = 2
PRAGMA schema.synchronous = FULL
PRAGMA schema.memory_limit = '1GB'
JSON_OBJECT()
JSON_OBJECT(*)
JSON_OBJECT('key1': 1, 'key2': TRUE)
JSON_OBJECT('id': '5', 'fld1': 'bla', 'fld2': 'bar')
JSON_OBJECT('x': NULL, 'y': 1 NULL ON NULL)
JSON_OBJECT('x': NULL, 'y': 1 WITH UNIQUE KEYS)
JSON_OBJECT('x': NULL, 'y': 1 ABSENT ON NULL WITH UNIQUE KEYS)
JSON_OBJECT('x': 1 RETURNING VARCHAR(100))
JSON_OBJECT('x': 1 RETURNING VARBINARY FORMAT JSON ENCODING UTF8)
PRIOR AS x
SELECT if.x
SELECT NEXT VALUE FOR db.schema.sequence_name
SELECT NEXT VALUE FOR db.schema.sequence_name OVER (ORDER BY foo), col
SELECT PERCENTILE_CONT(x, 0.5) OVER ()
WITH my_cte AS (SELECT 'a' AS desc) SELECT desc AS description FROM my_cte
WITH my_cte AS (SELECT 'a' AS asc) SELECT asc AS description FROM my_cte
SELECT * FROM case
SELECT * FROM schema.case
SELECT * FROM current_date
SELECT * FROM schema.current_date
SELECT /*+ SOME_HINT(foo) */ 1
SELECT /*+ REBALANCE */ * FROM foo
SELECT * FROM (tbl1 CROSS JOIN (SELECT * FROM tbl2) AS t1)
/* comment1 */ INSERT INTO x /* comment2 */ VALUES (1, 2, 3)
/* comment1 */ UPDATE tbl /* comment2 */ SET x = 2 WHERE x < 2
/* comment1 */ DELETE FROM x /* comment2 */ WHERE y > 1
/* comment */ CREATE TABLE foo AS SELECT 1
SELECT next, transform, if
SELECT "any", "case", "if", "next"
SELECT x FROM y ORDER BY x ASC
KILL '123'
KILL CONNECTION 123
KILL QUERY '123'
CHR(97)
SELECT * FROM UNNEST(x) WITH ORDINALITY UNION ALL SELECT * FROM UNNEST(y) WITH ORDINALITY
SELECT x FROM t1 UNION ALL SELECT x FROM t2 LIMIT 1
SELECT x FROM t1 UNION ALL SELECT x FROM t2 UNION ALL SELECT x FROM t3 LIMIT 1
WITH use(use) AS (SELECT 1) SELECT use FROM use
SELECT recursive FROM t
SELECT (ROW_NUMBER() OVER (PARTITION BY user ORDER BY date ASC) - ROW_NUMBER() OVER (PARTITION BY user, segment ORDER BY date ASC)) AS group_id FROM example_table
CAST(foo AS BPCHAR)
values
SELECT values
SELECT values AS values FROM t WHERE values + 1 > 3
SELECT truncate
SELECT only
TRUNCATE(a, b)
SELECT enum
SELECT unlogged
SELECT name
SELECT copy
SELECT rollup
SELECT unnest
SELECT cube, cube.x FROM cube
SELECT * FROM a STRAIGHT_JOIN b
SELECT COUNT(DISTINCT "foo bar") FROM (SELECT 1 AS "foo bar") AS t
SELECT vector
WITH all AS (SELECT 1 AS count) SELECT all.count FROM all
SELECT rename
