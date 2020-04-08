"""
bir tane tree'ye ihtiyacımız olacak. 
initial state root node olacak.
bulunduğumuz root'un goal state olup olmadığına bakmamız gerekiyor
değilse eğer çeşitli alınabilecek aksiyonları değerlendirmemiz gerekiyor
bunu current state'i genişleterek yapabiliyoruz bu da aslında şu oluyor yapılabilecek tüm aksiyonları
current state'a uyguluyoruz ve bu sayede yeni state'leri oluşturuyoruz Ve bunları ağaca yerleştiriyoruz.
Yani aslında bu sayede node'ların her biri bir state olmuş oluyor. Bağlantılarda o state'e geçmek için 
yapılacak olan aksiyon.

Current state'den gidilebilecek yeni stateleri belirlediğimize göre yapmamız gereken yeni statelerden hangisine
gideceğimizin belirlenmesi. Ki aslında search dediğimiz olay da bu.

Daha sonrasında seçilen  bir state'i expand etmemiz gerekecek. Expand edilerek yeni elde statelerden bazılarının
loopa neden olma durumu var. Yani diyelim ki x'i expand ettik ve a,b,c stateleri ortaya çıktı. Biz a'yı seçtik
A'yı expand ettik ve bu sefer x,y,z yi elde ettik. X'in olması loop'a neden olacak

Frontier: Bir t anında bulunan state'in expand edilerek oluşturulabilecek state kümesi.

Bu arada bizim ödevde kullanmamız gereken tree graph search tree olacak


Search algoritmaları bir data structure'a ihtiyaç duyuyor, oluşturulan search tree'lerin kaydını tutabilmek için
    - parent
    - state
    - action
    - pathCost

Bu bilgileri her bir node için bizlerin tutması gerekecek.

explored set dediğimiz yani bir state'ten expand edilerek keşfedilen stateleri dictionaryde
yani hashtable tutabiliriz

"""

from image_operations import read_image_rgb, show_image
from node import Node
from custom_queue import Priority_Queue, Priority_Queue_Heap
from time import time


def convert_image_to_nodes(image, row, column, goal_x, goal_y):
    return Node.from_image(image, row, column, goal_x, goal_y)

def child_node_not_seen(explored_nodes, frontier, child_node):
    return (child_node not in explored_nodes) and (frontier.not_exists(child_node))

def possible_total_cost_of_child_node(source_to_child_node_cost, child_node):
    return child_node.get_current_to_goal_cost() + source_to_child_node_cost

# Bu fonksiyon bizlere şey dönecek, şuanki node'tan gidilebilecek node'lara yani bir nevi alabileceğimiz aksiyonlara bakacak.
# Sadece gidilebilecek node'ları al total cost hesaplama. bunun hesabı sonradan yapılacak
def get_actions(image_nodes, current_node):
    actions = []
    
    row_count = len(image_nodes)
    column_count = len(image_nodes[0])
    
    x = current_node.get_x()
    y = current_node.get_y()
    
    if (x + 1 >= 0 and x + 1 < row_count):
        actions.append(image_nodes[x+1][y])
        
        if (y - 1 >= 0 and y - 1 < column_count):
            actions.append(image_nodes[x][y-1])
        
        if (x- 1 >= 0 and x- 1 < row_count):
            actions.append(image_nodes[x-1][y])
        
        if (y + 1 >= 0 and y + 1 < column_count):
            actions.append(image_nodes[x][y+1])
        
        if (x + 1 >= 0 and x + 1 < row_count and y + 1 >= 0 and y + 1 < column_count):
            actions.append(image_nodes[x+1][y+1])
        
        if (x + 1 >= 0 and x + 1 < row_count  and y - 1 >= 0 and y - 1 < column_count):
            actions.append(image_nodes[x+1][y-1])
        
        if (x - 1 >= 0 and x - 1 < row_count  and y + 1 >= 0 and y + 1 < column_count):
            actions.append(image_nodes[x-1][y+1])
        
        if (x - 1 >= 0 and  - 1 < row_count  and y - 1 >= 0 and y - 1 < column_count):
            actions.append(image_nodes[x-1][y-1])
    
    return actions

def calculate_cost_to_next_node(target_node):
    return 255 - target_node.get_red()

def find_solution(image_nodes, initial_state, goal_state, frontier):    
    current_node = image_nodes[initial_state['x']][initial_state['y']]
    current_node.set_parent(None)
    goal_node = image_nodes[goal_state['x']][goal_state['y']]
    frontier.add_node(current_node)    
    
    explored_nodes = set() ## goal_node'a gidilene kadar gezilen node'ları tutar baştan sona doğru
    
    while True:
        if frontier.is_empty():
            return False, explored_nodes
        
        current_node = frontier.pop()
        explored_nodes.add(current_node)
        print("Explored a node! x: {0}, y: {1}".format(current_node.get_x(), current_node.get_y()))
        
        if current_node == goal_node:        
            return True, explored_nodes, goal_node
        
        actions = get_actions(image_nodes, current_node)
        
        for child_node in actions:
            source_to_next_node_cost = current_node.get_source_to_current_cost() + calculate_cost_to_next_node(child_node)
            possible_total_cost = possible_total_cost_of_child_node(source_to_next_node_cost, child_node)
            
            if child_node_not_seen(explored_nodes, frontier, child_node):
                child_node.set_parent(current_node)
                child_node.set_source_to_current_cost(source_to_next_node_cost)
                frontier.add_node(child_node)        
            elif frontier.should_update_node(child_node, possible_total_cost):
                child_node.set_parent(current_node)
                frontier.update_node(child_node, possible_total_cost)

image, row, column = read_image_rgb(r'C:\Users\user\Desktop\best_case.png')

# Bizim için burada stateler aslında pixellerin konumu olmuş oluyor.                                
initial_state = {}
initial_state['x'] = 0
initial_state['y'] = 0

goal_state = {}
goal_state['x'] = 242
goal_state['y'] = 433

image_nodes = convert_image_to_nodes(image, row, column, goal_state['x'], goal_state['y'])

print("Started A* with array based priority queue implementation")
start_time = time()
is_successfull, visited_nodes, last_node = find_solution(image_nodes, initial_state, goal_state, Priority_Queue())
finish_time = time()
print("Completed at %s seconds" %(finish_time - start_time))


print("Found goal state: " + str(is_successfull))
print("Visited " + str(len(visited_nodes)) + " nodes")

show_image(image, last_node)

image, row, column = read_image_rgb(r'C:\Users\user\Desktop\best_case.png')

image_nodes = convert_image_to_nodes(image, row, column, goal_state['x'], goal_state['y'])

print("Started A* with array based priority queue implementation")
start_time = time()
is_successfull, visited_nodes, last_node = find_solution(image_nodes, initial_state, goal_state, Priority_Queue_Heap())
finish_time = time()
print("Completed at %s seconds" %(finish_time - start_time))

print("Found goal state: " + str(is_successfull))
print("Visited " + str(len(visited_nodes)) + " nodes")

show_image(image, last_node)
