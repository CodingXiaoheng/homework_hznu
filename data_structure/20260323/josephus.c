#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>

#define STATE_ALIVE 1
#define STATE_DEAD  0
#define MAKE_NODE(state, is_head, len) \
    (((uint32_t)(state) << 31) | ((uint32_t)(is_head) << 30) | (uint32_t)(len))
#define GET_STATE(node) ((node) >> 31)
#define GET_LEN(node)   ((node) & 0x3FFFFFFF)

void merge_forward(uint32_t *arr, int curr, int N) {
    while (1) {
        uint32_t len = GET_LEN(arr[curr]);
        int next_idx = curr + len;
        if (next_idx >= N) break; 
        
        if (GET_STATE(arr[curr]) == GET_STATE(arr[next_idx])) {
            uint32_t next_len = GET_LEN(arr[next_idx]);
            arr[curr] = MAKE_NODE(GET_STATE(arr[curr]), 1, len + next_len);
        } else {
            break; 
        }
    }
}

void josephus_optimized(int N, int M) {
    if (N <= 0 || M <= 0) return;

    uint32_t *arr = (uint32_t *)malloc(N * sizeof(uint32_t));
    if (!arr) {
        perror("Memory allocation failed");
        return;
    }

    arr[0] = MAKE_NODE(STATE_ALIVE, 1, N);

    int out_count = 0;
    int curr = 0;      
    
    // 引入剩余人数，算出本轮需要跨越的实际活人数
    int remaining = N;
    int k = (M - 1) % remaining + 1; 

    if (N <= 100) printf("出局顺序: ");

    while (out_count < N) {
        merge_forward(arr, curr, N);

        uint32_t state = GET_STATE(arr[curr]);
        uint32_t len = GET_LEN(arr[curr]);

        if (state == STATE_DEAD) {
            curr += len;
            if (curr >= N) curr -= N;
        } else {
            if (k > len) {
                k -= len;
                curr += len;
                if (curr >= N) curr -= N;
            } else {
                // 从当前往后数k个活人的偏移，如数2个为偏移1个
                int offset = k - 1;
                // 需要出局的人
                int target_idx = curr + offset;
                // 出局者右边剩余长度
                int right_len = len - offset - 1;

                if (right_len > 0) {
                    // 这里 target_idx + 1 是安全的，原逻辑中的 offset 和 len 关系
                    // 保证了当 target_idx == N - 1 时，right_len 一定 <= 0。
                    arr[target_idx + 1] = MAKE_NODE(STATE_ALIVE, 1, right_len);
                }
                arr[target_idx] = MAKE_NODE(STATE_DEAD, 1, 1);
                
                if (offset > 0) {
                    arr[curr] = MAKE_NODE(STATE_ALIVE, 1, offset);
                }

                if (out_count == N - 1) {
                    printf("\n 最后的幸存者是: %d\n", target_idx);
                } else if (N <= 100) {
                    printf("%d ", target_idx);
                }

                out_count++;
                remaining--;
                
                // 根据最新的存活人数，计算下一轮真正的步数
                if (remaining > 0) {
                    k = (M - 1) % remaining + 1;
                }

                curr = target_idx + 1; 
                if (curr >= N) curr -= N; // 去除取模
            }
        }
    }
    free(arr);
}

void josephus_simple(int N, int M) {
    if (N <= 0 || M <= 0) return;
    uint32_t *arr = (uint32_t *)malloc(N * sizeof(uint32_t));
    if (!arr) {
        perror("Memory allocation failed");
        return;
    }
    for (int i = 0; i < N; ++i) {
        arr[i] = i;
    }
    int curr = 0;
    int k = 0;
    if (N <= 100) {
        printf("出局顺序: ");
        k = 1;
    }
    int nxt;
    while (N > 1) {
        nxt = curr + M - 1;
        if (nxt >= N) {
            curr = nxt % N;
        }else{
            curr = nxt;
        }
        if (k) printf("%d ", arr[curr]);
        for (int i = curr; i <= N - 2; ++i) {
            arr[i] = arr[i + 1];
        }
        N--;
        // printf("%d \n",N);
    }
    printf("\n 最后的幸存者是: %d\n", arr[0]);
    free(arr);
}

//相对地址的实现
void josephus_relative(int N, int M) {
    void *memory_base = malloc(N * sizeof(int32_t));
    if (!memory_base) {
        perror("Memory allocation failed");
        return;
    }
    if(N<=100) printf("出局顺序: ");
    // 初始化
    int32_t *mb = (int32_t*)memory_base;
    for (int i = 0; i < N - 1; ++i) {
        mb[i] = 1;
    }
    mb[N-1] = -N + 1;

    int remaining = N;
    int curr = 0;
    // k代表还需要往后数的个数，1代表curr+1所在位置出局
    int k = M - 1;
    while (remaining > 1) {
        // 报数逻辑
        while (k > 1) {
            k--;
            curr += mb[curr];
        }
        // 出局逻辑
        int nxt = curr + mb[curr];
        if(N<=100) printf("%d ", nxt);
        mb[curr] = mb[curr] + mb[nxt];
        curr += mb[curr];
        remaining--;
        k = M - 1;
    }
    printf("\n 最后的幸存者是: %d\n", curr);
    free(memory_base);
}

//绝对地址的实现
void josephus_absolute(int N, int M) {
    void *memory_base = malloc(N * sizeof(int32_t));
    if (!memory_base) {
        perror("Memory allocation failed");
        return;
    }
    if(N<=100) printf("出局顺序: ");
    // 初始化
    int32_t *mb = (int32_t*)memory_base;
    for (int i = 0; i < N - 1; i++) {
        mb[i] = i+1;
    }
    mb[N-1] = 0;

    int remaining = N;
    int curr = 0;
    // k代表还需要往后数的个数，1代表curr+1所在位置出局
    int k = M - 1;
    while (remaining > 1) {
        // 报数逻辑
        while (k > 1) {
            k--;
            curr = mb[curr];
        }
        // 出局逻辑
        int nxt = mb[curr];
        if(N<=100) printf("%d ", nxt);
        mb[curr] = mb[nxt];
        curr = mb[curr];
        remaining--;
        k = M - 1;
    }
    printf("\n 最后的幸存者是: %d\n", curr);
    free(memory_base);
}

void run_perf_test(int test_id, int N, int M) {
    clock_t start, end;

    printf("【测试组 %d】 数据规模: N = %d, M = %d\n", test_id, N, M);
    printf("---------------------------------------------------------\n");

    // 1. 简单数组移动实现
    start = clock();
    josephus_simple(N, M);
    end = clock();
    printf("1. 简单数组实现 (simple)    耗时: %.6f 秒\n", (double)(end - start) / CLOCKS_PER_SEC);

    // 2. 状态合并优化实现
    start = clock();
    josephus_optimized(N, M);
    end = clock();
    printf("2. 状态合并实现 (optimized) 耗时: %.6f 秒\n", (double)(end - start) / CLOCKS_PER_SEC);

    // 3. 相对地址（步长）实现
    start = clock();
    josephus_relative(N, M);
    end = clock();
    printf("3. 相对地址实现 (relative)  耗时: %.6f 秒\n", (double)(end - start) / CLOCKS_PER_SEC);

    // 4. 绝对地址（单向链表）实现
    start = clock();
    josephus_absolute(N, M);
    end = clock();
    printf("4. 绝对地址实现 (absolute)  耗时: %.6f 秒\n", (double)(end - start) / CLOCKS_PER_SEC);
    
    printf("\n");
}

int main() {
    // 初始化随机数种子
    srand((unsigned int)time(NULL));

    printf("=========================================================\n");
    printf("                  约瑟夫环四种算法随机性能测试               \n");
    printf("=========================================================\n\n");

    // 循环测试 5 组随机数据
    for (int i = 1; i <= 8; i++) {
        // 为了确保生成的 N 能覆盖到 10^5 级别，且避免 N 较小(<=100)时大量打印序列
        // 我们将 N 的范围设置在 10,000 到 100,000 之间
        int N = (int)(((double)rand() / RAND_MAX) * 90000) + 10000;
        
        // M 的范围设定在 2 到 N/2 之间，确保报数逻辑有一定的复杂度
        int M = (int)(((double)rand() / RAND_MAX) * (N / 2)) + 2;

        run_perf_test(i, N, M);
    }

    printf("========================= 测试结束 =========================\n");

    return 0;
}