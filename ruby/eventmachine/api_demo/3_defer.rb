require 'eventmachine'  
require 'thread'  
  
## 推迟和并发处理
EM.run do  
    EM.add_timer(2) do  
        puts "Main #{Thread.current}"  
        EM.stop_event_loop  
    end  
    EM.defer do  
        puts "Defer #{Thread.current}"  
    end  
end 
=begin
Defer #<Thread:0x7fa871e33e08>   
#两秒后  
Main #<Thread:0x7fa87449b370>  
=end

## defer+callback
EM.run do  
    op = proc do  
        2+2  
    end  
    callback = proc do |count|  
        puts "2 + 2 == #{count}"  
        EM.stop  
    end  
    EM.defer(op, callback)  
end  
    
# the return value of op is passed to callback  
# 2 + 2 == 4  

## defer#next_tick
EM.run do    
    EM.add_periodic_timer(1) do    
      puts "Hai"    
    end   
     
    EM.add_timer(5) do    
        EM.next_tick do    
            EM.stop_event_loop    
        end    
    end    
end   
=begin
负责将一个代码块调度到Reactor的下一次迭代中执行，执行任务的是Reactor主线程。
所以，next_tick部分的代码不会立刻执行到，具体的调度是由EM完成的。

这里Reactor执行的过程用是同步的，所以太长的Reactor任务会长时间阻塞Reactor进程。
EventMachine中有一个最基本原则我们必须记住：Never block the Reactor!

next_tick的一个很常见的用法是递归的调用方式，将一个长的任务分配到Reactor的不同迭代周期去执行。
=end

EM.run do  
    n = 0    
    do_work = proc{    
        if n < 100   
            sleep 1 
            puts n 
            n += 1   
            EM.next_tick(do_work)  
        else  
            EM.stop  
        end  
    }  
    EM.next_tick(do_work)    
end 
