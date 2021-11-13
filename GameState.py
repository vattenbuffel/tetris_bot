from Actions import Actions
class GameState:
    def __init__(self, board, player, action:Actions, depth, parent):
        self.board = board
        self.parent = parent
        self.player = player
        self.action:Actions = action
        self.board = board
        self.depth = depth + 1# How deep this child is or how many actions it took to get here

        self.end = False
        self.children = []
        self.value = -(10**100)

    def best_child(self, end_child=False):
        # returns the next best state. If end_child it will go through all childs and grand children etc to find the best end state. If false then it will find the best child
        # If no children, return this

        if self.children == []:
            return self

        best_val = self.get_value()

        best_child = None
        for child in self.children:
            if child.value == best_val:
                best_child = child
                break
        
        if end_child:
            return best_child.best_child(end_child=True)
        return best_child
        
        raise Exception("Should not be able to get here. One child should have best val")

    def get_value(self):
        # Loops over all the children and sets this nodes value to the best value of it's children 
        if len(self.children) == 0:
            return self.value

        best_val = self.value
        for child in self.children:
            val = child.get_value()
            best_val = max(val, best_val)
        
        self.value = best_val
        return best_val

    def actions_get(self):
        # Returns all actions taken to get to this stateS
        actions = []
        parent = self
        while parent != None:
            actions.append(parent.action)
            parent = parent.parent
        
        actions.reverse()
        return actions[1:]
        
    def children_actions_get(self):
        # Returns the actions of all best children.
        children = [self]
        child = self
        while len(child.children):
            for child_new in child.children:
                if child_new.value == child.value:
                    child = child_new
                    break
            children.append(child)

        actions = [child.action for child in children]
        return actions

        








    