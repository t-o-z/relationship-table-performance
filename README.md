# relationship-table-performance

## Use docker postgres 9.4

```
docker run --name test-db -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -d postgres:9.4
```

## Work in container

```
docker exec -it test-db bash
```

## Create tables

```
DROP TABLE relations;
DROP TABLE points;

CREATE TABLE relations (
    id INT NOT NULL ,
    start_id INT NOT NULL ,
    end_id INT NOT NULL 
);

CREATE TABLE points (
    id INT NOT NULL ,
    point_id INT NOT NULL 
);
```

## Regist test data

```
brew install postgres
pip3 install psycopg2
python3 test.py
```

## Inspection the performance

```
(EXPLAIN) SELECT 
    relations.id AS relation_id,
    start_points.id AS start_point_id,
    end_points.id AS end_point_id 
FROM
    relations 
JOIN
    points AS start_points ON relations.start_id = start_points.point_id
JOIN
    points AS end_points ON relations.end_id = end_points.point_id
```

6518.0ms / 1,999,999 records

```
"Hash Join  (cost=132176.00..293083.00 rows=2000000 width=12)"
"  Hash Cond: (relations.end_id = end_points.point_id)"
"  ->  Hash Join  (cost=66088.00..164650.00 rows=2000000 width=12)"
"        Hash Cond: (relations.start_id = start_points.point_id)"
"        ->  Seq Scan on relations  (cost=0.00..36217.00 rows=2000000 width=12)"
"        ->  Hash  (cost=33275.00..33275.00 rows=2000000 width=8)"
"              ->  Seq Scan on points start_points  (cost=0.00..33275.00 rows=2000000 width=8)"
"  ->  Hash  (cost=33275.00..33275.00 rows=2000000 width=8)"
"        ->  Seq Scan on points end_points  (cost=0.00..33275.00 rows=2000000 width=8)"
```


* Add indexes

```
CREATE INDEX point_id_index ON points (point_id) ;
CREATE INDEX relation_start_index ON relations (start_id) ;
CREATE INDEX relation_end_index ON relations (end_id) ;
```

* 5320.1ms / 1,999,999 records

```
"Hash Join  (cost=66091.70..291826.50 rows=2000000 width=12)"
"  Hash Cond: (relations.start_id = start_points.point_id)"
"  ->  Merge Join  (cost=3.70..163393.50 rows=2000000 width=12)"
"        Merge Cond: (relations.end_id = end_points.point_id)"
"        ->  Index Scan using relation_end_index on relations  (cost=0.43..68168.43 rows=2000000 width=12)"
"        ->  Index Scan using point_id_index on points end_points  (cost=0.43..65226.43 rows=2000000 width=8)"
"  ->  Hash  (cost=33275.00..33275.00 rows=2000000 width=8)"
"        ->  Seq Scan on points start_points  (cost=0.00..33275.00 rows=2000000 width=8)"
```

* Add more indexes

```
CREATE INDEX relation_id_index ON relations (id) ;
CREATE INDEX point_p_id_index ON points (id) ;
CREATE INDEX relation_id_column_index ON relations (start_id, end_id) ;
commit;
```

* 5941.3ms / 1,999,999 records

```
"Hash Join  (cost=66091.70..291826.50 rows=2000000 width=12)"
"  Hash Cond: (relations.start_id = start_points.point_id)"
"  ->  Merge Join  (cost=3.70..163393.50 rows=2000000 width=12)"
"        Merge Cond: (relations.end_id = end_points.point_id)"
"        ->  Index Scan using relation_end_index on relations  (cost=0.43..68168.43 rows=2000000 width=12)"
"        ->  Index Scan using point_id_index on points end_points  (cost=0.43..65226.43 rows=2000000 width=8)"
"  ->  Hash  (cost=33275.00..33275.00 rows=2000000 width=8)"
"        ->  Seq Scan on points start_points  (cost=0.00..33275.00 rows=2000000 width=8)"
```
