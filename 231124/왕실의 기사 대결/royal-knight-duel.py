import sys
from collections import deque

input = sys.stdin.readline

# 상우하좌 순서
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

l, n, q = map(int, input().split())

# 입력받은 체스판 정보만 저장
a = [list(map(int, input().split())) for _ in range(l)]

# knight: 입력받은 기사의 정보
# shield: 몇 번째 기사의 방패가 있는지 저장
# chess: 방패가 있는 좌표들
knight = [0]
shield = [[0 for _ in range(l)] for _ in range(l)]
chess = dict()
for i in range(1, n+1):
    r, c, h, w, k = map(int, input().split())
    chess[i] = []
    for j in range(h):
        for jj in range(w):
            shield[r-1+j][c-1+jj] = i
            chess[i].append([r-1+j, c-1+jj])
    knight.append([r-1, c-1, h, w, k])

ans = 0
damage = [0 for _ in range(n+1)]  # 인덱스번째 기사가 받은 대미지 저장
for order in range(q):
    i, d = map(int, input().split())
    if knight[i] == 0:
        continue
    # 다음 칸에 벽이 있는지 확인
    wall = 0  # wall = 1 이면 이동 불가능
    x, y, _, _, _ = knight[i]
    qu = deque()
    qu.append([x, y])
    check = [[0 for _ in range(l)] for _ in range(l)]
    check[x][y] = 1
    move_shield = [0 for _ in range(n+1)]  # 몇 번째 방패가 이동하는지
    move_shield[i] = 1
    while qu:
        x, y = qu.popleft()
        for j in range(4):
            nx = x + dx[j]
            ny = y + dy[j]
            if 0 <= nx < l and 0 <= ny < l:
                if check[nx][ny] == 0:
                    if shield[nx][ny] == shield[x][y]:
                        check[nx][ny] = 1
                        qu.append([nx, ny])
            # d방향으로 이동할 때는 다른 방패를 밀어내는지, 다음 칸이 벽인지 확인
            if j == d:
                if 0 <= nx < l and 0 <= ny < l:
                    if check[nx][ny] == 0:
                        if shield[nx][ny] > 0 and shield[nx][ny] != shield[x][y]:
                            check[nx][ny] = 1
                            qu.append([nx, ny])
                            move_shield[shield[nx][ny]] = 1
                        if a[nx][ny] == 2:
                            wall = 1
                            break
                else:
                    wall = 1
                    break
        if wall == 1:
            break

    # 기사 이동
    # temp_shield에 방패를 먼저 이동시키고 나중에 shield를 수정
    temp_shield = [[0 for _ in range(l)] for _ in range(l)]
    if wall == 0:
        for idx in range(1, n+1):
            if move_shield[idx] == 1:
                temp_chess = []  # chess 수정을 위한 임시 리스트
                for x, y in chess[idx]:
                    nx = x + dx[d]
                    ny = y + dy[d]
                    temp_shield[nx][ny] = idx
                    temp_chess.append([nx, ny])
                # idx 번째 기사의 chess와 knight에서 좌표값 수정
                chess[idx] = temp_chess
                knight[idx][:2] = chess[idx][0]

        # 방패가 있는 좌표 수정
        for x in range(l):
            for y in range(l):
                if shield[x][y] > 0 and temp_shield[x][y] == 0:
                    if move_shield[shield[x][y]] == 1:
                        shield[x][y] = 0
                if temp_shield[x][y] > 0:
                    shield[x][y] = temp_shield[x][y]

        # 함정 확인
        for x in range(l):
            for y in range(l):
                if a[x][y] == 1 and shield[x][y] > 0:
                    idx = shield[x][y]
                    # 밀어내는 기사는 제외하고 밀려난 기사만 피해를 받음
                    if move_shield[idx] == 1 and idx != i:
                        if knight[idx] != 0:
                            knight[idx][-1] -= 1
                            damage[idx] += 1
                            # 체력이 0이되면 knight, damage를 0으로 초기화
                            if knight[idx][-1] == 0:
                                # chess에서 좌표를 불러와서 shield 값을 0으로
                                for xx, yy in chess[idx]:
                                    shield[xx][yy] = 0
                                knight[idx] = 0
                                damage[idx] = 0
                                continue
                                
print(sum(damage))