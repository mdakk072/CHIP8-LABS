import tkinter as tk
from tkinter import filedialog

# Liste des fichiers prédéfinis
fichiers_predefinis = ['fichier1.txt', 'fichier2.txt', 'fichier3.txt']

# Fonction pour charger un fichier à partir de la liste
def charger_fichier_predefini(fichier):
    print("Chargement du fichier :", fichier)

# Fonction pour charger un fichier en utilisant le bouton "Parcourir"
def charger_fichier_personnalise():
    # Ouvrir la boîte de dialogue pour sélectionner un fichier
    fichier = filedialog.askopenfilename()
    print("Chargement du fichier :", fichier)

# Créer la fenêtre
fenetre = tk.Tk()

# Titre de la fenêtre
fenetre.title("Chargement de fichier")

# Label pour la liste de fichiers
label_fichiers_predefinis = tk.Label(fenetre, text="Fichiers prédéfinis :")
label_fichiers_predefinis.pack()

# Boutons pour les fichiers prédéfinis
for fichier in fichiers_predefinis:
    bouton_fichier_predefini = tk.Button(fenetre, text=fichier, command=lambda fichier=fichier: charger_fichier_predefini(fichier))
    bouton_fichier_predefini.pack()

# Bouton "Parcourir"
bouton_parcourir = tk.Button(fenetre, text="Parcourir...", command=charger_fichier_personnalise)
bouton_parcourir.pack()

# Afficher la fenêtre
fenetre.mainloop()
