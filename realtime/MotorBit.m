classdef MotorBit
    properties (Constant)
        HEADER_FORMAT = 'uint8,uint16'; % 1 byte for header, 2 bytes for length
        POSITION_FORMAT = 'uint8,uint64'; % 1 byte for motor id, 8 bytes for position (double)
    end
    
    methods (Static)
        function bytes = from_base_model(command, data)
            if ismember(command, [1, 2, 3, 4])
                header = bitor(bitshift(1, 4), command);
                length = 3; % 1 byte for header + 2 bytes for length
                bytes = typecast(uint8([header, typecast(uint16(length), 'uint8')]), 'uint8');
            elseif command == 5 && ~isempty(data)
                header = bitor(bitshift(2, 4), command);
                data_bytes = [];
                for i = 1:length(data)
                    motor_id = data(i).motor_id;
                    position = data(i).position;
                    position_bits = typecast(double(position), 'uint64');
                    data_bytes = [data_bytes; typecast(uint8([motor_id, typecast(position_bits, 'uint8')]), 'uint8')];
                end
                length = 3 + length(data_bytes); % 1 byte for header + 2 bytes for length + data length
                bytes = [typecast(uint8([header, typecast(uint16(length), 'uint8')]), 'uint8'); data_bytes];
            else
                error('Invalid command or missing parameters');
            end
        end
        
        function message = into_base_model(bytes)
            header = bytes(1);
            length = typecast(bytes(2:3), 'uint16');
            if length ~= length(bytes)
                error('Message length does not match the length specified in the header');
            end
            command = bitand(header, 15);
            if ismember(command, [1, 2, 3, 4])
                message.command = command;
                message.data = [];
            elseif command == 5
                data = [];
                for i = 4:9:length(bytes)
                    motor_id = bytes(i);
                    position_bits = typecast(bytes(i+1:i+8), 'uint64');
                    position = typecast(position_bits, 'double');
                    data = [data; struct('motor_id', motor_id, 'position', position)];
                end
                message.command = command;
                message.data = data;
            else
                error('Invalid command');
            end
        end
    end
end