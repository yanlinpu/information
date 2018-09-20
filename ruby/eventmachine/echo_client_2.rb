require 'rubygems'
require 'eventmachine'

class Echo < EventMachine::Connection
  def initialize(*args)
    super
    send_data 'Hello'
    # stuff here...
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

EventMachine.run {
  EventMachine.connect '127.0.0.1', 10000, Echo
}