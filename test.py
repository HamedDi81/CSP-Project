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
    max_neighbor = 0
    min_domain = 100000
    index = 0

    for i in range(len(node.salons)):
        if len(node.salons[i].domain) > 1 :
            if len(node.salons[i].domain) < min_domain:
                min_domain = len(node.salons[i].domain)
                index = i
            
            elif len(node.salons[i].domain) == min_domain:
                if len(node.salons[i].neighbors) > max_neighbor:
                    max_neighbor = len(node.salons[i].neighbors)
                    index = i
        
        
    return index


def LCV(node: Node, salon: int) -> list[int]:
    domain_sort = node.salons[salon].domain.copy()
    score = 0
    for n in node.salons[salon].neighbors:
        if len(n.domain) == 1 and n.domain[0] in node.salons[salon].domain:
            domain_sort.remove(n.domain[0])

    for d in domain_sort:
        for n in node.salons[salon].neighbors:
            if d in n.domain:
                score += 1
        domain_sort[domain_sort.index(d)] = (score, d)
        score = 0

    domain_sort.sort(key = lambda x: x[0], reverse = True)
    for i in domain_sort:
        domain_sort[domain_sort.index(i)] = i[1]

    return domain_sort


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
    salons = getInput()

    problem = Node(salons)
    result = backtracking(problem)

    if result == None:
        print('No')
        return None

    for salon in result.salons:
        print(salon.domain[0] + 1, end = ' ')

if __name__ == '__main__':
    main()