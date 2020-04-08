from functools import cmp_to_key

class Priority_Queue:
    def __init__(self):
        self.queue = []
        self.items = set()
        self.max_item_count = 0
    
    def add_node(self, node):
        self.queue.append(node)
        self.items.add(node)
        
        size = len(self.items)
        
        if size > self.max_item_count:
            self.max_item_count = size
            
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
    
    def get_max_item_count(self):
        return self.max_item_count

class Priority_Queue_Heap:
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
        arr = self.queue
        size = len(self.items)
  
        for i in range(size//2 - 1, -1, -1): 
            self.heapify(i) 
            
        for i in range(size-1, 0, -1): 
            arr[i], arr[0] = arr[0], arr[i]
            self.heapify(i)         
    
    def heapify(self, i):
        arr = self.queue
        
        size = len(self.items)
        largest = i
        
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < size and arr[i].total_cost() < arr[left].total_cost():
            largest = left
        
        if right < size and arr[largest].total_cost() < arr[right].total_cost(): 
            largest = right 
                
        if largest != i: 
            arr[i], arr[largest] = arr[largest], arr[i] 
            self.heapify(largest)                     

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