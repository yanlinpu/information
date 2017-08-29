## EM提供的轻量级的并发机制
require 'eventmachine'  

# EvenMachine内置了两钟轻量级的并发处理机制：Deferrables和SpawnedProcesses。

=begin
1.EM::Deferrable
如果在一个类中include了EM::Deferrable，就可以把Callback和Errback关联到这个类的实例。
一旦执行条件被触发，Callback和Errback会按照与实例关联的顺序执行起来。
对应实例的#set_deferred_status方法就用来负责触发机制：
当该方法的参数是:succeeded，则触发callbacks；而如果参数是:failed，则触发errbacks。
触发之后，这些回调将会在主线程立即得到执行。当然你还可以在回调中(callbacks和errbacks)再次调用#set_deferred_status，改变状态。
=end
class MyDeferrable  
    include EM::Deferrable  
    def go(str)  
        puts "Go #{str} go"  
    end  
end  

EM.run do  
    df = MyDeferrable.new  

    df.callback do |x|  
        df.go(x)  
        df.set_deferred_status :failed, "FAILED"  
    end  

    df.errback do |x|
        df.go(x)
        EM.stop
    end

    EM.add_timer(1) do  
        df.set_deferred_status :succeeded, "SpeedRacer"  
    end  
    EM.add_timer(1) do  
        p 'ADDTIMER1'
    end
    EM.add_timer(0.5) do  
        p 'ADDTIMER0.5'
    end
end 


=begin
2.EM::SpawnedProcess
允许我们创建一个进程，把一个代码段绑定到这个进程上。然后我们就可以在某个时刻，让spawned实例被#notify方法触发，从而执行关联好的代码段。
它与Deferrable的不同之处就在于，这个block并不会立刻被执行到。
=end

EM.run do  
    s = EM.spawn do |val|  
        puts "Received #{val}"  
    end  
    
    EM.add_timer(1) do  
        s.notify "hello"  
    end  
    
    EM.add_periodic_timer(1) do  
        puts "Periodic"  
    end  
    
    EM.add_timer(5) do  
        EM.stop  
    end  
end