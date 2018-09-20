# mysql 数据库区别于其他数据库的最主要的一个特点就是其插件式的表存储引擎。

1. InnoDB 存储引擎

    ```
    InnoDB 存储引擎支持事务，其设计目标主要面向在线事务处理（OLTP）的应用。其特点是行锁设计、支持外键，并支持类似于Oracle的非锁定键，即默认读取操作不会产生锁。从Mysql数据库5.5.8版本之后，InnoDB存储引擎是默认的存储引擎。

    它可以将每个InnoDB存储引擎的表单独放到一个独立的idb文件中。

    对于表中存储的数据，InnoDB存储引擎采用了聚集（clustered）的方式，因此每张表的存储都是按主键的顺序进行存放的。如未指定主键，InnoDB存储引擎会为每一行生成一个6字节的ROWID，并以此作为主键。
    ```
2. MyISAM存储引擎

    ```
    MyISAM存储引擎不支持事务、表锁设计，支持全文索引，主要面向OLAP数据库应用。MyISAM存储引擎的缓冲池只缓存（cache）索引文件，而不缓存数据文件。

    MyISAM存储引擎表由MYD（存放数据文件）和MYI（存放索引文件）组成。可以使用myisampack工具来进一步压缩、解压数据文件。
    ```

3. NDB存储引擎
    
    ```
    NDB存储引擎是一个集群存储引擎，其结构是share noting的集群结构。特点是数据全部放在内存中。

    有一个问题值得注意，NDB存储引擎的连接操作（JOIN）是在MYSQL数据库层完成的，而不是在存储引擎层完成的。这意味着复杂的连接操作需要巨大的网络开销，因此查询速度很慢。
    ```
4. Memory存储引擎

    ```
    Memory存储引擎（之前称HEAP存储引擎）将表中数据存放在内存中，如果数据库重启或发生崩溃，表中的数据都将消失。适合用于存储临时数据的临时表。Memory存储引擎默认使用哈希索引，而不是B+树索引。

    只支持表锁，并发性能较差，不支持TEXT和BLOB列类型。最重要的是，存储变长字段（varchar）时是按照定长字段（char）的方式进行的，因此会浪费内存。
    ```

5. Archive存储引擎

    ```
    Archive存储引擎只支持INSERT和SELECT操作，从5.1开始支持索引。
    Archive存储引擎使用zlib算法将数据行（row）进行压缩后存储，压缩比例一般可达1：10。
    Archive存储引擎非常适合存储归档数据，如日志信息。
    其设计目的主要是提供高速的插入和压缩功能。
    ```

6. Federate存储引擎
7. Maria存储引擎

    ```
    可以看做MyISAM的后续版本。
    特点是：支持缓存数据和索引文件，应用了行锁设计，提供MVCC功能，支持事务和非事务安全的选项，以及更好的BLOB字符类型处理功能。
    ```

|特性|InnoDB|MyISAM|Memory|Archive|NDB|
|--|--|--|--|--|--|
|存储容量限制|64TB|NO|YES|NO|YES|
|事务支持|YES|NO|NO|NO|NO|
|锁的粒度|Row|Table|Table|Row|Row|
|MVCC支持|YES|NO|NO|YES|YES|
|B-Tree索引|YES|YES|YES|NO|YES|
|Hash索引|YES|NO|YES|NO|YES|
|全文索引|YES|YES|NO|NO|NO|
|数据缓存|YES|NO|YES|NO|YES|
|索引缓存|YES|YES|YES|NO|YES|
|数据压缩|NO|YES|NO|YES|YES|
|存储空间cost|High|Low|N/A|very low|low|
|Memory内存消耗|High|Low|Medium|Low|High|
|insert速度|Low|High|High|very high|High|
|外键|YES|NO|NO|NO|NO|

## 查看当前使用的MySQL数据库锁支持的存储引擎
`$ show engines \G;`
```
*************************** 1. row ***************************
      Engine: MRG_MyISAM
     Support: YES
     Comment: Collection of identical MyISAM tables
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 2. row ***************************
      Engine: CSV
     Support: YES
     Comment: CSV storage engine
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 3. row ***************************
      Engine: Aria
     Support: YES
     Comment: Crash-safe tables with MyISAM heritage
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 4. row ***************************
      Engine: MyISAM
     Support: YES
     Comment: MyISAM storage engine
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 5. row ***************************
      Engine: MEMORY
     Support: YES
     Comment: Hash based, stored in memory, useful for temporary tables
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 6. row ***************************
      Engine: InnoDB
     Support: DEFAULT
     Comment: Percona-XtraDB, Supports transactions, row-level locking, foreign keys and encryption for tables
Transactions: YES
          XA: YES
  Savepoints: YES
*************************** 7. row ***************************
      Engine: SEQUENCE
     Support: YES
     Comment: Generated tables filled with sequential values
Transactions: YES
          XA: NO
  Savepoints: YES
*************************** 8. row ***************************
      Engine: PERFORMANCE_SCHEMA
     Support: YES
     Comment: Performance Schema
Transactions: NO
          XA: NO
  Savepoints: NO
8 rows in set (0.00 sec)

ERROR: No query specified
```

## 创建不同搜索引擎的数据库表
`$ create table mytest Engine=MyISAM AS SELECT * FROM salaries;` 


