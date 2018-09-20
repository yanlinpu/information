Structure Query Language

分类:

- DDL
desc tablename
```
+----------+---------------+------+-----+---------+-------+
| Field    | Type          | Null | Key | Default | Extra |
+----------+---------------+------+-----+---------+-------+
| ename    | varchar(10)   | YES  |     | NULL    |       |
| hiredate | date          | YES  |     | NULL    |       |
| sal      | decimal(10,2) | YES  |     | NULL    |       |
| deptno   | int(2)        | YES  |     | NULL    |       |
+----------+---------------+------+-----+---------+-------+
4 rows in set (0.01 sec)
```

show create table tablename
```
mysql> show create table emp \G;
*************************** 1. row ***************************
       Table: emp
Create Table: CREATE TABLE `emp` (
  `ename` varchar(10) DEFAULT NULL,
  `hiredate` date DEFAULT NULL,
  `sal` decimal(10,2) DEFAULT NULL,
  `deptno` int(2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1
1 row in set (0.00 sec)

ERROR: 
No query specified
```