import os
import random
import time
import tkinter as tk
from CPU import CPU
import threading

from Display import Display

def getRomFiles():
    path = os.getcwd()  # récupère le répertoire de travail actuel

    ch8_files = []  # liste pour stocker les noms des fichiers .ch8

    # parcourt tous les fichiers dans le répertoire de travail
    for filename in os.listdir(path):
        if filename.endswith(".ch8"):  # vérifie si le fichier a l'extension .ch8
            ch8_files.append(filename)  # ajoute le nom du fichier à la liste
    return ch8_files

#print(ch8_files)  # affiche la liste des fichiers .ch8




class Debugger:
    """
    Classe représentant le débogueur de l'émulateur Chip8.
    """

class Debugger:
    """
    Classe représentant le débogueur de l'émulateur Chip8.
    """

    def __init__(self, cpu, rom_path):
        """
        Initialise le débogueur avec le CPU et le chemin d'accès au fichier ROM.
        """
        self.cpu = cpu
        self.cpu.running = False
        self.cpu.load_rom(rom_path)
        self.window = tk.Tk()
        self.window.title(f"Chip8 Debugger - {rom_path}")

        # Couleur de fond de la fenêtre
        self.bg_color = "white"

        # Frame pour afficher les instructions
        instructions_frame = tk.Frame(self.window, bg=self.bg_color)
        instructions_frame.pack(side=tk.LEFT, padx=5, pady=5)
        
        instructions_label = tk.Label(instructions_frame, text="Instructions:", bg=self.bg_color)
        instructions_label.pack(side=tk.TOP, padx=5, pady=5)

        self.instructions_text = tk.Text(instructions_frame, width=50, height=30)
        self.instructions_text.pack(side=tk.LEFT, padx=5, pady=5)

        instructions_scrollbar = tk.Scrollbar(instructions_frame, command=self.instructions_text.yview)
        instructions_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.instructions_text.config(yscrollcommand=instructions_scrollbar.set)
        

        # Frame pour afficher les registres

        registers_frame = tk.Frame(self.window, bg=self.bg_color)
        registers_frame.pack(side=tk.RIGHT, padx=5, pady=5)

        registers_label = tk.Label(registers_frame, text="Registres:", bg=self.bg_color)
        registers_label.pack(side=tk.TOP, padx=5, pady=5)

        self.registers_text = tk.Text(registers_frame, width=25, height=30)
        self.registers_text.pack(side=tk.LEFT, padx=5, pady=5)

        

        registers_scrollbar = tk.Scrollbar(registers_frame, command=self.registers_text.yview)
        registers_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.registers_text.config(yscrollcommand=registers_scrollbar.set)

        # Boutons pour exécuter les instructions
        buttons_frame = tk.Frame(self.window, bg=self.bg_color)
        buttons_frame.pack(side=tk.BOTTOM, padx=5, pady=5)

        step_button = tk.Button(buttons_frame, text="Step", command=self.step)
        step_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.run_button = tk.Button(buttons_frame, text="Run", command=self.toggle_run_pause)
        self.run_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Nouveaux boutons
        reset_button = tk.Button(buttons_frame, text="Reset", command=self.reset)
        reset_button.pack(side=tk.LEFT, padx=5, pady=5)

        random_rom_button = tk.Button(buttons_frame, text="Load Random ROM", command=self.load_random_rom)
        random_rom_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Personnalisation des couleurs et polices
        self.button_bg_color = "gray"
        self.button_font = ("Arial", 12)
        step_button.config(bg=self.button_bg_color, font=self.button_font)
        self.run_button.config(bg=self.button_bg_color, font=self.button_font)
        reset_button.config(bg=self.button_bg_color, font=self.button_font)
        random_rom_button.config(bg=self.button_bg_color, font=self.button_font)
        
        self.window.config(bg=self.bg_color)

       

    def update_registers(self):
        """
        Met à jour l'affichage des registres et des compteurs de temporisation.
        """
        self.registers_text.delete("1.0", tk.END)
        for i in range(16):
            self.registers_text.insert(tk.END, "V{}: {}\n".format(i, hex(self.cpu.V[i])))
        self.registers_text.insert(tk.END, "PC : {}\n".format(str(hex(self.cpu.pc)).upper()))
        self.registers_text.insert(tk.END, "Index : {}\n".format(str(hex(self.cpu.I)).upper()))
        self.registers_text.insert(tk.END, "Timer Delay : {}\n".format(self.cpu.delay_timer))
        self.registers_text.insert(tk.END, "Timer Son  : {}\n".format(self.cpu.sound_timer))
        self.registers_text.insert(tk.END, "Stack : {}\n".format(str(self.cpu.stack)))

    def reset(self):
        """
        Réinitialise l'exécution de la ROM en rechargeant le fichier ROM.
        """
        self.cpu.reset(run=False)
        self.cpu.load_rom(self.cpu.rom_path)
        self.updateWindow()
        
        self.run_button.config(text="Run")

    def load_random_rom(self):
        """
        Charge une ROM aléatoire pour le débogage.
        """
        roms = getRomFiles() # Liste de ROMs disponibles pour le débogage
        rom_path = random.choice(roms) # Choix aléatoire d'une ROM
        self.cpu.rom_path=rom_path
        self.reset() # Chargement de la ROM dans le processeur
        self.window.title(f"Chip8 Debugger - {rom_path}") # Mise à jour du titre de la fenêtre


    def toggle_run_pause(self):
        if self.cpu.running:
            self.cpu.running = False
            self.run_button.config(text="Run")
            self.updateWindow()

        else:
            self.cpu.running = True
            self.run_button.config(text="Pause")
            self.updateWindow()
    def close_window(self):
        """
        Ferme la fenêtre du débogueur.
        """
        self.window.destroy()


    def step(self):
        """
        Exécute l'instruction suivante et met à jour l'affichage.
        """
        self.cpu.cycle()
        self.updateWindow()

    def updateWindow(self):

        opcode = (self.cpu.memory[self.cpu.pc] << 8) | self.cpu.memory[self.cpu.pc + 1]
        self.instructions_text.insert(tk.END, f'${str(hex(self.cpu.pc)).upper()}: '+str(hex(opcode)).upper() + f" //{self.cpu.getInstructionHelp(opcode)}\n")

        self.registers_text.delete("1.0", tk.END)
        for i in range(16):
            self.registers_text.insert(tk.END, "V{}: {}\n".format(i, hex(self.cpu.V[i])))
        self.registers_text.insert(tk.END, "PC : {}\n".format(str(hex(self.cpu.pc)).upper()))
        self.registers_text.insert(tk.END, "Index : {}\n".format(str(hex(self.cpu.I)).upper()))
        self.registers_text.insert(tk.END, "Timer Delay : {}\n".format(self.cpu.delay_timer))
        self.registers_text.insert(tk.END, "Timer Son  : {}\n".format(self.cpu.sound_timer))
        self.registers_text.insert(tk.END, "Stack : {}\n".format(str(self.cpu.stack)))


        self.instructions_text.see(tk.END)

    def run(self):
        """
        Démarre l'affichage de la fenêtre.
        """
        #self.window.mainloop()
        while True :
            self.window.update()
            if self.cpu.running :
             self.cpu.cycle()
             print(f'>Run {self.cpu.running}',end='\r')
        
            # Attend un court instant pour éviter une utilisation excessive de la CPU
            time.sleep(0.001)
            
            # Si la fenêtre a été fermée, arrête la boucle
            if not self.window.winfo_exists():
                break 
cpu = CPU(display=Display())  # créer une instance de votre CPU
rom_path = "IBM Logo.ch8"  # le chemin d'accès à votre fichier ROM
#rom_path = "Figures.ch8"
roms=getRomFiles()
random_element = random.choice(roms)
debugger = Debugger(cpu, random_element)  # créer une instance du débogueur
debugger.run()
'''
display = Display()
key=Keypad(display.screen)
display.test()
display.close()

'''
