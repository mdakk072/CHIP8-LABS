import csv
import math
import os
import random
import time
import csv

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

class CPU:
    
    """
    Classe représentant le processeur (CPU) de l'émulateur Chip8.
    """

    def __init__(self,display=None,keypad=None):
        """
        Initialise le CPU avec les propriétés nécessaires.
        """
        self.cpustates=[]

        self.running = True
        self.memory = [0] * 4096  # 4K mémoire
        self.load_fonts()
        self.V = [0] * 16  # 16 registres V0-VF
        self.I = 0  # Registre d'index
        self.pc = 0x200  # Compteur de programme, commence à 0x200
        self.stack = []  # Pile pour stocker l'adresse de retour des sous-routines
        self.delay_timer = 0  # Minuterie de délai
        self.sound_timer = 0  # Minuterie de son
        self.display=display if display else None #instance de l'affichage que OpenAi doit me donner
        if display!=None:
            display.cpu=self
        self.opcode=0x12FF
        self.keypad=keypad  
        self.rom_path="IBM Logo.ch8"
        self.cycle_count=0
        self.toInc=2 #valeur d'increment du pc 2 ou 4 selon branch

        self.instructionsHelp={
    0x0: "No Op",
    0xE0: "Effacer écran",
    0xEE: "Retour sous-programme",
    0x1000: "Saut à NNN",
    0x2000: "Appel sous-programme à NNN",
    0x3000: "Saut si VX = NN",
    0x4000: "Saut si VX ≠ NN",
    0x5000: "Saut si VX = VY",
    0x6000: "Charger NN dans VX",
    0x7000: "Ajouter NN à VX",
    0x8000: "Opération arithmétique sur VX et VY",
    0x9000: "Saut si VX ≠ VY",
    0xA000: "Charger NNN dans I",
    0xB000: "Saut à NNN + V0",
    0xC000: "Charger nombre aléatoire masqué par NN dans VX",
    0xD000: "Dessiner sprite",
    0xE000: "Saut si touche pressée",
    0xF000: "Instruction spéciale F"
}


        self.instructions = {
    0x0000: self.noOp,           # Efface l'écran
    0xE0: self.clearDisplay,           # Efface l'écran
    0xEE: self.backFromSub,            # Retourne d'un sous-programme
    0x1000: self.jump,                   # Saut à l'adresse NNN
    0x2000: self.branchToSub,            # Appel de sous-programme à l'adresse NNN
    0x3000: self.skipIfVXEqNN,           # Saut conditionnel si VX == NN
    0x4000: self.skipIfVXNotEqNN,        # Saut conditionnel si VX != NN
    0x5000: self.skipIfVxEqVy,           # Saut conditionnel si VX == VY
    0x6000: self.setVx,                  # Charge NN dans VX
    0x7000: self.addToVx,                # Ajoute NN à VX
    0x8000: self.ArithmeticInstruction,  # Instruction arithmétique sur VX et VY
    0x9000: self.skipIfVxNotEqVy,        # Saut conditionnel si VX != VY
    0xA000: self.setIndex,               # Charge l'adresse NNN dans I
    0xB000: self.JumpOffset,             # Saut à l'adresse NNN + V0
    0xC000: self.Random,                 # Charge dans VX un nombre aléatoire masqué par NN
    0xD000: self.displayDraw,            # Dessine un sprite à l'écran
    0xE000: self.SkipIfKeyPressedInstruction,  # Saut conditionnel si une touche est pressée
    0xF000: self.handle_F_instruction    # Instruction spéciale F
}




    def reset(self,run=True,soundT=2):
        """
        Réinitialise l'état du CPU.
        """
        self.cpustates=[]
        self.running = run
        self.memory = [0] * 4096  # 4K mémoire
        self.load_fonts()
        self.V = [0] * 16  # 16 registres V0-VF
        self.I = 0  # Registre d'index
        self.pc = 0x200  # Compteur de programme, commence à 0x200
        self.stack = []  # Pile pour stocker l'adresse de retour des sous-routines
        self.delay_timer = 00  # Minuterie de délai
        self.sound_timer = soundT  # Minuterie de son
        self.display.clear()
        self.cycle_count=0
        self.load_rom(self.rom_path)

    def bootLogo(self):
        rom_path = "IBM Logo.ch8"
        start_time = time.time()
        cycles_per_second = 600  # ajustez ce nombre pour régler la vitesse d'exécution de la ROM
        s=0   
        while True:
         
            if time.time() - start_time >= 5:
                self.reset(soundT=math.cos(int(time.time())))

                break


            if time.time() - start_time <= 3:
                

                self.load_rom(f'roms//{rom_path}')
                while self.pc != 552:
                    self.cycle()
                    time.sleep(1/cycles_per_second)
                
                    
            
                #self.reset(soundT=5-int(time.time() - start_time))

                if time.time() - start_time <= 3: self.reset(soundT=math.cos(int(time.time())))


    def getInstructionHelp(self,opcode=None):
     opcodeMsb = opcode & 0xF000
     try:
        if opcodeMsb == 0x0000:
            if opcode == 0x00E0:
                return f"{opcode:04x} - Effacer l'écran"
            elif opcode == 0x00EE:
                return f"{opcode:04x} - Retour à l'appelant depuis une sous-routine"
        elif opcodeMsb == 0x1000:
            return f"{opcode:04x} - Sauter à l'adresse {opcode & 0x0FFF}"
        elif opcodeMsb == 0x2000:
            return f"{opcode:04x} - Appeler la sous-routine à l'adresse {opcode & 0x0FFF}"
        elif opcodeMsb == 0x3000:
            return f"{opcode:04x} - Sauter l'instruction suivante si V{opcode & 0x0F00 >> 8:01x} == {opcode & 0x00FF}"
        elif opcodeMsb == 0x4000:
            return f"{opcode:04x} - Sauter l'instruction suivante si V{opcode & 0x0F00 >> 8:01x} != {opcode & 0x00FF}"
        elif opcodeMsb == 0x5000:
            return f"{opcode:04x} - Sauter l'instruction suivante si V{opcode & 0x0F00 >> 8:01x} == V{opcode & 0x00F0 >> 4:01x}"
        elif opcodeMsb == 0x6000:
            return f"{opcode:04x} - Mettre V{opcode & 0x0F00 >> 8:01x} à {opcode & 0x00FF}"
        elif opcodeMsb == 0x7000:
            return f"{opcode:04x} - Ajouter {opcode & 0x00FF} à V{opcode & 0x0F00 >> 8:01x}"
        elif opcodeMsb == 0x8000:
            x = (opcode & 0x0F00) >> 8
            y = (opcode & 0x00F0) >> 4
            
            if opcode & 0x000F == 0x0000:
                return f"{opcode:04x} - Mettre V{x:01x} à V{y:01x}"
            elif opcode & 0x000F == 0x0001:
                return f"{opcode:04x} - Faire V{x:01x} = V{x:01x} OU V{y:01x}"
            elif opcode & 0x000F == 0x0002:
                return f"{opcode:04x} - Faire V{x:01x} = V{x:01x} ET V{y:01x}"
            elif opcode & 0x000F == 0x0003:
                return f"{opcode:04x} - Faire V{x:01x} = V{x:01x} XOR V{y:01x}"
            elif opcode & 0x000F == 0x0004:
                return f"{opcode:04x} - Ajouter V{y:01x} à V{x:01x} avec retenue"
            elif opcode & 0x000F == 0x0005:
                return f"{opcode:04x} - Soustraire V{y:01x} de V{x:01x} avec retenue"
            elif opcode & 0x000F == 0x0006:
                return f"{opcode:04x} - Décaler V{x:01x} à droite de 1 bit"
            elif opcode & 0x000F == 0x0007:
                return f"{opcode:04x} - Faire V{x:01x} = V{y:01x} - V{x:01x} avec retenue"
            elif opcode & 0x000F == 0x000E:
                return f"{opcode:04x} - Décaler V{x:01x} à gauche de 1 bit"
        elif opcodeMsb == 0x9000:
            return f"{opcode:04x} - Sauter l'instruction suivante si V{opcode & 0x0F00 >> 8:01x} != V{opcode & 0x00F0 >> 4:01x}"
        elif opcodeMsb == 0xA000:
            return f"{opcode:04x} - Mettre I à l'adresse {opcode & 0x0FFF}"
        elif opcodeMsb == 0xB000:
            return f"{opcode:04x} - Sauter à l'adresse V0 + {opcode & 0x0FFF}"
        elif opcodeMsb == 0xC000:
            return f"{opcode:04x} - Mettre V{opcode & 0x0F00 >> 8:01x} à un nombre aléatoire entre 0 et 255 ET {opcode & 0x00FF}"
        elif opcodeMsb == 0xD000:
            return f"{opcode:04x} - Dessiner un sprite à la position (V{opcode & 0x0F00 >> 8:01x}, V{opcode & 0x00F0 >> 4:01x}) de largeur 8 pixels et de hauteur {opcode & 0x000F} pixels"
        elif opcodeMsb == 0xE000:
            if opcode & 0x00FF == 0x009E:
                x = (opcode & 0x0F00) >> 8

                return f"{opcode:04x} - Sauter l'instruction suivante si la touche V{x:01x} est pressée"
            elif opcode & 0x00FF == 0x00A1:
                x = (opcode & 0x0F00) >> 8
                return f"{opcode:04x} - Sauter l'instruction suivante si la touche V{x:01x} n'est pas pressée"
        elif opcodeMsb == 0xF000:
            x = (opcode & 0x0F00) >> 8
            
            if opcode & 0x00FF == 0x0007:
                return f"{opcode:04x} - Mettre V{x:01x} à la valeur de la delay timer"
            elif opcode & 0x00FF == 0x000A:
                return f"{opcode:04x} - Attendre une pression de touche et la stocker dans V{x:01x}"
            elif opcode & 0x00FF == 0x0015:
                return f"{opcode:04x} - Mettre la valeur de V{x:01x} dans le delay timer"
            elif opcode & 0x00FF == 0x0018:
                return f"{opcode:04x} - Mettre la valeur de V{x:01x} dans le sound timer"
            elif opcode & 0x00FF == 0x001E:
                return f"{opcode:04x} - Ajouter V{x:01x} à I"
            elif opcode & 0x00FF == 0x0029:
                return f"{opcode:04x} - Placer l'adresse du sprite de V{x:01x} dans I"
            elif opcode & 0x00FF == 0x0033:
                return f"{opcode:04x} - Stocker la représentation décimale de V{x:01x} dans la mémoire"
            elif opcode & 0x00FF == 0x0055:
                return f"{opcode:04x} - Stocker les valeurs de V0 à V{x:01x} dans la mémoire, à partir de l'adresse I"
            elif opcode & 0x00FF == 0x0065:
                return f"{opcode:04x} - Remplir V0 à V{x:01x} avec les valeurs stockées dans la mémoire, à partir de l'adresse I"
        else:return f'?????????'

     except Exception as e : 
         print(f'>Error with OPCODE {hex(opcode).upper()} : {e}')
         return"Erreur COM"


    def load_fonts(self):

        '''
        Charge les fonts dans la mémoire à l'adresse 0x000.
        '''
        fonts = [
        0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
        0x20, 0x60, 0x20, 0x20, 0x70,  # 1
        0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
        0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
        0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
        0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
        0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
        0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
        0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
        0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
        0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
        0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
        0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
        0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
        0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
        0xF0, 0x80, 0xF0, 0x80, 0x80,  # F
                                            ]
        for i in range(len(fonts)):
            self.memory[i] = fonts[i]

    def load_rom(self, rom_path=None,save=False):
        """
        Charge le fichier ROM à partir du chemin d'accès spécifié dans la mémoire.
        """
        if rom_path: self.rom_path=rom_path 
        rom_file = open(self.rom_path, 'rb')
        #rom_file = open('mon_programme.ch8', 'rb')
        rom_data = rom_file.read()
        rom_file.close()
        if save : 
            f=open(self.rom_path.replace('ch8','txt'),'w')
        for i in range(len(rom_data)):
            if save:
                f.write(str(hex(rom_data[i])).upper()+'\n')
            self.memory[self.pc + i] = rom_data[i]
        if save :
            f.close()
    def incPc(self,):
        self.pc+=self.toInc
        self.toInc=2 # cas de subrtoutine

    def load_random_rom(self):
        """
        Charge une ROM aléatoire pour le débogage.
        """
        roms = getRomFiles() # Liste de ROMs disponibles pour le débogage
        rom_path = random.choice(roms) # Choix aléatoire d'une ROM
        self.rom_path='roms/'+rom_path

        #self.rom_path=rom_path
        self.reset(run=True)
        self.load_rom(self.rom_path)



    def cycle(self):
        """
        Exécute un cycle d'instruction sur le CPU.
        """
        try:
            self.opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]
        except:
            input()
        self.execute_opcode()
        self.keypad.randomKey()
        if self.delay_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer > 0:
            self.display.play_sound()
            self.sound_timer -= 1

        self.display.refresh()
        if self.keypad:
            self.keypad.listenKey()
        
        # Sauvegarde des informations dans un fichier CSV
        state = self.get_state()
        '''
        with open('dataset.csv', mode='a', newline='') as csv_file:
            fieldnames = ['opcode', 'previous_opcode', 'next_opcode', 'pc', 'V', 'I', 'screen_pixels', 'stack', 'delay_timer', 'sound_timer','pressed_keys']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # Écrit l'en-tête du fichier CSV s'il est vide
            if csv_file.tell() == 0:
                writer.writeheader()

            writer.writerow(state)
        '''

        self.cycle_count += 1
        self.incPc()

    def get_state(self):
        state = {
            'opcode': self.opcode,
            'previous_opcode': self.memory[self.pc - 2] << 8 | self.memory[self.pc - 1],
            'next_opcode': self.memory[self.pc + 2] << 8 | self.memory[self.pc + 3],
            'pc': self.pc,
            'V': self.V,
            'I': self.I,
            'screen_pixels': self.display.pixels ,
            'stack': self.stack,
            'delay_timer': self.delay_timer,
            'sound_timer': self.sound_timer,
            'pressed_keys':self.keypad.pressedKeys,
        }
        return state

    def decode_input(self, opcode=None):
        if opcode is None:
            opcode = self.opcode
            
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4
        code = opcode & 0x00FF

        if opcode == 0x00E0:
            return f"CLS"
        elif opcode == 0x00EE:
            return f"RET"
        elif opcode & 0xF000 == 0x0000:
            return f"SYS {code:X}"
        elif opcode & 0xF000 == 0x1000:
            return f"JP {code:X}"
        elif opcode & 0xF000 == 0x2000:
            return f"CALL {code:X}"
        elif opcode & 0xF000 == 0x3000:
            return f"SE V{x:X}, {code:X}"
        elif opcode & 0xF000 == 0x4000:
            return f"SNE V{x:X}, {code:X}"
        elif opcode & 0xF00F == 0x5000:
            return f"SE V{x:X}, V{y:X}"
        elif opcode & 0xF000 == 0x6000:
            return f"LD V{x:X}, {code:X}"
        elif opcode & 0xF000 == 0x7000:
            return f"ADD V{x:X}, {code:X}"
        elif opcode & 0xF00F == 0x8000:
            return f"LD V{x:X}, V{y:X}"
        elif opcode & 0xF00F == 0x8001:
            return f"OR V{x:X}, V{y:X}"
        elif opcode & 0xF00F == 0x8002:
            return f"AND V{x:X}, V{y:X}"
        elif opcode & 0xF00F == 0x8003:
            return f"XOR V{x:X}, V{y:X}"
        elif opcode & 0xF00F == 0x8004:
            return f"ADD V{x:X}, V{y:X}"
        elif opcode & 0xF00F == 0x8005:
            return f"SUB V{x:X}, V{y:X}"
        elif opcode & 0xF00F == 0x8006:
            return f"SHR V{x:X} {{, V{y:X}}}"
        elif opcode & 0xF00F == 0x8007:
            return f"SUBN V{x:X}, V{y:X}"
        elif opcode & 0xF00F == 0x800E:
            return f"SHL V{x:X} {{, V{y:X}}}"
        elif opcode & 0xF00F == 0x9000:
            return f"SNE V{x:X}, V{y:X}"
        elif opcode & 0xF000 == 0xA000:
            return f"LD I, {code:X}"
        elif opcode & 0xF000 == 0xB000:
            return f"JP V0, {code:X}"
        elif opcode & 0xF000 == 0xC000:
            return f"RND V{x:X}, {code:X}"
        elif opcode & 0xF000 == 0xD000:
            y = (opcode & 0x00F0) >> 4
            return f"DRW V{x:X}, V{y:X}, {code & 0x000F}"
        elif opcode & 0xF0FF == 0xE09E:
            return f"SKP V{x:X}"
        elif opcode & 0xF0FF == 0xE0A1:
            return f"SKNP V{x:X}"
        elif opcode & 0xF000 == 0xF000:
            if opcode & 0x00FF == 0x0007:
                return f"LD V{x:X}, DT"
            elif opcode & 0x00FF == 0x000A:
                return f"LD V{x:X}, K"
            elif opcode & 0x00FF == 0x0015:
                return f"LD DT, V{x:X}"
            elif opcode & 0x00FF == 0x0018:
                return f"LD ST, V{x:X}"
            elif opcode & 0x00FF == 0x001E:
                return f"ADD I, V{x:X}"
            elif opcode & 0x00FF == 0x0029:
                return f"LD F, V{x:X}"
            elif opcode & 0x00FF == 0x0033:
                return f"LD B, V{x:X}"
            elif opcode & 0x00FF == 0x0055:
                return f"LD [I], V0-V{x:X}"
            elif opcode & 0x00FF == 0x0065:
                return f"LD V0-V{x:X}, [I]"
            else:
                return f"Unknown opcode {opcode:04X}"
        else:
            return f"Unknown opcode {opcode:04X}"


    
    def decode_instruction(self,instruction=None):
        VX=[0,1,2,3,4,5,6,7,8,9,'A','B','C','D','E','F',]
        if  instruction==None:
            instruction = self.opcode
        opcode = instruction & 0xF000
        x = (instruction & 0x0F00) >> 8
        x=VX[x]
        y = (instruction & 0x00F0) >> 4
        nnn = instruction & 0x0FFF
        kk = instruction & 0x00FF
        if opcode == 0x0000:
            return "CLS"
        elif opcode == 0x00E0:
            return "RET"
        elif opcode == 0x1000:
            return f"JP {nnn:X}"
        elif opcode == 0x2000:
            return f"CALL {nnn:X}"
        # Ajouter des entrées pour chaque code d'opération
        # en utilisant des fonctions lambda pour retourner
        # la chaîne de caractères appropriée.
        instructions = {
            0x3000: lambda: f"SE V{x}, {kk:X}",
            0x4000: lambda: f"SNE V{x}, {kk:X}",
            0x5000: lambda: f"SE V{x}, V{y}",
            0x6000: lambda: f"LD V{x}, {kk:X}",
            0x7000: lambda: f"ADD V{x}, {kk:X}",
            0x8000: lambda: self.decode_arithmetic(instruction),
            0x9000: lambda: f"SNE V{x}, V{y}",
            0xA000: lambda: f"LD I, {nnn:X}",
            0xB000: lambda: f"JP V0, {nnn:X}",
            0xC000: lambda: f"RND V{x}, {kk:X}",
            0xD000: lambda: f"DRW V{x}, V{y}, {instruction & 0x000F}",
            0xE000: lambda: self.decode_input(instruction),
            0xF000: lambda: self.decode_misc(instruction)
        }
        if opcode in instructions:
            return instructions[opcode]()
        else:
            return "UNKNOWN"

    def decode_misc(self,instruction=None):
        if  instruction==None:
            instruction = self.opcode
        x = (instruction & 0x0F00) >> 8
        
        if instruction == 0x00E0:
            return "CLS"
        elif instruction == 0x00EE:
            return "RET"
        elif instruction & 0x00FF == 0x001E:
            return f"ADD I, V{x}"
        elif instruction & 0x00FF == 0x0007:
            return f"LD V{x}, DT"
        elif instruction & 0x00FF == 0x000A:
            return f"LD V{x}, K"
        elif instruction & 0x00FF == 0x0015:
            return f"LD DT, V{x}"
        elif instruction & 0x00FF == 0x0018:
            return f"LD ST, V{x}"
        elif instruction & 0x00FF == 0x001E:
            return f"ADD I, V{x}"
        elif instruction & 0x00FF == 0x0029:
            return f"LD F, V{x}"
        elif instruction & 0x00FF == 0x0033:
            return f"LD B, V{x}"
        elif instruction & 0x00FF == 0x0055:
            return f"LD [I], V{x}"
        elif instruction & 0x00FF == 0x0065:
            return f"LD V{x}, [I]"
        else:
            return "Unknown instruction"
  

    def decode_arithmetic(self,opcode=None):
        if  opcode==None:opcode = self.opcode
        #opcode = self.opcode
        #print(hex(opcode).upper())
        #print(hex(opcode & 0xF000))
        if opcode & 0xF000 == 0x8000:
            if opcode & 0xF == 0x0:
                return f"LD V{opcode >> 8 & 0xF}, V{opcode >> 4 & 0xF}"
            elif opcode & 0xF == 0x1:
                return f"OR V{opcode >> 8 & 0xF}, V{opcode >> 4 & 0xF}"
            elif opcode & 0xF == 0x2:
                return f"AND V{opcode >> 8 & 0xF}, V{opcode >> 4 & 0xF}"
            elif opcode & 0xF == 0x3:
                return f"XOR V{opcode >> 8 & 0xF}, V{opcode >> 4 & 0xF}"
            elif opcode & 0xF == 0x4:
                return f"ADD V{opcode >> 8 & 0xF}, V{opcode >> 4 & 0xF}"
            elif opcode & 0xF == 0x5:
                return f"SUB V{opcode >> 8 & 0xF}, V{opcode >> 4 & 0xF}"
            elif opcode & 0xF == 0x6:
                return f"SHR V{opcode >> 8 & 0xF}"
            elif opcode & 0xF == 0x7:
                return f"SUBN V{opcode >> 8 & 0xF}, V{opcode >> 4 & 0xF}"
            elif opcode & 0xF == 0xE:
                return f"SHL V{opcode >> 8 & 0xF}"
        
        return  "UNKNOWN"


    def execute_opcode(self, ):
        try:
            #if self.opcode in [0xEE,0xE0]:
                #print(self.instructions[self.opcode])
            if self.opcode in self.instructions:
                #print('yaaay ',hex(self.opcode),f' {self.instructionsHelp[self.opcode]}')
                #self.running=False
                #if self.opcode&0XF000==0XF000:print(f'>{hex(self.opcode).upper()} : noooo wrong IF')
                self.instructions[self.opcode]()
            else:
                opcodeMsb=self.opcode&0xF000
                #if self.opcode&0XF000==0XF000:print(f'>{hex(self.opcode).upper()} : {self.instructions[opcodeMsb]}')

                self.instructions[opcodeMsb]()
        except:
            pass
            #print(f'>OPCODE error : {hex(self.opcode).upper()}')
        """
        Exécute l'instruction correspondant à l'opcode spécifié.
        """
        # TODO: Implémentez la logique de décodage des opcodes et d'exécution des instructions.
        #A faire plustard

    def run(self):
        """
        Démarre l'exécution de la ROM chargée dans la mémoire.
        """
        while True:
            if self.running:
                self.cycle()
    def save_state(self):
        state = {
            'pc': self.pc,
            'registers': self.V.copy(),
            'i': self.I,
            'stack': self.stack.copy(),
            'delay_timer': self.delay_timer,
            'sound_timer': self.sound_timer,
            'memory': self.memory.copy(),  # copie la mémoire actuelle
            'opcode':self.opcode,
            'prev_opcode':self.memory[self.pc-1],
            'next_opcode':self.memory[self.pc+1],
            'screen'    :self.display.pixels.copy()
        }
        self.cpustates.append(state)

    def step_back(self):
        if len(self.cpustates) > 1:
            # Récupère le dernier état de la CPU et de la mémoire sauvegardé
            state = self.cpustates[-1]
            self.cpustates.pop()  # Enlève l'état actuel de la liste
            
            # Charge l'état de la CPU et de la mémoire
            self.pc = state['pc']
            self.V = state['registers']
            self.I = state['i']
            self.stack = state['stack']
            self.delay_timer = state['delay_timer']
            self.sound_timer = state['sound_timer']
            self.memory = state['memory']
            self.cycle_count-=1
            #self.display.refreshBack()

    '''
    Instructions : 
    '''
    def noOp(self):
        pass

    def clearDisplay(self):

        if self.display:
            self.display.clear()
    
    def jump(self):
        self.pc=self.opcode&0x0FFF
        self.toInc=0
    
    def setVx(self,):
        """
        Affecte la valeur `value` au registre Vx du CPU.
        """
        x = (self.opcode & 0x0F00) >> 8 #Index du registre Vx à modifier (entre 0 et 15).
        nn = self.opcode & 0x00FF   #Valeur à affecter au registre (entre 0 et 255).
        self.V[x] = nn
 
    def addToVx(self):
        # Récupère le numéro de registre Vx en masquant l'opcode avec 0x0F00 et en le décalant de 8 bits vers la droite
        Vx = (self.opcode & 0x0F00) >> 8
        # Récupère la valeur NN en masquant l'opcode avec 0x00FF
        NN = self.opcode & 0x00FF
        # Ajoute NN à la valeur de Vx
        self.V[Vx] += NN

    def setIndex(self):
        '''
        Instruction ANNN : Set Index Register I
        '''
        # Extraire la valeur NNN de l'opcode actuel
        address = self.opcode & 0x0FFF
        # Assigner la valeur NNN à l'index register I
        self.I = address
        # Passer à l'instruction suivante

    def displayDraw(self):
        x = self.V[(self.opcode & 0x0F00) >> 8]
        y = self.V[(self.opcode & 0x00F0) >> 4]
        height = self.opcode & 0x000F
        self.V[0xF] = 0  # Réinitialise le registre VF

        for row in range(height):
            sprite_byte = self.memory[self.I + row]
            for col in range(8):
                sprite_pixel = (sprite_byte >> (7 - col)) & 0x01
                screen_x = (x + col) % 64
                screen_y = (y + row) % 32
                screen_pixel = self.display.get_pixel(screen_x, screen_y)
                if sprite_pixel == 1 and screen_pixel == 1:
                    self.V[0xF] = 1
                self.display.set_pixel(screen_x, screen_y,sprite_pixel ^ screen_pixel) 

    def backFromSub(self):
        # Retour de sous-routine
        self.pc = self.stack.pop()
    
    def branchToSub(self):
        # Appel de sous-routine
        self.stack.append(self.pc)
        self.toInc=0
        self.pc = self.opcode & 0x0FFF

    def skipIfVXEqNN(self):
        """
        3XNN - Skip next instruction if VX equals NN.
        Compare the value in register VX to NN, and if they are equal, skip the next instruction (increment PC by 4).
        If they are not equal, simply move on to the next instruction (increment PC by 2).
        """
        x = (self.opcode & 0x0F00) >> 8  # Récupère le numéro de registre X.
        nn = self.opcode & 0x00FF  # Récupère la valeur NN.
        #print(hex(self.opcode).upper())
        if self.V[x] == nn:
            self.toInc= 4  # Incrémente PC de 4 si VX == NN.
        else:
            self.toInc=  2  # Sinon incrémente PC de 2.

    def skipIfVXNotEqNN(self):
        """
        4XNN - Skip next instruction if VX doesn't equal NN.
        Compare the value in register VX to NN, and if they are not equal, skip the next instruction (increment PC by 4).
        If they are equal, simply move on to the next instruction (increment PC by 2).
        """
        x = (self.opcode & 0x0F00) >> 8  # Récupère le numéro de registre X.
        nn = self.opcode & 0x00FF  # Récupère la valeur NN.
        if self.V[x] != nn:
            self.toInc= 4   # Incrémente PC de 4 si VX != NN.
        else:
            self.toInc=  2 # Sinon incrémente PC de 2.

    def skipIfVxEqVy(self):
        """
        5XY0 - Skip next instruction if VX equals VY.
        Compare the value in register VX to the value in register VY, and if they are equal, skip the next instruction (increment PC by 4).
        If they are not equal, simply move on to the next instruction (increment PC by 2).
        """
        x = (self.opcode & 0x0F00) >> 8  # Récupère le numéro de registre X.
        y = (self.opcode & 0x00F0) >> 4  # Récupère le numéro de registre Y.
        if self.V[x] == self.V[y]:
            self.toInc= 4  # Incrémente PC de 4 si VX == VY.
        else:
            self.toInc=  2  # Sinon incrémente PC de 2.

    def skipIfVxNotEqVy(self):
        """
        9XY0 - Skip next instruction if VX doesn't equal VY.
        Compare the value in register VX to the value in register VY, and if they are not equal, skip the next instruction (increment PC by 4).
        If they are equal, simply move on to the next instruction (increment PC by 2).
        """
        x = (self.opcode & 0x0F00) >> 8  # Récupère le numéro de registre X.
        y = (self.opcode & 0x00F0) >> 4  # Récupère le numéro de registre Y.
        if self.V[x] != self.V[y]:
            self.toInc= 4  # Incrémente PC de 4 si VX != VY.
        else:
            self.toInc=  2 # Sinon incrémente PC de 2.
    
    def ArithmeticInstruction(self):
        # Récupère l'opcode et l'instruction
        opcode = self.opcode
        instruction = opcode & 0xF000

        # Exécute l'instruction en fonction de son type
        if instruction == 0x8000: # Instructions 8XY_
            sub_instruction = opcode & 0x000F
            
            if sub_instruction == 0x0:
                # 8XY0: Set VX = VY
                #print("8XY0: Set VX = VY")
                self.V[(opcode & 0x0F00) >> 8] = self.V[(opcode & 0x00F0) >> 4]
            
            elif sub_instruction == 0x1:
                # 8XY1: Set VX = VX OR VY
                #print("8XY1: Set VX = VX OR VY")
                self.V[(opcode & 0x0F00) >> 8] |= self.V[(opcode & 0x00F0) >> 4]
            
            elif sub_instruction == 0x2:
                # 8XY2: Set VX = VX AND VY
                #print("8XY2: Set VX = VX AND VY")
                self.V[(opcode & 0x0F00) >> 8] &= self.V[(opcode & 0x00F0) >> 4]
            
            elif sub_instruction == 0x3:
                # 8XY3: Set VX = VX XOR VY
                #print("8XY3: Set VX = VX XOR VY")
                self.V[(opcode & 0x0F00) >> 8] ^= self.V[(opcode & 0x00F0) >> 4]
            
            elif sub_instruction == 0x4:
                # 8XY4: Set VX = VX + VY, VF = carry
                #print("8XY4: Set VX = VX + VY, VF = carry")
                result = self.V[(opcode & 0x0F00) >> 8] + self.V[(opcode & 0x00F0) >> 4]
                
                if result > 255:
                    # La valeur ne peut être stockée sur 8 bits, il y a donc une retenue
                    self.V[0xF] = 1
                else:
                    self.V[0xF] = 0
                        
                self.V[(opcode & 0x0F00) >> 8] = result & 0xFF # Garde uniquement les 8 bits de poids faible
                
            elif sub_instruction == 0x5:
                # 8XY5: Set VX = VX - VY, VF = NOT borrow
                #print("8XY5: Set VX = VX - VY, VF = NOT borrow")
                if self.V[(opcode & 0x0F00) >> 8] > self.V[(opcode & 0x00F0) >> 4]:
                    # Il n'y a pas de retenue
                    self.V[0xF] = 1
                else:
                    self.V[0xF] = 0
                        
                self.V[(opcode & 0x0F00) >> 8] -= self.V[(opcode & 0x00F0) >> 4]
            
            elif sub_instruction == 0x6:
                # 8XY6: Set VX = VX SHR 1, VF = LSB of VX before shift
                x = (opcode & 0x0F00) >> 8
                #print(f"8XY6 - Set V{x:01X} = V{x:01X} SHR 1, VF = {self.V[0xF]:01X}")
                self.V[0xF] = self.V[x] & 0x1
                self.V[x] >>= 1

            elif sub_instruction == 0x7:
                # 8XY7: Set VX = VY - VX, VF = NOT borrow
                if self.V[(opcode & 0x00F0) >> 4] > self.V[(opcode & 0x0F00) >> 8]:
                    self.V[0xF] = 0
                else:
                    self.V[0xF] = 1
                        
                self.V[(opcode & 0x0F00) >> 8] = (self.V[(opcode & 0x00F0) >> 4] - self.V[(opcode & 0x0F00) >> 8]) & 0xFF
                
                # Vérification
                #print(f"8XY7 - Set VX = VY - VX, VF = NOT borrow: VX({(opcode & 0x0F00) >> 8}) = {self.V[(opcode & 0x0F00) >> 8]}, VF = {self.V[0xF]}")

            elif sub_instruction == 0xE:
                # 8XYE: Set VX = VX SHL 1, VF = MSB of VX before shift
                self.V[0xF] = (self.V[(opcode & 0x0F00) >> 8] & 0x80) >> 7
                self.V[(opcode & 0x0F00) >> 8] = (self.V[(opcode & 0x0F00) >> 8] << 1) & 0xFF
                
                # Vérification
                #print(f"8XYE - Set VX = VX SHL 1, VF = MSB of VX before shift: VX({(opcode & 0x0F00) >> 8}) = {self.V[(opcode & 0x0F00) >> 8]}, VF = {self.V[0xF]}")

            
    def JumpOffset(self):
        # BNNN Jump to address NNN plus the value of register V0
        address = self.opcode & 0x0FFF
        self.pc = address + self.V[0]

    def Random(self):
        # CXNN Generate a random number, AND it with NN, and store the result in VX
        x = (self.opcode & 0x0F00) >> 8
        nn = self.opcode & 0x00FF
        self.V[x] = random.randint(0, 255) & nn
    
    def SkipIfKeyPressedInstruction(self):
        """Exécute l'instruction EX9E ou EXA1"""

        # Récupérer le numéro de la touche depuis VX
        key_num = self.V[(self.opcode & 0x0F00) >> 8]
        #print(f'{hex(key_num).upper()}  - {self.keypad.keys[key_num]}    ',end='\r')

        # Vérifier si la touche correspondante est appuyée ou non
        if (self.opcode & 0x00FF) == 0x9E:
            if self.keypad.keys[key_num]:
                self.toInc= 4
            else :self.toInc=2
        elif (self.opcode & 0x00FF) == 0xA1:
            if not self.keypad.keys[key_num]:
                self.toInc= 4
            else :self.toInc=2

    def handle_F_instruction(self, ):
        opcode=self.opcode
        #print(hex(opcode).upper())
        
        instruction = opcode & 0x00FF
        x = (opcode >> 8) & 0x000F
        
        if instruction == 0x0007:
            # FX07 sets VX to the current value of the delay timer
            self.V[x] = self.delay_timer
            #print(f"FX07 - Set VX to delay_timer. X:{x}, VX:{self.V[x]}, delay_timer:{self.delay_timer}")
        elif instruction == 0x0015:
            # FX15 sets the delay timer to the value in VX
            self.delay_timer = self.V[x]
            #print(f"FX15 - Set delay_timer to VX. X:{x}, VX:{self.V[x]}, delay_timer:{self.delay_timer}")
        elif instruction == 0x0018:
            # FX18 sets the sound timer to the value in VX
            self.sound_timer = self.V[x]
            #print(f"FX18 - Set sound_timer to VX. X:{x}, VX:{self.V[x]}, sound_timer:{self.sound_timer}")
        elif instruction == 0x001E:
            # FX1E adds VX to the index register I
            self.I += self.V[x]
            #print(f"FX1E - Add VX to I. X:{x}, VX:{self.V[x]}, I:{self.I}")
        elif instruction == 0x000A:
            # FX0A waits for a key press and stores the key value in VX
            #print('hahahahah')
            
            #key_pressed = self.wait_for_key_press()
            if len(self.keypad.pressedKeys)!=0:
                key_pressed = self.keypad.pressedKeys[0]
            else : key_pressed=0x00
            self.V[x] = key_pressed
            #print(f"FX0A - Wait for key press and set VX to the key value. X:{x}, VX:{self.V[x]}")
        elif instruction == 0x0029:
            # FX29 sets I to the address of the font character in VX
            self.I = self.V[x] * 5 # Each character is 5 bytes long
            #print(f"FX29 - Set I to font address in VX. X:{x}, VX:{self.V[x]}, I:{self.I}")
        elif instruction == 0x0033:
            # FX33 stores the binary-coded decimal representation of VX at the addresses I, I+1, and I+2
            self.memory[self.I] = self.V[x] // 100
            self.memory[self.I+1] = (self.V[x] // 10) % 10
            self.memory[self.I+2] = self.V[x] % 10
            #print(f"FX33 - Store binary-coded decimal of VX in memory. X:{x}, VX:{self.V[x]}, I:{self.I}")
        elif instruction == 0x0055:
            # FX55 stores V0 to VX (inclusive) in memory starting at address I
            for i in range(x + 1):
                self.memory[self.I + i] = self.V[i]
            # On the original interpreter, when the operation is done, I = I + X + 1.
            self.I += x + 1
            #print(f"FX55 - Store V0 to VX in memory. X:{x}, VX:{self.V[x]}, I:{self.I}")
        elif instruction == 0x0065:
            # FX65 fills V0 to VX (inclusive) with values from memory starting at address I
            for i in range(x + 1):
                self.V[i] = self.memory[self.I + i]
            # On the original interpreter, when the operation is done, I = I + X + 1.
            self.I += x + 1
            #print(f"FX65 - Load V0 to VX from memory. X:{x}, I:{self.I}")
        else:pass
            #print(f"Unknown Instruction: {hex(opcode).upper()}")

