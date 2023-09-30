# 문제 잘 읽자 -> 제대로 안 읽어서 시간 날림

n, m, K = map(int, input().strip().split())
arr = []
g = [[list() for _ in range(n)] for _ in range(n)]
result = 0
for _ in range(m):
    x, y, m, s, d = map(int, input().strip().split())
    x, y = x - 1, y - 1
    g[x][y] = [(m, s, d)]  # 격자가 최선이 아닐 수도?
    arr.append(tuple([x,y,m,s,d]))    # 인덱스, 질량, 속력, 방향

dx = [-1, -1, 0, 1, 1, 1, 0, -1]   # ↑, ↗, →, ↘, ↓, ↙, ←, ↖
dy = [0, 1, 1, 1, 0, -1, -1, -1]

# d = (d+1)%n
def move(g,arr):
    '''
        움직이고, 합성
    '''
    # 1. 이동 먼저 - move
    tmp = [[list() for _ in range(n)] for _ in range(n)]
    for i in range(len(arr)):   # ✅ n*n 보다 arr 순회를 택함   
        x, y, m, s, d = arr[i]
        x, y = (x + s * dx[d]) % n, (y + s * dy[d]) % n  # ✅ python에서는 이렇게, 격자를 넘어서는 (음수가 되는) 인덱스가 있어도 괜찮음
        tmp[x][y].append((m, s, d))
    
    # 2. 합성
    arr = []
    for i in range(n):
        for j in range(n):   # ✅ 격자 돌면서 일일히 확인, 0->아무일x, 1->그대로arr업데이트, 2↑->합성
            if len(tmp[i][j])>1:    # 합성
                M,S,D = 0,0,[]
                for l in tmp[i][j]:
                    m, s, d = l
                    M+=m
                    S+=s
                    D.append(d%2)  # ✅ 한 종류라면, 나머지 계산 했을때 (0)or(1)이렇게 나올 테지만, 두 종류라면 (0,1)
                    # if D%2==0:   # ❗상하좌우 관련 문제 잘못 읽음
                    
                M = M//5
                S = S//len(tmp[i][j])
                D = set(D)
                if len(D)==1:      # 이것도 잘못 읽음, ❗한 종류라면 -> 상하좌우
                    D = [0,2,4,6]
                else:
                    D = [1,3,5,7]  # ❗하나라도 다른 종류라면 -> 대각선
                tmp[i][j] = list()
                if M==0:           # 질량 없으면, 없던 일
                    pass
                else:
                    for k in range(4):
                        tmp[i][j].append((M,S,D[k]))     # ✅ graph랑 arr 모두를 업데이트
                        arr.append((i,j,M,S,D[k]))
            elif len(tmp[i][j]) == 1:
                # print(tmp[i][j])
                m,s,d = tmp[i][j][0]
                arr.append((i,j,m,s,d))

    return tmp,arr

def remain(g):
    '''
        마지막 남은 원소의 합을 구하는 함수
    '''
    global result
    for x in range(n):
        for y in range(n):
            if len(g[x][y])>0:
                for l in g[x][y]:    # 해당 칸의 원소만큼 더해줌
                    result += l[0]

def printg(g):
    for i in range(len(g)):
        print(g[i])

'''
    main 함수: 1초가 지날 때 마다 move
'''
for k in range(K):
    g,arr = move(g,arr)   # ✅ 방식: arr와 g 두 개로 관리. g = [[],[],..], arr=[(i,j,m,s,d), (),(),...]

remain(g)
print(result)