def mul(arr):
    r = 1
    for el in arr:
        r *= el
    return r


class Pstate:
    def __init__(self, P):
        self.P = P
        self.Q = [1 - pi for pi in P]
    
    def __call__(self, s):
        return mul([
            self.P[i] if si else self.Q[i] 
            for i,si in enumerate(s)
        ])


class ExistPath:
    def __init__(self, graph):
        self.graph = graph
    
    def __call__(self, *, from_, to_, through):
        for v in self.graph[from_]:
            if v == to_:
                return True
            if v in through:
                through_ = [vertex for vertex in through if vertex != v]
                if self(from_=v, to_=to_, through=through_):
                    return True
        return False


def get_state(i, n):
    return [i&(1<<k) != 0 for k in range(n)]


class Workable:
    def __init__(self, graph, start_index, end_index):
        self.start_index = start_index
        self.end_index = end_index
        self.exist_path = ExistPath(graph)
    
    def __call__(self, s):
        through = [i+1 for i,si in enumerate(s) if si]
        return self.exist_path(
            from_=self.start_index,
            to_=self.end_index,
            through=through 
        )

n = 9 
start_index = 0
end_index = n + 1

E = {
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

workable = Workable(E, start_index, end_index)
p_state = Pstate(P)
all_states = [get_state(i, n) for i in range(2**n)]
workable_states = [*filter(workable, all_states)]
p_system = sum([p_state(s) for s in workable_states])
print("Ймовірність безвідмовної роботи системи:", p_system)
