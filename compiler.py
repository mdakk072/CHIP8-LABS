opcodes = {
    "CLS": "00E0",
    "RET": "00EE",
    "JP": "1NNN",
    "CALL": "2NNN",
    "SE": "3XNN",
    "SNE": "4XNN",
    "SEXY": "5XY0",
    "LD": {
        "VX": "6XNN",
        "DT": "FX07",
        "ST": "FX18",
        "I": "ANNN",
        "F": "FX29",
        "B": "FX33",
        "[I]": "FX55",
        "VX,[I]": "FX65",
        "VX,VY": "8XY0",
        "VX,byte": "7XNN",
        "OR": "8XY1",
        "AND": "8XY2",
        "XOR": "8XY3",
        "ADD": "8XY4",
        "SUB": "8XY5",
        "SHR": "8XY6",
        "SUBN": "8XY7",
        "SHL": "8XYE",
        "RND": "CXNN",
        "DRW": "DXYN",
        "SKP": "EX9E",
        "SKNP": "EXA1",
        "LD": {
            "DT,VX": "FX15",
            "ST,VX": "FX18",
            "I,VX": "FX1E",
        },
    },
}


def assemble(file_asm, file_chip8):
    # Ouvre le fichier d'assembly et le fichier de sortie
    with open(file_asm) as f_asm, open(file_chip8, "w") as f_chip8:
        # Parcourt chaque ligne du fichier d'assembly
        for line in f_asm:
            # Ignore les commentaires
            if ";" in line:
                line = line[:line.index(";")]
            # Enlève les espaces en début et fin de ligne
            line = line.strip()
            # Ignore les lignes vides
            if not line:
                continue
            # Divise la ligne en mots
            words = line.split()
            # Convertit chaque mot en majuscules
            words = [word.upper() for word in words]
            # Obtient l'opcode correspondant
            opcode = opcodes.get(words[0])
            # Vérifie si l'opcode est valide
            if opcode is None:
                raise ValueError(f"Invalid opcode '{words[0]}' in line '{line}'")
            # Vérifie si l'opcode est une instruction LD
            if words[0] == "LD":
                # Obtient le deuxième argument (Vx, DT, ST ou I)
                arg = words[1]
                # Obtient l'opcode correspondant à l'instruction LD avec l'argument spécifié
                opcode = opcodes["LD"].get(arg)
                # Vérifie si l'opcode est valide
                if opcode is None:
                    raise ValueError(f"Invalid LD argument '{arg}' in line '{line}'")
                # Obtient le troisième argument (byte ou Vx)
                arg = words[2]
            else:
                # Obtient le premier argument (Vx ou label ou NNN)
                arg = words[1]
            # Convertit l'argument en hexadécimal
            if arg.startswith("V"):
                arg = int(arg[1:], 16)
            else:
                arg = int(arg, 16)
            # Concatène l'opcode et l'argument en code machine
            if opcode == "ANNN":
                code = format(arg, "04X")
            elif opcode == "2NNN":
                code = format(arg, "04X")
            elif opcode == "1NNN":
                code = format(arg, "04X")
            elif opcode == "JP":
                code = format(arg, "03X")
            elif opcode == "LD":
                if words[2].startswith("V"):
                    code = f"{opcode[0:2]}{arg:X}{opcode[3:]}"
                else:
                    code = f"{opcode[0:2]}{arg:X}"
            else:
                code = opcode
                if opcode[2] == "X":
                    code = f"{opcode[0:2]}{arg:X}{opcode[3:]}"
                elif opcode[3] == "X":
                    code = f"{opcode[0:3]}{arg:X}"
            # Écrit le code machine dans le fichier de sortie
            f_chip8.write(code + "\n")
assemble("mon_programme.asm", "mon_programme.ch8")

