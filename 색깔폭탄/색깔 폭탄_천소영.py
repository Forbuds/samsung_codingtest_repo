'''
    while 폭탄 있을때
        1. 큰 묶음 찾기 (빨강은 깍두기)  ✅ big
        2. 없애기
        3. 중력 작용 (주의: 돌은 그대로) ✅ grivity
        4. 회전
        5. 중력 작용
'''
import sys
from collections import deque
input = sys.stdin.readline

n,m = map(int, input().strip().split())   #m 은 빨강 이외 종류
g = []
for _ in range(n):
    g.append(list(map(int, input().strip().split())))
result = 0
dx = [0,0,-1,1]
dy = [1,-1,0,0]

def printg(g):
    for i in range(len(g)):
        print(g[i])
def gravity(g):   #  -2가 빈 칸, -1 돌 0 빨강   # 맞음
    '''
    중력이 작용하여 위에 있던 폭탄들이 떨어지지만, 여기서 유의해야 할 점은 
    돌은 특이한 성질을 띄고 있기 때문에 중력이 작용하더라도 떨어지지 않습니다.
    '''
    # g = [[-1,-1,1,1],[1,-1,-2,1],[1,2,-1,-2],[-2,-2,2,2]]
    # g = [[2,1,1,-1],[2,2,-1,-1],[-2,-1,1,1],[-2,-2,-2,1]]

    for y in range(n):
        # print(f'y: {y}')
        for x in range(n-1,0,-1):
            # print(x,x-1)
            if g[x][y]==-2:  # 빈칸인 경우에만 조건 확인하기
                if g[x-1][y]==-1:   # 윗 칸이 돌일 경우는 pass
                    continue
                else:
                    cnt=1
                    while True:
                        if x-cnt>=0:
                            if g[x-cnt][y]>-1:    # 윗 칸이 폭탄일 때 멈춤
                                # print('------',cnt)
                                for i in range(cnt-1,-1,-1):
                                    # 0 1
                                    # 1 2
                                    # print('--',x-i,x-i-1)
                                    g[x-i][y],g[x-(i+1)][y] = g[x-(i+1)][y],g[x-i][y]
                                    # printg(g)
                                break
                            elif g[x-cnt][y]==-1:
                                break
                            else:
                                cnt +=1
                        else:
                            break
            else:
                pass

            # -2가 나오면 바꿔치기, -1 나오면 멈춤

            # 색 / 색  -> 그대로
            # 빈칸 / 색 -> 그대로
            # 돌 / 색  ->  그대로
  
            # 색 / 빈칸 -> 바꾸기    V
            # 돌 / 빈칸 -> 그대로  
            # 빈칸 / 빈칸 -> while   V

            # 색 / 돌  -> 그대로
            # 빈칸 / 돌 -> 그대로
            # 돌 -> 돌 _> 그대로

    # printg(g)

    return g


def rotate(g):
    '''
    반시계 방향으로 90' 만큼 회전합니다.
    '''

    # 1 2 3
    # 4 5 6
    # 7 8 9

    # 3 6 9
    # 2 5 8
    # 1 4 7

    # zip으로 이터러블 한 *g를 묶어 주면 [1,4,7][2,5,8] 이렇게 묶인다. 
    # 순서를 마지막 인덱스로 해 주면 그게 반시계 90도

    # print(list(map(list, zip(*g)))[::-1])
    return list(map(list, zip(*g)))[::-1]





# 폭탄 묶음" 2개이상,  같은 색, 
def bfs(x,y,g,c):
    '''
        폭탄 묶음 찾으면서, 기준점 찾기  -> 이 return 값으로 big함수에서 비교
    '''

    q = deque([(x,y)])
    v = [[0]*n for _ in range(n)]   # ✅ 빨간 폭탄은 깍두기이기 때문에, bfs할때마다 초기화해줘야 함.
    v[x][y] =1
    ground = (-1,-1)
    if (x,-y)>ground:      # ✅ 행이 가장 큰 순서, 열이 가장 작은 순서로 본 그룹의 기준점(ground)을 택한다.
        ground = (x,-y)

    cnt = 1
    red = 0

    while q:
        x,y = q.popleft()
        for i in range(4):
            nx,ny = x+dx[i],y+dy[i]
            if 0<=nx<n and 0<=ny<n and v[nx][ny]==0:
                if g[nx][ny]==c:            # ✅ 색깔이라면, cnt에 추가, 기준점 업뎃
                    q.append((nx,ny))
                    v[nx][ny] = 1
                    cnt+=1
                    # case 1    # ✅ ground update는 case 1, case 2 중에 고르면 될 듯
                    ground = max((nx,-ny),ground) 
                    # case 2
                    # if (nx,-ny)>ground:
                    #     ground = (nx,-ny)

                elif g[nx][ny]==0:           # ✅ 빨강이라면, cnt와 red에 추가
                    q.append((nx,ny))
                    v[nx][ny] = 1
                    cnt+=1
                    red+=1
                else:
                    pass
    # print(cnt)
    # printg(v)

    return (cnt,-red,ground[0],ground[1])



# 가장 큰 폭탄 묶음 찾기
def big(g):
    '''

    폭탄 묶음이란 2개 이상의 폭탄 (모두 같은 색깔의 폭탄) (빨간색 포함하여 2개의 색깔로)
    V 빨간색 폭탄으로만 이루어져 있는 경우는 올바른 폭탄 묶음이 아니며
    V 격자 연결


    (1) 크기가 큰 폭탄 묶음들 중 빨간색 폭탄이 가장 적게 포함된 것 부터 선택합니다.
    (2) 기준점 중 가장 행이 큰 폭탄 묶음을 선택합니다. 
        기준점이란, 묶음 중 빨간색이 아니면서 행이 가장 큰 칸
        열이 가장 작은 칸을 의미합니다.
    (3) 폭탄 묶음의 기준점 중 가장 열이 작은 폭탄 묶음을 선택합니다.
    '''
    tmp = []
    best = (-1,-1,-1,-1)   # ❓기준점이 red도 -1이 되는 이유를 모르겠음
    
    for x in range(n):
        for y in range(n):
            c = g[x][y]
            if c>0:                     # 0말고 색깔 폭탄이 있다면
                tmp = bfs(x,y,g,c)      # bfs로 그룹 구하면서 (그룹에 있는 폭탄 개수, red개수, x, -y)
                if tmp[0]>1:            # 폭탄 2개 이상 == 폭탄 묶음
                    if tmp>best:
                        best = tmp
    # print(best)
    return best


def delete(x,y,g):   # 
    '''
        폭탄 터지는 함수
    '''

    q = deque([(x,y)])
    v=[[0]*n for _ in  range(n)]
    v[x][y] =1
    c = g[x][y]
    g[x][y]=-2
    

    while q:
        x,y = q.popleft()
        for i in range(4):
            nx,ny = x+dx[i],y+dy[i]
            if 0<=nx<n and 0<=ny<n and (g[nx][ny]==0 or g[nx][ny]==c) and v[nx][ny]==0:
                v[nx][ny] = 1
                g[nx][ny] = -2
                q.append((nx,ny))

    return g


while True:
    # printg(g)

    best = big(g)            # ✅ 큰 폭탄 묶음 찾기
    # print(best)
    if best==(-1,-1,-1,-1):  # 폭탄 없다(update 안됨)
        break
    else:
        c,red,x,y = map(int, best)


        # 폭탄들을 전부 제거합니다. 
        g = delete(x,-y,g)
        # print('d')
        # printg(g)
        result += c**2
        # print(f'----{c}')

        
        # 폭탄들이 제거된 이후에는 중력이 작용하여 위에 있던 폭탄들이 떨어지지만,
        # 반시계 방향으로 90' 만큼 격자 판에 회전이 일어납니다.
        # 다시 중력이 작용하며, 이때 역시 돌은 절대로 떨어지지 않습니다.
        g = gravity(g)
        g = rotate(g)
        g = gravity(g)


print(result)