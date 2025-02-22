classdef DummyServer < handle
    properties
        udpSocket
        bufferSize = 1024;
    end
    
    methods
        function obj = DummyServer(port)
            obj.udpSocket = udp('0.0.0.0', 'LocalPort', port, 'InputBufferSize', obj.bufferSize);
            obj.udpSocket.DatagramReceivedFcn = @(src, event) obj.datagramReceived(src, event);
            fopen(obj.udpSocket);
            fprintf('UDP Server started on port %d\n', port);
        end
        
        function datagramReceived(obj, src, ~)
            data = fread(src, src.BytesAvailable);
            fprintf('Received %s from %s:%d\n', char(data'), src.DatagramAddress, src.DatagramPort);
            fwrite(src, 'ACK');
        end
        
        function delete(obj)
            fclose(obj.udpSocket);
            delete(obj.udpSocket);
            fprintf('UDP Server closed\n');
        end
    end
end

% Usage
server = DummyServer(12345);
pause(3600); % Run for 1 hour
delete(server);