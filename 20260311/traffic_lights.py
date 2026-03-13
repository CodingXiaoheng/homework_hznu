import networkx as nx
import matplotlib.pyplot as plt

def generate_traffic_phases(n):
    """
    生成 n 分岔路口的交通流向冲突图，并使用图着色算法划分信号灯相位。
    """
    # 1. 定义圆周上的点
    # 对于每个路口 i (0 到 n-1)，按照顺时针方向，设定 Entry（进圆）和 Exit（出圆）
    # 假设顺时针方向依次为 Entry_i, Exit_i
    def entry_point(i): return 2 * i
    def exit_point(i): return 2 * i + 1

    # 2. 生成所有可能的流向 (Nodes)
    # 流向表示为元组 (i, j)，即从路口 i 驶向路口 j
    flows = [(i, j) for i in range(n) for j in range(n) if i != j]
    
    # 3. 构建冲突图
    G = nx.Graph()
    G.add_nodes_from(flows)

    # 判断两条弦是否在圆内相交
    def chords_intersect(p1, p2, p3, p4):
        # 整理第一条弦的端点，使其从小到大
        a, b = min(p1, p2), max(p1, p2)
        # 如果第二条弦的两个端点 (p3, p4) 中，有且仅有一个严格位于 (a, b) 之间，则两弦相交
        return (a < p3 < b) ^ (a < p4 < b)

    # 遍历所有流向对，寻找冲突 (Edges)
    for idx1 in range(len(flows)):
        for idx2 in range(idx1 + 1, len(flows)):
            flow1, flow2 = flows[idx1], flows[idx2]
            i, j = flow1
            u, v = flow2

            # 合流冲突 (终点相同)
            if j == v:
                # G.add_edge(flow1, flow2, reason="Merging")
                continue
            
            # 分流冲突（起点相同）
            if i == u:
                continue

            # 冲突判定 2: 轨迹交叉 (几何弦相交)
            p1, p2 = entry_point(i), exit_point(j)
            p3, p4 = entry_point(u), exit_point(v)
            if chords_intersect(p1, p2, p3, p4):
                G.add_edge(flow1, flow2, reason="Crossing")

    # 使用图着色算法解决信号灯相位问题
    # 贪心着色算法：相邻（有冲突）的节点不能染同一种颜色
    coloring = nx.coloring.greedy_color(G, strategy='DSATUR')
    
    # 将结果按颜色（相位）分组
    phases = {}
    for flow, color in coloring.items():
        phases.setdefault(color, []).append(flow)

    return G, phases, flows

def print_and_visualize(n):
    G, phases, flows = generate_traffic_phases(n)
    
    print(f"=== {n} 分岔路口信号灯相位划分 ===")
    print(f"总流向数: {len(flows)}")
    print(f"总冲突数: {G.number_of_edges()}")
    print(f"最少所需相位数 (颜色数): {len(phases)}\n")
    
    for color in sorted(phases.keys()):
        phase_flows = phases[color]
        flow_strs = [f"路口{f[0]}->路口{f[1]}" for f in phase_flows]
        print(f"相位 {color + 1}: {', '.join(flow_strs)}")

    # 绘制冲突图
    plt.figure(figsize=(8, 6))
    pos = nx.circular_layout(G)
    
    # 节点按相位着色
    node_colors = [coloring[node] for node in G.nodes() for coloring in [nx.coloring.greedy_color(G, strategy='largest_first')]]
    
    nx.draw(G, pos, with_labels=True, node_color=node_colors, cmap=plt.cm.rainbow, 
            node_size=2000, font_size=10, font_weight="bold", edge_color="gray")
    plt.title(f"{n}-Way Intersection Traffic Conflict Graph", fontsize=14)
    plt.show()

# 运行示例
if __name__ == "__main__":
    print_and_visualize(n=8)