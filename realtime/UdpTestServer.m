% Import the MotorBit class
import MotorBit;

% Create a UDP server
udpServer = udpport("LocalPort", 9999);

disp('UDP server is running...');

while true
    % Wait for data
    data = read(udpServer, 1024, "uint8");
    
    if ~isempty(data)
        try
            % Parse the received data using MotorBit
            message = MotorBit.into_base_model(data);
            
            % Display the parsed message
            disp('Received message:');
            disp(message);
        catch ME
            disp('Failed to parse message:');
            disp(ME.message);
        end
    end
end