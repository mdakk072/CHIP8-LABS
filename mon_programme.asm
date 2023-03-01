LD I, FONT5  ; Charge l'adresse du sprite du chiffre 5 dans le registre I
LD V0, 20    ; Charge la position horizontale du sprite dans le registre V0
LD V1, 20    ; Charge la position verticale du sprite dans le registre V1
LD V2, 5     ; Charge la largeur du sprite dans le registre V2
LD V3, 10    ; Charge la hauteur du sprite dans le registre V3
DRW V0, V1, V2, V3  ; Dessine le sprite à la position (20, 20) à l'écran
