require 'rubygems'  
require 'eventmachine'  
  
=begin
post_init   当实例创建好，连接还没有完全建立的时候调用。一般用来做初始化
connection_completed   连接完全建立好的时候调用
receive_data(data)   当收到另一端的数据时调用。数据是成块接收的
unbind   当客户端断开连接的时候调用
此外，还有#close_connection#close_connection_after_writing这两个方法供用户断开连接。
=end
## Client example1 
class EchoClient < EventMachine::Connection
    def initialize(*args)
        super
        @hello = args.first || 'Hello'
        # stuff here...
    end

    def post_init
        send_data(@hello)
    end
     
    def receive_data(data)
        p 'receive_data'
        p data
        send_data data
        close_connection_after_writing 
    end
  
    def unbind
        p ' connection totally closed'
    end
end
  
=begin
EventMachine.run {
    EventMachine.connect '127.0.0.1', 10000, EchoClient
}
=end

## Client example2
class EchoClient2 < EM::Connection
    attr_reader :queue

    def initialize(q)
        @queue = q
        cb = Proc.new do |msg|
            p msg
            send_data(msg)
            q.pop &cb
        end
        q.pop &cb
    end
  
    def post_init
        send_data('Hello')
    end
  
    def receive_data(data)
        p 'receive_data'
        p data
    end
end
  
class KeyboardHandler < EM::Connection
    include EM::Protocols::LineText2
    attr_reader :queue
  
    def initialize(q)
        @queue = q
    end
  
    def receive_line(data)
        @queue.push(data)
        p @queue
    end
end