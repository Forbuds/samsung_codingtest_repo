"""
[중력 적용하기]
풀이시간 : 1시간 13분
1. 중력 적용하는 방법은 2가지가 있다. 새로운 그리드 + 마지막 위치 OR 기존 그리드 + 빈칸 갯수

[실수]
- 기준점 찾는 부분에서 약간 헤맸다. 시작점이 기준점이 될 기회를 빠트렸다.
- 색깔 폭탄의 조건이 2개 이상인데 2개면 묶음이 안되게 만들어놨었다.
"""
from typing import List
from collections import deque
import sys

input = sys.stdin.readline

BLACK = -1
RED = -2

answer = 0
N, M = map(int, input().split())
grid = list(list(map(int, input().split())) for _ in range(N))  # -1:돌, 0:빨강

for r in range(N):
    for c in range(N):
        # 빈칸을 0으로 쓰기 위해 빨간색을 -2로 바꿈
        if grid[r][c] == 0:
            grid[r][c] = RED

dr = [-1, 1, 0, 0]
dc = [0, 0, -1, 1]


def in_range(r: int, c: int) -> bool:
    return 0 <= r < N and 0 <= c < N


def bfs(row: int, col: int, check: List[List[int]]) -> tuple[int, int, int, int]:
    """
    색깔(1~M) 폭탄의 위치를 전달받아 BFS 탐색을 진행.
    이때 빨간색과 해당 색상의 블록으로만 이동할 수 있다.
    :param row: 색상 폭탄의 행
    :param col: 색상 폭탄의 열
    :param check: 폭탄 묶음에 포함된 폭탄들 또 BFS 돌기 싫어서 전달받은 2차원 배열
    :return: 총 폭탄 수, 빨간 폭탄 수, 기준점 행, 기준점 열
    """
    visited = [[False] * N for _ in range(N)]  # 이번 BFS에서만 사용하는 방문 배열

    color = grid[row][col]
    q = deque([(row, col)])
    visited[row][col] = True

    block_cnt = 1  # 시작 폭탄 포함
    red_cnt = 0
    standard_row = row  # [주의] 여길 0으로 했더니 시작점은 기준점이 될 기회를 잃음
    standard_col = col

    while q:
        r, c = q.popleft()

        for d in range(4):
            nr, nc = r + dr[d], c + dc[d]
            if in_range(nr, nc) and not visited[nr][nc] and grid[nr][nc] in (RED, color):
                q.append((nr, nc))
                visited[nr][nc] = True  # BFS 함수 안에서만 사용
                check[nr][nc] = True  # find_bomb_set 함수에서 같은 폭탄묶음 탐색 못 하도록 방지
                if grid[nr][nc] == RED:
                    red_cnt += 1
                else:
                    block_cnt += 1
                    # 같은 색일 때만 기준점이 될 수 있다.
                    if (nr, -nc) > (standard_row, -standard_col):
                        standard_row, standard_col = nr, nc

    return block_cnt + red_cnt, red_cnt, standard_row, standard_col


def find_bomb_set() -> List[int]:
    """
    터트릴 폭탄 묶음을 찾는 함수
    :return: 찾았는지 여부, 터트릴 폭탄의 기준점(행, 열)
    """
    check = [[False] * N for _ in range(N)]  # 폭탄 묶음 확인
    # 우선 순위에 따라 가장 불리한 상황의 값으로 초기화
    cnt, red_cnt, row, col = 0, N * N, 0, N

    for r in range(N):
        for c in range(N):
            if not check[r][c] and grid[r][c] > 0:
                check[r][c] = True
                now_cnt, now_red_cnt, now_row, now_col = bfs(r, c, check)
                # 전부 빨간색이거나 2개 미만이라면 폭탄 묶음이 아니다.
                if now_cnt == now_red_cnt or now_cnt < 2:
                    continue
                # 우선순위에 따라 바꿔야 한다면, 바꾼다.
                if (now_cnt, -now_red_cnt, now_row, -now_col) > (cnt, -red_cnt, row, -col):
                    cnt, red_cnt, row, col = now_cnt, now_red_cnt, now_row, now_col

    # 폭탄 묶음을 찾지 못 했다면, 이제 끝내야한다.
    if cnt == 0:
        return [False, -1, -1]
    return [True, row, col]


def explode(row, col) -> None:
    """
    터트릴 폭탄 묶음의 한 위치를 받아와서 BFS를 돌며 터트린다.
    :param row: 행
    :param col: 열
    :return:
    """
    global answer
    visited = [[False] * N for _ in range(N)]

    color = grid[row][col]
    explode_cnt = 1

    q = deque([(row, col)])
    visited[row][col] = True
    grid[row][col] = 0

    while q:
        r, c = q.popleft()

        for d in range(4):
            nr, nc = r + dr[d], c + dc[d]
            if in_range(nr, nc) and not visited[nr][nc] and grid[nr][nc] in (RED, color):
                q.append((nr, nc))
                visited[nr][nc] = True
                grid[nr][nc] = 0
                explode_cnt += 1

    answer += explode_cnt * explode_cnt


def gravity() -> None:
    """
    중력 함수, '돌'을 만난다면 이제까지의 빈칸만큼 비우고, 빈칸을 0으로 초기화
    """
    for col in range(N):
        blank = 0
        # 바닥에서부터 빈칸이 몇개 누적인지 센다.
        # 색깔 폭탄이면 빈칸 개수만큼 내린다.
        # 돌을 만나면 빈칸 개수를 초기화하고, 개수만큼 0으로 돌 밑부터 초기화한다.
        for row in range(N - 1, -1, -1):
            if grid[row][col] == BLACK:
                for blank_row in range(1, blank+1):
                    grid[row+blank_row][col] = 0
                blank = 0
            elif grid[row][col] == 0:
                blank += 1
            else:
                grid[row + blank][col] = grid[row][col]

        # 빈칸이 남았다면 위에서부터 지운다.
        for blank_row in range(blank):
            grid[blank_row][col] = 0


def rotate_reverse_clock() -> None:
    """
    반시계 방향으로 회전하기!
    """
    rotated = [[0] * N for _ in range(N)]
    for r in range(N):
        for c in range(N):
            rotated[N - c - 1][r] = grid[r][c]

    for r in range(N):
        grid[r] = rotated[r][:]


def solution():
    while True:
        found, row, col = find_bomb_set()  # 터트릴 폭탄의 기준점 반환
        if not found:  # 폭탄 묶음을 찾지 못 한다면 멈춘다.
            break
        explode(row, col)  # BFS 또 돌면서 터트리기
        gravity()
        rotate_reverse_clock()
        gravity()

    print(answer)


solution()