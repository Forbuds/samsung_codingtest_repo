"""
풀이시간 : 57분
주의사항
1. 주사위의 3,4 위치를 반대로 썼다가 틀렸다.
2. 회전해놓고 붙여넣기를 안했다.
"""
from collections import deque

N, M = map(int, input().split())
board = list(list(map(int, input().split())) for _ in range(N))

# 상/우/하/좌 (시계방향 90' 기준)
dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]

dice = [
    [0, 1, 0],
    [4, 2, 3],
    [0, 6, 0],
    [0, 5, 0]
]

d_row, d_col, d_dir = 0, 0, 1  # 초기 위치와 방향


def in_range(r, c):
    return 0 <= r < N and 0 <= c < N


def move_and_score():
    global d_row, d_col, d_dir
    if not in_range(d_row + dr[d_dir], d_col + dc[d_dir]):
        # 만약 진행 도중 다음과 같이 격자판을 벗어나게 된다면, 반사되어 방향이 반대로 바뀌게 된 뒤 한 칸 움직이게 됩니다.
        d_dir = (d_dir + 2) % 4

    d_row += dr[d_dir]
    d_col += dc[d_dir]

    visited = [[False] * N for _ in range(N)]

    # 초기 위치
    visited[d_row][d_col] = True
    num, cnt = board[d_row][d_col], 1
    q = deque([(d_row, d_col)])

    while q:
        r, c = q.popleft()

        for d in range(4):
            nr, nc = r + dr[d], c + dc[d]
            if in_range(nr, nc) and not visited[nr][nc] and board[nr][nc] == num:
                q.append((nr, nc))
                visited[nr][nc] = True
                cnt += 1

    return num * cnt


def rotate_dice():
    global d_dir
    # 주사위 복사
    new_dice = [[0] * 3 for _ in range(4)]

    for r in range(4):
        new_dice[r] = dice[r][:]

    # 주사위 면 회전
    if d_dir == 0:  # 위로
        for r in range(4):
            new_dice[(r - 1) % 4][1] = dice[r][1]
    elif d_dir == 2:  # 아래로
        for r in range(4):
            new_dice[(r + 1) % 4][1] = dice[r][1]
    elif d_dir == 1:  # 오른쪽
        for r in range(3):
            for c in range(3):
                new_dice[c][2 - r] = dice[r][c]
    else:  # 왼쪽
        for r in range(3):
            for c in range(3):
                new_dice[2 - c][r] = dice[r][c]

    # 주사위 회전한거 붙여넣기
    for r in range(4):
        dice[r] = new_dice[r][:]

    # 주사위 방향 조절
    if board[d_row][d_col] < dice[2][1]:
        # 주사위의 아랫면이 보드의 해당 칸에 있는 숫자보다 크면 현재 진행방향에서 90' 시계방향으로 회전하여 다시 이동을 진행하게 되고,
        d_dir = (d_dir + 1) % 4
    elif board[d_row][d_col] > dice[2][1]:
        # 주사위의 아랫면의 숫자가 더 작다면 현재 진행방향에서 90' 반시계방향으로 회전하게 되며,
        d_dir = (d_dir - 1) % 4
    # 동일하다면 현재 방향으로 계속 진행하게 됩니다.


def solution():
    answer = 0
    # 한 칸 움직임(격자 밖 처리) + 점수 얻기
    for _ in range(M):
        answer += move_and_score()
        # 주사위의 면이 바뀌고, 방향을 조절함
        rotate_dice()
    print(answer)


solution()