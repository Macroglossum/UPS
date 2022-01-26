from random import randint
from tkinter import Button
import pygame
import timeit
from pygame import *
pygame.font.init()

class Button:
    def __init__(self, x, y, width, height, position) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.position = position
        self.text = ''

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if (self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height):
            return True
        else: 
            return False

class Gui():
    def __init__(self) -> None:
        self.width = 1500
        self.height = 1000
        self.win = pygame.display.set_mode((self.width, self.height))
        self.opponentCards = [1, 1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1, -1] 
        #self.btns = ['', '', '', '', '','', '', '', '', '', '', '', ''] #13. karta = deck
        self.btns = [Button(0, 0, 0, 0, -10), Button(0, 0, 0, 0, -10), Button(0, 0, 0, 0, -10), Button(0, 0, 0, 0, -10),
        Button(0, 0, 0, 0, -10), Button(0, 0, 0, 0, -10), Button(0, 0, 0, 0, -10), Button(0, 0, 0, 0, -10), Button(0, 0, 0, 0, -10),
        Button(0, 0, 0, 0, -10), Button(0, 0, 0, 0, -10), Button(0, 0, 0, 0, -10), Button(0, 0, 0, 0, -10)] 
        self.LeftRight = [Button(0, 0, 0, 0, -10), Button(0, 0, 0, 0, -10)]
        self.left_added = 0
        self.right_added = 0
        pygame.display.set_caption("Client")

    #Create waiting lobby
    def create_lobby(self):
            clock = pygame.time.Clock()
            clock.tick(10)
            self.win.fill('gray')
            pygame.font.init()
            font = pygame.font.SysFont("comicsans", 40, 0, 0)
            text = font.render("Waiting for another Player...",1, 'black')
            self.win.blit(text, (self.width/2 - text.get_width()/2, self.height/2 - text.get_height()/2))
            pygame.display.update()
    
    #Create default game screen, only with opponents cards and deck
    def create_game(self):
        self.win.fill('gray')
        font = pygame.font.SysFont("comicsans", 20)
        text = font.render("Opponents cards", 1, 'black')
        self.win.blit(text, (700, 20))

        text = font.render("Yours cards", 1, 'black')
        self.win.blit(text, (720, 850))

        image = pygame.image.load(r'/home/ester/Desktop/Client/Pictures/Card_back.png')
        self.win.blit(image, (self.width/2 - 62, self.height/2))
        self.btns[12] = Button(self.width/2 - 62, self.height/2, 125, 50, 13)

        a = 550
        for i in range(6):
            image = pygame.image.load(r'/home/ester/Desktop/Client/Pictures/Card_back.png')
            image = pygame.transform.rotate(image, 90)
            self.win.blit(image, (a, 50))
            a += 70
        pygame.display.update()
                      
    #First screen after opening, 'click to play'
    def menu_screen(self) -> int:
        run = True
        clock = pygame.time.Clock()

        while run:
            clock.tick(60)
            self.win.fill('gray')
            font = pygame.font.SysFont("comicsans", 60)
            text = font.render("Click to Play!", 1, 'black')
            self.win.blit(text, (self.width/2 - text.get_width()/2, self.height/2 - text.get_height()/2))
            pygame.display.update()

            #Change after click of mouse
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return(1)
        return(0)
    
    def click_players_cards(self):
        run = True
        while(run):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for btn in self.btns:
                        if (btn.position != -10. and btn.click(pos)):
                            return(btn.position)
    
    def click_sides(self):
        run = True
        while(run):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for btn in self.LeftRight:
                        if (btn != -10 and btn.click(pos)):
                            return(btn.position)

    def write_turn(self, number):
        font = pygame.font.SysFont("comicsans", 60)
        if (number == 0):
            self.text = font.render("Your turn!", 1, 'black')
        elif (number == 1):
            self.text = font.render("Opponent is playing...", 1, 'black')
        self.win.blit(self.text, (self.width/2 - self.text.get_width()/2, self.height/2 - self.text.get_height()/2 - 130))
        pygame.display.update()
    
    def delete_write(self, player):
        font = pygame.font.SysFont("comicsans", 60)
        if (player == 1): self.text = font.render("Opponent is playing...", 1, 'red')
        pygame.display.update()

    #Add first card to screen
    def first_card(self, name):
        image = pygame.image.load(r'/home/ester/Desktop/Client/Pictures/' + name + '.png')
        self.win.blit(image, (self.width/2 - 62, self.height/2 - 70))
        pygame.display.update()

        self.LeftRight = [Button(self.width/2 - 62, self.height/2 - 70, 62.5, 50, -1),
                          Button(self.width/2 -62 + 62.5, self.height/2 - 70, 62.5, 50, -2)] #-1 = left, -2 = right
        
    def add_opponents_card(self, position):
        a = 550
        image = pygame.image.load(r'/home/ester/Desktop/Client/Pictures/Card_back.png')
        image = pygame.transform.rotate(image, 90)
      
        if (position == 1): 
            self.win.blit(image, (a, 50))
            self.opponentCards[position-1] = 1
        if (position == 2):
            self.win.blit(image, (a + 70, 50))
            self.opponentCards[position-1] = 1
        if (position == 3): 
            self.win.blit(image, (a + 2*70, 50))
            self.opponentCards[position-1] = 1
        if (position == 4): 
            self.win.blit(image, (a + 3*70, 50))
            self.opponentCards[position-1] = 1
        if (position == 5):
            self.win.blit(image, (a + 4*70, 50))
            self.opponentCards[position-1] = 1
        if (position == 6): 
            self.win.blit(image, (a + 5*70, 50))
            self.opponentCards[position-1] = 1
        if (position == 7):
            self.win.blit(image, (a, 180))
            self.opponentCards[position-1] = 1
        if (position == 8): 
            self.win.blit(image, (a +70, 180))
            self.opponentCards[position-1] = 1
        if (position == 9): 
            self.win.blit(image, (a + 2*70, 180))
            self.opponentCards[position-1] = 1
        if (position == 10): 
            self.win.blit(image, (a + 3*70, 180))
            self.opponentCards[position-1] = 1
        if (position == 11): 
            self.win.blit(image, (a + 4*70, 180))
            self.opponentCards[position-1] = 1
        if (position == 12): 
            self.win.blit(image, (a + 5*70, 180))
            self.opponentCards[position-1] = 1
        pygame.display.update()

    #Add players cards
    def players_cards(self, name, position) -> int:
        image = pygame.image.load(r'/home/ester/Desktop/Client/Pictures/' + name + '.png')
        image = pygame.transform.rotate(image, 90)
        a = 550
        if (position == 1): 
            self.win.blit(image, (a, self.height - 300))
            self.btns[position-1] = Button(a, self.height - 300, 50, 125, position-1)
        if (position == 2): 
            self.win.blit(image, (a + 70, self.height - 300))
            self.btns[position-1] = Button(a +70, self.height - 300, 50, 125, position-1)
        if (position == 3): 
            self.win.blit(image, (a + 2*70, self.height - 300))
            self.btns[position-1] = Button(a + 2*70, self.height - 300, 50, 125, position-1)
        if (position == 4): 
            self.win.blit(image, (a + 3*70, self.height - 300))
            self.btns[position-1] = Button(a +3*70, self.height - 300, 50, 125, position-1)
        if (position == 5): 
            self.win.blit(image, (a + 4*70, self.height - 300))
            self.btns[position-1] = Button(a +4*70, self.height - 300, 50, 125, position-1)
        if (position == 6): 
            self.win.blit(image, (a + 5*70, self.height - 300))
            self.btns[position-1] = Button(a +5*70, self.height - 300, 50, 125, position-1)
        if (position == 7): 
            self.win.blit(image, (a, self.height - 430))
            self.btns[position-1] = Button(a, self.height - 430, 50, 125, position-1)
        if (position == 8): 
            self.win.blit(image, (a + 70, self.height - 430))
            self.btns[position-1] = Button(a +70, self.height - 430, 50, 125, position-1)
        if (position == 9): 
            self.win.blit(image, (a + 2*70, self.height - 430))
            self.btns[position-1] = Button(a +2*70, self.height - 430, 50, 125, position-1)
        if (position == 10): 
            self.win.blit(image, (a + 3*70, self.height - 430))
            self.btns[position-1] = Button(a +3*70, self.height - 430, 50, 125, position-1)
        if (position == 11): 
            self.win.blit(image, (a + 4*70, self.height - 430))
            self.btns[position-1] = Button(a +4*70, self.height - 430, 50, 125, position-1)
        if (position == 12): 
            self.win.blit(image, (a + 5*70, self.height - 430))
            self.btns[position-1] = Button(a +5*70, self.height - 430, 50, 125, position-1)
        pygame.display.update()
        return 0
    
    def delete_back_card(self):
        pygame.draw.rect(self.win, 'gray', (self.width/2 - 62, self.height/2, 125, 50))
        print('Fuck')
        self.btns[12] = None
        pygame.display.update()

    def delete_opponents_card(self, position):
        a = 550
        if (position == 1): 
            pygame.draw.rect(self.win, 'gray', (a, self.height - 950, 50, 125))
            self.opponentCards[position-1] = -1
        if (position == 2): 
            pygame.draw.rect(self.win, 'gray', (a + 70, self.height - 950, 50, 125))
            self.opponentCards[position-1] = -1
        if (position == 3): 
            pygame.draw.rect(self.win, 'gray', (a + 2*70, self.height - 950, 50, 125))
            self.opponentCards[position-1] = -1
        if (position == 4): 
            pygame.draw.rect(self.win, 'gray', (a + 3*70, self.height - 950, 50, 125))
            self.opponentCards[position-1] = -1
        if (position == 5): 
            pygame.draw.rect(self.win, 'gray', (a + 4*70, self.height - 950, 50, 125))
            self.opponentCards[position-1] = -1
        if (position == 6): 
            pygame.draw.rect(self.win, 'gray', (a + 5*70, self.height - 950, 50, 125))
            self.opponentCards[position-1] = -1
        if (position == 7): 
            pygame.draw.rect(self.win, 'gray', (a, 180, 50, 125))
            self.opponentCards[position-1] = -1
        if (position == 8): 
            pygame.draw.rect(self.win, 'gray', (a + 70, self.height - 430, 50, 125))
            self.opponentCards[position-1] = -1
        if (position == 9): 
            pygame.draw.rect(self.win, 'gray', (a + 2*70, self.height - 430, 50, 125))
            self.opponentCards[position-1] = -1
        if (position == 10): 
            pygame.draw.rect(self.win, 'gray', (a + 3*70, self.height - 430, 50, 125))
            self.opponentCards[position-1] = -1
        if (position == 11): 
            pygame.draw.rect(self.win, 'gray', (a + 4*70, self.height - 430, 50, 125))
            self.opponentCards[position-1] = -1
        if (position == 12): 
            pygame.draw.rect(self.win, 'gray', (a + 5*70, self.height - 430, 50, 125))
            self.opponentCards[position-1] = -1
        pygame.display.update()
    
    def delete_players_card(self, position): 
        a = 550
        if (position == 7): 
            pygame.draw.rect(self.win, 'gray', (a, self.height - 430, 50, 125))
            self.btns[position-1] = None
        if (position == 8): 
            pygame.draw.rect(self.win, 'gray', (a + 70, self.height - 430, 50, 125))
            self.btns[position-1] = None
        if (position == 9): 
            pygame.draw.rect(self.win, 'gray', (a + 2*70, self.height - 430, 50, 125))
            self.btns[position-1] = None
        if (position == 10): 
            pygame.draw.rect(self.win, 'gray', (a + 3*70, self.height - 430, 50, 125))
            self.btns[position-1] = None
        if (position == 11): 
            pygame.draw.rect(self.win, 'gray', (a + 4*70, self.height - 430, 50, 125))
            self.btns[position-1] = None
        if (position == 12): 
            pygame.draw.rect(self.win, 'gray', (a + 5*70, self.height - 430, 50, 125))
            self.btns[position-1] = None
        if (position == 1): 
            pygame.draw.rect(self.win, 'gray', (a, self.height - 300, 50, 125))
            self.btns[position-1] = None
        if (position == 2): 
            pygame.draw.rect(self.win, 'gray', (a + 70, self.height - 300, 50, 125))
            self.btns[position-1] = None
        if (position == 3): 
            pygame.draw.rect(self.win, 'gray', (a + 2*70, self.height - 300, 50, 125))
            self.btns[position-1] = None
        if (position == 4): 
            pygame.draw.rect(self.win, 'gray', (a + 3*70, self.height - 300, 50, 125))
            self.btns[position-1] = None
        if (position == 5): 
            pygame.draw.rect(self.win, 'gray', (a + 4*70, self.height - 300, 50, 125))
            self.btns[position-1] = None
        if (position == 6): 
            pygame.draw.rect(self.win, 'gray', (a + 5*70, self.height - 300, 50, 125))
            self.btns[position-1] = None
        pygame.display.update()
                    
    def add_card(self, name, sight, flipped):
        image = pygame.image.load(r'/home/ester/Desktop/Client/Pictures/' + name + '.png')
        if (sight == -2):
            if (self.right_added <= 1):
                if (flipped == True):  
                    image = pygame.transform.rotate(image, 180)
                self.win.blit(image, (self.width/2 - 62 + (self.right_added + 1) * 125, self.height/2 - 70))
                self.LeftRight[1] = Button(self.width/2 - 62 + (self.right_added + 1) * 125 + 62.5, self.height/2 - 70, 62.5, 50, 1)
            elif (self.right_added <= 2):
                if (flipped == True):  
                    image = pygame.transform.rotate(image, 180)
                image = pygame.transform.rotate(image, 90)
                self.win.blit(image, (self.width/2 - 62 + (self.right_added + 1) * 125 - 50, self.height/2 - 70 + 50))
                self.LeftRight[1] = Button(self.width/2 - 62 + (self.right_added + 1) * 125 - 50, self.height/2 - 70 + 50 + 62.5, 50, 62.5, 1)
            elif (self.right_added <= 3):
                if (flipped == True):  
                    image = pygame.transform.rotate(image, 180)
                image = pygame.transform.rotate(image, 90)
                self.win.blit(image, (self.width/2 - 62 + (2 + 1) * 125 - 50, self.height/2 - 70 + 50 + 125)) 
                self.LeftRight[1] = Button(self.width/2 - 62 + (2 + 1) * 125 - 50, self.height/2 - 70 + 50 + 125 + 62.5, 50, 62.5, 1)           
            elif (self.right_added <= 4):
                if (flipped == True):  
                    image = pygame.transform.rotate(image, 180)
                self.win.blit(image, (self.width/2 - 62 + (2 + 1) * 125 - 50, self.height/2 - 70+ 50 + 125 *2))
                self.LeftRight[1] = Button(self.width/2 - 62 + (2 + 1) * 125 - 50 + 62.5, self.height/2 - 70+ 50 + 125 *2, 62.5, 50, 1)
            elif (self.right_added <= 9):
                if (flipped == True):  
                    image = pygame.transform.rotate(image, 180)
                image = pygame.transform.rotate(image, 90)
                self.win.blit(image, (self.width/2 - 62 + (3 + 1) * 125 - 50, self.height/2 - 70 + 50 + 125 * 2 - 62.5 - 12.5 - (self.right_added - 5) * 125))
                self.LeftRight[1] = Button(self.width/2 - 62 + (3 + 1) * 125 - 50, self.height/2 - 70 + 50 + 125 * 2 - 62.5 - 12.5 - (self.right_added - 5) * 125 +62.5, 50, 62.5, 1)
            elif (self.right_added <= 10):
                if (flipped == True):  
                    image = pygame.transform.rotate(image, 180)
                self.win.blit(image, (self.width/2 - 62 + (3 + 1) * 125 - 50 + 50, self.height/2 - 70 + 50 + 125 * 2 - 62.5 - 12.5 - (self.right_added - 6) * 125))
                self.LeftRight[1] = Button(self.width/2 - 62 + (3 + 1) * 125 - 50 + 50 +62.5, self.height/2 - 70 + 50 + 125 * 2 - 62.5 - 12.5 - (self.right_added - 6) * 125, 62.5, 50, 1)
            elif (self.right_added <= 15):
                if (flipped == True):  
                    image = pygame.transform.rotate(image, 180)
                image = pygame.transform.rotate(image, 90)
                self.win.blit(image, (self.width/2 - 62 + (3 + 1) * 125 - 50 +125, self.height/2 - 70 + 50 + 125 * 2 - 62.5 - 12.5 - (self.right_added -11) * 125 + 50))
                self.LeftRight[1] = Button(self.width/2 - 62 + (3 + 1) * 125 - 50 +125, self.height/2 - 70 + 50 + 125 * 2 - 62.5 - 12.5 - (self.right_added -11) * 125 + 50 +62.5, 50, 62.5, 1)
            elif (self.right_added <= 16):
                if (flipped == True):  
                    image = pygame.transform.rotate(image, 180)
                self.win.blit(image, (self.width/2 - 62 + (3 + 1) * 125 - 50 + 50 +125, self.height/2 - 70 + 50 + 125 * 2 - 62.5 - 12.5 - (self.right_added - 16) * 125 +12.5+ 50 +62.5))
                self.LeftRight[1] = Button(self.width/2 - 62 + (3 + 1) * 125 - 50 + 50 +125 + 62.5, self.height/2 - 70 + 50 + 125 * 2 - 62.5 - 12.5 - (self.right_added - 16) * 125 +12.5+ 50 +62.5, 62.5, 50, 1)
            elif (self.right_added <= 22):
                if (flipped == True):  
                    image = pygame.transform.rotate(image, 180)
                image = pygame.transform.rotate(image, 90)
                self.win.blit(image, (self.width/2 - 62 + (3 + 1) * 125 - 50 + 50 +125 + 12.5 + 62.5, self.height/2 - 70 + 50 + 125 * 2 - 62.5 - 12.5 - (self.right_added - 16) * 125 +12.5+ 50 +62.5))
                self.LeftRight[1] = Button(self.width/2 - 62 + (3 + 1) * 125 - 50 + 50 +125 + 12.5 + 62.5, self.height/2 - 70 + 50 + 125 * 2 - 62.5 - 12.5 - (self.right_added - 16) * 125 +12.5+ 50 +62.5 +62.5, 50, 62.5, 1)
            elif (self.right_added <= 25):
                if (flipped == True):  
                    image = pygame.transform.rotate(image, 180)
                self.win.blit(image, (self.width/2 - 62 + (3 + 1) * 125 - 50 + 50 + 62.5 + 12.5 +125 - (self.right_added - 22)*125, self.height/2 - 70 + 50 + 125 * 2 - 62.5 - 12.5 - (5) * 125+ 50 - 50))
                self.btns[1] = Button(self.width/2 - 62 + (3 + 1) * 125 - 50 + 50 + 62.5 + 12.5 +125 +62.5- (self.right_added - 22)*125, self.height/2 - 70 + 50 + 125 * 2 - 62.5 - 12.5 - (5) * 125+ 50 - 50, 62.5, 50, 1)
            elif (self.right_added <= 26):
                if (flipped == True):  
                    image = pygame.transform.rotate(image, 180)
                image = pygame.transform.rotate(image, 90)
                self.win.blit(image, (self.width/2 - 62 + (3 + 1) * 125 - 50 + 50 + 62.5 + 12.5 +125 - (self.right_added - 23)*125, self.height/2 - 70 + 50*2+ 125 * 2 - 62.5 - 12.5 - (5) * 125+ 50 - 50))
                self.LeftRight[1] = Button(self.width/2 - 62 + (3 + 1) * 125 - 50 + 50 + 62.5 + 12.5 +125 - (self.right_added - 23)*125, self.height/2 - 70 + 50*2+ 125 * 2 - 62.5 - 12.5 - (5) * 125+ 50 - 50 + 62.5, 50, 62.5, 1)
            self.right_added += 1
            
        if (sight == -1):
            if (self.left_added <= 1):
                if (flipped == True):  
                    image = pygame.transform.rotate(image, 180)
                self.win.blit(image, (self.width/2 - 62 - (self.left_added + 1) * 125, self.height/2 - 70))
                self.LeftRight[0] = Button(self.width/2 - 62 - (self.left_added + 1) * 125 + 62.5, self.height/2 - 70, 62.5, 50, 0)
            elif (self.left_added <= 3):
                if (flipped == True):  
                    image = pygame.transform.rotate(image, 180)
                image = pygame.transform.rotate(image, 90)
                self.win.blit(image, (self.width/2 - 62 - 2 * 125, self.height/2 - 70 + 50 + (self.left_added % 2) * 125))
                self.LeftRight[0] = Button(self.width/2 - 62 - 2 * 125, self.height/2 - 70 + 50 + (self.left_added % 2) * 125 + 62.5, 50, 62.5, 0)
            elif (self.left_added <= 4):
                if (flipped == True):  
                    image = pygame.transform.rotate(image, 180)
                self.win.blit(image, (self.width/2 - 62 -12.5 - 2 * 125 - 62.5, self.height/2 - 70 + 50 + 2 * 125))
                self.LeftRight[0] = Button(self.width/2 - 62 -12.5 - 2 * 125 - 62.5 +62.5, self.height/2 - 70 + 50 + 2 * 125, 62.5, 50, 0)
            elif (self.left_added <= 9):
                if (flipped == True):  
                    image = pygame.transform.rotate(image, 180)
                image = pygame.transform.rotate(image, 90)
                self.win.blit(image, (self.width/2 - 125 - 2 * 125 - 62, self.height/2 - 70 + 50 - (self.left_added - 6) * 125 + 50))
                self.LeftRight[0] = Button(self.width/2 - 125 - 2 * 125 - 62, self.height/2 - 70 + 50 - (self.left_added - 6) * 125 + 50 +62.5, 50, 62.5, 0)
            elif (self.left_added <= 10):
                if (flipped == True):  
                    image = pygame.transform.rotate(image, 180)
                self.win.blit(image, (self.width/2 - 125 - 2 * 125 - 62 - 125, self.height/2 - 70 + 50 - (self.left_added - 7) * 125 + 50))
                self.LeftRight[0] = Button(self.width/2 - 125 - 2 * 125 - 62 - 125 +62.5, self.height/2 - 70 + 50 - (self.left_added - 7) * 125 + 50, 62.5, 50, 0)
            elif (self.left_added <= 15):
                if (flipped == True):  
                    image = pygame.transform.rotate(image, 180)
                image = pygame.transform.rotate(image, 90)
                self.win.blit(image, (self.width/2 - 125 - 2 * 125 - 62 - 125, self.height/2 - 70 + 50 - (self.left_added - 12) * 125 + 100))
                self.LeftRight[0] = Button(self.width/2 - 125 - 2 * 125 - 62 - 125, self.height/2 - 70 + 50 - (self.left_added - 12) * 125 + 100 +62.5, 50, 62.5, 0)
            elif (self.left_added <= 16):
                if (flipped == True):  
                    image = pygame.transform.rotate(image, 180)
                self.win.blit(image, (self.width/2 - 125 - 2 * 125 - 62 -62.5 -62.5 - 125, self.height/2 - 70 + 50 - (self.left_added - 17) * 125 + 100 + 62.5 + 12.5))
                self.LeftRight[0] = Button(self.width/2 - 125 - 2 * 125 - 62 -62.5 -62.5 - 125 +62.5, self.height/2 - 70 + 50 - (self.left_added - 17) * 125 + 100 + 62.5 + 12.5, 62.5, 50, 0)
            elif (self.left_added <= 22):
                if (flipped == True):  
                    image = pygame.transform.rotate(image, 180)
                image = pygame.transform.rotate(image, 90)
                self.win.blit(image, (self.width/2 - 125 - 2 * 125 - 62 -62.5 -62.5 - 125, self.height/2 - 70 + 50 - (self.left_added - 17) * 125 + 100 + 62.5 + 12.5))
                self.LeftRight[0] = Button(self.width/2 - 125 - 2 * 125 - 62 -62.5 -62.5 - 125, self.height/2 - 70 + 50 - (self.left_added - 17) * 125 + 100 + 62.5 + 12.5 +62.5, 50, 62.5, 0)
            elif (self.left_added <= 25):
                if (flipped == True):  
                    image = pygame.transform.rotate(image, 180)
                self.win.blit(image, (self.width/2 - 125 - 2 * 125 - 62 -62.5 -62.5 - 125 + 50 + (self.left_added -23) *125, self.height/2 - 70 + 50 - (5) * 125 + 100 + 62.5 + 12.5))
                self.LeftRight[0] = Button(self.width/2 - 125 - 2 * 125 - 62 -62.5 -62.5 - 125 + 50 + (self.left_added -23) *125 +62.5, self.height/2 - 70 + 50 - (5) * 125 + 100 + 62.5 + 12.5, 62.5, 50, 0)
            elif (self.left_added <= 26):
                if (flipped == True):  
                    image = pygame.transform.rotate(image, 180)
                image = pygame.transform.rotate(image, 90)
                self.win.blit(image, (self.width/2 - 125 -50 - 2 * 125 - 62 -62.5 -62.5 - 125 + 50 + (self.left_added -23) *125, self.height/2 - 70 + 50 - (5) * 125 + 100 + 62.5 + 12.5+50))
                self.LeftRight[0] = Button(self.width/2 - 125 -50 - 2 * 125 - 62 -62.5 -62.5 - 125 + 50 + (self.left_added -23) *125, self.height/2 - 70 + 50 - (5) * 125 + 100 + 62.5 + 12.5+50+62.5, 50, 62.5, 0)
            self.left_added += 1
        pygame.display.update()
            