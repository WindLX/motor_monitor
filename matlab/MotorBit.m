classdef MotorBit
    properties (Constant)
        HEADER_FORMAT = 'uint8';
        LENGTH_FORMAT = 'uint8';
        POSITION_FORMAT = 'uint8 uint64';
        FIXED_LENGTH = 146;
    end
    
    methods (Static)
        function [command, data_len, data] = intoBaseModel(rawData)
            command = uint8(1);
            data_len = uint8(0);
            data = zeros(16, 2);

            if length(rawData) ~= MotorBit.FIXED_LENGTH
                error('Message length does not match the fixed length');
            end    
            header = typecast(rawData(1), 'uint8');
            command = bitand(header, 15);

            if ismember(command, [1, 2, 3, 4])
                data = zeros(16, 2);
            elseif command == 5
                data_len = typecast(rawData(2), 'uint8');
                for i = 1:data_len
                    motor_id = typecast(rawData(3 + (i-1)*9), 'uint8');
                    motor_id = double(motor_id);
                    position_bit = rawData(4 + (i-1)*9 : 11 + (i-1)*9);
                    position = swapbytes(typecast(position_bit, 'uint64'));
                    position = typecast(position, 'double');
                    data(i, :) = [motor_id, position];
                end
            else
                error('Invalid command');
            end
        end
    end
end