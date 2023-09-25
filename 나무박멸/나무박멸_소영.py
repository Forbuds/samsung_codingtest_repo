
# https://www.codetree.ai/training-field/frequent-problems/problems/tree-kill-all/description?page=1&pageSize=20

import sys

input = sys.stdin.readline
n, M, K, c = map(int, input().strip().split())
arr = []
arr_kill = [[0] * n for _ in range(n)]
for i in range(n):
    arr.append(list(map(int, input().strip().split())))
result = 0  # m년동안 박멸한 나무 수

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]
dxd = [1, 1, -1, -1]
dyd = [1, -1, 1, -1]


def printg(arr):
    for i in range(len(arr)):
        print(arr[i])


def grow(arr):  # 백트래킹 써볼까 했는데, 어차피 다 봐야하는 것 아닌가?
    tmp_grow = [[0] * (n) for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if arr[i][j] > 0:
                tmp = 0
                for p in range(4):
                    nx, ny = i + dx[p], j + dy[p]
                    if 0 <= nx < n and 0 <= ny < n and arr[nx][ny] > 0:
                        tmp += 1
                tmp_grow[i][j] += tmp
    return [[arr[i][j] + tmp_grow[i][j] for j in range(n)] for i in range(n)]


def bun(arr):  # 제초제도 고려해야 함

    je = -1
    tmp_bun = [[0] * (n) for _ in range(n)]
    for x in range(n):
        for y in range(n):
            if arr[x][y] > 0:
                tmp = []
                for i in range(4):
                    nx, ny = x + dx[i], y + dy[i]
                    if 0 <= nx < n and 0 <= ny < n:
                        if arr[nx][ny] == 0 and arr_kill[nx][ny] >= 0:
                            tmp.append((nx, ny))
                if len(tmp) != 0:
                    cnt = arr[x][y] // len(tmp)
                else:
                    cnt = 0
                for nx, ny in tmp:
                    tmp_bun[nx][ny] += cnt

    return [[arr[i][j] + tmp_bun[i][j] for j in range(n)] for i in range(n)]


def dio(arr, x, y, flag):
    if flag:
        tmp = []
        tmp.append((x, y))
        for i in range(4):
            for k in range(1, K+1):
                nx, ny = x + dxd[i] * k, y + dyd[i] * k
                if 0 <= nx < n and 0 <= ny < n:
                    if arr[nx][ny] <= 0:
                        tmp.append((nx, ny))
                        break
                    else:
                        tmp.append((nx, ny))
        # print(tmp)

        return tmp

    else:
        tmp = 0
        tmp += arr[x][y]
        for i in range(4):
            for k in range(1, K+1):
                nx, ny = x + dxd[i] * k, y + dyd[i] * k
                if 0 <= nx < n and 0 <= ny < n:
                    if arr[nx][ny] <= 0:
                        break
                    else:
                        tmp += arr[nx][ny]
        # print(tmp)

        return tmp


def kill(arr, arr_kill, result):  # 제초제는 - 값으로 해야 겠더라
    # 가장 나무가 많이 박멸되는 칸에 제초제를 뿌린다.
    tmp_tree = (0, 0, 0)
    for x in range(n):
        for y in range(n):
            if arr[x][y] >0:
                tmp_tree = max(tmp_tree, (dio(arr, x, y, False), x, y), key=lambda x: (x[0], -x[1], -x[2]))

    # print(tmp_tree)
    tmp_arr = dio(arr, tmp_tree[1], tmp_tree[2], True)
    # print(tmp_arr)
    # print(f'arr_kill: {arr_kill}')
    print('delete : ',tmp_arr,tmp_tree[0])
    for x, y in tmp_arr:
        if arr[x][y]!=-1:
            arr_kill[x][y] =  -c
            arr[x][y] = 0

    # 없앤 나무의 수
    # 제초제 유지

    result += tmp_tree[0]
    return arr, arr_kill, result


for m in range(M):
    print('------------------------')

    print('---arr')
    printg(arr)

    arr = grow(arr)

    print('---g')
    printg(arr)

    arr = bun(arr)

    print('---bun')
    printg(arr)

    arr_kill = [[arr_kill[x][y] + 1 if arr_kill[x][y] < 0 else 0 for y in range(n)] for x in range(n)]

    print('---arr_kill')
    printg(arr_kill)

    arr, arr_kill, result = kill(arr, arr_kill, result)

    print('---arr')
    printg(arr)
    print('---arr_kill')
    printg(arr_kill)

print(result)

#continue로 짤 것