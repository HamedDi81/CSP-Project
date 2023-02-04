import sys
class Node:
    salons: list['Salon']

    def __init__(self, salons: list['Salon']) -> None:
        self.salons = salons

    def addSalon(self, salon: 'Salon') -> None:
        self.salons.append(salon)
    
    def copy(self) -> 'Node':
        newNode = Node([])
        for salon in self.salons:
            newNode.addSalon(salon.copy())
        return newNode

class Salon:
    neighbors: list[int]
    domain: list[int]
    assigned: bool

    def __init__(self, neighbors: list['Salon'], domain: list[int], assigned = False) -> None:
        self.neighbors = neighbors
        self.domain = domain
        self.assigned = assigned

    def addDomain(self, group: int) -> None:
        self.domain.append(group)

    def addNeighbor(self, salon: int) -> None:
        self.neighbors.append(salon)

    def copy(self) -> 'Salon':
        return Salon(self.neighbors, self.domain.copy(), self.assigned)


def MRV(node: Node) -> int:
    max_neighbor = 0
    min_domain = sys.maxsize
    index = 0

    for i in range(len(node.salons)):
        if not node.salons[i].assigned:
            if len(node.salons[i].domain) < min_domain:
                min_domain = len(node.salons[i].domain)
                index = i
    
    for i in range(len(node.salons)):
            if len(node.salons[i].domain) == min_domain and not node.salons[i].assigned:
                if len(node.salons[i].neighbors) > max_neighbor:
                    max_neighbor = len(node.salons[i].neighbors)
                    index = i
        
    return index


def LCV(node: Node, salon: int) -> list[int]:
    domain_sort = node.salons[salon].domain.copy()
    score = 0

    i = 0
    while i < len(domain_sort):
        d = domain_sort[i]
        for n in node.salons[salon].neighbors:
            neighbor = node.salons[n]
            if d in neighbor.domain:
                if len(neighbor.domain) == 1:
                    domain_sort.remove(d)
                    score = -1
                    i -= 1
                    break
                else : score += 1
        if score != -1:
            domain_sort[domain_sort.index(d)] = (score, d)
        score = 0
        i += 1

    domain_sort.sort(key = lambda x: x[0])
    for i in domain_sort:
        domain_sort[domain_sort.index(i)] = i[1]

    return domain_sort


def forward_checking(node: Node, salon: int, group: int) -> None:
    for neighbor in node.salons[salon].neighbors:
        neighbor = node.salons[neighbor]
        if group in neighbor.domain:
            neighbor.domain.remove(group)

def constraint_varibale(node:Node) -> list[tuple['Salon', 'Salon']]:
    constraint=list()
    for salon in node.salons:
        for neighbor in salon.neighbors:
            neighbor = node.salons[neighbor]
            constraint.append((salon,neighbor))
    return constraint


def AC3(node: Node , queue:list=None) -> bool:
    if queue == None:
        queue = constraint_varibale(node)

    while queue:
        (salon_i,salon_j)= queue.pop(0)
        if remove_inconsistent_values(salon_i, salon_j):
            if len(salon_i.domain) == 0: 
                return False
                
            for salon_k in salon_i.neighbors:
                salon_k = node.salons[salon_k]
                if (salon_k, salon_i) not in queue: #TODO debug test
                    queue.append((salon_k, salon_i))
                    
    return True
      

def remove_inconsistent_values(cell_i : Salon, cell_j : Salon) -> bool: #returns true if a value is removed
    removed = False

    for value in cell_i.domain:
        if not any([value != poss for poss in cell_j.domain]):
        # if cell_j.domain == [value]:
            cell_i.domain.remove(value)
            removed = True
        
    return removed

def isSatisfy(node: Node, salon: int, group: int) -> bool:
    for neighbor in node.salons[salon].neighbors:
        neighbor = node.salons[neighbor]
        if neighbor.domain == [group]:
            return False

    return True


def isComplete(node: Node) -> bool:
    for salon in node.salons:
        if not salon.assigned:
            return False

    return True


def isFailure(node: Node) -> bool:
    for salon in node.salons:
        if len(salon.domain) == 0:
            return True

    return False


def backtracking(root: Node) -> Node | None:
    stack = [(root, None, None)]

    while stack:
        state, salon, group = stack.pop()

        if isFailure(state):
            continue

        if isComplete(state):
            return state

        if salon != None:
            forward_checking(state, salon, group)
        else:
            if not AC3(state):
                return None

        salon = MRV(state)
        for group in LCV(state, salon)[-1::-1]:
            if isSatisfy(state, salon, group):
                child = state.copy()
                child.salons[salon].domain = [group]
                child.salons[salon].assigned = True
                stack.append((child, salon, group))
        

    return None


def testGenerator() -> list['Salon']:
    from random import randint as rant, choices
    n = int(input('n = '))
    m = int(input('m = '))
    e = int(input('e = '))

    salons : list['Salon'] = []
    for i in range(n):
        salons.append(Salon([], []))

    L = [str(i) for i in range(1,n+1)]
    for i in range(m):
        chs = choices(L,k=rant(1,n))
        for k in range(len(chs)):
            j = k+1
            while j < len(chs):
                if chs[k] == chs[j]:
                    chs.pop(j)
                    j -= 1
                j += 1
        chs.sort()
        for salon in chs:
            salon = int(salon) - 1
            salons[salon].addDomain(i)

    # e = rant(m*2,m*(m-1)/2)

    edges = set()
    while len(edges) != e:
        t = tuple(x for x in choices(L,k=2))
        t_e = (t[1],t[0])
        if t_e not in edges and t[0] != t[1]:
            edges.add(t)
            
    for edge in edges:
        a, b = (int(edge[0]) - 1, int(edge[1]) -1)
        salons[a].addNeighbor(b)
        salons[b].addNeighbor(a)
    
    return salons

def getInput():
    n, m = (int(x) for x in input().split())
    salons : list['Salon'] = []
    for i in range(n):
        salons.append(Salon([], []))

    for i in range(m):
        for salon in input().split():
            salon = int(salon) - 1
            salons[salon].addDomain(i)

    e = int(input())
    for i in range(e):
        a, b = (int(x) - 1 for x in input().split())
        salons[a].addNeighbor(b)
        salons[b].addNeighbor(a)
    
    return salons


def main() -> None:
    # salons = getInput()
    salons = testGenerator()

    problem = Node(salons)

    from datetime import datetime

    start = datetime.now()
    result = backtracking(problem)
    end = datetime.now()
    print(end-start)
    if result == None:
        print('No')
        return None

    for salon in result.salons:
        print(salon.domain[0] + 1, end = ' ')

if __name__ == '__main__':
    main()