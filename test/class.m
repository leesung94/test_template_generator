classdef BasicClass
   properties
      Value {mustBeNumeric}
   end
   methods
      function rone = roundOff(obj)
         r = round([obj.Value],2);
      end
      function rtwo = multiplyBy(obj,n)
         r = [obj.Value] * n;
      end
   end
end