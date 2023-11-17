N, Q = map(int, input().split())
q1 = list(map(int, input().split()))

p, a = [0]+q1[1:N+1], [0]+q1[N+1:2*N+1]
# power <= N 으로 주어지는데, 실제로 log2 N < 20(이진트리)
for i in range(1, N+1):
    if a[i] > 20:
        a[i] = 20

noti = [True]*(N+1)
n_listen = [0]+[0]*N
diff = [[0 for i in range(22)] for j in range(N+1)]

for i in range(1, N+1):
    cur = i # 1번 영향끼치는 모든 거 계산
    c = a[i]
    diff[cur][c] += 1
    while p[cur] and c: # 부모가 있을 때 & 권한이 있을 떄, 트리 올라가면서 갱신 
        cur = p[cur]
        c -= 1 # 한 층 올라왔응게
        if c:
            diff[cur][c] += 1 # 나한테 diff c인 애 한 명 더 있네
        n_listen[cur] += 1 # 한 명 더 올라올 수 있네

def toggle_noti(chatroom_id):
    cur = p[chatroom_id] # 부모부터 바꾸기 시작
    num = 1 # diff 값 > 자기 = 1 / 부모 층 = 2 / 조부모 층 = 3
    while cur:
        for i in range(num, 22):
            n_listen[cur] += diff[chatroom_id][i] if not noti[chatroom_id] else -diff[chatroom_id][i]
            if i > num:
                diff[cur][i-num] += diff[chatroom_id][i] if not noti[chatroom_id] else -diff[chatroom_id][i]
        if not noti[cur]:
            break
        cur = p[cur]
        num += 1
    noti[chatroom_id] = not noti[chatroom_id]

def set_authority(chatroom_id, authority):
    before = a[chatroom_id]
    authority = min(authority, 20)
    a[chatroom_id] = authority

    diff[chatroom_id][before] -= 1
    if noti[chatroom_id]:
        cur = p[chatroom_id]
        num = 1
        # 상위 채팅으로 이동하며 nx와 val 값을 갱신합니다.
        while cur:
            if before >= num:
                n_listen[cur] -= 1
            if before > num:
                diff[cur][before - num] -= 1
            if not noti[cur]:
                break
            cur = p[cur]
            num += 1

    diff[chatroom_id][authority] += 1
    if noti[chatroom_id]:
        cur = p[chatroom_id]
        num = 1
        # 상위 채팅으로 이동하며 nx와 val 값을 갱신합니다.
        while cur:
            if authority >= num:
                n_listen[cur] += 1
            if authority > num:
                diff[cur][authority - num] += 1
            if not noti[cur]:
                break
            cur = p[cur]
            num += 1

def change_parents(chatroom_id1, chatroom_id2):
    before_noti1 = noti[chatroom_id1]
    before_noti2 = noti[chatroom_id2]

    if noti[chatroom_id1]:
        toggle_noti(chatroom_id1)
    if noti[chatroom_id2]:
        toggle_noti(chatroom_id2)

    p[chatroom_id1], p[chatroom_id2] = p[chatroom_id2], p[chatroom_id1]

    if before_noti1:
        toggle_noti(chatroom_id1)
    if before_noti2:
        toggle_noti(chatroom_id2)


for qi in range(Q-1):
    command = list(map(int, input().split()))

    cmd_type = command[0]
    if cmd_type == 200:
        # 알림망 설정 ON/OFF
        chatroom_id = command[1]
        toggle_noti(chatroom_id)
    elif cmd_type == 300:
        # 권한 세기 변경
        chatroom_id, authority = command[1], command[2]
        set_authority(chatroom_id, authority)
    elif cmd_type == 400:
        # 부모 채팅방 교환
        chatroom_id1, chatroom_id2 = command[1], command[2]
        change_parents(chatroom_id1, chatroom_id2)
    elif cmd_type == 500:
        # 알림을 받을 수 있는 채팅방 수 조회
        chatroom_id = command[1]
        print(n_listen[chatroom_id])
        #print(diff[chatroom_id])