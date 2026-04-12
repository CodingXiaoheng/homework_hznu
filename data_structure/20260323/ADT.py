from abc import ABC, abstractmethod
import time
import random

# ==========================================
# 1. 线性表 ADT 抽象基类
# ==========================================
class LinearList(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def insert(self, index, val):
        pass

    @abstractmethod
    def delete(self, index):
        pass

    @abstractmethod
    def search(self, val):
        pass

    @abstractmethod
    def __len__(self):
        pass

# ==========================================
# 2. 顺序表 (基于 Python list)
# ==========================================
class SequentialList(LinearList):
    def __init__(self):
        self._data = []

    def insert(self, index, val):
        self._data.insert(index, val)

    def delete(self, index):
        if 0 <= index < len(self._data):
            return self._data.pop(index)
        raise IndexError("Index out of bounds")

    def search(self, val):
        try:
            return self._data.index(val)
        except ValueError:
            return -1

    def __len__(self):
        return len(self._data)

    def append(self, val):
        self._data.append(val)

    def sort(self):
        self._data = self._merge_sort(self._data)

    def _merge_sort(self, arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = self._merge_sort(arr[:mid])
        right = self._merge_sort(arr[mid:])
        return self._merge(left, right)

    def _merge(self, left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

# ==========================================
# 3. 双向链表及节点定义
# ==========================================
class Node:
    def __init__(self, val=0):
        self.val = val
        self.prev = None
        self.next = None

class LinkedList(LinearList):
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def append(self, val):
        new_node = Node(val)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self._size += 1

    # --- 遍历类基本操作 ---
    def insert(self, index, val):
        if index < 0 or index > self._size:
            raise IndexError("Index out of bounds")

        if index == self._size:
            self.append(val)
            return

        new_node = Node(val)

        if index == 0:
            # 头部插入
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        else:
            # 中间插入：找到 index 处的节点，在其前插入
            curr = self.head
            for _ in range(index):
                curr = curr.next
            # 内联 insert_before 逻辑，不调用会修改 _size 的方法
            new_node.prev = curr.prev
            new_node.next = curr
            curr.prev.next = new_node
            curr.prev = new_node

        # 头部和中间插入都在这里统一计数一次
        self._size += 1

    def delete(self, index):
        if index < 0 or index >= self._size:
            raise IndexError("Index out of bounds")
        curr = self.head
        for _ in range(index):
            curr = curr.next
        return self.delete_node(curr)

    def search(self, val):
        """返回第一个值为 val 的节点引用，找不到返回 None"""
        curr = self.head
        while curr:
            if curr.val == val:
                return curr
            curr = curr.next
        return None

    # --- 非遍历的增删方法 O(1) ---
    def insert_after(self, node, val):
        """在给定节点之后插入新节点"""
        if not node:
            return
        new_node = Node(val)
        new_node.next = node.next
        new_node.prev = node
        if node.next:
            node.next.prev = new_node
        else:
            self.tail = new_node
        node.next = new_node
        self._size += 1
        return new_node

    def insert_before(self, node, val):
        """在给定节点之前插入新节点"""
        if not node:
            return
        new_node = Node(val)
        new_node.prev = node.prev
        new_node.next = node
        if node.prev:
            node.prev.next = new_node
        else:
            self.head = new_node
        node.prev = new_node
        self._size += 1
        return new_node

    def delete_node(self, node):
        """直接删除给定的节点"""
        if not node:
            return None
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        self._size -= 1
        val = node.val
        node.prev = node.next = None
        del node
        return val

    # --- 链表的归并排序 (指针重排) ---
    def sort(self):
        if not self.head or not self.head.next:
            return
        self.head = self._merge_sort(self.head)
        self.head.prev = None
        curr = self.head
        while curr and curr.next:
            curr = curr.next
        self.tail = curr

    def _get_mid(self, head):
        slow = head
        fast = head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow

    def _merge_sort(self, head):
        if not head or not head.next:
            return head
        mid_node = self._get_mid(head)
        right_head = mid_node.next
        mid_node.next = None
        if right_head:
            right_head.prev = None
        left_sorted = self._merge_sort(head)
        right_sorted = self._merge_sort(right_head)
        return self._merge(left_sorted, right_sorted)

    def _merge(self, left, right):
        dummy = Node(0)
        curr = dummy
        while left and right:
            if left.val <= right.val:
                curr.next = left
                left.prev = curr
                left = left.next
            else:
                curr.next = right
                right.prev = curr
                right = right.next
            curr = curr.next
        if left:
            curr.next = left
            left.prev = curr
        if right:
            curr.next = right
            right.prev = curr
        new_head = dummy.next
        if new_head:
            new_head.prev = None
        return new_head

# ==========================================
# 4. 性能测试与分析
# ==========================================
def benchmark_sorting():
    DATA_SIZE = 1000000
    print(f"正在生成 {DATA_SIZE} 个随机整数...")
    raw_data = [random.randint(0, 1000000) for _ in range(DATA_SIZE)]

    seq_list = SequentialList()
    linked_list = LinkedList()

    print("正在加载数据到数据结构中...")
    for val in raw_data:
        seq_list.append(val)
        linked_list.append(val)

    print("-" * 30)

    start_time = time.time()
    seq_list.sort()
    seq_time = time.time() - start_time
    print(f"顺序表 (SequentialList) 手工归并排序耗时: {seq_time:.4f} 秒")

    start_time = time.time()
    linked_list.sort()
    link_time = time.time() - start_time
    print(f"双向链表 (LinkedList) 归并排序耗时: {link_time:.4f} 秒")

    print("-" * 30)
    print("排序正确性检查: ", end="")
    is_correct = True
    curr = linked_list.head
    for i in range(len(seq_list)):
        if seq_list._data[i] != curr.val:
            is_correct = False
            break
        # print(curr.val)
        curr = curr.next
    print("通过" if is_correct else "失败")
    ## Debug代码
    # curr = linked_list.head
    # while curr:
    #     print(curr.val, end=" ")
    #     curr = curr.next
    # print()

if __name__ == "__main__":
    benchmark_sorting()