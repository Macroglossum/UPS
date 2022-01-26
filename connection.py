import socket
import threading
import re
#import gui

class Connection():
    def __init__(self) -> None:
        self.HOST = '127.0.0.1'
        self.PORT = 10035
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.HOST, self.PORT))
        self.data = ''
        self.status = ''
        self.card_to_add = ['']
        self.player_start_cards = ['', '', '', '', '', '', '']

    #accept message from server   
    def recieve_from_server(self):
        while(True):
            self.data = ''
            self.data = self.socket.recv(1024)
            self.data = self.data.decode('UTF-8')
            self.data.strip()
            change = False
            if (self.data != ''):
                print('delka: ', len(self.data))
                print(self.data)
            if (';;connected;;' in self.data): 
                print('Connected to server')
                self.status += '0'
            if (';;lobby;;' in self.data): 
                print('Waiting in lobby...')
                self.status += '1'
            if (';;game;;' in self.data): 
                print('And shall we begin!')
                if (';;lobby;;' in self.data): self.status.replace('1', '2')
                else: self.status += '2'
            if (';;first_card:' in self.data): 
                self.status += ';;first_card:'
                self.status += self.data.split(';;first_card:', 1)[1]
            if (';;card' in self.data):
                self.player_start_cards = re.findall(";;card[0-5]:[0-6]_[0-6];;", self.data)
                self.status += "starting_cards"
            if (';;waiting;;' in self.data):
                if ('yourturn' in self.status): 
                    self.status.replace('yourturn', 'waiting')
                    self.status = self.status('waiting', 1)[1]
                else: self.status += "waiting"
                print(self.status)
            if (';;yourturn;;' in self.data):
                if ('waiting' in self.status): 
                    self.status.replace('waiting', 'yourturn')
                    self.status = self.status('yourturn', 1)[1]
                else: self.status += "yourturn" 
                print(self.status)
            if (';;addtohand:' in self.data):
                self.card_to_add = re.findall(";;addtohand:[0-6]_[0-6]>[0-9][0-1]?;;", self.data)
                self.status += "add_card_hand"
            if (';;addtoboard:' in self.data):
                self.card_to_add = re.findall(";;addtoboard:[0-6]_[0-6]>-[1,2]<[0-9][0-1]?;;", self.data)
                print(self.card_to_add)
                self.status += "add_to_board"
            if (';;change;;' in self.data or change == True):
                #self.n.status = self.n.status.replace('watt', 'yourturn')
                self.status += 'yourturn'


    #send message to server
    def send_to_server(self, message):
        self.socket.sendall(str.encode(message))