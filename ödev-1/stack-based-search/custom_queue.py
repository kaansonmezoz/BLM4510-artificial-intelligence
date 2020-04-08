class Priority_Queue:
    def __init__(self):
        self.queue = []
        self.items = set()
    
    def add_node(self, node):
        ## burada node'un eklenip eklenmediği de kontrol edilmeli ayrıca...
        ## queue'da bu eleman varsa gerekli işlemler yapılmalı ne gibi ?
        ## cost'u eğer aynı elemanın diğer versiyonundan daha az ise costun değiştirilmesi gerekir.
        ## sonrasında da tekrardan sıralanması
        self.queue.append(node)
        self.items.add(node)
        
    def update_node(self, node, source_to_current_cost):
        node.set_source_to_current_cost(source_to_current_cost)
        self.sort()
    
    ## total_cost'a göre sıralanmalı burası. total_cost'lar eşitse goal'a daha yakın olanı öne koy.
    ## yani current_to_goal_cost
    def sort(self): 
        return 

    def is_empty(self):
        return len(self.queue) == 0
    
    def exists(self, node):
        return node in self.items
    
    def not_exists(self, node):
        return node not in self.items
    
    def pop(self):
        node = self.queue.pop()
        self.items.discard(node)
        return node
    
    def should_update_node(self, node, possible_total_cost):
        return self.exists(node) and node.total_cost() > possible_total_cost