class Node:
    def __init__(self, x, y, red, current_to_goal_cost):
        self.x = x
        self.y = y
        self.red = red
        self.source_to_current_cost = 0
        self.current_to_goal_cost = current_to_goal_cost

    @classmethod
    def from_image(cls, image, row, column, goal_x, goal_y):        
        image_nodes = [[0 for y in range(column)] for x in range(row)]
        
        goal_red = image[goal_x][goal_y][0]
        current_to_goal_cost = 255 - goal_red

        for i in range(row):        
            for j in range(column):            
                red = image[i][j][0]
                image_nodes[i][j] = cls(i, j, red, current_to_goal_cost)
    
        return image_nodes
    
    def set_parent(self, parent_node):
        self.parent = parent_node
    
    def set_source_to_current_cost(self, source_to_current_cost):
        self.source_to_current_cost = source_to_current_cost
    
    def set_total_cost(self, total_cost):
        self.total_cost = total_cost    
        
    def update(self, source_to_current_cost, current_to_goal_cost):
        self.source_to_current_cost = source_to_current_cost
        self.current_to_goal_cost = current_to_goal_cost
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_red(self):
        return self.red
    
    def get_source_to_current_cost(self):
        return self.source_to_current_cost
    
    def get_current_to_goal_cost(self):
        return self.current_to_goal_cost
    
    def total_cost(self):
        return self.current_to_goal_cost + self.source_to_current_cost
    
    def get_parent(self):
        return self.parent