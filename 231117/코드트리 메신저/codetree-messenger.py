# class Chatroom:
#     def __init__(self, id, parent=None, authority=0):
#         self.id = id
#         self.parent = parent
#         self.children = []
#         self.authority = authority
#         self.notification_on = True

#     def add_child(self, child):
#         self.children.append(child)

#     def toggle_notification(self):
#         self.notification_on = not self.notification_on

#     def set_authority(self, authority):
#         self.authority = authority

#     def set_parent(self, parent):
#         self.parent = parent

# def initialize_chatrooms(parents, authorities):
#     chatrooms = {0: Chatroom(0)}
#     for i, parent_id in enumerate(parents, start=1):
#         chatrooms[i] = Chatroom(i, chatrooms[parent_id], authorities[i-1])
#         chatrooms[parent_id].add_child(chatrooms[i])
#     return chatrooms
        
# def count_reachable_chatrooms(chatroom):
#     count = 0
#     current = chatroom.parent  # 현재 채팅방의 부모부터 시작
#     steps = chatroom.authority

#     while current and steps > 0:
#         if current.notification_on:
#             count += 1
#         current = current.parent
#         steps -= 1

#     return count

### class 화 포기 & Solution 참조

N, Q = map(int, input().split())

# q1 = 100 초기화
q1 = list(map(int, input().split()))
p = [None]+q1[1:N+1]
a = [None]+q1[N+1:2*N+1]
for i in range(1, N+1):
        # 채팅의 권한이 20을 초과하는 경우 20으로 제한합니다.
        if a[i] > 20:
            a[i] = 20

# chatrooms = initialize_chatrooms(p, a)
notification = [None]+[False]*N
num_can_reach = [None]+[0]*N
diff = [[0 for i in range(22)] for j in range(N+1)]

for i in range(1, N+1):
    cur = i
    c = a[i]
    diff[cur][c] += 1
    while p[cur] and c: # 부모가 있을 때 & 권한이 있을 떄, 트리 올라가면서 갱신 
        cur = p[cur]
        c -= 1 # 한 층 올라왔응게
        if c:
            diff[cur][c] += 1 # 나한테 diff c인 애 한 명 더 있네
        num_can_reach[cur] += 1 # 한 명 더 올라올 수 있네

def toggle_notification(chatroom_id):
    cur = p[chatroom_id]
    num = 1
    while cur:
        for i in range(num, 22):
            num_can_reach[cur] += diff[chatroom_id][i] if notification[chatroom_id] else -diff[chatroom_id][i]
            if i > num:
                diff[cur][i-num] += diff[chatroom_id][i] if notification[chatroom_id] else -diff[chatroom_id][i]
        if notification[cur]:
            break
        cur = p[cur]
        num += 1
    notification[chatroom_id] = not notification[chatroom_id]

def set_authority(chatroom_id, authority):
    before = a[chatroom_id]
    authority = min(authority, 20)
    a[chatroom_id] = authority

    diff[chatroom_id][before] -= 1
    if not notification[chatroom_id]:
        cur = p[chatroom_id]
        num = 1
        # 상위 채팅으로 이동하며 nx와 val 값을 갱신합니다.
        while cur:
            if before >= num:
                num_can_reach[cur] -= 1
            if before > num:
                diff[cur][before - num] -= 1
            if notification[cur]:
                break
            cur = p[cur]
            num += 1

    diff[chatroom_id][authority] += 1
    if not notification[chatroom_id]:
        cur = p[chatroom_id]
        num = 1
        # 상위 채팅으로 이동하며 nx와 val 값을 갱신합니다.
        while cur:
            if authority >= num:
                num_can_reach[cur] += 1
            if authority > num:
                diff[cur][authority - num] += 1
            if notification[cur]:
                break
            cur = p[cur]
            num += 1

def change_parents(chatroom_id1, chatroom_id2):
    before_noti1 = notification[chatroom_id1]
    before_noti2 = notification[chatroom_id2]

    if not notification[chatroom_id1]:
        toggle_notification(chatroom_id1)
    if not notification[chatroom_id2]:
        toggle_notification(chatroom_id2)

    p[chatroom_id1], p[chatroom_id2] = p[chatroom_id2], p[chatroom_id1]

    if not before_noti1:
        toggle_notification(chatroom_id1)
    if not before_noti2:
        toggle_notification(chatroom_id2)


for qi in range(Q-1):
    command = list(map(int, input().split()))

    cmd_type = command[0]
    if cmd_type == 200:
        # 알림망 설정 ON/OFF
        chatroom_id = command[1]
        toggle_notification(chatroom_id)
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
        print(num_can_reach[chatroom_id])
        #print(diff[chatroom_id])