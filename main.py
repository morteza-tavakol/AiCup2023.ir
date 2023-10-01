import random
from src.game import Game
import time 


flag = False
def initializer(game: Game):

    my_id = game.get_player_id()['player_id']
    print(game.get_player_id()['player_id'])
    strategic_nodes = game.get_strategic_nodes()['strategic_nodes']
    score = game.get_strategic_nodes()['score']
    strategic_nodes = list(zip(strategic_nodes, score))
    strategic_nodes.sort(key=lambda x: x[1], reverse=True)
    strategic_nodes, score = list(zip(*strategic_nodes))
    adj = game.get_adj()
    owner = game.get_owners()

    list_of_my_nodes = []
    for i in owner.keys():
        if owner[str(i)] == my_id:
            list_of_my_nodes.append(i)

    if len(list_of_my_nodes) <= 3:
        for i in strategic_nodes:
            if owner[str(i)] == -1:
                print(game.put_one_troop(i), "-- putting one troop on strategic node ", i)
                return

    if len(list_of_my_nodes) <= 11:
            for i in range(5):
                owner = game.get_owners()
                node = random.choice(list(owner.keys()))
                if owner[node] == -1:
                    print(game.put_one_troop(int(node)))
                    return


def turn(game: Game):
    global flag
    my_id = game.get_player_id()['player_id']
    strategic_nodes = game.get_strategic_nodes()['strategic_nodes']
    score = game.get_strategic_nodes()['score']
    strategic_nodes = list(zip(strategic_nodes, score))
    strategic_nodes.sort(key=lambda x: x[1], reverse=True)
    strategic_nodes, score = list(zip(*strategic_nodes))
    owner = game.get_owners()
    adj = game.get_adj()
    # turn_number = game.get_turn_number()['turn_number']

    ### state 1 : put troop ###

    for i in range(5):
        node = random.choice(list(owner.keys()))
        if owner[node] == -1 and game.get_number_of_troops_to_put()['number_of_troops'] > 1:
            print(game.put_troop(int(node) , 1 ))
            break

    list_of_my_nodes = []
    for i in owner.keys():
        if owner[str(i)] == my_id:
            list_of_my_nodes.append(int(i))

    list_of_my_strategic_nodes = []
    for i in strategic_nodes:
        if owner[str(i)] == my_id:
            list_of_my_strategic_nodes.append(int(i))

    for i in strategic_nodes:
        if owner[str(i)] == my_id and game.get_number_of_fort_troops()[str(i)] < 15 and game.get_number_of_troops_to_put()['number_of_troops'] > 2:
            print(game.put_troop(int(i) , 2))

    if game.get_number_of_troops_to_put()['number_of_troops'] > 0:
        for i in strategic_nodes:
            if owner[str(i)] != my_id:
                for j in adj[str(i)]:
                    if game.get_number_of_troops_to_put()['number_of_troops'] > 0 :
                        if owner[str(j)] == my_id:
                            print(game.put_troop(int(j) , game.get_number_of_troops_to_put()['number_of_troops']))  
                            break
                        elif owner[str(j)] == -1:
                            print(game.put_troop(int(j) , game.get_number_of_troops_to_put()['number_of_troops'] )) 
                            break
                
                for k in adj[str(j)]:
                    if game.get_number_of_troops_to_put()['number_of_troops'] > 0 :
                        if owner[str(k)] == -1:
                            print(game.put_troop(int(k) , game.get_number_of_troops_to_put()['number_of_troops']))  
                            break

    if game.get_number_of_troops_to_put()['number_of_troops'] > 1 :
        node = random.choice(list_of_my_nodes)
        print(game.put_troop(int(node) , game.get_number_of_troops_to_put()['number_of_troops']  ))

    ### state 2 : attack ###
    print(game.next_state())
    owner = game.get_owners()
    adj = game.get_adj()
                
    for x in range(5):
        for i in owner.keys():
            if owner[str(i)] == my_id:
                for j in adj[str(i)]:
                    if int(i) in strategic_nodes:
                        if int(j) in strategic_nodes and owner[str(j)] != my_id and owner[str(j)] != -1:
                            if game.get_number_of_troops()[str(i)] > (game.get_number_of_troops()[str(j)] + game.get_number_of_fort_troops()[str(j)]):
                                print(game.attack(int(i) , int(j) , 0.1 , 0.99))
                                owner = game.get_owners()
                                break
                                
        for i in owner.keys():
            if owner[str(i)] == my_id:
                for j in adj[str(i)]:
                    if int(i) in strategic_nodes:
                        if int(j) not in strategic_nodes and owner[str(j)] != my_id and owner[str(j)] != -1:
                            if game.get_number_of_troops()[str(i)] > ((game.get_number_of_troops()[str(j)] + game.get_number_of_fort_troops()[str(j)]) * 8):
                                print(game.attack(int(i) , int(j) , 2.0 , 0.01))
                                owner = game.get_owners()
                                break
                                
        for i in owner.keys():
            if owner[str(i)] == my_id:
                for j in adj[str(i)]:
                    if int(i) not in strategic_nodes:
                        if int(j) in strategic_nodes and owner[str(j)] != my_id and owner[str(j)] != -1:
                            if game.get_number_of_troops()[str(i)] > (game.get_number_of_troops()[str(j)] + game.get_number_of_fort_troops()[str(j)]):
                                print(game.attack(int(i) , int(j) , 0.1 , 0.99))
                                owner = game.get_owners()
                                break
                                
        for i in owner.keys():
            if owner[str(i)] == my_id:
                for j in adj[str(i)]:
                    if int(i) not in strategic_nodes:
                        if int(j) not in strategic_nodes and owner[str(j)] != my_id and owner[str(j)] != -1:
                            if game.get_number_of_troops()[str(i)] >  game.get_number_of_troops()[str(j)]:
                                for k in adj[str(j)] :
                                    if int(k) in strategic_nodes and game.get_number_of_troops()[str(i)] >  (game.get_number_of_troops()[str(j)] + game.get_number_of_fort_troops()[str(j)]):
                                        print(game.attack(int(i), int(j), 0.1, 0.99))
                                        owner = game.get_owners()
                                        break
                                    
    ### state 3 : move troop ###
    print(game.next_state())

    ### state 4 : fortification ###
    print(game.next_state())
    owner = game.get_owners()
    
    list_of_my_strategic_nodes = []
    for i in strategic_nodes:
        if owner[str(i)] == my_id:
            list_of_my_strategic_nodes.append(int(i))

    if flag == False:
        fort_node = -1
        for i in strategic_nodes:     
            if int(i) in list_of_my_strategic_nodes:
                if game.get_number_of_troops()[str(i)] > 8 :
                    fort_node = i
                    print(game.fort(fort_node ,( game.get_number_of_troops()[str(i)] - 1)))
                    flag = True
                    break

    print(game.next_state())
