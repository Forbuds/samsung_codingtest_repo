"""
풀이시간 : 52분
- 공 맞는 부분 구현하기가 까다로웠다.
"""

from collections import deque

N, M, K = map(int, input().split())
grid = list(list(map(int, input().split())) for _ in range(N))
teams = [deque() for _ in range(M)]  # 각 팀의 인원 (머리 -> 꼬리)
routes = [deque() for _ in range(M)]  # 각 팀의 경로 (꼬리 뒤 -> 머리 앞)

answer = 0  # 점수의 총 합

# 우 상 좌 하
dr = [0, -1, 0, 1]
dc = [1, 0, -1, 0]


def in_range(r, c):
    return 0 <= r < N and 0 <= c < N


def init():
    # 팀 BFS로 정보 저장
    visited = [[False] * N for _ in range(N)]
    idx = 0

    for row in range(N):
        for col in range(N):
            if grid[row][col] == 1:
                q = deque([(row, col)])
                teams[idx].append((row, col))
                visited[row][col] = True

                while q:
                    r, c = q.popleft()

                    for d in range(4):
                        nr, nc = r + dr[d], c + dc[d]
                        if in_range(nr, nc) and not visited[nr][nc] and grid[nr][nc] != 0:
                            if grid[r][c] == 1 and grid[nr][nc] != 2:
                                continue
                            if grid[r][c] == 2 and grid[nr][nc] not in (2, 3):
                                continue
                            if grid[r][c] == 3 and grid[nr][nc] != 4:
                                continue

                            q.append((nr, nc))
                            visited[nr][nc] = True

                            if grid[nr][nc] < 4:
                                teams[idx].append((nr, nc))
                            else:
                                routes[idx].append((nr, nc))

                idx += 1


def move():
    for idx in range(M):
        routes[idx].appendleft(teams[idx].pop())
        teams[idx].appendleft(routes[idx].pop())


def set_direction(rnd):
    direction = (rnd // N) % 4
    start_row, start_col = 0, 0

    # 방향에 따라 시작 위치가 다르다.
    if direction == 0:
        start_row = rnd % N
    elif direction == 1:
        start_col = rnd % N
        start_row = N - 1
    elif direction == 2:
        start_row = N - (rnd % N) - 1
        start_col = N - 1
    else:
        start_col = N - (rnd % N) - 1

    throw(start_row, start_col, direction)


def throw(sr, sc, drc):
    global answer

    # (머리에서 몇 번째 사람, 몇 번 팀) 인지 기록
    grid = [[(0, 0)] * N for _ in range(N)]

    for t in range(M):
        for i in range(len(teams[t])):
            r, c = teams[t][i]
            grid[r][c] = (i+1, t)

    for step in range(N):
        nr, nc = sr + dr[drc]*step, sc + dc[drc]*step
        member_idx, team_idx = grid[nr][nc]

        if member_idx:
            # 사람이 있다!
            answer += member_idx ** 2
            teams[team_idx].reverse()
            routes[team_idx].reverse()
            break


def solution():
    init()
    for rnd in range(K):
        move()
        set_direction(rnd)

    print(answer)

solution()