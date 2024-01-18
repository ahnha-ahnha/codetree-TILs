import sys
import copy

input = sys.stdin.readline
#input----------
# def -1
def int_minus(x):
    return int(x)-1
n, m , k  = map(int, input().split())
a = [list(map(int, input().split())) for _ in range(n)] # 벽 위치
people = [tuple(map(int_minus, input().split())) for _ in range(m)] # 사람위치 좌표 (+1씩 되어있음)

# 출력해야할 정답값
pathn = 0 # 모든 참가자들의 이동 거리 합
exit = tuple(map(int_minus, input().split()))


# move ============
# 1) 움직일 수 있는 곳 확인 -> eixt과 값 빼기
# 2) 움직이기 - pathn 계산
def move(pathn):
    global people
    for i, p in enumerate(people):
        row = exit[0]- p[0] # row방 어디로 얼마나 가야하는지
        column = exit[1]-p[1] # column방향 어디로 얼마나 가야하는지
        # 움직이는 우선순위: row -> column / 그 방향이 벽이 아니여야 가능
        # row먼저 check
        if row !=0:
            move = 1 if row>0 else -1
            newpr, newpc = p[0]+move, p[1]
            if 0<=newpr<n and 0<=newpc<n and a[newpr][newpc]==0:
                #움직일 수 있음
                people[i] = (newpr, newpc)
                pathn +=1
                continue # 움직였으면, 감
        # 그다음 column check -> elif 대신 if써야함
        if column !=0:
            move = 1 if column>0 else -1
            newpr, newpc = p[0], p[1] + move
            if 0<=newpr<n and 0<=newpc<n and a[newpr][newpc]==0:
                #움직일 수 있음
                people[i] = (newpr, newpc)
                pathn +=1
    return pathn

# distance (rotate box search) ============
def distance(one, two):
    # rotation 을 위한 distance계산
    # input: 두 좌표 (하나는 출구, 하나는 사람)
    # ouput: (distance, 작은 r좌표, 작은 c좌표)
    row = abs(one[0]-two[0])
    column = abs(one[1] - two [1])
    d,r,c = max(row, column), min(one[0], two[0]), min(one[1], two[1])
    if row>column:
        # 변의 길이를 결정하는게 row라면, row는 그대로. column시작점을 옮길 수 있음
        c = max(one[1], two[1])- d
        while c<0:
            c+=1
        return (d,r,c)
    elif row<column:
        r = max(one[0], two[0])- d
        while r<0:
            r+=1
        return (d,r,c)
    else:
        return (d,r,c)

# rotate ============
def rotate():
    global a, people, exit
    # 1)  rotate할 위치 찾기-------
    distancelist =[]
    for p in people:
        distancelist.append(distance(exit, p))
    distancelist= sorted(distancelist) # distance, r, c 순으로 작은것 순으로 배열
    d, r, c = distancelist[0] # roated할 크기, distance 정해짐

    #2) rotate하기 --------
    tempa=copy.deepcopy(a) #
    newpeople =[]
    newexit =exit
    for i in range(d+1):
        for j in range(d+1):
            if tempa[r+i][c+j] >0: # 2) 벽 -1
                tempa[r+i][c+j]-=1
            a[r+j][c+d-i] = tempa[r+i][c+j] # 1)공간 rotate
            while (r+i, c+j) in people: # 3) people 안에 있으면, 사람도 rotate된 값으로
                people.remove((r+i, c+j))
                newpeople.append((r+j, c+d-i))
            if (r+i,c+j) == exit: # 4) exit rotate & update
                newexit =(r+j, c+d-i)

    people = people+newpeople # 2) people update
    exit = newexit


# main ============
for i in range(k):
    pathn = move(pathn) # 1) 움직이기

    while exit in people: # 2) exit으로 나간 것 정리
        people.remove((exit))
    if len(people) ==0:
        break
    rotate() #3) 돌리기



#정답 출력
print(pathn)
print(exit[0]+1, end=" ")
print(exit[1]+1)