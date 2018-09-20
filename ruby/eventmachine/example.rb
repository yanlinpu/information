require 'rubygems'
require 'eventmachine'
require 'em-http'
require 'json'
=begin
post_init　handler对象创建后，注意client模式时，即使连接还未建立也会被调用
connection_completed　主动连接远端服务器，连接建立时
receive_data　有数据可读时, 在这里需要处理协议细节
unbind　连接关闭，主动关闭，对方关闭或网络错误
=end
## Timer Example

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


## Server Example

module Server
    def receive_data(data)
        puts data
        send_data(data)
    end
end
# EM.run {EM.start_server 'localhost', 8080, Server}


## Server Example2
class EchoServer < EM::Connection
    attr_accessor :option, :status

    def receive_data(data)
        p "#{@status} -- #{data}"
        send_data(data)
    end
end

=begin
EM.run do
    EM.start_server 'localhost', 8080, EchoServer do |conn|
        conn.option = {:my => 'options'}
        conn.status = :OK
    end
end
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

=begin
EM.run {
    q = EM::Queue.new
    EM.connect('127.0.0.1', 8080, EchoClient2, q)
    EM.open_keyboard(KeyboardHandler, q)
}
=end

## chat Example

module Chat
     # Called after the connection with a client has been established
    def post_init      
        # Add ourselves to the list of clients
        (@@connections ||= []) << self  
        p @@connections
        send_data "Please enter your name: "
    end 
   
    # Called on new incoming data from the client
    def receive_data data
        # The first message from the user is its name
        @name ||= data.strip

        @@connections.each do |client|
            # Send the message from the client to all other clients
            client.send_data "#{@name} says: #{data}"
        end
    end
end
=begin 
# Start a server on localhost, using port 8081 and hosting our Chat application
EventMachine::run doß
    EventMachine::start_server "localhost", 8081, Chat
end 
=end

## EM::Deferrable && em-http Example
class LanguageDetector
    URL = "http://www.google.com/uds/GlangDetect"
  
    include EM::Deferrable
  
    def initialize(text)
        request = EM::HttpRequest.new(URL).get({
            :query => {:v => "1.0", :q => text}
        })
        # http = EventMachine::HttpRequest.new('http://stream.twitter.com/1/statuses/filter.json').post({
        #     :head => { 'Authorization' => [username, password] },
        #     :query => { "track" => "newtwitter" }
        # })
        # This is called if the request completes successfully (whatever the code)
        request.callback {
            if request.response_header.status == 200
                info = JSON.parse(request.response)["responseData"]
                if info['isReliable']
                    self.succeed(info['language'])
                else
                    self.fail("Language could not be reliably determined")
                end
            else
                self.fail("Call to fetch language failed")
            end
        }
  
        # This is called if the request totally failed
        request.errback {
            self.fail("Error making API call")
        }
    end
end
  
EM.run {
    detector = LanguageDetector.new("Sgwn i os yw google yn deall Cymraeg?")
    detector.callback { |lang| puts "The language was #{lang}" }
    detector.errback { |error| puts "Error: #{error}" }
}