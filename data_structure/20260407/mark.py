import time
import copy
import numpy as np

# ================= 共享的基础类和生成函数 =================

class ListQueue:
    def __init__(self):
        self.data = []
        self.currentLength = 0
    def enqueue(self, x):
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

class StepNode:
    def __init__(self, currStep, prevStep=None):
        self.currentPoint = currStep
        self.prevPoint = prevStep

def generateMaze(n):
    # 使用版本2的迷宫生成（包含起点终点保底机制，路障密度较合理）
    M = np.random.random((n+2, n+2))
    M[:, 0] = 1
    M[:, n+1] = 1
    M[0, :] = 1
    M[n+1, :] = 1
    M[M > 0.75] = 1  
    M[M <= 0.75] = 0
    M[1][1] = 0
    M[n][n] = 0
    return M.tolist()


# ================= 版本 1: 队列/广度优先搜索 (BFS) =================

def getAllNextPoint_BFS(M, currentPoin):
    i, j = currentPoin
    result = []
    if M[i][j+1] == 0:
        result.append((i, j+1))
    if M[i+1][j] == 0:
        result.append((i+1, j))
    if M[i][j-1] == 0:
        result.append((i, j-1))
    if M[i-1][j] == 0:
        result.append((i-1, j))
    return result

def solve_by_bfs(M, startPoint, endPoint):
    tempNode = StepNode(startPoint, None)
    q = ListQueue()
    q.enqueue(tempNode)
    i, j = startPoint[0], startPoint[1]
    M[i][j] = 2
    
    found = False
    while not q.is_empty():
        head_point = q.readhead()
        cp = head_point.currentPoint
        if cp[0] == endPoint[0] and cp[1] == endPoint[1]:
            found = True
            break
        
        cp_node = q.outqueue()
        next_list = getAllNextPoint_BFS(M, cp_node.currentPoint)
        for p in next_list:
            tempNode = StepNode(p, cp_node)
            q.enqueue(tempNode)
            i, j = p[0], p[1]
            M[i][j] = 2
            
    return found


# ================= 版本 2: 递归/深度优先搜索 (DFS) =================

def getAllNextPoint_DFS(M, currentPoint):
    i, j = currentPoint
    result = []
    if i < j:
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    else:
        directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
    for di, dj in directions:
        ni, nj = i + di, j + dj
        if M[ni][nj] == 0:
            result.append((ni, nj))
    return result

class DFSSolver:
    def __init__(self, maze, start, end):
        self.M = maze
        self.start = start
        self.end = end
        self.final_node = None

    def solve(self):
        start_node = StepNode(self.start)
        return self._dfs(start_node)

    def _dfs(self, curr_node):
        cp = curr_node.currentPoint
        self.M[cp[0]][cp[1]] = 2
        
        if cp[0] == self.end[0] and cp[1] == self.end[1]:
            self.final_node = curr_node
            return True
        
        next_points = getAllNextPoint_DFS(self.M, cp)
        for next_p in next_points:
            next_node = StepNode(next_p, curr_node)
            if self._dfs(next_node):
                return True
        return False


# ================= 性能测试基准 =================

def run_performance_test(test_count=100, maze_size=20):
    print(f"开始性能测试：运行 {test_count} 次，迷宫大小 {maze_size}x{maze_size}")
    
    bfs_total_time = 0
    dfs_total_time = 0
    
    bfs_success_count = 0
    dfs_success_count = 0

    for i in range(test_count):
        # 1. 生成统一的测试地图
        base_maze = generateMaze(maze_size)
        start_point = (1, 1)
        end_point = (maze_size, maze_size)
        
        # 2. 为两个算法准备独立的深拷贝数据（避免原地修改的互相污染）
        maze_for_bfs = copy.deepcopy(base_maze)
        maze_for_dfs = copy.deepcopy(base_maze)
        
        # --- 测试 BFS ---
        start_time = time.perf_counter()
        bfs_result = solve_by_bfs(maze_for_bfs, start_point, end_point)
        bfs_total_time += (time.perf_counter() - start_time)
        if bfs_result:
            bfs_success_count += 1

        # --- 测试 DFS ---
        start_time = time.perf_counter()
        dfs_solver = DFSSolver(maze_for_dfs, start_point, end_point)
        dfs_result = dfs_solver.solve()
        dfs_total_time += (time.perf_counter() - start_time)
        if dfs_result:
            dfs_success_count += 1
            
        # 验证双方是否在同一张地图上得出相同的可达结论
        assert bfs_result == dfs_result, f"逻辑异常：回合 {i} 中算法对是否连通的结果不一致！"

    # ================= 输出测试报告 =================
    print("-" * 40)
    print("【测试结果报告】")
    print(f"测试轮数：{test_count} 轮")
    print(f"迷宫连通率 (存在解)：{(bfs_success_count/test_count)*100:.1f}%")
    print("-" * 40)
    print(f"版本 1 (Queue/BFS) 总耗时: {bfs_total_time:.6f} 秒")
    print(f"版本 1 (Queue/BFS) 平均耗时: {(bfs_total_time/test_count):.6f} 秒/次")
    print("-" * 40)
    print(f"版本 2 (Recursion/DFS) 总耗时: {dfs_total_time:.6f} 秒")
    print(f"版本 2 (Recursion/DFS) 平均耗时: {(dfs_total_time/test_count):.6f} 秒/次")
    print("-" * 40)
    
    if bfs_total_time < dfs_total_time:
        print(f"🏆 结论: 版本 1 (BFS) 速度更快，比版本 2 快约 {dfs_total_time/bfs_total_time:.2f} 倍。")
    else:
        print(f"🏆 结论: 版本 2 (DFS) 速度更快，比版本 1 快约 {bfs_total_time/dfs_total_time:.2f} 倍。")

if __name__ == "__main__":
    run_performance_test(test_count=500, maze_size=30)