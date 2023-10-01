'''
    바닥과 격자에 쓰여진 숫자를 기준으로 방향 구하고, 정육면체를 굴리면서 격자 바닥의 숫자로 점수를 얻는 문제
'''
import sys
from collections import deque
input = sys.stdin.readline

n,M = map(int, input().strip().split())
g = []
for _ in range(n):
    g.append(list( map(int, input().strip().split())))

clock = [(0,1),(1,0),(0,-1),(-1,0)]
r_clock = [x for x in clock[::-1]]

# print(clock)
# print(r_clock)
def direction(b,g_,ddx,ddy):      
    '''
        방향은 주사위의 아랫면과 격자의 숫자로 정해짐
        b는 bottom, 주사위 바닥 점수 / g_는 격자의 점수
    '''
    if b>g_:
        ddx,ddy = clock[(clock.index((ddx,ddy))+1)%4]
    elif b<g_:
        ddx,ddy = r_clock[(r_clock.index((ddx,ddy))+1)%4]
    return ddx,ddy


def roll(top,right,front,ddx,ddy):
    '''
        굴림함수
        펼쳤을 때
    '''
    if (ddx,ddy)==(1,0):
        c_list = [7-front,right,front,7-right]  # ✅ [top,right,-,-] 
        r_list = [top,7-top]                    # ✅ [front,-] 이 두 행렬에서 변형이 일어남
    elif (ddx,ddy) == (-1,0):
        c_list = [front,right,7-front,7-right]
        r_list = [7-top,top]
    elif (ddx,ddy) == (0,-1):
        c_list = [right,7-top,7-right,top]
        r_list = [front,7-front]
    else:
        c_list = [7-right,top,right,7-top]  
        r_list = [front,7-front]

    return c_list,r_list

dx = [1,-1,0,0]
dy = [0,0,1,-1]
def printg(arr):
    for i in range(len(arr)):
        print(arr[i])

def score(x,y):
    '''
        점수는 현재 바닥 점수를 기준으로, bfs로 연관된 그룹 칸 수 만큼 점수를 얻는다. 
        현재 바닥 index 기준으로 bfs
    '''
    ground = g[x][y]
    q = deque([(x,y)])
    v = [[0]*n for _ in range(n)]
    v[x][y] = 1
    cnt = 1
    while q:
        x,y = q.popleft()
        for i in range(4):
            nx, ny = x+dx[i], y+dy[i]
            if 0<=nx<n and 0<=ny<n:
                if v[nx][ny] == 0 and g[nx][ny]==ground:
                    v[nx][ny]=1
                    q.append((nx,ny))
                    cnt+=1
    # printg(v)
    # print(cnt*g[x][y])
    return cnt*g[x][y]


result = 0

# ----------------------------------------------------------처음

x,y = 0,0                   # 처음에 0,0 에 놓여있음
ddx,ddy = 0,1               # 처음에는 항상 오른쪽
top,right,front = 1,3,2     # 처음에 보이는 주사위 면
c_list,r_list = roll(top,right,front,ddx,ddy)
top,right,front = c_list[0],c_list[1],r_list[0]   # 굴린 후
# print(top,right,front)
x,y = x+ddx,y+ddy
result += score(x,y)

# ----------------------------------------------------------M-1 번만큼 돌아감

for m in range(M-1):

    ddx,ddy = direction(c_list[2],g[x][y],ddx,ddy)   # ✅ 방향 업데이트
    if 0<=x+ddx<n and 0<=y+ddy<n:
        pass
    else:
        ddx,ddy = -ddx,-ddy        # ✅ 격자 밖에 나가변 반향됨
    x,y = x+ddx,y+ddy

    c_list,r_list = roll(top,right,front,ddx,ddy)    # ✅ 굴림
    top,right,front = c_list[0],c_list[1],r_list[0]  # ✅ 보이는 모양 바뀜
    # print(top,right,front)
    result += score(x,y)    # ✅ 점수
print(result)