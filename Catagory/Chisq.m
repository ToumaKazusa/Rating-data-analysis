function [ Chi_square, data ] = Chisq(x, y)
%CHISQ Summary of this function goes here
%   Detailed explanation goes here

[m, n] = size(x);
Chi_square = zeros(1, n);

for i = 1:n;
    a = 0;
    b = 0;
    c = 0;
    d = 0;
    for j = 1:m;
        if y(j) == 1
            if x(j, i) >= 1
                a = a + 1;
            else
                c = c + 1;
            end
        else
            if x(j, i) >= 1
                b = b + 1;
            else
                d = d + 1;
            end
        end
    end
    if a+b == 0
        disp('error1!')
    end
    if c+d == 0
        disp('error2!')
    end
    Chi_square(i) = sqrt((a*d - b*c)^2/((a+b)*(c+d)));
end

C1 = Chi_square;
[value, pos] = max(C1); 
data = [x(:, pos)];
C1(pos) = 0;
for i = 1:99
   [value, pos] = max(C1);
   data = [data, x(:, pos)];
   C1(pos) = 0;              
end

