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

from image_operations import read_image_rgb
from node import Node
from custom_queue import Priority_Queue


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
    
    if x == 0:
        actions.append(image_nodes[x+1][y])
        
        if y == 0:
            actions.append(image_nodes[x][y+1])
            actions.append(image_nodes[x+1][y+1])
        elif y == column_count - 1:
            actions.append(image_nodes[x][y-1])
            actions.append(image_nodes[x+1][y-1])
        else:
            actions.append(image_nodes[x][y+1])
            actions.append(image_nodes[x][y-1])
                    
            actions.append(image_nodes[x+1][y+1])
            actions.append(image_nodes[x+1][y-1])    
    elif x == row_count - 1:
        actions.append(image_nodes[x-1][y])

        if y == 0:
            actions.append(image_nodes[x][y+1])
            actions.append(image_nodes[x-1][y+1])
        elif y == column_count - 1:
            actions.append(image_nodes[x][y-1])
            actions.append(image_nodes[x-1][y-1])
        else:
            actions.append(image_nodes[x][y+1])
            actions.append(image_nodes[x][y-1])
            
            actions.append(image_nodes[x-1][y+1])
            actions.append(image_nodes[x-1][y-1])    

    else:
        actions.append(image_nodes[x-1][y])
        actions.append(image_nodes[x+1][y])
        
        if y == 0:
            actions.append(image_nodes[x][y+1])
            
            actions.append(image_nodes[x-1][y+1])
            actions.append(image_nodes[x+1][y+1])        
        if y == column_count-1:
            actions.append(image_nodes[x][y-1])
            
            actions.append(image_nodes[x-1][y-1])
            actions.append(image_nodes[x+1][y-1])
        else:
            actions.append(image_nodes[x][y+1])            
            actions.append(image_nodes[x][y-1])
            
            
            actions.append(image_nodes[x-1][y+1])
            actions.append(image_nodes[x-1][y-1])
                        
            actions.append(image_nodes[x+1][y+1])                    
            actions.append(image_nodes[x+1][y-1])
                        
    
    return actions

def calculate_cost_to_next_node(target_node):
    return 255 - target_node.get_red()

def find_solution(image_nodes, initial_state, goal_state):    
    frontier = Priority_Queue()    
    current_node = image_nodes[initial_state['x']][initial_state['y']]
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
            return True, explored_nodes
        
        actions = get_actions(image_nodes, current_node)
        
        for child_node in actions:
            source_to_next_node_cost = current_node.get_source_to_current_cost() + calculate_cost_to_next_node(child_node)
            possible_total_cost = possible_total_cost_of_child_node(source_to_next_node_cost, child_node)
            
            if child_node_not_seen(explored_nodes, frontier, child_node):
                child_node.set_source_to_current_cost(source_to_next_node_cost)
                frontier.add_node(child_node)        
            elif frontier.should_update_node(child_node, possible_total_cost):
                frontier.update_node(child_node, possible_total_cost)

# Bizim için burada stateler aslında pixellerin konumu olmuş oluyor.                                
initial_state = {}
initial_state['x'] = 0
initial_state['y'] = 0

goal_state = {}
goal_state['x'] = 15
goal_state['y'] = 15


image, row, column = read_image_rgb(r'C:\Users\user\Desktop\438e7e33-80c6-4f28-b520-f1034c7c01ab.jpg')
image_nodes = convert_image_to_nodes(image, row, column, goal_state['x'], goal_state['y'])

is_successfull, visited_nodes = find_solution(image_nodes, initial_state, goal_state)