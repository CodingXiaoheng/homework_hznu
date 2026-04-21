class SimplePQ:
    """
    默认值越小优先级越高
    """
    def __init__(self, key=lambda x:x, reverse=False):
        self.data = []
        self.currentLength = 0
        self.key = key
        self.reverse = reverse
    def is_empty(self):
        return self.currentLength == 0
    def size(self):
        return self.currentLength
    def insert(self, x):
        self.data.append(x)
        self.currentLength += 1
    def pop(self):
        if self.is_empty():
            return None
        self.data.sort(key=self.key, reverse=not self.reverse)
        self.currentLength -= 1
        return self.data.pop(-1)
    def get(self):
        if self.is_empty():
            return None
        self.data.sort(key=self.key, reverse=not self.reverse)
        return self.data[-1]
    def print_queue(self):
        print(self.data)
        return

class HeapPQ:
    """
    默认值越小优先级越高
    """
    def __init__(self, key=lambda x:x, reverse=False):
        self.data = []
        self.currentLength = 0
        self.key = key
        self.reverse = reverse
    def is_empty(self):
        return self.currentLength == 0
    def size(self):
        return self.currentLength
    def insert(self, x):
        self.data.append(x)
        self.__shift_up(self.currentLength)
        self.currentLength += 1
    def __shift_up(self, k):
        """
        0-based索引
        """
        if k == 0:
            return
        parent = (k-1)//2
        if self.reverse:
            if self.key(self.data[k]) > self.key(self.data[parent]):
                self.data[k], self.data[parent] = self.data[parent], self.data[k]
                self.__shift_up(parent)
        else:
            if self.key(self.data[k]) < self.key(self.data[parent]):
                self.data[k], self.data[parent] = self.data[parent], self.data[k]
                self.__shift_up(parent)
    def __shift_down(self, k):
        """
        0-based索引
        """
        left = 2*k+1
        right = 2*k+2
        if left >= self.currentLength:
            return
        if self.reverse:
            target = left if right >= self.currentLength or self.key(self.data[left]) > self.key(self.data[right]) else right
            if self.key(self.data[target]) > self.key(self.data[k]):
                self.data[k], self.data[target] = self.data[target], self.data[k]
                self.__shift_down(target)
        else:
            target = left if right >= self.currentLength or self.key(self.data[left]) < self.key(self.data[right]) else right
            if self.key(self.data[target]) < self.key(self.data[k]):
                self.data[k], self.data[target] = self.data[target], self.data[k]
                self.__shift_down(target)
    def pop(self):
        if self.is_empty():
            return None
        self.data[0], self.data[-1] = self.data[-1], self.data[0]
        t = self.data.pop(-1)
        self.currentLength -= 1
        self.__shift_down(0)
        return t
    def get(self):
        if self.is_empty():
            return None
        return self.data[0]
    def print_heap(self):
        print(self.data)
        return

class TestUnit:
    import random
    import time
    def test_pq(self, pq, n, data_generator=None, print_result=True):
        random = self.random
        time = self.time

        # 生成测试数据
        if data_generator is None:
            data_generator = lambda:random.randint(0,65535)
        test_data = [data_generator() for _ in range(n)]
        
        # 测试插入性能
        start_time = time.perf_counter()
        for x in test_data:
            pq.insert(x)
        insert_time = time.perf_counter() - start_time
        
        # 测试弹出性能与正确性
        results = []
        start_time = time.perf_counter()
        while not pq.is_empty():
            results.append(pq.pop())
        pop_time = time.perf_counter() - start_time
        
        # 验证排序正确性
        is_sorted = all(results[i] <= results[i+1] for i in range(len(results)-1))
        if pq.reverse:
            is_sorted = all(results[i] >= results[i+1] for i in range(len(results)-1))
            
        if print_result:
            print(f"PQ Type: {type(pq).__name__}")
            print(f"Insert Time: {insert_time:.6f}s, Pop Time: {pop_time:.6f}s")
            print(f"Correctness (Sorted): {is_sorted}")
            
        return insert_time, pop_time, is_sorted

if __name__ == "__main__":
    heapPQ = HeapPQ()
    simplePQ = SimplePQ()
    for i in [15, 10, 20, 8, 12, 18, 25]:
        heapPQ.insert(i)
        simplePQ.insert(i)
    heapPQ.print_heap()
    simplePQ.print_queue()
    print(heapPQ.pop())
    print(simplePQ.pop())
    heapPQ.print_heap()
    simplePQ.print_queue()
    for i in [30,5]:
        heapPQ.insert(i)
        simplePQ.insert(i)
    heapPQ.print_heap()
    simplePQ.print_queue()
    while not heapPQ.is_empty():
        print(heapPQ.pop())
    print(heapPQ.pop())
    while not simplePQ.is_empty():
        print(simplePQ.pop())
    print(simplePQ.pop())

    # 测试
    tester = TestUnit()
    n = 1000
    print(f"Testing with {n} elements...")
    tester.test_pq(SimplePQ(reverse=True), n, print_result=True)
    tester.test_pq(HeapPQ(reverse=True), n, print_result=True)
    for n in [5000, 10000]:
        print(f"Testing with {n} elements...")
        tester.test_pq(SimplePQ(reverse=False), n, print_result=True)
        tester.test_pq(HeapPQ(reverse=False), n, print_result=True)
    
