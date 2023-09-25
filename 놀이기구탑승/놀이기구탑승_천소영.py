import sys

input =sys.stdin.readline

n = int(input())
arr =  {} 
result = 0
g = [[0]*n for _ in range(n)]

for i in range(n*n):
    l = list(map(int, input().strip().split()))   # 중복 가능
    arr[l[0]] = l[1:]
    
# print(arr)

p_list = []

# 비어있는 칸 중에서, 인접한 칸 중에서
# 인접한 칸 중에서, 
dx = [ 0,0,1,-1]
dy = [1,-1,0,0]
def is_in(x,y):
    if 0<=x<n and 0<=y<n :
        return True
    else:
        return False
arr_keys = list(arr.keys())
g[1][1] = arr_keys[0]
def printg(arr):
    for i in range(len(arr)):
        print(arr[i])
# printg(g)

for p in arr_keys[1:]:
    # print(f'--------------{p}')

    # p_list순회
    tmp_all = []
    for i in range(n):
        for j in range(n):
            if g[i][j]==0:
                cnt = 0
                cnt_blank = 0
                for k in range(4):
                    # 현재 위치에 좋아하는 학생이 있는가, 몇 명 있는가?? 위치는 어딘가?
                    nx,ny = i+dx[k],j+dy[k]
                    if is_in(nx,ny):
                        if (g[nx][ny] in arr[p]) :
                            cnt+=1
                        if g[nx][ny]==0:
                            cnt_blank+=1
                tmp_all.append((cnt,cnt_blank,i,j))
    tmp_all = sorted(tmp_all, key = lambda x: (-x[0],-x[1],x[2],[3]))
    # print(tmp_all)
    x,y = tmp_all[0][2], tmp_all[0][3]
    
            
    # p_list.append((x,y))
    g[x][y] = p
    # printg(g)


for i in range(n):
    for j in range(n):
        current = g[i][j]
        cnt = 0
        for k in range(4):
            nx,ny = i+dx[k],j+dy[k]
            if is_in(nx,ny) and (g[nx][ny] in arr[current]):
                cnt+=1
        if cnt==0:
            continue
        else:
            
            result += 10**(cnt-1)
print(result)