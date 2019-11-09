function [m,s] = stat(x,...
                    y,...
                    z)
    n = length(x);
    m = sum(x)/n;
    s = sqrt(sum((x-m).^2/n));
end