# explain extended ... && show warnings

使用explain extended， 然后使用 show warnings命令去获得查询执行计划及实际运行方式（查看查询是如何优化与执行的）。

```
workflow_registerguide 实际存储为guide_id
$ explain extended select count(1) from user_guide where user_id in (
	select user_id from workflow_registerguide where gui_name = '张婵真'
)
$ show warnings

'Note', '1276', 'Field or reference \'tourguide.user_guide.user_id\' of SELECT #2 was resolved in SELECT #1'
'Note', '1003', 'select count(1) AS `count(1)` from `tourguide`.`user_guide` semi join (`tourguide`.`workflow_registerguide`) where (`tourguide`.`workflow_registerguide`.`gui_name` = \'张婵真\')'
```


