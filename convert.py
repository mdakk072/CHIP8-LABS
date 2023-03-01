import pandas as pd

# Ouvrir le fichier CSV
df = pd.read_csv("dataset2.csv")

# Utiliser eval() pour convertir les chaînes de caractères en listes
print('ok1')
df["V"] = df["V"].apply(eval)
print('ok2')


df = df.drop("screen_pixels", axis=1)


#df["screen_pixels"] = df["screen_pixels"].apply(eval)

print('ok3')

df["stack"] = df["stack"].apply(eval)
print('ok4')

df["pressed_keys"] = df["pressed_keys"].apply(eval)
print('ok5')

# Enregistrer les modifications dans un nouveau fichier CSV
df.to_csv("dataset2_modifie.csv", index=False)
