from contextvars import copy_context
from lib2to3.pytree import convert
import threading
from turtle import pos, position
import gui
import connection
import re
import time

class Manager():
    def __init__(self) -> None:
        self.n = connection.Connection()
        self.game = gui.Gui()
        self.player_id = 2

        thread_recieve = threading.Thread(target = self.n.recieve_from_server)   
        thread_recieve.start()
        
        menu = 0
        while(menu == 0):
            menu = self.game.menu_screen()

        thread_send = threading.Thread(target = self.n.send_to_server('play'))
        thread_send.start()

        while (self.server_handler == 1):
            self.game.create_lobby()
            self.player_id = 1

        handler = -1
        while (handler != 2):
            self.game.create_lobby()
            handler = self.server_handler()
            if (handler == 2): 
                self.game.create_game()
        print('Your game is ready')
        
        #first card and players first six cards
        if (';;first_card:' in self.n.status):
            card = self.n.status.split(';;first_card:', 1)[1]
            self.game.first_card(card[0] + '_' + card[1])

        if ('starting_cards' in self.n.status):
            for i in range (6):
                card = re.findall("[0-6]_[0-6]", self.n.player_start_cards[i])
                self.game.players_cards(card[0], i + 1)
        
        while(1):
            #get first click of player
            while ('yourturn' in self.n.status):
                click_position_card = -1
                #questions
                self.game.write_turn(0)
                click_position_card = self.game.click_players_cards()
                if (click_position_card != -1): 
                    print(click_position_card)
                    position_to_send = ';;position_card:' + str(click_position_card) + ';;'
                    thread_send = threading.Thread(target = self.n.send_to_server(position_to_send))
                    thread_send.start()
                    #questions
                    if ('13' not in position_to_send):
                        click_place_card = self.game.click_sides() 
                        end_position_to_send = ';;destination_card:' + str(click_place_card) + ';;'
                        thread_send = threading.Thread(target = self.n.send_to_server(end_position_to_send))  
                        thread_send.start()   
                        print(click_place_card)
                    

                print(self.n.status)
                ##instructions
                if ('add_card_hand' in self.n.status):
                    card = re.findall("[0-6]_[0-6]", self.n.card_to_add[0])
                    place1 = re.findall(">[0-9][0-1]?;;", self.n.card_to_add[0])
                    place = re.findall("[0-9][0-1]?", place1[0])
                    place[0] = int(place[0]) + 1
                    self.game.players_cards(card[0], place[0])
                    self.n.status = self.n.status.replace('yourturn', '')
                    break
                if ('add_to_board' in self.n.status):
                    i = re.findall("[0-6]", self.n.card_to_add[0])
                    if (int(i[0]) <= int(i[1])): 
                        rotation = False
                        card = i[0] + "_" + i[1]
                    else: 
                        rotation = True
                        card = i[1] + "_" + i[0]
                    #card = re.findall("[0-6]_[0-6]", self.n.card_to_add[0])
                    place1 = re.findall(">-[1,2]", self.n.card_to_add[0])
                    place = re.findall("-[1,2]", place1[0])
                    self.game.add_card(card, int(place[0]), rotation)
                    place2 = re.findall("<[0-9][0-1]?;;", self.n.card_to_add[0])
                    place3 = re.findall("[0-9][0-1]?", place2[0])
                    self.game.delete_players_card(int(place3[0]) + 1)
                    self.n.status = self.n.status.replace('yourturn', '')
                    break
                #if ('tryagain' in self.n.status):
                    #print('try again')

            
            while ('waiting' in self.n.status):               
                self.game.write_turn(1)
                thread_send = threading.Thread(target = self.n.send_to_server(';;done?;;'))
                thread_send.start()
                time.sleep(0.5)
                if ('add_card_hand' in self.n.status):
                    place1 = re.findall(">[0-9][0-1]?;;", self.n.card_to_add[0])
                    place = re.findall("[0-9][0-1]?", place1[0])
                    place[0] = int(place[0]) + 1
                    self.game.add_opponents_card(place[0])
                    self.n.status = self.n.status.replace('waiting', 'watt')
                    print(self.n.status + '------------')
                if ('add_to_board' in self.n.status):
                    i = re.findall("[0-6]", self.n.card_to_add[0])
                    if (int(i[0]) <= int(i[1])): 
                        rotation = False
                        card = i[0] + "_" + i[1]
                    else: 
                        rotation = True
                        card = i[1] + "_" + i[0]
                    #card = re.findall("[0-6]_[0-6]", self.n.card_to_add[0])
                    place1 = re.findall(">-[1,2]", self.n.card_to_add[0])
                    place = re.findall("-[1,2]", place1[0])
                    self.game.add_card(card, int(place[0]), rotation)
                    place2 = re.findall("<[0-9][0-1]?;;", self.n.card_to_add[0])
                    place3 = re.findall("[0-9][0-1]?", place2[0])
                    self.game.delete_opponents_card(int(place3[0]) + 1)
                    self.n.status = self.n.status.replace('waiting', 'watt')
                    print(self.n.status + '------------')
            
    
    def status_change_handler(self):
        print('Im trying')

    #0...connected, 1...lobby, 2...game-screen
    def server_handler(self) -> int:
        #Vubec nic nevypisuje zde!!!
        if ('2' in self.n.status):
            #print('dva')
            return 2
        if ('1' in self.n.status):
            #print('jedna')
            return 1
        return 0