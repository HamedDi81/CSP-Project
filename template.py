class Node:
    salons: list['Salon']
    R: dict[tuple[int, int], list[tuple[int]]]


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


def getConstaint(salons: list['Salon']):
    pass


def MRV(node: Node) -> int:
    pass


def LCV(node: Node, salon: int) -> list[int]:
    pass


def forward_checking(node: Node, salon: int, value: int) -> None:
    pass


def AC3(node: Node) -> None:
    pass


def backtracking(root: Node) -> Node:
    pass


n: int
m: int
e: int
salons: list['Salon']


def getInput():
    globals()['n'], globals()['m'] = (int(x) for x in input().split())
    globals()['salons'] = []
    for i in range(n):
        salons.append(Salon())

    for i in range(m):
        for group in input().split():
            group = int(group) - 1
            salons[i].addDomain(group)

    globals()['e'] = int(input())
    for i in range(e):
        a, b = (int(x) - 1 for x in input().split())
        salons[a].addNeighbor(salons[b])


def main():
    getInput()
