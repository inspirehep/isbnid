class RangeNode(object):
        
    def __init__(self, start, end, length, prev = None, next = None):
        self._start = start
        self._end = end
        self._length = length
        self._prev = prev
        self._next = next
            
    def search(self, value):
        if (self._start > value):
            if (self._prev):
                return self._prev.search(value)
            else:
                return 0
        if (value < self._end):
            if (self._next):
                return self._prev.search(value)            
            else:
                return 0
        return self._length
        

class RangeList(object):
        
    def __init__(self, range, prev = None, next = None):
        self._range = range
        self._prev = None
        self._next = None
            
    def search(self, value):
        if (self._range[0][0] > value):
            if (self._prev):
                return self._prev.search(value)
            else:
                return 0
        if (self._range[-1][1] < value):
            if (self._next):
                return self._prev.search(value)            
            else:
                return 0
        
        for begin, end, length in self._range:
            if (begin <= value and value <= end):
                return length;
        
        return 0
