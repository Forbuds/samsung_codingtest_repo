# 10시 41분 시작
import sys
input = sys.stdin.readline

n,M = map(int, input().strip().split())
g = []
pill_arr = []
rule = []

for _ in range(n):
    g.append(list(map(int, input().strip().split())))

for _ in range(M):
    d,p = map(int, input().strip().split())
    rule.append([d-1,p])

dx = [0,-1,-1,-1,0,1,1,1]
dy = [1,1,0,-1,-1,-1,0,1]

result = 0

for i in range(n-1,n-3,-1):
    for j in range(0,2):
        # print(i,j)
        pill_arr.append((i,j))
# pill[4][2] = 1

def is_in(x,y):
    if 0<=x<n and 0<=y<n :
        return True
    else:
        return False

def printg(arr):
    for i in range(len(arr)):
        print(arr[i])


def move(d,p,pill_arr):
    tmp = []

    for x,y in pill_arr:
        tmp.append(((x+dx[d]*p)%n,(y+dy[d]*p)%n))
    return tmp

dxd = [-1,-1,1,1]
dyd = [-1,1,-1,1]

def grow(pill_arr,g):
    for x,y in pill_arr:
        g[x][y]+=1
    
    for x,y in pill_arr:
        cnt = 0
        for i in range(4):
            nx,ny = x+dxd[i],y+dyd[i]
            if is_in(nx,ny) and g[nx][ny]>0:
                cnt+=1
        g[x][y]+=cnt
    # printg(g)

    return g


def crop(pill_arr,g):
    tmp = []

    for x in range(n):
        for y in range(n):
            if (x,y) in pill_arr:
                continue
            else:
                if g[x][y]>=2:
                    g[x][y] -= 2
                    tmp.append((x,y))

    return tmp,g

for m in range(M):
    d,p = rule[m]
    # 특수 영양제 이동
    pill_arr = move(d,p,pill_arr)
    # 영양제 투입
    # 성장
    g = grow(pill_arr,g)
    pill_arr,g = crop(pill_arr,g)
    # 잘라내고 영양제 추가

result = 0

for i in range(n):
    result += sum(g[i])
    
print(result)