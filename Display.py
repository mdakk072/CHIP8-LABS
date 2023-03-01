import random
from tkinter import filedialog
import numpy as np
import pygame

from Keypad import Keypad

import pygame

class Display:
    def __init__(self, scale=5,menu=False,cpu=None):
        self.menu=menu
        # Initialisation de la classe Display
        self.scale = scale
        pygame.init() # Initialisation de Pygame
        self.screen = pygame.display.set_mode((128 * scale, 64 * scale),)
        self.rateHz=60#Hz
        self.pixels = [[0 for _ in range(64)] for _ in range(32)] # Déclaration de la variable pixels
        self.volume=0.5
        self.cpu=cpu
        pygame.display.set_caption(f"Emulateur Chip-8 ")

        self.Icon = pygame.image.load('assets/icon.png')
        pygame.display.set_icon(self.Icon)

        # Ajout de la barre de menu
        if menu:
           
            self.add_menu()

        self.draw()

    def add_menu(self):
        # Création de la barre de menu
        self.menu_bar = pygame.Surface((128 * self.scale, 20))
        self.menu_bar.fill((255, 255, 255))

        # Ajout des boutons à la barre de menu
        button_width = 80
        button_height = 16
        self.button_width = 80
        self.button_height = 16
        load_rom_button = pygame.Surface((button_width, button_height))
        load_rom_button.fill((100, 100, 100))
        self.load_rom_button_rect = load_rom_button.get_rect()
        self.load_rom_button_rect.x = 10
        self.load_rom_button_rect.y = 2
        load_rom_text = pygame.font.SysFont('Arial', 14).render('Load Rom', True, (255, 255, 255))
        load_rom_text_rect = load_rom_text.get_rect(center=load_rom_button.get_rect().center)
        load_rom_button.blit(load_rom_text, load_rom_text_rect)

        reset_button = pygame.Surface((button_width, button_height))
        reset_button.fill((100, 100, 100))
        self.reset_button_rect = reset_button.get_rect()
        self.reset_button_rect.x = self.load_rom_button_rect.x + button_width + 10
        self.reset_button_rect.y = 2
        reset_button_text = pygame.font.SysFont('Arial', 14).render('Reset', True, (255, 255, 255))
        reset_button_text_rect = reset_button_text.get_rect(center=reset_button.get_rect().center)
        reset_button.blit(reset_button_text, reset_button_text_rect)

        random_rom_button = pygame.Surface((button_width, button_height))
        random_rom_button.fill((100, 100, 100))
        self.random_rom_button_rect = random_rom_button.get_rect()
        self.random_rom_button_rect.x = self.reset_button_rect.x + button_width + 10
        self.random_rom_button_rect.y = 2
        random_rom_button_text = pygame.font.SysFont('Arial', 14).render('Random ROM', True, (255, 255, 255))
        random_rom_button_text_rect = random_rom_button_text.get_rect(center=random_rom_button.get_rect().center)
        random_rom_button.blit(random_rom_button_text, random_rom_button_text_rect)

        OnOff_button = pygame.Surface((button_width, button_height))
        OnOff_button.fill((100, 100, 100))

        self.OnOff_button_rect = OnOff_button.get_rect()
        self.OnOff_button_rect.x = self.random_rom_button_rect.x + button_width + 10
        self.OnOff_button_rect.y = 2
        OnOff_button_text = pygame.font.SysFont('Arial', 14).render('ON / OFF', True, (255, 255, 255))
        OnOff_button_text_rect = OnOff_button_text.get_rect(center=OnOff_button.get_rect().center)
        OnOff_button.blit(OnOff_button_text, OnOff_button_text_rect)

        # Affichage des boutons sur la barre de menu
        self.menu_bar.blit(load_rom_button, self.load_rom_button_rect)
        self.menu_bar.blit(reset_button, self.reset_button_rect)
        self.menu_bar.blit(random_rom_button, self.random_rom_button_rect)
        self.menu_bar.blit(OnOff_button, self.OnOff_button_rect)

        # Affichage de la barre de menu sur l'écran
        self.screen.blit(self.menu_bar, (0, 0))
        pygame.display.update()
        '''
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.load_rom_button_rect.collidepoint(mouse_pos):
                        self.load_rom()
                    elif self.reset_button_rect.collidepoint(mouse_pos):
                        self.reset()
                    elif self.random_rom_button_rect.collidepoint(mouse_pos):
                        self.random_rom()
                    elif self.OnOff_button_rect.collidepoint(mouse_pos):
                        self.toggleOnOff()
        '''
        
        # Gestion des événements pour chaque bouton
    def getMenuKey(self):
        
        i=1000
        while i!=0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.load_rom_button_rect.collidepoint(mouse_pos):
                        self.load_rom()
                        return

                    elif self.reset_button_rect.collidepoint(mouse_pos):
                        self.reset()
                        return

                    elif self.random_rom_button_rect.collidepoint(mouse_pos):
                        self.random_rom()
                        return

                    elif self.OnOff_button_rect.collidepoint(mouse_pos):
                        self.toggleOnOff()
                        return
            i-=1
        

    def load_rom(self):
        # Fonction appelée lors du clic sur le bouton Load Rom
        self.cpu.load_random_rom()
        pygame.display.set_caption(f"Emulateur Chip-8 {self.cpu.rom_path.split('/')[-1]}")

        # Répertoire par défaut
        repertoire_par_defaut = "roms/"
        # Ouvrir la boîte de dialogue pour sélectionner un fichier
        fichier = filedialog.askopenfilename(initialdir=repertoire_par_defaut)
        self.cpu.load_rom(fichier,)


    def reset(self):
        # Fonction appelée lors du clic sur le bouton Reset
        #print("Reset button clicked")
        self.cpu.reset()

    def random_rom(self):
        # Fonction appelée lors du clic sur le bouton Random Rom
        #print("Random Rom button clicked")
        self.cpu.load_random_rom()
    def toggleOnOff(self):
        # Fonction appelée lors du clic sur le bouton Random Rom
        #print("ON / OFF clicked")
        OnOff_button = pygame.Surface((self.button_width, self.button_height))
        self.OnOff_button_rect = OnOff_button.get_rect()
        self.OnOff_button_rect.x = self.random_rom_button_rect.x + self.button_width + 10
        self.OnOff_button_rect.y = 2
        
        if self.cpu.running:
            OnOff_button_text = pygame.font.SysFont('Arial', 14).render('OFF', True, (255, 255, 255))
            OnOff_button_text_rect = OnOff_button_text.get_rect(center=OnOff_button.get_rect().center)
            OnOff_button.fill((255, 0, 0))
            self.cpu.reset(run=False)
            
        else:
            OnOff_button_text = pygame.font.SysFont('Arial', 14).render('ON', True, (255, 255, 255))
            OnOff_button_text_rect = OnOff_button_text.get_rect(center=OnOff_button.get_rect().center)
            OnOff_button.fill((70, 255, 180))
            self.cpu.reset(run=True)
        
        OnOff_button.blit(OnOff_button_text, OnOff_button_text_rect)
        self.menu_bar.blit(OnOff_button, self.OnOff_button_rect)
        self.screen.blit(self.menu_bar, (0, 0))
        pygame.display.update()
        
        
            #self.cpu.boot


    def clear(self):
        # Efface l'écran en mettant tous les pixels à 0
        self.pixels = [[0 for _ in range(64)] for _ in range(32)]
        self.draw()

    def draw(self, pixels=None):
        # Créer une surface de la taille de l'écran
        surface = pygame.Surface((64 * self.scale, 32 * self.scale))
        
        # Remplir la surface avec une couleur de fond
        surface.fill((3, 50, 255))
        
        # Si aucun pixels n'est fourni, utiliser les pixels actuels de la puce
        if pixels is None:
            pixels = self.pixels
        
        # Parcourir tous les pixels et dessiner un rectangle pour ceux qui ont la valeur 1
        for y in range(32):
            for x in range(64):
                if pixels[y][x]:
                    color = (255, 255, 255) # Blanc pour les pixels allumés
                else:
                    color = (3, 50, 255) # Noir pour les pixels éteints
                    
                rect = pygame.Rect(x * self.scale, y * self.scale, self.scale, self.scale)
                pygame.draw.rect(surface, color, rect)
        
        # Redimensionner la surface pour un affichage plus grand
        
        y_offset =  self.menu_bar.get_height() if self.menu else 0

        surface = pygame.transform.scale(surface, (128 * self.scale, (64 * self.scale)-self.scale))
        # Définir la position de l'affichage de la surface en utilisant une valeur de décalage pour les coordonnées y
        
        self.screen.blit(surface, (0, y_offset))
        # Dessiner la surface à l'écran
        #self.screen.blit(surface, (0, 0))
        
        # Actualiser l'affichage
        pygame.display.flip()


        # Affiche la surface à l'écran


    def draw_pixel(self, x, y, value):
        # Mise à jour du pixel
        self.pixels[x][y] ^= value

        # Ajout de la coordonnée à la liste des pixels modifiés
        self.modified_pixels.append((x, y))




    def refresh(self):
            
            self.draw()
            pygame.display.flip() # Met à jour l'écran
            #pygame.time.wait(1000 // self.rateHz) # Attend 1/60ème de seconde (environ 16 ms) pour simuler un taux de rafraîchissement de 60 Hz
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
