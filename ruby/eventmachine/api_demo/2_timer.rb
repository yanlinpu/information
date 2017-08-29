require 'eventmachine'  
EM.run do  
  p = EM::PeriodicTimer.new(1) do  
    puts "Tick ..."  
  end  
  
  EM::Timer.new(5) do  
    puts "BOOM"  
    p.cancel  
  end  
  
  EM::Timer.new(8) do  
    puts "The googles, they do nothing"  
    EM.stop  
  end  
end  

   
=begin 
输出：
Tick...  
Tick...  
Tick...  
Tick...  
BOOM  
The googles, they do nothing  
=end

EM.run do
    EM.add_periodic_timer(1) do # 周期
        p "Tick ..."
    end

    EM.add_timer(3) do # 一次
        p "I waited 3 seconds."
        EM.stop_event_loop
    end
end
# "Tick ..."
# "Tick ..."
# "I waited 3 seconds."