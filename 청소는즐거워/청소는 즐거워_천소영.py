# 해설 참고
# https://www.codetree.ai/training-field/frequent-problems/problems/cleaning-is-joyful/description?page=2&pageSize=20

import copy
import math

n = int(input())
g = []
for _ in range(n):
    g.append(list(map(int, input().strip().split())))

'''
빙빙 돌며 + 
처음에 정가운데 격자에는 먼지가 존재하지 않습니다. 
정가운데부터 시작하여 아래 그림과 같이 나선형으로 바닥 청소를 하려 합니다.
-> 만나면 방향을 바구는 방식이 아닌, 1->1->2->2-> 이런 형식임.
-> 방향은 왼쪽, 아래, 오른쪽, 위
'''

dx = [0, 1, 0, -1]  # 주의: 아래로 갈 때 x + 1
dy = [-1, 0, 1, 0]
result = 0  # 격자 밖으로 떨어진 먼지 양의 총합

def is_in(x, y):
    return 0 <= x < n and 0 <= y < n

dust_tmp = [[0, 0, 2, 0, 0],
            [0, 10, 7, 1, 0],
            [5, 0, 0, 0, 0],
            [0, 10, 7, 1, 0],
            [0, 0, 2, 0, 0]]  # a를 뺀 나머지 먼지를 미리 배열로 만들어 둠

dust_ratio = []
dust_ratio.append(dust_tmp)

for i in range(3):
    '''
    회전하는 dust 배열 미리 만들어 두기
    '''
    tmp = list(map(list, zip(*dust_tmp)))[::-1]  # zip 사용법: list를 *list를 이용해 iterable하게 만들어 둔다.
    dust_ratio.append(tmp)
    dust_tmp = tmp

def printg(g):
    for i in range(len(g)):
        print(g[i])

def add_dust(cx, cy, d):
    '''
    5*5 뚝 떼어서 계산한다.
    
    (cx - 2) + i
    (가운데 - 반 : 기준점) + i

    '''
    global result, g
    dust = g[cx][cy]
    g[cx][cy] = 0
    tmp = 0
    
    for i in range(5):
        for j in range(5):
            # print(cx-2+i,cy-2+j,i,j)
            c_dust = dust * (dust_ratio[d][i][j]) // 100
            tmp += c_dust
            if is_in(cx - 2 + i, cy - 2 + j) :
                g[cx - 2 + i][cy - 2 + j] += c_dust   # 격자 안에 있다면 더해주고,
            else:
                result += c_dust                      # 격자 밖에 있다면 result에 더해주자
    if is_in(cx + dx[d], cy +dy[d]):
        g[cx + dx[d]][cy + dy[d]] += dust - tmp       # a를 채워주되, a도 격자 안에 있는지 확인 필.
    else:
        result += dust-tmp

    # printg(g)


# cy-2   cx,cy-1 cx,cy cx,cy+1
#    cx+1,cy-1

# 2,0   2,1     2.2   2.3 2,4
#    3.1     3.2   3.3

# cx-2+i
# add_dust(2,1,0)


def move():
    '''
    빗자루가 이동할 때마다 빗자루가 이동한 위치의 격자(Curr)에 있는 먼지가 함께 이동하는데
    아래의 비율에 맞춰서 먼지가 이동하게 됩니다.
    이동한 먼지는 기존의 먼지 양에 더해지고,
    v 빗자루가 이동한 위치(Curr)에 있는 먼지는 모두 없어지게 됩니다.
    a%에 해당하는 먼지 양은 다른 격자에 이동한 먼지의 양을 모두 합한 것을 이동한 위치에 있던
    먼지의 양에서 빼고 남은 먼지에 해당합니다.
    비율을 곱해줄 때 소숫점 아래의 숫자는 버림해줍니다.
    '''

    g = [[0] * n for _ in range(n)]
    d = 0
    x, y = n // 2, n // 2
    cnt = 1
    num = 2
    i = 0
    while True:
        if x == 0 and y == 0:  # 0,0 인덱스에 도착한다면 break
            break
        else:
            if i == 2:   # 두 번 돌면 길이 올려주기
                cnt += 1
                i = 0
            else:
                for j in range(cnt):
                    x, y = x + dx[d], y + dy[d]
                    add_dust(x, y, d)
                    if x == 0 and y == 0:
                        break
                d = (d + 1) % 4
                i += 1
    return

move()
print(result)