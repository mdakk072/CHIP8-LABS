import random
import numpy as np
import pygame

from Keypad import Keypad

class Display:
    def __init__(self, scale=5):
        # Initialisation de la classe Display
        self.scale = scale
        pygame.init() # Initialisation de Pygame
        pygame.display.set_caption("Emulateur Chip-8")
        #self.screen = pygame.display.set_mode((64 * scale, 32 * scale),)
        self.screen = pygame.display.set_mode((128 * scale, 64 * scale),)
        #self.screen = pygame.display.set_mode((128 * scale, 64 * scale),)
        self.rateHz=240#Hz
        self.pixels = [[0 for _ in range(64)] for _ in range(32)] # Déclaration de la variable pixels
        self.draw()
        self.pixelsstack=[]
        self.modified_pixels = []

        self.volume=0.8

    def clear(self):
        # Efface l'écran en mettant tous les pixels à 0
        self.pixels = [[0 for _ in range(64)] for _ in range(32)]
        self.draw()

    def draw(self,pixels=None):
        # Crée une surface de la taille de l'écran
        surface = pygame.Surface((64 * self.scale, 32 * self.scale))
        surface.fill((34, 34, 255))
        if pixels==None:pixels=self.pixels

        # Parcourt tous les pixels et dessine un rectangle rouge pour ceux qui ont la valeur 1
        for y in range(32):
            for x in range(64):
                if pixels[y][x]:
                    color =  (170, 170, 170)
                    rect = pygame.Rect(x * self.scale, y * self.scale, self.scale, self.scale)
                    pygame.draw.rect(surface, color, rect)
        
        surface = pygame.transform.scale(surface,(128 * self.scale, 64 * self.scale))

        # Affiche la surface à l'écran
        self.screen.blit(surface, (0, 0))
        pygame.display.flip()

    def draw_pixel(self, x, y, value):
        # Mise à jour du pixel
        self.pixels[x][y] ^= value

        # Ajout de la coordonnée à la liste des pixels modifiés
        self.modified_pixels.append((x, y))




    def refresh(self):
            self.pixelsstack.append(self.screen.copy())
            
            self.draw()
            self.screen.flip() # Met à jour l'écran
            pygame.time.wait(1000 // self.rateHz) # Attend 1/60ème de seconde (environ 16 ms) pour simuler un taux de rafraîchissement de 60 Hz
            #spygame.time.wait(1000 // 1000) # Attend 1/60ème de seconde (environ 16 ms) pour simuler un taux de rafraîchissement de 60 Hz
    def set_pixel(self, x, y,sp=None):
        if sp !=None:
            self.pixels[y][x] =sp
        # Change la valeur du pixel à la position donnée (0 ou 1)
        else:
            self.pixels[y][x] ^= 1
    def get_pixel(self,x,y):
        return self.pixels[y][x]
    
    def play_sound(self, volume=1.0):
        volume=self.volume
        pygame.mixer.init(frequency=44100, size=-16, channels=1)

        frequency = 440 
        duration = 1
        duty_cycle = 3 

        samples = int(frequency * duration)
        half_period = int(frequency / (2 * duty_cycle))

        waveform = np.zeros(samples)

        for i in range(0, samples, half_period):
            waveform[i:i+int(half_period*duty_cycle)] = 30000
            waveform[i+int(half_period*duty_cycle):i+half_period] = -30000

        waveform = np.reshape(waveform, (-1, 1))
        waveform = np.repeat(waveform, 2, axis=1)

        # ajuster le volume
        sound_array = (waveform * 32767 / np.max(np.abs(waveform))).astype('int16')
        sound_array = (sound_array * volume).astype('int16')

        sound = pygame.sndarray.make_sound(sound_array)
        sound.play()

    
    def test(self):
        # Teste l'affichage en dessinant des motifs aléatoires jusqu'à ce que l'utilisateur appuie sur une touche pour quitter
        self.clear()
        self.draw()
        pygame.display.flip() # Met à jour l'écran
        pygame.time.wait(1000)
        wait = True
        
        while wait:
            #key.listenKey()
            #print(key.keystate,end='\r')
            # Dessine une forme aléatoire
            self.clear()
            for i in range(random.randint(1, 10)):
                x = random.randint(0, 63)
                y = random.randint(0, 31)
                self.set_pixel(x, y)
            self.draw()
            pygame.display.flip() # Met à jour l'écran
            self.play_sound()
            pygame.time.wait(1000 // 10) # Attend 1/60ème de seconde (environ 16 ms) pour simuler un taux de rafraîchissement de 60 Hz

            # Vérifie si l'utilisateur a appuyé sur une touche pour quitter
            '''
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    wait = False
                elif event.type == pygame.KEYDOWN:
                    wait = False
            '''

        # Ferme la fenêtre Pygame
        pygame.quit()
    
    def close(self):
        # Ferme la fenêtre Pygame
        pygame.quit()