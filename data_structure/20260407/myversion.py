import sys
import numpy as np
import matplotlib.pyplot as plt

n = 0

# --- 沿用老师的节点类 ---
class StepNode:
    def __init__(self, currStep, prevStep=None):
        self.currentPoint = currStep
        self.prevPoint = prevStep

# --- 沿用老师的迷宫生成 ---
def generateMaze(n):
    # 生成 n+2 规格的迷宫（含边界）
    M = np.random.random((n+2, n+2))
    M[:, 0] = 1
    M[:, n+1] = 1
    M[0, :] = 1
    M[n+1, :] = 1
    M[M > 0.75] = 1  # 墙壁密度调整为 0.25 左右，增加通路概率
    M[M <= 0.75] = 0
    # 确保起点和终点是通路
    M[1][1] = 0
    M[n][n] = 0
    return M.tolist()

# --- 沿用老师的绘图方式 ---
def show_map(resultMatrix):
    plt.figure(figsize=(10, 10))
    # 使用 jet 映射：0-空地, 1-墙, 2-已遍历, 3-最终路径
    plt.imshow(resultMatrix, cmap=plt.get_cmap('jet'), vmin=0, vmax=3)
    plt.title("DFS Maze Solving (Red=Path, LightBlue=Visited, DarkBlue=Wall)")
    plt.xticks(())
    plt.yticks(())
    plt.show()

# --- 获取相邻节点的逻辑 ---
def getAllNextPoint(M, currentPoint):
    i, j = currentPoint
    result = []
    # 基于迷宫出入口都在对角线上，这是一个简单的启发规则：尽可能沿对角线走
    if i<j:
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    else:
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for di, dj in directions:
        ni, nj = i + di, j + dj
        # 只要是 0 (空地) 就可以走
        if M[ni][nj] == 0:
            result.append((ni, nj))
    return result

# --- 封装我的 DFS 逻辑 ---
class DFSSolver:
    def __init__(self, maze, start, end):
        self.M = maze
        self.start = start
        self.end = end
        self.final_node = None

    def solve(self):
        # 初始化起点
        start_node = StepNode(self.start)
        return self._dfs(start_node)

    def _dfs(self, curr_node):
        # 注：递归调用系统函数实际上隐式地利用了操作系统的函数调用栈。
        # 这里的递归深度优先搜索(DFS)等效于运用明确的栈数据结构进行求解，
        # 保留此原生递归实现可以避免套用抽象数据结构带来的额外封箱解箱开销，保留代码精简原意。
        cp = curr_node.currentPoint
        
        # 1. 标记当前点为已访问 (状态 2)
        self.M[cp[0]][cp[1]] = 2
        
        # 2. 检查是否到达终点
        if cp[0] == self.end[0] and cp[1] == self.end[1]:
            self.final_node = curr_node
            return True
        
        # 3. 递归探索邻居
        next_points = getAllNextPoint(self.M, cp)
        for next_p in next_points:
            next_node = StepNode(next_p, curr_node)
            if self._dfs(next_node):
                return True
        
        return False

def main():
    # 1. 初始化
    n = 20
    maze = generateMaze(n)
    start_point = (1, 1)
    end_point = (n, n)
    
    # 2. 实例化 DFS 求解器并执行
    solver = DFSSolver(maze, start_point, end_point)
    found = solver.solve()
    
    # 3. 结果表达
    if not found:
        print("DFS 未找到可行路径！")
        # 即使没找到，也展示一下遍历过的区域
        show_map(maze)
    else:
        # 回溯路径并标记为 3
        p = solver.final_node
        path_coords = []
        while p is not None:
            path_coords.append(p.currentPoint)
            maze[p.currentPoint[0]][p.currentPoint[1]] = 3
            p = p.prevPoint
        
        # 打印路径坐标（倒序打印，从起点到终点）
        print("找到路径：")
        print(" -> ".join([str(c) for c in path_coords[::-1]]))
        
        # 展示最终地图
        show_map(maze)

if __name__ == "__main__":
    main()