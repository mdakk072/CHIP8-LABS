
import random
from Keypad import Keypad 
from Display import Display
from CPU import CPU



import os

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

roms=getRomFiles()
random_element = random.choice(roms)






display=Display(menu=True)
#display.getMenuKey()

keypad=Keypad(display)
cpu = CPU(display=display,keypad=keypad)

cpu.bootLogo()
print(random_element)
cpu.load_rom(f'roms//{random_element}',)
#cpu.load_rom(rom_path,save=True)
#cpu.run()

def run():
    while True:
        display.getMenuKey()
        if cpu.running:
            cpu.cycle()
        display.getMenuKey()
        
run()