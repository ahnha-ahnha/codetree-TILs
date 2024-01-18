import sys
from collections import deque

input = sys.stdin.readline
dx = [1, -1, 0, 0]
dy = [0, 0, 1, -1]

n, m, k = map(int, input().split())

# q에 참가자의 좌표를 저장
a = [list(map(int, input().split())) for _ in range(n)]
q = deque()
for i in range(m):
    x, y = map(int, input().split())
    q.append([x - 1, y - 1])

# 출구의 좌표를 저장하고 지도에 값을 10으로 한다
ex, ey = map(int, input().split())
ex -= 1
ey -= 1
a[ex][ey] = 10

ans = 0
for _ in range(k):
    qlen = len(q)
    # 현재 q에 있는 좌표만 불러와서 이동한다
    for _ in range(qlen):
        try:
            x, y = q.popleft()
            length = abs(ex - x) + abs(ey - y)
            cand = []
            for i in range(4):
                nx = x + dx[i]
                ny = y + dy[i]
                if 0 <= nx < n and 0 <= ny < n:
                    if a[nx][ny] == 0:
                        # 이동했을때 출구와의 거리가 더 가까워지면 cand에 저장
                        n_length = abs(ex - nx) + abs(ey - ny)
                        if n_length < length:
                            cand.append([nx, ny])
                    elif a[nx][ny] == 10:
                        # 출구에 도착하면 즉시 종료한다
                        raise NotImplemented

            if cand:
                # bfs에서 상하 이동을 먼저하기 때문에 cand[0]이 다음 좌표가 된다
                nx, ny = cand[0]
                ans += 1
                q.append([nx, ny])
            else:
                # 이동이 불가능하면 처음좌표 [x, y]를 다시 넣어준다
                q.append([x, y])

        except:
            ans += 1
    
    # 참가자가 없으면 종료
    if len(q) == 0:
        break
    
    # 브루트포스로 참가자와 출구를 포함한 최소 정사각형을 찾는다
    try:
        for l in range(1, 10):
            for i in range(n):
                for j in range(n):
                    if j + l >= n:
                        break
                    if i <= ex <= i + l and j <= ey <= j + l:
                        for x, y in q:
                            if i <= x <= i + l and j <= y <= j + l:
                                tx, ty, length = i, j, l
                                raise NotImplemented
    except:
        pass
    
    # 참가자 위치를 회전시키기 위해서 참가자 좌표 기록을 위한 c를 만든다
    # 참가자가 있는 좌표는 c에서 해당좌표 값에 1을 더해준다
    c = [[0 for _ in range(n)] for _ in range(n)]
    while q:
        x, y = q.popleft()
        c[x][y] += 1
    
    # rotate에 정사각형 범위만큼의 c를 넣어준다
    rotate = []
    for i in range(length + 1):
        rotate.append(c[tx + i][ty:ty + length + 1])
    # rotate를 회전시킨다
    rotate = list(zip(*rotate[::-1]))
    for i in range(length + 1):
        rotate[i] = list(rotate[i])
    # 정사각형 범위만큼 c와 rotate를 교체한다
    for i in range(length + 1):
        c[tx + i][ty:ty + length + 1] = rotate[i]
    
    # c에서 0이 아닌 좌표를 해당 값만큼 q에 넣어준다
    for i in range(n):
        for j in range(n):
            if c[i][j] > 0:
                for _ in range(c[i][j]):
                    q.append([i, j])

    # 위에서 참가자 좌표를 회전시키는 것과 똑같이 지도 a를 회전시킨다
    rotate = []
    for i in range(length + 1):
        rotate.append(a[tx + i][ty:ty + length + 1])
    rotate = list(zip(*rotate[::-1]))
    for i in range(length + 1):
        rotate[i] = list(rotate[i])
        # 벽은 1을 빼준다
        for j in range(length + 1):
            if 0 < rotate[i][j] < 10:
                rotate[i][j] -= 1
    for i in range(length + 1):
        a[tx + i][ty:ty + length + 1] = rotate[i]
    
    # 출구 좌표를 수정해준다
    for i in range(n):
        for j in range(n):
            if a[i][j] == 10:
                ex, ey = i, j

print(ans)
print(ex + 1, ey + 1)