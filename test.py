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
    neighbors: list['Salon']
    domain: list[int]

    def __init__(self, neighbors: list['Salon'], domain: list[int]) -> None:
        self.neighbors = neighbors
        self.domain = domain

    def addDomain(self, group: int):
        self.domain.append(group)

    def addNeighbor(self, salon: 'Salon'):
        self.neighbors.append(salon)

    def copy(self) -> 'Salon':
        return Salon(self.neighbors, self.domain.copy())


def MRV(node: Node) -> int:
    for i in range(len(node.salons)):
        if len(node.salons[i].domain) > 1:
            return i


def LCV(node: Node, salon: int) -> list[int]:
    return node.salons[salon].domain


def forward_checking(node: Node, salon: int, group: int) -> None:
    node.salons[salon].domain = [group]


def AC3(node: Node) -> None:
    pass


def isSatisfy(node: Node, salon: int, group: int) -> bool:
    for neighbor in node.salons[salon].neighbors:
        if neighbor.domain == [group]:
            return False

    return True


def isComplete(node: Node) -> bool:
    for salon in node.salons:
        if len(salon.domain) != 1:
            return False

    return True


def isFailure(node: Node) -> bool:
    for salon in node.salons:
        if len(salon.domain) == 0:
            return True

    return False


def backtracking(root: Node) -> Node | None:
    stack = [root]

    while stack:
        state = stack.pop()

        if isComplete(state):
            return state

        salon =  MRV(state)
        for group in LCV(state, salon)[-1::-1]:
            if isSatisfy(state, salon, group):
                child = state.copy()
                forward_checking(child, salon, group)
                stack.append(child)
        

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
        salons[a].addNeighbor(salons[b])
        salons[b].addNeighbor(salons[a])
    
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
        salons[a].addNeighbor(salons[b])
        salons[b].addNeighbor(salons[a])
    
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