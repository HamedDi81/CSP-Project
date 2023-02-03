from template import Node, isSatisfy, isComplete, isFailure, MRV, LCV, forward_checking

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