import tkinter as tk
from tkinter import ttk
import pygame
import time
import math
import données
import random




global selectedOnClick



selectedOnClick=False
M=        [[-1, -1, -1, -1, -1],
          [0, -1, -1, -1, -1, 0],
         [0, 0, -1, -1, -1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 1, 1, 1, 0, 0],
           [0, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1]]
height=500
width=500
main_bg="#2C3E50"

pygame.mixer.init()

def defilementGauche(x,x_end,y,canvas,distance=8,speed=2,color=None,txt=None,_font=None,_tag=None): #défilement de text vers la gauche
    if x>x_end:
        canvas.delete(_tag)
        x -= 8
        canvas.create_text(x, y, fill=color, text=txt,font=_font, tag=_tag)

        canvas.after(int(2),defilementGauche,x,x_end,y,canvas,distance,speed,color,txt,_font,_tag)


def defilementDroite(x,x_end,y,canvas,distance=8,speed=2,color=None,txt=None,_font=None,_tag=None): #défilement de text vers la droite
    if x<x_end:
        canvas.delete(_tag)
        x += 8
        canvas.create_text(x, y, fill=color, text=txt,font=_font, tag=_tag)
        canvas.after(int(2),defilementDroite,x,x_end,y,canvas,distance,speed,color,txt,_font,_tag)

def defilCredit(canvas): #permet de gérer l'animation des crédits au moment du start
    defilementGauche(height * 0.5, -height, width * 0.55, canvas, 8, 4, "black", "Created by Nassim & Gabriel",("Comic sans MS", 10), ['auteurs'])
    defilementDroite(height*0.5,2*height, width*0.45,canvas,8,4, "black", "Abalone", ("Comic Sans MS", 50,"bold"), ['txt'])





def logo(canvas): # affiche le logo
    canvas.create_polygon(250, 25, 325, 62, 325, 137, 250, 175, 175, 137, 175, 62, fill="#582900", outline="black",width=2, tag=['logo'])
    canvas.create_oval(225, 35, 275, 85, fill="white", tag=['logo'])
    canvas.create_oval(225, 115, 275, 165, fill="black", tag=['logo'])



def demarrage(): #lance le menu de démarrage
    global animStart
    animStart=True # statut de l'animation du bouton start #cette manip est inutile mais, si supprimée penser à modifier les appels aux variables respectives
    pygame.mixer.music.load("loop-menu.mp3")
    pygame.mixer.music.play(loops=-1)
    dem = tk.Canvas(fen, height=500, width=500, background="#2C3E50")  # Couleur élégante (bleu-gris foncé)
    dem.create_text(height * 0.5, width * 0.45, fill="black", text="Abalone", font=("Comic Sans MS", 50, "bold"),tag=['txt'])
    def apparitionCredit(height,width,dem,t):#on fait appraitre les crédits au bout d'un certain temps, temps pdt lequel le bouton start est désactivé
        if t>0:
            dem.after(1000,apparitionCredit,height,width,dem,t-1)
        else:
            dem.create_text(height * 0.5, width * 0.55, fill="black", text="Created by Nassim & Gabriel",font=("Comic Sans MS", 10), tag=['auteurs'])

            start.config(state="normal")


    def on_start(): #commande du bouton start
        global animStart
        bruitage = pygame.mixer.Sound("interface.mp3")
        bruitage.play()
        defilCredit(dem)
        animStart = False
        start.destroy()
        fen.after(1000,dem.destroy)
        resolution_window()

    def animeButton(x=250,y=350,sens=1): #permet de donner une animation type lévitation au bouton
        if animStart:
            if y==353 or y==347:
                sens = -sens
                y+=sens
                if animStart:
                    dem.delete('start')
                    dem.create_window(x,y,window=start,tag=['start'])
                    dem.after(250,animeButton,x,y,sens)
            else:
                y+=sens
                if animStart:
                    dem.delete('start')
                    dem.create_window(x,y,window=start,tag=['start'])
                    dem.after(100,animeButton,x,y,sens)




    def startBigger(event): #on agrandit le bouton
        bruitage = pygame.mixer.Sound("pop.mp3")
        bruitage.play()
        start.config(font=("Arial", 16, "bold"),pady=20,padx=30)

    def startSmaller(event): #on réduit la taille du bouton
        start.config(font=("Arial", 12, "bold"),pady=10,padx=20)


    start = tk.Button(fen,state="disabled", text="Start", padx=20, pady=10, bg="#3498DB", fg="white", font=("Arial", 12, "bold"), bd=2,relief="raised", activebackground="#16A085", activeforeground="white", command=on_start)
    dem.create_window(250, 350, window=start,tag=['start'])
    apparitionCredit(height,width,dem,1)
    logo(dem)

    dem.focus_set()
    start.bind("<Enter>",startBigger)
    start.bind("<Leave>",startSmaller)
    animeButton()
    dem.pack()



def calculer_points_hexagone(centre_x, centre_y, rayon, rotation=0): #fabrication hexagone
    points = []
    for i in range(6):
        angle_deg = 60 * i - 30 + rotation
        angle_rad = math.radians(angle_deg)
        x = centre_x + rayon * math.cos(angle_rad)
        y = centre_y + rayon * math.sin(angle_rad)
        points.append((x, y))
    return points

def place_hole(canvas,points): # creation des emplacements des boules en fonction de la taille du plateau (maxX,maxY)
    global long,larg,caseXY
    caseXY=[[]for i in range(9)]
    occupationxEspace=0.5 #pourcentage d'espace alloué à l'espacement
    occupationxCarre=0.5
    Lminmax=[(points[3],points[4]),(points[2],points[5]),(points[1],points[0])] # contient le coordonnées min et max de x et y trié dans l'ordre et par couple (x,y)
    cpt=0
    minX=Lminmax[cpt][0][0]
    maxX=Lminmax[cpt][1][0]
    linesize=maxX-minX

    espacementx = occupationxEspace * (linesize / 4)
    taillexcarre = occupationxCarre * (linesize / 5)


    Ymin=Lminmax[0][0][1]
    Ymax=Lminmax[2][1][1]
    linesizey=Ymax-Ymin

    espacementy=linesizey/20.78

    for j in range(5):
        y1 = (larg/5.4)+j*(taillexcarre+espacementy)
        y2 = (larg/5.4)+j*(taillexcarre+espacementy)+taillexcarre
        if j!=0: # décalage
            minX-=(espacementx+taillexcarre)/2

        for i in range(5+j):
            x1=minX+(espacementx+taillexcarre)*i
            x2=minX+(espacementx+taillexcarre)*i+taillexcarre
            canvas.create_rectangle(x1,y1,x2,y2,fill="white",outline="black",tags=("case",f"case_{j}_{i}"))
            caseXY[j].append((x1,y1,x2,y2))
    cpt2 = 0
    for j in range(5,9):
        y1 = (larg/5.4) + j * (taillexcarre + espacementy)
        y2 = (larg/5.4) + j * (taillexcarre + espacementy) + taillexcarre
        if j != 0:  # decalage
            minX += (espacementx + taillexcarre) / 2

        for i in range((8-cpt2)):
            x1 = minX + (espacementx + taillexcarre) * i
            x2 = minX + (espacementx + taillexcarre) * i + taillexcarre
            canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black",tags=("case",f"case_{j}_{i}"))
            caseXY[j].append((x1, y1, x2, y2))
        cpt2+=1


def aff(M,event=None):
    try: #on efface les cases s'ils elles existent
        canvas.delete("case")
    except: #sinon on ne lève pas d'erreur
        pass
    finally: # quoi qu'il arrive on affichera les éléments suivants
        emptygrid()
        for i in range(len(M)):
            for j in range(len(M[i])):
                canvas.delete(f"case_{i}_{j}")
                if M[i][j]==1:
                    canvas.create_oval(caseXY[i][j][0],caseXY[i][j][1],caseXY[i][j][2],caseXY[i][j][3],fill="white",outline="black",tags=("case",f"{i}{j}","black"))
                elif M[i][j]==0:
                    canvas.create_rectangle(caseXY[i][j][0],caseXY[i][j][1],caseXY[i][j][2],caseXY[i][j][3],fill="white",outline="black",tags=("case",f"{i}{j}"))
                else:
                    canvas.create_oval(caseXY[i][j][0],caseXY[i][j][1],caseXY[i][j][2],caseXY[i][j][3],fill="black",outline="black",tags=("case",f"{i}{j}","white"))

def getCoord(i,j): #renvoie les coordonnées de la case (x,y)
    return caseXY[i][j]


def aff_pos(event):
    print(event.x,event.y)

def emptygrid(): #vide la grille du jeu
    points = calculer_points_hexagone(width / 2, width / 2, width / 2.5, 90)
    canvas.create_polygon(points, fill="blue")
    place_hole(canvas, points)

def checkInCase(a,b): # verifie si on est bien dans une case
    for i in range(len(caseXY)):
        for j in range(len(caseXY[i])):
            if caseXY[i][j][0] < a < caseXY[i][j][2] and caseXY[i][j][1] < b < caseXY[i][j][3]:
                return True
    return False

def getCase(event): #donne les indices des cases dans lesquelles on se situe avec une tolérance
    toléranceLower=0.98
    toléranceHigher=1.02
    for i in range(len(caseXY)):
        for j in range(len(caseXY[i])):
            if caseXY[i][j][0]*toléranceLower <= event.x <= caseXY[i][j][2]*toléranceHigher and caseXY[i][j][1]*toléranceLower <= event.y <= caseXY[i][j][3]*toléranceHigher:
                return (i,j)
            else:

                #print(caseXY)
                #print(f"{caseXY[i][j][0]} <= {event.x} <= {caseXY[i][j][2]} and {caseXY[i][j][1]} <= {event.y} <= {caseXY[i][j][3]}")
                #canvas.delete(f"case_{i}_{j}")
                #x1, y1, x2, y2 = getCoord(i, j)
                #canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black", tags=("case", f"{i}{j}"))
                pass


def mainCanvas(fen,longueur,largeur): # creation du plateau de jeu
    global canvas,height,width
    height=longueur
    width=largeur
    canvas = tk.Canvas(fen,height=largeur,width=largeur,background="red")
    points=calculer_points_hexagone(largeur/2,largeur/2,largeur/2.5,90)
    canvas.create_polygon(points,fill="blue")
    place_hole(canvas,points)
    canvas.pack()

def aff_selection(event): #crée un cercle de selection
    global selected
    if not selectedOnClick:
        selected=True
        x=event.x
        y=event.y
        try:
            (i,j)=getCase(event)
            x1,y1,x2,y2=getCoord(i,j)
            canvas.create_oval(x1-1,y1-1,x2+1,y2+1,outline="red",width=2,tags=("selection"))
            canvas.tag_lower("selection", "case") #mise en arrière plan du cercle de selection afin d'éviter les conflits entre leave et enter, et éviter les plantages de tkinter

        except:
            pass


def supprimer_selection(event): # supprime le cercle de sélection s'il existe
    global selected
    if selected:
        selected=False
        canvas.delete("selection")

def onClick(event): # creation du cercle de selection avec clique
    try:
        canvas.delete("selection")
        (i, j) = getCase(event)
        x1, y1, x2, y2 = getCoord(i, j)
        canvas.create_oval(x1 - 1, y1 - 1, x2 + 1, y2 + 1, outline="green", width=2, tags=("selectionClick"))
        canvas.tag_lower("selectionClick","case")
    except:
        pass

def delOnClick(event): #supression du cercle de selection avec clique
    try:
        canvas.delete("selectionClick")
    except:
        pass

def select_active(): #active la selection en survol autour des cases
    canvas.tag_bind("case","<Enter>",aff_selection)
    canvas.tag_bind("case","<Leave>",supprimer_selection)
    canvas.tag_bind("case","<Button-1>",onClick)
    canvas.bind("<Button-3>",delOnClick)


def play():
    global turn
    print("play")
    turn = random.randint(1,2)
    canvas.create_text(larg/2,long*0.1,text=f"joueur {turn} à toi de jouer")
    select_active()
    """while True:

        if turn==1:
            canvas.focus("white")
            canvas.tag_bind()
            pass
"""



def resolution_window(): #fenêtre de demande de résolution

    def changeRes(): #met à jour la résolution de la fenêtre en fonction de la résolution sélectionnée
        global long, larg
        long=int(choixVal.get().split("x")[0])
        larg=int(choixVal.get().split("x")[1])
        res.destroy()
        fen.geometry(f"{choixVal.get()}")
        mainCanvas(fen,int(choixVal.get().split("x")[1]),int(choixVal.get().split("x")[1]))



    choix = ["1920x1080", "1280x720", "800x600", "640x480", "480x360", "320x240"]

    res = tk.Toplevel() # on crée une fenêtre "fille"
    res.geometry("300x150")
    res.resizable(False,False)
    choixVal = tk.StringVar()
    choixVal.set(choix[1])


    valide = tk.Button(res,text="valider",command=changeRes)
    label =tk.Label(res,text="Choisissez une résolution :")
    labtest = tk.Label(res,textvariable=choixVal)

    liste = ttk.Combobox(res,textvariable=choixVal, values=choix,state="readonly") # barre de séléction pour les résolutions
    test = tk.Button(fen, text="test",command=lambda: aff(M))
    test2 = tk.Button(fen, text="play",command=lambda: play())

    test2.pack(side="left")
    test.pack(side="right")
    valide.pack(side="bottom")
    label.pack(side="top")
    liste.pack()
    labtest.pack()
    res.mainloop()

fen=tk.Tk()
fen.configure(background=main_bg)
fen.geometry("500x500")
fen.resizable(False,False)
fen.title("salut")

#demarrage()
resolution_window()



fen.mainloop()