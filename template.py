class Node:
    salons: list['Salon']

    def __init__(self, salons: list['Salon'] = []) -> None:
        self.salons = salons

    def addSalon(self, salon: 'Salon') -> None:
        self.salons.append(salon)


class Salon:
    neighbors: list['Salon']
    domain: list[int]

    def __init__(self) -> None:
        self.neighbors = []
        self.domain = []

    def addDomain(self, group: int):
        self.domain.append(group)

    def addNeighbor(self, salon: 'Salon'):
        self.neighbors.append(salon)


def MRV(node: Node) -> int:
    pass


def LCV(node: Node, salon: int) -> list[int]:
    pass


def forward_checking(node: Node, salon: int, group: int) -> None:
    pass


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
    pass


def getInput():
    n, m = (int(x) for x in input().split())
    salons : list['Salon'] = []
    for i in range(n):
        salons.append(Salon())

    for i in range(m):
        for salon in input().split():
            salon = int(salon) - 1
            salons[salon].addDomain(i)

    e = int(input())
    for i in range(e):
        a, b = (int(x) - 1 for x in input().split())
        salons[a].addNeighbor(salons[b])
        salons[b].addNeighbor(salons[a])


def main() -> None:
    salons = getInput()

    problem = Node(salons)
    result = backtracking(problem)

    if result == None:
        print('No')
        return None

    for salon in result:
        print(salon.domain[0], end = ' ')
