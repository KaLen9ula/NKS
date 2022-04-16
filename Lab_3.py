from math import log


def mul(arr):
    r = 1
    for el in arr:
        r *= el
    return r


def get_state(i, n):
    return [1 if (i & (1<<k)) != 0 else 0 for k in range(n)]


class ExistPath:
    def __init__(self, graph):
        self.graph = graph

    def __call__(self, *,from_, to_, through):
        for v in self.graph[from_]:
            if v == to_:
                return True
            if v in through:
                through_ = [vertex for vertex in through if vertex != v]
                if self(from_=v, to_=to_, through=through_):
                    return True
        return False


class PState:
    def __init__(self, P):
        self.P = P
        self.Q = [1-pi for pi in P]
        
    def __call__(self, s):
        return mul([
            self.P[i] if si == 1 else self.Q[i]
            for i,si in enumerate(s) 
        ])


class Workable:
    def __init__(self, graph, start, end):
        self.start = start
        self.end = end
        self.exist_path = ExistPath(graph)

    def __call__(self, s):
        through = [i+1 for i,si in enumerate(s) if si == 1]
        return self.exist_path(
            from_=self.start,
            to_=self.end,
            through=through
        )
        

def factorial(n):
    return mul(range(1, n+1))


n = 9
start_index = 0
end_index = n+1

G = {
    0: [1, 2],         
    1: [0, 2, 3, 4],   
    2: [0, 1, 3, 5],   
    3: [1, 2, 4, 5],   
    4: [1, 3, 7, 8],   
    5: [2, 3, 6],      
    6: [5, 7, 9],      
    7: [4, 6, 8, 9],   
    8: [4, 7, 9, 10],  
    9: [6, 7, 8, 10],  
    10: []             
}

P = [
    0.46, 
    0.05, 
    0.98, 
    0.16, 
    0.77, 
    0.51, 
    0.83, 
    0.16, 
    0.28  
]

Q = [1-pi for pi in P]

T = 2027

k1 = 2
k2 = 2

workable = Workable(G, start_index, end_index)
p_state = PState(P)
all_states = [get_state(i, n) for i in range(2**n)]
workable_states = [*filter(workable, all_states)]

p_system = sum([p_state(state) for state in workable_states])
q_system = 1 - p_system
t_system = -T / log(p_system)
print("Дані системи без резервування")
print(f"{p_system = }")
print(f"{q_system = }")
print(f"{t_system = }")


def generalLoaded(k, T, p_system):
    p_reserved_system = 1 - (1 - p_system)**(k+1)
    q_reserved_system = 1 - p_reserved_system
    t_reserved_system = -T / log(p_reserved_system)

    return p_reserved_system, q_reserved_system, t_reserved_system


def generalNonloaded(k, T, p_system):
    p_reserved_system = 1 - (1 - p_system) / factorial(k+1)
    q_reserved_system = 1 - p_reserved_system
    t_reserved_system = -T / log(p_reserved_system)

    return p_reserved_system, q_reserved_system, t_reserved_system


def seperativeNonloaded(k, T, Q, workable_states):
    Q_reserved = [qi**(k+1) for qi in Q]
    P_reserved = [1-qr for qr in Q_reserved]
    p_reserved_state = PState(P_reserved)

    p_reserved_system = 1 - 1 / factorial(k + 1) * (1 - sum([
        p_reserved_state(state) 
        for state in workable_states
    ]))
    q_reserved_system = 1 - p_reserved_system
    t_reserved_system = -T / log(p_reserved_system)

    return p_reserved_system, q_reserved_system, t_reserved_system


print(f"Загальне навантаженне (k={k1})")

p_reserved_system, q_reserved_system, t_reserved_system = \
    generalLoaded(k1, T, p_system)
print(f"{p_reserved_system = }")
print(f"{q_reserved_system = }")
print(f"{t_reserved_system = }")
print(f"Gp = {p_reserved_system / p_system}")
print(f"Gq = {q_reserved_system / q_system}")
print(f"Gt = {t_reserved_system / T}")


print(f"Загальне ненавантаженне (k={k2})")

p_reserved_system, q_reserved_system, t_reserved_system = \
    generalNonloaded(k2, T, p_system)
print(f"{p_reserved_system = }")
print(f"{q_reserved_system = }")
print(f"{t_reserved_system = }")
print(f"Gp = {p_reserved_system / p_system}")
print(f"Gq = {q_reserved_system / q_system}")
print(f"Gt = {t_reserved_system / T}")
