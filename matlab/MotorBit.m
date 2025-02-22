classdef MotorBit
    properties (Constant)
        HEADER_FORMAT = 'uint8';
        LENGTH_FORMAT = 'uint8';
        POSITION_FORMAT = 'uint8 uint64';
        FIXED_LENGTH = 146;
    end
    
    methods (Static)
        function data = fromBaseModel(message)
            if ismember(message.command.command, [1, 2, 3, 4])
                header = uint8(message.command.command);
                data = typecast(header, 'uint8');
                data = [data; zeros(MotorBit.FIXED_LENGTH - length(data), 1, 'uint8')];
            elseif message.command.command == 5 && ~isempty(message.data)
                header = uint8(message.command.command);
                array_length = uint8(length(message.data));
                data = typecast(header, 'uint8');
                data = [data; typecast(array_length, 'uint8')];
                for i = 1:length(message.data)
                    motor_id = uint8(message.data(i).motor_id);
                    position = typecast(double(message.data(i).position), 'uint64');
                    data = [data; typecast(motor_id, 'uint8'); typecast(position, 'uint8')];
                end
                data = [data; zeros(MotorBit.FIXED_LENGTH - length(data), 1, 'uint8')];
            else
                error('Invalid command or missing parameters');
            end
        end
        
        function message = intoBaseModel(data)
            if length(data) ~= MotorBit.FIXED_LENGTH
                error('Message length does not match the fixed length');
            end
            header = typecast(data(1), 'uint8');
            command = bitand(header, 15);
            if ismember(command, [1, 2, 3, 4])
                message = MotorMessage.createMessage(command);
            elseif command == 5
                array_length = typecast(data(2), 'uint8');
                data_array = [];
                for i = 3:9:3 + array_length * 9 - 1
                    motor_id = typecast(data(i), 'uint8');
                    position_bits = typecast(data(i+1:i+8), 'uint64');
                    position = typecast(position_bits, 'double');
                    data_array = [data_array; struct('motor_id', motor_id, 'position', position)];
                end
                message = MotorMessage.createMessage(command, data_array);
            else
                error('Invalid command');
            end
        end
    end
end