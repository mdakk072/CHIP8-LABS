import math
from sly import Lexer
from graphviz import Digraph
import os
from PIL import Image,ImageOps,ImageDraw,ImageFont

class AnalyseurLexical(Lexer):
    



    # Mots-clés
    VAR = r'var'
    BYTE = r'byte'
    WORD = r'word'
    STRING = r'string'
    WHILE = r'while'
    IF = r'if'
    ELSE = r'else'
    FUNCTION = r'function'
    RETURN = r'return'
    PRINT = r'print'
    STRINGCHAR = r"'[^\n']*'"
    STACKOP = r"stack\.(push|pop)"    
    # Autres symboles
    EQ = r'='
    PLUS = r'\+'
    LT = r'<'
    LBRACE = r'{'
    RBRACE = r'}'
    LPAREN = r'\('
    RPAREN = r'\)'
    SEMI = r';'
    COLON = r':'
    COMMA = r','
    NUMBER = r'\d+'
    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
    IGNORE = r'[\t\n\f\r ]+'
    tokens = {
    'VAR': VAR, 'BYTE': BYTE, 'WORD': WORD, 'STRING': STRING, 'WHILE': WHILE,
    'IF': IF, 'ELSE': ELSE, 'FUNCTION': FUNCTION, 'RETURN': RETURN, 'PRINT': PRINT,
    'NUMBER': NUMBER, 'IDENTIFIER': IDENTIFIER, 'EQ': EQ, 'PLUS': PLUS, 'LT': LT,
    'LBRACE': LBRACE, 'RBRACE': RBRACE, 'LPAREN': LPAREN, 'RPAREN': RPAREN,
    'SEMI': SEMI, 'IGNORE': IGNORE, 'COLON': COLON,'COMMA': COMMA,'STRINGCHAR':STRINGCHAR,'STACKOP':STACKOP,
}

    def error(self, t):
        print(f"Il y a une erreur de syntaxe à la ligne {self.lineno} : caractère '{t.value[0]}' non valide")
        self.index += 1
        #input()

    def IDENTIFIER(self, t):
        keywords = {'var': 'VAR', 'byte': 'BYTE', 'word': 'WORD', 'string': 'STRING',
            'while': 'WHILE', 'if': 'IF', 'else': 'ELSE', 'function': 'FUNCTION',
            'return': 'RETURN', 'print': 'PRINT'}
        t.type = keywords.get(t.value, 'IDENTIFIER')
        return t

    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    def STRING(self, t):
        t.value = t.value.strip("'")
        return t
   



def test(code=None):
    if not code : code = [
        "var x: byte = 10",
        "var y: word = 100",
        "var z: string = 'hello'",
        "while (x < y) {",
        "  if (x == 5) {",
        "    print('x est gal à 5')",
        "  } else {",
        "    print('x n est pas gal à 5')",
        "  }",
        "  x = x + 1",
        "}",
        "function my_function(arg1: byte, arg2: word) {",
        "  var local_var: string = 'local variable'",
        "  print(local_var)",
        "  return arg1 + arg2",
        "}",
        "my_function(1, 2)"
    ]

    lexer = AnalyseurLexical()
    for line in code:
        tokens = lexer.tokenize(line)
        print(f"Line: {line}")
        for token in tokens:
            print(f"  {token.type}: {token.value}")
        print('==========')





def testGraph(code=None):
    if not code:
        code = [
            "var x: byte = 10",
            "var y: word = 100",
            "var z: string = 'hello'",
            "while (x < y) {",
            "  if (x == 5) {",
            "    print('x est gal à 5')",
            "  } else {",
            "    print('x n est pas égal à 5')",
            "  }",
            "  x = x + 1",
            "}",
            "function my_function(arg1: byte, arg2: word) {",
            "  var local_var: string = 'local variable'",
            "  print(local_var)",
            "  return arg1 + arg2",
            "}",
            "my_function(1, 2)"
        ]

    lexer = AnalyseurLexical()

    # créer un graphe global pour tous les clusters
    dot = Digraph(comment='Analyseur lexical', format='png', graph_attr={'rankdir': 'LR', 'splines': 'ortho'})
    dot.attr('node', shape='plaintext', fontname='arial')

    # diviser le graphe en clusters
    cluster_idx = 0
    max_nodes_per_cluster = 4
    dot_cluster = None
    imagesPath=[]

    for i, line in enumerate(code):
        
        # créer un nouveau cluster pour chaque groupe de n noeuds
        cluster_idx += 1
        dot_cluster = Digraph(comment=f'Cluster {cluster_idx}', format='png', graph_attr={'rankdir': 'LR', })
        dot_cluster.attr('node', shape='plaintext', fontname='arial')
        # ajouter un noeud pour chaque ligne
        dot_cluster.node(str(i), line)
        tokens = lexer.tokenize(line)
        for ii ,token in enumerate(tokens):
            # ajouter un noeud pour chaque token
            dot_cluster.node(str(i) + "_" + str(token.type), str(token.value), fontname='arial',
                         color=get_token_color(token.type), style='filled', fillcolor='lightgray')
            # ajouter une arête entre le noeud de la ligne et le noeud du token
            dot_cluster.edge(str(i), str(i) + "_" + str(token.type), label=str(token.type))

        #if i % max_nodes_per_cluster == max_nodes_per_cluster - 1 or i == len(code) - 1:
            # ajouter le cluster au graphe global
            
            # enregistrer l'image du cluster dans un dossier "Test Results"
        dot.subgraph(dot_cluster)
        
        if not os.path.exists("Test Results"):
            os.makedirs("Test Results")
        dot_cluster.render(f"Test Results/Line {cluster_idx}", format="png")
        imagesPath.append(f"Test Results/Line {i+1}.png")
        # Récupérer la taille de chaque image et stocker dans une liste
    sizes = []
    for path in imagesPath:
        with Image.open(path) as img:
            sizes.append(img.size)

    # calculer la taille totale de la grille
    max_width = max(size[0] for size in sizes)
    max_height = max(size[1] for size in sizes)
    grid_width = int(math.sqrt(len(imagesPath))) + 1
    grid_height = (len(imagesPath) // grid_width) + 1
    grid_size = (grid_width * max_width, grid_height * max_height)
    # créer une image vierge pour stocker toutes les images
    all_images = Image.new('RGB', grid_size, color='white')
    # ajouter chaque image à l'image vierge
    for i, path in enumerate(imagesPath):
        with Image.open(path) as img:
            img = img.resize((max_width, max_height), resample=Image.BICUBIC)
            x = (i % grid_width) * max_width
            y = (i // grid_width) * max_height
            img_with_border = ImageOps.expand(img, border=5, fill='black')
            all_images.paste(img_with_border, (x, y))
    # enregistrer l'image combinée
    all_images.save(os.path.join("Test Results", 'All.png'))
    # ouvrir l'image combinée
    all_images.show()

def get_token_color(token_type):
    if token_type in ['KEYWORD', 'PUNCTUATION']:
        return 'gray'
    elif token_type == 'IDENTIFIER':
        return 'lightblue'
    elif token_type == 'NUMBER':
        return 'lightgreen'
    elif token_type == 'STRING':
        return 'pink'
    else:
        return 'white'



def read_chip8_code(filename):
    instructions = []
    with open(filename, 'r') as f:
        for line in f:
            # Ignore comments and whitespace
            line = line.split(';')[0].strip()
            if not line:
                continue
            instructions.append(line)
    return instructions


code=read_chip8_code('testcode.mv8')
#test(code)
testGraph(code)
