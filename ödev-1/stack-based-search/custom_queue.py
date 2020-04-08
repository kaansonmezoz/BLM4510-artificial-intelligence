from functools import cmp_to_key

class Priority_Queue:
    def __init__(self):
        self.queue = []
        self.items = set()
    
    def add_node(self, node):
        self.queue.append(node)
        self.items.add(node)
        self.sort()
        
    def update_node(self, node, source_to_current_cost):
        node.set_source_to_current_cost(source_to_current_cost)
        self.sort()
    
    def sort(self): 
        self.queue.sort(key = cmp_to_key(self.compare))
    
    def compare(self, first_node, second_node):
        difference = first_node.total_cost() - second_node.total_cost()
        
        if difference != 0:
            return difference
        
        # hangisinin goal'e gitmesi daha az maliyetli ise o önce gelir.
        return first_node.get_current_to_goal_cost() - second_node.get_current_to_goal_cost() 
        
    def is_empty(self):
        return len(self.queue) == 0
    
    def exists(self, node):
        return node in self.items
    
    def not_exists(self, node):
        return node not in self.items
    
    def pop(self):
        node = self.queue.pop(0)
        self.items.discard(node)
        return node
    
    def should_update_node(self, node, possible_total_cost):
        return self.exists(node) and node.total_cost() > possible_total_cost