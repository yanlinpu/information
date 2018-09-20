require 'rubygems'
require 'eventmachine'

class Echo < EventMachine::Connection
  def post_init
    send_data 'Hello'
  end

  def receive_data(data)
    p 'receive_data'
    p data
  end
end

EventMachine.run {
  EventMachine::connect '0.0.0.0', 10000, Echo
}