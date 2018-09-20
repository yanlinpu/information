require 'rubygems'
require 'eventmachine'
class EchoServer < EM::Connection
    def receive_data(data)
        p data
        if data.strip =~ /exit$/i
            EM.stop
        else
            send_data(data)
        end
    end
end

EM.run do
    # Control + C to stop
    Signal.trap("INT") {EM.stop}
    Signal.trap("TERM") {EM.stop}

    EM.start_server('0.0.0.0', 10000, EchoServer)
end