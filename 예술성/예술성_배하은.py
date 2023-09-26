from collections import deque

N = int(input())
art = list(list(map(int, input().split())) for _ in range(N))

dr = [-1, 1, 0, 0]
dc = [0, 0, -1, 1]


def grouping():
    """
    그룹별 숫자, 위치 정보(BFS 탐색)를 저장한다.
    다른 그룹이라도 숫자가 같을 수 있기 때문에 dictionary로 저장 할 수 없다.
    위치 정보는 set으로 저장해서, 맞닿은 변을 찾을 때 빠르게 했다.
    맞닿은 변은 그냥 또 BFS를 돌면서 상대 숫자인지 중복 포함 확인하면 된다.
    """
    groups = []

    visited = [[False] * N for _ in range(N)]

    for r in range(N):
        for c in range(N):
            if not visited[r][c]:  # 이미 그룹에 포함된 숫자는 패스
                # 처음 위치
                num = art[r][c]
                pos = {(r, c)}

                # BFS 준비
                q = deque([(r, c)])
                visited[r][c] = True

                while q:
                    row, col = q.popleft()

                    for d in range(4):
                        nrow, ncol = row + dr[d], col + dc[d]

                        if 0 <= nrow < N and 0 <= ncol < N and not visited[nrow][ncol] and art[nrow][ncol] == num:
                            q.append((nrow, ncol))
                            pos.add((nrow, ncol))
                            visited[nrow][ncol] = True

                groups.append([num, pos])

    # (그룹 a에 속한 칸의 수 + 그룹 b에 속한 칸의 수 )
    # x 그룹 a를 이루고 있는 숫자 값 x 그룹 b를 이루고 있는 숫자 값
    # x 그룹 a와 그룹 b가 서로 맞닿아 있는 변의 수
    score = 0

    group_cnt = len(groups)
    # combinations으로 만들어도 되는데, 그냥 2중 for문으로 처리했다.
    for first in range(group_cnt-1):
        for second in range(first+1, group_cnt):
            f_num, f_pos = groups[first]  # 첫 번째 그룹의 숫자와 위치
            s_num, s_pos = groups[second]  # 두 번째 그룹의 숫자와 위치

            edges = 0  # 맞닿은 변의 개수
            for r, c in f_pos:
                for d in range(4):
                    nr, nc = r + dr[d], c + dc[d]
                    if (nr, nc) in s_pos:  # set으로 저장한 이유
                        edges += 1

            score += (len(f_pos) + len(s_pos)) * f_num * s_num * edges

    return score


def rotate_art():
    new_art = [[0] * N for _ in range(N)]  # 회전한 내용 저장
    half = N // 2

    # 십자 모양의 경우 통째로 반시계 방향으로 90' 회전합니다.
    for step in range(N):
        # N // 2 행의 0 -> N-1 열은, N-1 -> 0 행의 N//2 열이 됨
        new_art[N-1-step][half] = art[half][step]
        # 0 -> N-1 행의 N//2 열은 -> N//2 행의 0 -> N-1 열이 됨
        new_art[half][step] = art[step][half]

    # 십자 모양을 제외한 4개의 정사각형은 각각 개별적으로 시계 방향으로 90'씩 회전이 진행됩니다.
    for sr in (0, half+1):
        for sc in (0, half+1):
            # 4개의 정사각형 하나씩 보면서 회전
            for r in range(half):
                for c in range(half):
                    new_art[sr+c][sc+half - 1 - r] = art[sr+r][sc+c]

    # 회전한 것 반영
    for r in range(N):
        art[r] = new_art[r][:]


def solution():
    answer = 0
    for _ in range(4):
        answer += grouping()
        rotate_art()
    print(answer)


solution()
