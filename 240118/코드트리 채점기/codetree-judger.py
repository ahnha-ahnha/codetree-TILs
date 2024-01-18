from heapq import heappush, heappop, heapify
import sys
input = sys.stdin.readline
MAX = float('inf')

Q = int(input())
querys = [input().split() for _ in range(Q)]
grading_domain = dict()
prev_ended_domain = dict()
domains = set()
waited_task = dict()
waited_url = set()
tot_waited = 0

for i in range(Q) :
    query, *body = querys[i]
    if query <= '200' :
        domain = body[-1].split('/')[0]
        domains.add(domain)
        grading_domain[domain] = False
        prev_ended_domain[domain] = -1
        if domain not in waited_task :
            waited_task[domain] = list()

_, N, u0 = querys[0]
d0 = u0.split('/')[0]
graders = [(-1,-1) for _ in range(int(N))]
empty_graders = list(range(int(N)))
heapify(empty_graders)
heappush(waited_task[d0], (1, 0, u0))
waited_url.add(u0)
tot_waited += 1

for i in range(1, Q) :
    query, *body = querys[i]
    if query == '200' :
        t, p, u = body
        d = u.split('/')[0]
        if u in waited_url :
            continue
        waited_url.add(u)
        heappush(waited_task[d], (int(p), int(t), u))
        tot_waited += 1
    elif query == '300' :
        if not empty_graders or not tot_waited:
            continue
        t = int(body[0])
        target_d, priority, target_u = '', (MAX, MAX), ''
        for d in domains :
            if grading_domain[d] or prev_ended_domain[d] > t or not waited_task[d]:
                continue
            tp, tt, tu = waited_task[d][0]
            if priority <= (tp, tt) :
                continue
            target_d, priority, target_u = d, (tp, tt), tu

        if priority < (MAX, MAX) :
            idx = heappop(empty_graders)
            grading_domain[target_d] = True
            waited_url.discard(target_u)
            graders[idx] = (t, target_d)
            heappop(waited_task[target_d])
            tot_waited -= 1

    elif query == '400' :
        t, idx = map(int, body)
        idx -= 1
        if graders[idx] == (-1, -1) :
            continue
        s, d = graders[idx]
        graders[idx] = (-1, -1)
        grading_domain[d] = False
        prev_ended_domain[d] = s + (t - s)*3
        heappush(empty_graders, idx)
    else :
        print(tot_waited)