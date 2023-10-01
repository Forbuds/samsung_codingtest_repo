"""
[나선형 이동하기]
풀이시간 : 30분
1. 빗자루 방향에 따른 비율 변화는, 코드로 작성하기 너무 어렵다. 하드코딩이 편한 경우
2. 나선형 이동하는 테크닉은 여러개가 있는데, 같은 거리 2번 가는게 제일 편하다.
"""
import sys
input = sys.stdin.readline

N = int(input())
grid = list(list(map(int, input().split())) for _ in range(N))
answer = 0  # 격자 밖으로 나간 먼지 양

# 왼 - 아 - 오 - 위
dr = [0, 1, 0, -1]
dc = [-1, 0, 1, 0]

# 그냥 하드 코딩이 편한 것 같아요
ratio = [
    [
        [0, 0, 2, 0, 0],
        [0, 10, 7, 1, 0],
        [5, 0, 0, 0, 0],
        [0, 10, 7, 1, 0],
        [0, 0, 2, 0, 0]
    ],
    [
        [0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [2, 7, 0, 7, 2],
        [0, 10, 0, 10, 0],
        [0, 0, 5, 0, 0]
    ],
    [
        [0, 0, 2, 0, 0],
        [0, 1, 7, 10, 0],
        [0, 0, 0, 0, 5],
        [0, 1, 7, 10, 0],
        [0, 0, 2, 0, 0]
    ],
    [
        [0, 0, 5, 0, 0],
        [0, 10, 0, 10, 0],
        [2, 7, 0, 7, 2],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0]
    ]
]


def in_range(r, c):
    return 0 <= r < N and 0 <= c < N


def sweep(row, col, drt):
    global answer
    p = ratio[drt]  # 이번 방향에 맞는 배율이 저장된 2차원 배열
    total = grid[row][col]  # 이 위치의 먼지
    left = total  # a%에 저장할 양

    for r in range(5):
        for c in range(5):
            if p[r][c]:
                dust = (total * p[r][c]) // 100
                nr, nc = row-2 + r, col-2 + c  # grid에서의 위치
                if not in_range(nr, nc):
                    answer += dust
                else:
                    grid[nr][nc] += dust
                left -= dust

    # 바로 앞칸
    fr, fc = row + dr[drt], col + dc[drt]
    if in_range(fr, fc):
        grid[fr][fc] += left
    else:
        answer += left

    grid[row][col] = 0


def solution():
    # 빗자루 위치, 방향, 거리
    row, col, drt, dist = N // 2, N // 2, 0, 1

    while True:
        for _ in range(2):
            for _ in range(dist):
                row += dr[drt]
                col += dc[drt]
                sweep(row, col, drt)
                if row == 0 and col == 0:
                    return
            drt = (drt + 1) % 4
        dist += 1


solution()
print(answer)

