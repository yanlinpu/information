## 概述
InnoDB存储引擎是第一个完整支持ACID事务的MySQL存储引擎。其特点是行锁设计、支持MVCC、支持外键、提供一致性非锁定读，同时被设计用来最有效地利用以及使用内存和CPU。

## 体系架构
InnoDB存储引擎是多线程的模型，因此其后台有多个不同的后台线程，负责处理不同的任务。

- Master Thread

    主要负责将缓冲池的数据异步刷新到磁盘，保证数据的一致性

- IO Thread

    在InnoDB存储引擎中大量的使用了AIO（Async IO）来处理写IO请求。IO Thread主要负责这些IO请求的回调处理。`$ show variables like 'innodb_%io_threads';`

- Purge Thread

    事务被提交后，其所使用的undolog可能不在需要，因此需要PurgeThread来回收已经使用并分配的undo页。`$ show variables like 'innodb_pruge_threads' \G;`

- Page Cleaner Thread

    脏页的刷新操作都放入到单独的线程中完成，减轻Master Thread的工作及对于用于查询线程的阻塞。


## 内存

- 缓存池

    InnoDB存储引擎是基于磁盘存储，并将其中的记录按照页的方式进行管理。在数据库中进行读取页的操作，首先将从磁盘读到的页存放在缓存中，下一次在读相同的页时，首先判断是否存在缓存池中。若存在，直接读取该页。否则，读取磁盘上的页。对于页的修改操作，则首先修改缓存池中的页，然后再以一定的频率刷新到磁盘上。页从缓冲池刷新回磁盘的操作并不是在每次页发生更新时触发，而是通过一种称为Checkpoint的机制刷新回磁盘。`$ show variables like 'innodb_buffer_pool_size' \G;`

    缓冲池是一个很大的内存区域，其中存放各种类型的页。通常来说，数据库中的缓存池是通过LRU(Latest Recent Used，最近最少使用)算法来进行管理的。即最频繁使用的页在LRU列表的前端，而最少使用的页在LRU列表的末尾。当缓冲池不能存放新读取到的页时，将首先释放LRU列表中尾端的页。

    在InnoDB存储引擎中，缓存池中页的默认大小为16KB，同样使用LRU算法对缓存池进行管理。在InnoDB存储引擎中，LRU列表中还加入了midpoint位置。新读取到的页，并不是直接放入到LRU列表的首部，而是放入到LRU列表的midpoint位置。这个算法在InnoDB存储引擎下称为“midpoint insertion strategy”。默认5/8处。`$ show variables like 'innodb_old_blocks_pct'\G;`midpoint之前的称为new列表，之后的称为old列表。

    InnoDB存储引擎引入另一个参数`$ show variables like 'innodb_old_blocks_time' \G;`来进一步管理LRU列表，用于表示页读取到mid位置后需要等待多久才会被加入到LRU列表的热端。

    InnoDB存储引擎从1.0.x版本开始支持压缩页的功能，即将原本16KB的页压缩为1KB，2KB，4KB，8KB。对于非16K的页，是通过unzip_LRU列表进行管理的。`$ show variables like 'in'\G;`

## checkpoint

倘若每次一个页发生变化，就将新页的版本刷新到磁盘，那么这个开销是非常大的。若热点数据集中在某几个页中，那么数据库的性能将变得非常差。同时，如果在从缓冲池将页的新版本刷新到磁盘时发生宕机，那么数据将不能恢复了。为了避免发生数据丢失的问题，当前事务数据库系统普遍采用了write ahead log策略，即当事务提交时，先写重做日志，在修改页。当由于发生宕机而导致数据丢失时，通过重做日志来完成数据的恢复。

checkpoint技术的目的是解决一下几个问题：

    1. 缩短数据库恢复的时间；
        当数据库发生宕机时，不需要重做所有日志，因为checkpoint之前的页都已经刷新到磁盘。故只需对checkpoint后的重做日志进行恢复
    2. 缓冲池不够用时，将脏页刷新到磁盘；
        当缓冲池不够用时，根据LRU算法会溢出最近最少使用的页，若此页为脏页，那么需要强行执行checkpoint，将脏页也就是页的新版本刷回磁盘。
    3. 重做日志不可用时，刷新脏页；
        当前事务数据库系统对重做日志的设计都是循环使用的，并不是无限增大的。

checkpoint种类(2种)

- sharp checkpoint

    sharp checkpoint发生在数据库关闭时，将所有的脏页都刷新回磁盘，这是默认的工作方式`$ show variables like 'innodb_fast_shutdown'\G;`

- fuzzy checkpoint

    fuzzy checkpoint发生情况

    1. Master Thread checkpoint
    2. FLUSH_LRU_LIST checkpoint `$ show variables like 'innodb_lru_scan_depth'\G;` 默认1024
    3. Async/Sync Flush checkpoint 
    4. Dirty Page too much checkpoint `$ show variables like 'innodb_max_dirty_pages_pct'\G;`

## InnoDB 关键特性

- 插入缓冲（Insert Buffer）`$ show variables like 'innodb_change_buffer_max_size'\G;` 25代表1/4。
- 两次写（Double Write）
- 自适应哈希索引（Adaptive Hash Index）
- 异步IO（Async IO）
- 刷新邻接页（Flush Neighbor Page）
