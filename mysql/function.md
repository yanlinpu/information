## 常用命令
- 查看创建函数功能是否开启

    `SHOW VARIABLES LIKE '%func%';`

- 开启创建函数功能，将variable_name设置为1

    `SET GLOBAL log_bin_trust_function_creators=1;`

- 查看数据库中所有函数

    `SHOW FUNCTION STATUS;`

- 查看具体的函数

    `SHOW CREATE FUNCTION test_func;`

- 删除函数

    `DROP FUNCTION test_func;`

- 创建查询函数

    ```
    DELIMITER $$
    CREATE FUNCTION test_func(param1 VARCHAR(20),param2 INT,param3 CHAR(5))
    RETURNS  INT
    BEGIN
        DECLARE ret_val INT;--定义变量
        SELECT MAX(id) INTO ret_val FROM test;
        RETURN ret_val;
    END$$
    ```

- 执行函数

    `SELECT test_func('var',45,'char');`
use ylp;
show variables like 'log_bin_trust_function_creators';
show variables like '%func%'
# ON--1--开启  OFF--0--关闭
#SET global log_bin_trust_function_creators = 1;
#select * from language_cert_type

show function status

DELIMITER $$
CREATE FUNCTION first_func(param1 varchar(5),parmam2 varchar(5),param3 varchar(10)) 
RETURNS TINYINT 
BEGIN 
   RETURN 1; 
END 
$$

select first_func(1,2,3)



--创建赋值函数
DELIMITER $$
CREATE FUNCTION test_func1(param1 INT,param2 VARCHAR(20))
RETURNS INT
BEGIN
    DECLARE return_val INT;
    DECLARE val INT DEFAULT 2;
    IF val>1 THEN
        SET return_val = val;
    ELSE
        SET return_val = 1;
    END IF;
 RETURN return_val;
END

