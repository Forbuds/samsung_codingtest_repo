# 노가다성으로 해결

from collections import deque
from itertools import combinations

n = int(input())
g = []
for _ in range(n):
    g.append(list(map(int, input().strip().split())))
def printg(g):
    for i in range(len(g)):
        print(g[i])
dx = [0,0,-1,1]
dy = [1,-1,0,0]

def harmony(l):
    '''
    그룹 a와 그룹 b의 조화로움은 
    (그룹 a에 속한 칸의 수 + 그룹 b에 속한 칸의 수 ) 
    x 그룹 a를 이루고 있는 숫자 값 
    x 그룹 b를 이루고 있는 숫자 값 
    x 그룹 a와 그룹 b가 서로 맞닿아 있는 변의 수로 정의됩니다.
    하나 차이나는 쌍의 숫자: 각 원소를 tmp에 저장해 두고 비교해야 하나?
    set으로 비교하면 좋을텐데
    '''
    a,b = l[0],l[1]
    
    len_a,len_b = len(a[0]),len(b[0])
    n_a,n_b = a[1],b[1]
    touch = 0

    return (len_a+len_b )*n_a*n_b

def bfs(x,y,c,v):
    '''
        ✅ 그룹에 해당하는 인덱스 모두 return하기
    '''

    tmp = [(x,y)]
    q = deque([(x,y)])
    v[x][y] = 1
    while q:
        x,y  = q.popleft()
        for i in range(4):
            nx,ny = x+dx[i], y+dy[i]
            if 0<=nx<n and 0<=ny<n and g[nx][ny]==c and v[nx][ny]==0:
                v[nx][ny]=1
                q.append((nx,ny))
                tmp.append((nx,ny))
    return tmp,v

def combi(l,k,s,g_each,pairs):
    '''
        ✅ 그룹 조합
    '''
    if l==2:
        pairs.append(list(s))
        return 
    else:
        for i in range(k,len(g_each)):
            s.append(g_each[i])
            combi(l+1,i+1,s,g_each,pairs)
            s.pop()


def art_score(g):
    '''
        예술점수 구하기
        1. 그룹 만들기
        2. 그룹 쌍 조합 구하기
        3. 그룹 쌍 중에 인접한 쌍의 예술 점수 모두 더하기
    '''

    score = 0  # 초기 예술 점수

    v = [[0]*n for _ in range(n) ]

    g_each = []     #쌍 생성
    for x in range(n):
        for y in range(n):
            if v[x][y]==0:
                # print(x,y,g[x][y])
                # g_each.append([bfs(x,y,g[x][y]),g[x][y]])
                tmp,v = bfs(x,y,g[x][y],v)
                g_each.append([tmp,g[x][y]])

    pairs = []
    combi(0,0,[],g_each,pairs)    # ✅ DFS로 구한 조합 쌍은 iterable하기 때문에 for문으로 다룬다.

    for pair in pairs:
        # print(pair)
        # p1 = set([ (x+1,y) for x,y in pair[0][0]])
        # p1.update(set([ (x,y+1) for x,y in pair[0][0]]))
        p1 = []
        p2 = set(pair[1][0])
        num = 0
        for i in range(4):
            for x,y in pair[0][0]:
                if (x+dx[i],y+dy[i]) in p2:   # ✅ 인접한 변이 있을 때마다 num+1 
                    num+=1
        if num>0: # ✅ 인접하지 않다면 pass
            score+= harmony(pair)*num   # ✅ 조화로운 점수 harmony로 계산

    return score
# art_score()

def clock(g):

    # 1 2 3
    # 4 5 6
    # 7 8 9

    # 7 4 1
    # print(list(zip(*g[::-1])))

    return list(map(list, zip(*g[::-1])))


def rclock(g):
    # print(list(map(list,zip(*g))[::-1]))
    return list(map(list,zip(*g)))[::-1]

def rotate(g):
    # ✅ 회전은 정중을 기준으로 두 선을 그어 만들어지는 십자 모양과 그 외 부분으로 나뉘어 진행됩니다
    # 1 2
    # 3 4  ✅ 순서 헷갈리지 말 것
    # 4분면
    r1 = clock([[ g[x][y]  for y in range(0,n//2)] for x in range(0,n//2)   ])
    r2 = clock([[ g[x][y]  for y in range(n//2+1,n)] for x in range(0,n//2)   ])
    r3 = clock([[ g[x][y]  for y in range(0,n//2)] for x in range(n//2+1,n)   ])
    r4 = clock([[ g[x][y]  for y in range(n//2+1,n)] for x in range(n//2+1,n)   ])

    # 십자 모양십자 모양
    cross = rclock(g)

    # 범위 나눠서 진행
    for x in range(n):
        for y in range(n):
            if x==n//2 or y==n//2:
                g[x][y] = cross[x][y]
            elif x<n//2:
                if y<n//2:
                    g[x][y] = r1[x][y]
                
                else:
                    g[x][y] = r2[x][y-n//2-1]
            else:
                if y<n//2:
                    g[x][y] = r3[x-n//2-1][y]
                
                else:
                    g[x][y] = r4[x-n//2-1][y-n//2-1]

    # printg(g)
    return g

def sol(g):
    result = art_score(g)   # 예술 점수 구하고
    for i in range(3):
        g = rotate(g)       # 회전 -> 예술 점수
        result += art_score(g)

    print(result)
sol(g)