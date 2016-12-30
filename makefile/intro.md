## vim编写Makefile http://www.ruanyifeng.com/blog/2015/02/make.html

- vim 编写makefile设置 makefile:2: *** missing separator.  Stop. 

  1. 文件名叫Makefile        http://bigwhite.blogbus.com/logs/74509182.html
  2. `:set noexpandtab`  
  3. ctrl-v -> tab          http://blog.csdn.net/happen23/article/details/50680282
  4. `.RECIPEPREFIX = >`  .RECIPEPREFIX指定，大于号（>）替代tab键

- makefile格式
  ```
  <target> : <prerequisites> 
  [tab]  <commands>
  ```
  1. 目标target
    ```
    # Makefile
    clean:
      rm -rf *.o
    
    $ make clean
    # => rm -rf *.o
    # 如果存在clean文件 则不执行rm， 需要用到伪目标 .PHONY
  
    .PHONY: clean
    clean:
      rm -rf *.o temp
    ```
  
  2. 前置条件（prerequisites）  
  
    前置条件通常是一组文件名，之间用空格分隔。它指定了"目标"是否重新构建的判断标准：
    只要有一个前置文件不存在，或者有过更新（前置文件的last-modification时间戳比目标的时间戳新），"目标"就需要重新构建。
    
    ```
    .PHONY: result.txt
    result.txt: source.txt
      cp source.txt result.txt
    source.txt:
      echo "this is the source" > source.txt
    ```
    
  3. 命令（commands）
  
    ```
    var-lost:
      export foo=bar
      echo "foo=[$$foo]"
     
    # 取不到foo的值 因为两行命令在两个不同的进程执行。
    # 一个解决办法是将两行命令写在一行，中间用分号分隔。
    var-kept:
      export foo=bar; echo "foo=[$$foo]"
    # 另一个解决办法是在换行符前加反斜杠转义
    var-kept:
      export foo=bar; \
      echo "foo=[$$foo]"
    ```
    
  4. 其他
    
    1. 关闭回声（echoing）
    
      由于在构建过程中，需要了解当前在执行哪条命令，所以通常只在注释和纯显示的echo命令前面加上@。
      
      ```
        test:
          @# 这是测试
          @echo TODO
      ```
    2. 变量和赋值符
      
      ```
        txt = Hello World
        test:
          @echo $(txt)
          # 调用Shell变量，需要在美元符号前，再加一个美元符号，这是因为Make命令会对美元符号转义。
          @echo $$HOME
      ```
    3. 自动变量（Automatic Variables）
    
      - $@
      
        $@指代当前目标  
        
        ```
        a.txt b.txt: 
          touch $@
        # =============
        a.txt:
          touch a.txt
        b.txt:
          touch b.txt
        ```
      - $<
      
        $< 指代第一个前置条件
        
      - $?
      
        指代比目标更新的所有前置条件，之间以空格分隔
        
      - $^
      
        所有前置条件
        
      - $*
      
        指代匹配符 % 匹配的部分， 比如% 匹配 f1.txt 中的f1 ，$* 就表示 f1
        
      - $(@D) 和 $(@F)
        
        $(@D) 和 $(@F) 分别指向 $@ 的目录名和文件名。比如，$@是 src/input.c，那么$(@D) 的值为 src ，$(@F) 的值为 input.c。
        
      - $(<D) 和 $(<F)
      
        $(<D) 和 $(<F) 分别指向 $< 的目录名和文件名。
   
    4. 判断和循环
    
      ```
      # 判断当前编译器是否 gcc
      ifeq ($(CC),gcc)
        libs=$(libs_for_gcc)
      else
        libs=$(normal_libs)
      endif
      # for each
      LIST = one two three
      all:
        for i in $(LIST); do \
          echo $$i; \
        done
      ```
      
    5. 函数
    
      ```
      $(function arguments)
      # 或者
      ${function arguments}
      ```
