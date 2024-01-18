from heapq import heappush, heappop
import heapq

Q = int(input())
command = list(input().split())
J = int(command[1])  # 채점기 개수
Waiting_Judger = list(range(1, J + 1))
Waiting_Queue = []  # 채점 대기 큐 (우선순위, 시간, URL)
Judging = {}  # 현재 채점기 작동 J_id : [시작시간, URL]
History = {}  # 도메인별 마지막 채점 시간 기록 Domain : [Start, Gap]

heappush(Waiting_Queue, (0, 1, command[2]))

for _ in range(Q - 1):
    command = list(input().split())
    cmd_type, t = int(command[0]), int(command[1])

    if cmd_type == 200:
        p, u = int(command[2]), command[3]
        # 채점 대기 큐에서 같은 URL이 있는지 확인
        if not any(u == queued_u for _, _, queued_u in Waiting_Queue):
            heappush(Waiting_Queue, (p, t, u))

    elif cmd_type == 300:
        if Waiting_Queue and Waiting_Judger:
            while Waiting_Queue:
                p, enter_time, url = heappop(Waiting_Queue)
                if url not in History or t >= History[url][0] + 3 * History[url][1]:
                    J_id = min(Waiting_Judger)
                    Judging[J_id] = [t, url]
                    Waiting_Judger.remove(J_id)
                    break

    elif cmd_type == 400:
        J_id = int(command[2])
        if J_id in Judging:
            start_time, url = Judging.pop(J_id)
            History[url] = [start_time, t - start_time]
            Waiting_Judger.append(J_id)

    elif cmd_type == 500:
        print(len(Waiting_Queue))