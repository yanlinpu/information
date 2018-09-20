require 'rubygems'
require 'eventmachine'

class Echo < EM::Connection
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

EM.run {
  q = EM::Queue.new

  EM.connect('127.0.0.1', 10000, Echo, q)
  EM.open_keyboard(KeyboardHandler, q)
}