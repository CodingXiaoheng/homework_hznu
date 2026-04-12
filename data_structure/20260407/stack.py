# ================= 栈的抽象定义及其顺序与链式实现 =================

class SeqStack:
    """顺序栈的实现"""
    def __init__(self, capacity=10000):
        self.data = [None] * capacity
        self.top = -1
        self.capacity = capacity
        
    def isEmpty(self):
        return self.top == -1
        
    def push(self, x):
        if self.top >= self.capacity - 1:
            raise OverflowError("Stack is full")
        self.top += 1
        self.data[self.top] = x
        
    def pop(self):
        if self.isEmpty():
            raise KeyError("Stack is empty")
        x = self.data[self.top]
        self.top -= 1
        return x
        
    def readtop(self):
        if self.isEmpty():
            raise KeyError("Stack is empty")
        return self.data[self.top]


class LinkNode:
    """链式栈的节点实现"""
    def __init__(self, x, next_=None):
        self._data = x
        self._next = next_


class LinkStack:
    """链式栈的实现"""
    def __init__(self):
        self.Top = None       

    def pop(self):
        if self.isEmpty():
            raise KeyError('stack is empty now')
        x = self.Top._data
        self.Top = self.Top._next
        return x

    def push(self, x):
        tp = LinkNode(x)
        tp._next = self.Top
        self.Top = tp

    def readtop(self):
        if self.isEmpty():
            raise KeyError('stack is empty now')
        return self.Top._data

    def isEmpty(self):
        return self.Top == None
