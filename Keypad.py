# importing pygame module
import random
import pygame
import threading
# importing sys module
import sys



class Keypad : 

    def __init__(self,display=None) -> None:
        # initialising pygame
        if display==None:
            pygame.init()

            # creating display
            self.display = pygame.display.set_mode((300, 300))
        else : self.display=display

        self.pressedKeys=[]
        
        # defining keymap dictionary
        self.keymap = {
                        pygame.K_1: 0x1, pygame.K_2: 0x2, pygame.K_3: 0x3, pygame.K_4: 0xc,
                        pygame.K_q: 0x4, pygame.K_w: 0x5, pygame.K_e: 0x6, pygame.K_r: 0xd,
                        pygame.K_a: 0x7, pygame.K_s: 0x8, pygame.K_d: 0x9, pygame.K_f: 0xe,
                        pygame.K_z: 0xa, pygame.K_x: 0x0, pygame.K_c: 0xb, pygame.K_v: 0xf}
        self.keys={
                        0x1 : False ,0x2 : False ,0x3 : False ,0xc : False ,
                        0x4 : False ,0x5 : False ,0x6 : False ,0xd : False ,
                        0x7 : False ,0x8 : False ,0x9 : False ,0xe : False ,
                        0xa : False ,0x0 : False ,0xb : False ,0xf : False ,}
        self.keysIndex={
                        0x1 : 0 ,0x2 : 1 ,0x3 : 2 ,0xc : 3 ,
                        0x4 : 4 ,0x5 : 5 ,0x6 : 6 ,0xd : 7 ,
                        0x7 : 8 ,0x8 : 9 ,0x9 : 10 ,0xe : 11 ,
                        0xa : 12 ,0x0 : 13 ,0xb : 14 ,0xf : 15 ,}
        self.keysLabel=[k for k in  self.keys]
       # self.listenKeys()
    def listenKey(self):
        
            for i,key in enumerate(self.keys):
                pass
                #self.keystate[i]=False
                #self.keys[key]=False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in self.keymap:
                        key_value = self.keymap[event.key]
                        self.keys[key_value]=True
                        if key_value not  in self.pressedKeys:
                            self.pressedKeys.append(key_value)
                if event.type == pygame.KEYUP:
                    if event.key in self.keymap:
                        key_value = self.keymap[event.key]
                        self.keys[key_value]=False
                        if key_value   in self.pressedKeys:
                            self.pressedKeys.remove(key_value)
                #print(self.keystate,end='                            \r')
    def listenKeys(self):
        while True:
           self.listenKey()
           print(self.keystate,end='                            \r')
    def randomKey(self):
        self.pressedKeys=[]
        self.keys={
                        0x1 : False ,0x2 : False ,0x3 : False ,0xc : False ,
                        0x4 : False ,0x5 : False ,0x6 : False ,0xd : False ,
                        0x7 : False ,0x8 : False ,0x9 : False ,0xe : False ,
                        0xa : False ,0x0 : False ,0xb : False ,0xf : False ,}
        numkeys=random.randint(0,6)
        while  len(self.pressedKeys)<numkeys :
            rkey=random.choice(self.keysLabel)
            if rkey not in self.pressedKeys:
                self.pressedKeys.append(rkey)
                self.keys[rkey]=True
    



    
