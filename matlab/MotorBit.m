classdef MotorBit
    properties (Constant)
        HEADER_FORMAT = 'uint8';
        LENGTH_FORMAT = 'uint8';
        MOTOR_ID_FORMAT = 'uint8';
        INT_FORMAT = 'int32';
        FIXED_LENGTH = 138;
    end
    
    methods (Static)
        function [command, data_len, data] = intoBaseModel(rawData)
            if length(rawData) ~= MotorBit.FIXED_LENGTH
                error('Message length does not match the fixed length');
            end
            
            header = typecast(rawData(1), 'uint8');
            command = bitand(header, 15);
            data_len = 0;
            data = zeros(8, 4);  % motor_id, position, velocity, current

            if ismember(command, [1, 2, 3, 4])
                return;
            end
            
            data_len = typecast(rawData(2), 'uint8');
            if data_len > 8
                error('Data length cannot exceed 8');
            end
            
            for i = 1:data_len
                motor_id = typecast(rawData(3 + (i-1)*13), 'uint8');
                motor_id = double(motor_id);
                
                position = typecast(rawData(4 + (i-1)*13 : 7 + (i-1)*13), 'int32');
                velocity = typecast(rawData(8 + (i-1)*13 : 11 + (i-1)*13), 'int32');
                current = typecast(rawData(12 + (i-1)*13 : 15 + (i-1)*13), 'int32');
                
                data(i, :) = [motor_id, position, velocity, current];
            end
        end

        function rawData = fromBaseModel(command, data)
            if ~ismember(command, [1, 2, 3, 4, 5, 6, 7, 8])
                error('Invalid command');
            end
            
            rawData = zeros(1, MotorBit.FIXED_LENGTH, 'uint8');
            rawData(1) = command;
            
            if ismember(command, [1, 2, 3, 4])
                return;
            end
            
            data_len = size(data, 1);
            if data_len > 8
                error('Data length cannot exceed 8');
            end
            
            rawData(2) = data_len;
            
            for i = 1:data_len
                rawData(3 + (i-1)*13) = data(i, 1);  % motor_id
                rawData(4 + (i-1)*13 : 7 + (i-1)*13) = typecast(int32(data(i, 2)), 'uint8');  % position
                rawData(8 + (i-1)*13 : 11 + (i-1)*13) = typecast(int32(data(i, 3)), 'uint8');  % velocity
                rawData(12 + (i-1)*13 : 15 + (i-1)*13) = typecast(int32(data(i, 4)), 'uint8');  % current
            end
        end
    end
end