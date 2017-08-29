require 'rubygems'  
require 'eventmachine'  
  
## class
class Echo < EM::Connection    
    def receive_data(data)    
        send_data(data)    
    end    
end  
   
EM.run do    
    EM.start_server("0.0.0.0", 10000, Echo)    
end 

## module
module Echo1  
    def receive_data(data)  
        send_data(data)  
    end  
end  
=begin  
EM.run do  
    EM.start_server("0.0.0.0", 10000, Echo1)  
end 
=end

## block
=begin
EM.run do  
    EM.start_server("0.0.0.0", 10000) do |srv|  
        def srv.receive_data(data)  
            send_data(data)  
        end  
    end  
end 
=end

## 同的连接互相交换信息
class Pass < EM::Connection  
    attr_accessor :a, :b  
    def receive_data(data)  
        send_data "#{@a} #{data.chomp} #{b}"  
    end  
end  

=begin
EM.run do  
    EM.start_server("127.0.0.1", 10000, Pass) do |conn|  
        conn.a = "Goodbye"  
        conn.b = "world"  
    end  
end  
=end

