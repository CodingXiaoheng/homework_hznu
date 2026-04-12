import sys

class ListQueue:
    def __init__(self):
        self.data = []
        self.currentLength = 0
    def enqueue(self,x):
        self.data.append(x)
        self.currentLength += 1
    def outqueue(self):
        if self.is_empty():
            return None
        t = self.data.pop(0)
        self.currentLength -= 1
        return t
    def is_empty(self):
        return self.currentLength == 0
    def readhead(self):
        return self.data[0]
    
def show_map(resultMatrix):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(12,12))
    plt.imshow(resultMatrix, cmap=plt.get_cmap('jet'), vmin=0, vmax=3)
    plt.xticks(())
    plt.yticks(())
    plt.show()
    
def generateMaze(n):
    import numpy as np
    M = np.random.random((n+2,n+2))
    M[:,0]=np.ones((n+2))
    M[:,n+1]=np.ones((n+2))
    M[0,:]=np.ones((n+2))
    M[n+1,:]=np.ones((n+2))
    M[M>0.8]=1
    M[M<=0.8]=0
    M=M.tolist()
    return M
class StepNode:
    def __init__(self,currStep,prevStep=None):
        self.currentPoint = currStep
        self.prevPoint = prevStep
def getAllNextPoint(M:list,currentPoin:tuple)->list|None:
    i,j =currentPoin
    result =[]
    if M[i][j+1] == 0:
        result.append((i,j+1))
    if M[i+1][j] == 0:
        result.append( (i+1,j))
    if M[i][j-1] == 0:
        result.append((i,j-1))
    if M[i-1][j] == 0:
        result.append((i-1,j))
    return result
def findWayByQueue():
    # step1 初始化迷宫
    M = generateMaze(20)
    startPoint = (1,1)
    endPoint = (20,20)
    # step2 入口入队
    tempNode = StepNode(startPoint,None)
    q=ListQueue()
    q.enqueue(tempNode)
    i,j = startPoint[0],startPoint[1]
    M[i][j] = 2
    
    # step3 循环至队空
    while not q.is_empty():
        # 取队头，判断是否已是出口
        head_point:StepNode = q.readhead()
        cp = head_point.currentPoint
        if cp[0]==endPoint[0] and cp[1]==endPoint[1]:
            break
        # 将所有下一步入队
        cp_node:StepNode = q.outqueue()
        next_list = getAllNextPoint(M,cp_node.currentPoint)
        for p in next_list:
            tempNode=StepNode(p,cp_node)
            q.enqueue(tempNode)
            i,j = p[0],p[1]
            M[i][j] = 2
    
    # step4 结果表达
    if q.is_empty():
        print("No such way!")
    else:
        p = head_point
        while p is not None:
            i,j = p.currentPoint[0],p.currentPoint[1]
            print(f"({i},{j})<----",end="")
            M[i][j]=3
            p = p.prevPoint
        sys.stdout.flush()
        show_map(M)
    
if __name__ == "__main__":
    findWayByQueue()