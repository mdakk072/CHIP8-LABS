import json
import os
import random
import time
import tkinter as tk
from CPU import CPU
import threading
from Keypad import Keypad

from Display import Display

keypadKeys=[0X1 ,0X2 ,0X3 ,0XC ,
            0X4 ,0X5 ,0X6 ,0XD ,
            0X7 ,0X8 ,0X9 ,0XE ,
            0Xa ,0X0 ,0XB ,0XF ,]
def getRomFiles():
    path = os.getcwd()  # récupère le répertoire de travail actuel
    path+=r'//roms'
    ch8_files = []  # liste pour stocker les noms des fichiers .ch8

    # parcourt tous les fichiers dans le répertoire de travail
    for filename in os.listdir(path):
        if filename.endswith(".ch8"):  # vérifie si le fichier a l'extension .ch8
            ch8_files.append(filename)  # ajoute le nom du fichier à la liste
    return ch8_files

#print(ch8_files)  # affiche la liste des fichiers .ch8


import tkinter as tk

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
        self.instructions_frame = tk.Frame(self.window, bg=self.bg_color)
        self.instructions_frame.grid(row=0, column=0, padx=5, pady=5)

        self.instructions_label = tk.Label(self.instructions_frame, text="Instructions:", bg=self.bg_color)
        self.instructions_label.grid(row=0, column=0, padx=1, pady=1)

        self.instructions_text = tk.Text(self.instructions_frame, width=70, height=30)
        self.instructions_text.grid(row=1, column=0, padx=2, pady=2)
        opcode = (self.cpu.memory[self.cpu.pc] << 8) | self.cpu.memory[self.cpu.pc + 1]
        self.instructions_text.insert(tk.END, f'$Adress: ', 'HEXadress')
        self.instructions_text.insert(tk.END, 'Opcode', 'opcode')
        self.instructions_text.insert(tk.END, f"    //Commentaire\n", 'com')

        # Définition des tags de style
        self.instructions_text.tag_configure('HEXadress', font=('Segoe UI Symbol', 12, 'bold'))
        self.instructions_text.tag_configure('HEXadressK', font=('Segoe UI Symbol', 12, 'bold'), foreground='red')
        self.instructions_text.tag_configure('com', font=('Segoe UI Symbol', 12, ))
        self.instructions_text.tag_configure('opcode', font=('Segoe UI Symbol', 12, ))
        self.instructions_scrollbar = tk.Scrollbar(self.instructions_frame, command=self.instructions_text.yview)
        self.instructions_scrollbar.grid(row=1, column=1, sticky="NS")
        # Boutons pour exécuter les instructions
        self.buttons_frame = tk.Frame(self.instructions_frame, bg=self.bg_color)
        self.buttons_frame.grid(row=2, column=0, padx=5, pady=5)

        self.step_button = tk.Button(self.buttons_frame, text="Step", command=self.step)
        self.step_button.grid(row=0, column=0, padx=5, pady=5)

        self.step_button = tk.Button(self.buttons_frame, text="Step Back", command=self.stepBack)
        self.step_button.grid(row=0, column=1, padx=5, pady=5)

        self.run_button = tk.Button(self.buttons_frame, text="Run", command=self.toggle_run_pause)
        self.run_button.grid(row=0, column=2, padx=5, pady=5)

        # Nouveaux boutons
        self.reset_button = tk.Button(self.buttons_frame, text="Reset", command=self.reset)
        self.reset_button.grid(row=0, column=3, padx=5, pady=5)

        self.reset_button = tk.Button(self.buttons_frame, text="Stop", command=self.stop)
        self.reset_button.grid(row=0, column=4, padx=5, pady=5)

        self.instructions_text.config(yscrollcommand=self.instructions_scrollbar.set)
        # LabelFrame pour afficher les informations CPU
        self.cpu_frame = tk.LabelFrame(self.window, text="CPU Infos", bg=self.bg_color)
        self.cpu_frame.grid(row=0, column=1,padx=5, pady=5, )

        # Label et Entry pour les registres V0-VF
        self.v_registers_label = tk.Label(self.cpu_frame, text="Registres V0-VF", bg=self.bg_color)
        self.v_registers_label.grid(row=0, column=0, padx=5, pady=5, sticky="W")

        self.v_registers_entries = []
        for i in range(8):
            # Afficher deux registres par ligne
            v_register_label1 = tk.Label(self.cpu_frame, text=f"V{i*2:X}: ", bg=self.bg_color)
            v_register_label1.grid(row=i, column=0, padx=5, pady=5, sticky="E")
            v_register_entry1 = tk.Entry(self.cpu_frame, width=5,state="normal")
            v_register_entry1.grid(row=i, column=1, padx=5, pady=5)

            v_register_label2 = tk.Label(self.cpu_frame, text=f"V{i*2+1:X}: ", bg=self.bg_color)
            v_register_label2.grid(row=i, column=2, padx=5, pady=5, sticky="E")
            v_register_entry2 = tk.Entry(self.cpu_frame, width=5,state="normal")
            v_register_entry2.grid(row=i, column=3, padx=5, pady=5)
            self.v_registers_entries.append(v_register_entry1)
            self.v_registers_entries.append(v_register_entry2)

        # Label et Entry pour le registre d'adresse I
        self.i_register_label = tk.Label(self.cpu_frame, text="Registre I: ", bg=self.bg_color)
        self.i_register_label.grid(row=8, column=0, padx=5, pady=5, sticky="E")
        self.i_register_entry = tk.Entry(self.cpu_frame, width=10)
        self.i_register_entry.grid(row=8, column=1, columnspan=3, padx=5, pady=5)

        # Label et Entry pour le registre de programme
        self.pc_label = tk.Label(self.cpu_frame, text="Program Counter: ", bg=self.bg_color)
        self.pc_label.grid(row=9, column=0, padx=5, pady=5, sticky="E")
        self.pc_entry = tk.Entry(self.cpu_frame, width=10)
        self.pc_entry.grid(row=9, column=1, columnspan=3, padx=5, pady=5)

        # Label et Entry pour le registre de pile
        self.sp_label = tk.Label(self.cpu_frame, text="Stack Pointer: ", bg=self.bg_color)
        self.sp_label.grid(row=10, column=0, padx=5, pady=5, sticky="E")
        self.sp_entry = tk.Entry(self.cpu_frame, width=10)
        self.sp_entry.grid(row=10, column=1, columnspan=3, padx=5, pady=5)

        # Label et Entry pour le compteur de cycles
        self.cycle_count_label = tk.Label(self.cpu_frame, text="Cycles: ", bg=self.bg_color)
        self.cycle_count_label.grid(row=11, column=0, padx=5, pady=5, sticky="E")
        self.cycle_count_entry = tk.Entry(self.cpu_frame, width=10)
        self.cycle_count_entry.grid(row=11, column=1, columnspan=3, padx=5, pady=5)
        # Label et Entry pour le compteur de DelayTimer
        self.delay_timer_label = tk.Label(self.cpu_frame, text="DTimer: ", bg=self.bg_color)
        self.delay_timer_label.grid(row=12, column=0, padx=5, pady=5, sticky="E")
        self.delay_timer_entry = tk.Entry(self.cpu_frame, width=10)
        self.delay_timer_entry.grid(row=12, column=1, columnspan=3, padx=5, pady=5)
        # Label et Entry pour le compteur de DelaySound
        self.delay_sound_label = tk.Label(self.cpu_frame, text="Dsound: ", bg=self.bg_color)
        self.delay_sound_label.grid(row=13, column=0, padx=5, pady=5, sticky="E")
        self.delay_sound_entry = tk.Entry(self.cpu_frame, width=10)
        self.delay_sound_entry.grid(row=13, column=1, columnspan=3, padx=5, pady=5)
        self.rateScale_label = tk.Label(self.cpu_frame, text="Rate (Hz): ", bg=self.bg_color)
        self.rateScale_label.grid(row=14, column=0, padx=5, pady=5, sticky="E")
        self.rateScale = tk.Scale(self.cpu_frame, from_=1, to=2000, orient=tk.HORIZONTAL, )
        self.rateScale.set(self.cpu.display.rateHz)
        self.rateScale.grid(row=14, column=1, columnspan=3, padx=5, pady=5)
        self.soundScale_label = tk.Label(self.cpu_frame, text="Sound: ", bg=self.bg_color)
        self.soundScale_label.grid(row=15, column=0, padx=5, pady=5, sticky="E")
        self.soundScale = tk.Scale(self.cpu_frame, from_=0, to=10, orient=tk.HORIZONTAL, )
        #self.cpu.display.volume=0.8
        self.soundScale.set(self.cpu.display.volume*10)

        self.soundScale.grid(row=15, column=1, columnspan=3, padx=5, pady=5)
        # Création de la frame
        self.rom_frame = tk.LabelFrame(self.window, text=f"ROMs {len(getRomFiles())} ", bg=self.bg_color)
        self.rom_frame.grid(row=1, column=1, padx=5, pady=5)

        # Création de la liste box pour afficher les ROM disponibles
        self.rom_listbox = tk.Listbox(self.rom_frame, width=30,height=5)
        self.rom_listbox.grid(row=0, column=0, padx=5, pady=5)
        for file_name in getRomFiles():
            self.rom_listbox.insert(tk.END, file_name)

        self.rombuttons_frame = tk.Frame(self.rom_frame, bg=self.bg_color)
        self.rombuttons_frame.grid(row=2, column=0, padx=5, pady=5)
        # Création des boutons pour charger une ROM et générer une ROM aléatoire
        self.load_rom_button = tk.Button(self.rombuttons_frame, text="Charger une ROM", command=self.loadSelectedRom)
        self.load_rom_button.grid(row=0, column=0, padx=0, pady=0)

        self.random_rom_button = tk.Button(self.rombuttons_frame, text="Générer une ROM aléatoire", command=self.load_random_rom)
        self.random_rom_button.grid(row=0, column=1, padx=0, pady=0)


        self.keypad_frame = tk.Frame(self.window, bg=self.bg_color)
        self.keypad_frame.grid(row=1, column=0, padx=5, pady=5)

        # Création des 16 labels pour les touches
        self.key_labels = []
        for i in range(16):
            row = i // 4
            col = i % 4

            label = tk.Button(self.keypad_frame, text=hex(keypadKeys[i]).upper(),command=lambda button_text=hex(keypadKeys[i]).upper(): self.handleDebugBtn(button_text))
            label.grid(row=row, column=col, padx=5, pady=5)
            label.configure(bg='red')

  

            self.key_labels.append(label)


        self.updateWindow()

    def handleDebugBtn(self,Button):
            Button=int(Button,16)
            if self.cpu.keypad.keys[Button]==True and (Button in self.cpu.keypad.pressedKeys):


                self.cpu.keypad.keys[Button]=False
                self.cpu.keypad.pressedKeys.remove(Button)
            else:
                self.cpu.keypad.keys[Button]=True
                self.cpu.keypad.pressedKeys.append(Button)
            self.updateWindow()
            


    def reset(self):
        """
        Réinitialise l'exécution de la ROM en rechargeant le fichier ROM.
        """
        self.cpu.reset(run=True)
        
        
        self.instructions_text.insert(tk.END, f'        == Reset ==     \n','reset')
        self.instructions_text.tag_configure('reset', font=('Segoe UI Symbol', 12, 'bold'))
        self.run_button.config(text="Pause")


        self.updateWindow()
    def refreshRate(self, ):
        # Met à jour la valeur de self.rateHz en fonction de la position du curseur sur le Scale
        self.cpu.display.rateHz = int(self.rateScale.get())
    def refreshSound(self,):
        self.cpu.display.volume=self.soundScale.get()*0.1
    def stop(self):
        """
        Réinitialise l'exécution de la ROM en rechargeant le fichier ROM.
        """
        self.cpu.reset(run=False)
        self.cpu.load_rom(self.cpu.rom_path)
        self.instructions_text.delete('1.0', tk.END)

        self.updateWindow()

        
        self.run_button.config(text="Run")


    def load_random_rom(self):
        """
        Charge une ROM aléatoire pour le débogage.
        """
        roms = getRomFiles() # Liste de ROMs disponibles pour le débogage
        rom_path = random.choice(roms) # Choix aléatoire d'une ROM
        self.cpu.rom_path='/roms/'+rom_path
        self.reset() # Chargement de la ROM dans le processeur
        self.window.title(f"Chip8 Debugger - {rom_path}") # Mise à jour du titre de la fenêtre

    def loadSelectedRom(self):
    # Récupération du nom de la ROM sélectionnée
        selected_rom = r'roms/'+self.rom_listbox.get(tk.ACTIVE)

        # Vérification que le fichier existe
        if not os.path.isfile(selected_rom):
            print("Erreur", f"Le fichier {selected_rom} n'existe pas.")
            return

        # Chargement de la ROM dans le processeur
        self.cpu.rom_path = selected_rom
        self.reset()

        # Mise à jour du titre de la fenêtre
        self.window.title(f"Chip8 Debugger - {selected_rom}")
    def updateCPUregs(self):
        for i in range(16):
                self.cpu.V[i]=int(self.v_registers_entries[i].get(),16)
        self.cpu.I=int(self.i_register_entry.get(),16)
        self.cpu.pc=int(self.pc_entry.get(),16)
        #self.cpu.sp=json.load((self.sp_entry.get()),)
        self.cpu.cycle_count=int(self.cycle_count_entry.get(),)
        

    def toggle_run_pause(self):
        if self.cpu.running:
            self.cpu.running = False
            self.run_button.config(text="Run")
            self.updateCPUregs()
            self.updateWindow()

        else:
            for i in range(16):
                self.cpu.V[i]=int(self.v_registers_entries[i].get(),16)
            self.cpu.running = True
            self.run_button.config(text="Pause")
            self.updateWindow()

    def close_window(self):
        """
        Ferme la fenêtre du débogueur.
        """
        self.window.destroy()
    

    def update_label_colors(self):
        self.cpu.keypad.listenKey()
        for labeelIndex,k in enumerate(keypadKeys):
           
            if self.cpu.keypad.keys[k]:
                self.key_labels[labeelIndex].configure(bg='green')
            else:
                self.key_labels[labeelIndex].configure(bg='red')

    def step(self):
        """S
        Exécute l'instruction suivante et met à jour l'affichage.
        """
        self.updateCPUregs()
        self.cpu.cycle()
        self.update_label_colors()

        self.updateWindow()
    def stepBack(self):
        """S
        Exécute l'instruction suivante et met à jour l'affichage.
        """
        #self.updateCPUregs()
        self.cpu.step_back()
        #self.instructions_text.edit_undo()
        # obtenir le contenu actuel du widget Text

        # supprimer le dernier caractère ajouté
        text_content = self.instructions_text.get("1.0", "end-1c")

        # Diviser le contenu en une liste de phrases
        phrases = text_content.splitlines()

        # Supprimer la dernière phrase
        phrases.pop()
        phrases.pop()

        # Effacer tout le contenu du widget Text
        self.instructions_text.delete("1.0", tk.END)

        # Réinsérer les phrases restantes
        new_text_content = "\n".join(phrases)
        new_text_content +="\n"
        self.instructions_text.insert("1.0", new_text_content)
        self.update_label_colors()

        self.updateWindow()
        


    def updateWindow(self):
        self.cpu.decode_instruction()
        
        opcode = (self.cpu.memory[self.cpu.pc] << 8) | self.cpu.memory[self.cpu.pc + 1]
        
        self.instructions_text.insert(tk.END, f'${str(hex(self.cpu.pc)).upper()}: ', )
        self.instructions_text.insert(tk.END, str(hex(opcode)).upper(), )
        if 'st'in self.cpu.decode_input(opcode).lower() or self.cpu.sound_timer>0:
            pass#print('haaaaa')
        if 'k' in self.cpu.decode_instruction(opcode).lower():
            self.instructions_text.insert(tk.END, '  '+self.cpu.decode_input(opcode), )
        else:
            #self.instructions_text.insert(tk.END, '  '+self.cpu.decode_instruction(opcode), 'HEXadress')
            self.instructions_text.insert(tk.END, '  '+self.cpu.decode_input(opcode), )
        try:
            self.instructions_text.insert(tk.END, f" //{self.cpu.getInstructionHelp(opcode).split('-')[-1]}\n",)
        except:
            time.sleep(0.001)
       # if self.cpu.getInstructionHelp(opcode) =="No Op":print(str(hex(opcode)).upper() ,opcode,f" {self.cpu.getInstructionHelp(opcode)} ")
        for i in range(16):
        
         
            self.v_registers_entries[i].delete(0, tk.END)
            self.v_registers_entries[i].insert(0, hex(self.cpu.V[i]).upper())

        self.i_register_entry.delete(0, tk.END)
        self.i_register_entry.insert(tk.END, hex(self.cpu.I).upper())
        self.pc_entry.delete(0, tk.END)
        self.pc_entry.insert(tk.END, hex(self.cpu.pc).upper())
        self.sp_entry.delete(0, tk.END)
        self.sp_entry.insert(tk.END, str([hex(spi).upper() for spi in self.cpu.stack]))
        self.cycle_count_entry.delete(0, tk.END)
        self.cycle_count_entry.insert(tk.END, str(self.cpu.cycle_count))
        self.delay_sound_entry.delete(0, tk.END)
        self.delay_sound_entry.insert(tk.END, self.cpu.sound_timer)
        self.delay_timer_entry.delete(0, tk.END)
        self.delay_timer_entry.insert(tk.END, self.cpu.delay_timer)
        
       


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
             self.updateWindow()
            self.update_label_colors()
            self.refreshRate()
            self.refreshSound()

            # Attend un court instant pour éviter une utilisation excessive de la CPU
            time.sleep(0.0001)
            #if self.cpu.memory[self.cpu.pc+3] in [0xEE,0xE0]: 
                #self.toggle_run_pause()
            #if self.cpu.opcode&0XF000==0XF000 and self.cpu.running==True:self.toggle_run_pause()
            
            # Si la fenêtre a été fermée, arrête la boucle
            if not self.window.winfo_exists():
                break 


display = Display()
#key=Keypad(display.screen)
key=Keypad(display=display)
cpu = CPU(display=display,keypad=key)  # créer une instance de votre CPU
rom_path = "roms/IBM Logo.ch8"  # le chemin d'accès à votre fichier ROM
#rom_path = "Figures.ch8"
roms=getRomFiles()
#random_element = random.choice(roms)
debugger = Debugger(cpu, rom_path)  # créer une instance du débogueur
debugger.run()
'''
display = Display()
key=Keypad(display.screen)
display.test()
display.close()

'''
