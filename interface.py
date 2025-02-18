import tkinter as tk
from tkinter import ttk
import pygame
import time



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



def demarrage():
    global animStart
    animStart=True # statut de l'animation du bouton start
    longueur=height #cette manip est inutile mais, si supprimées pense à modifier les appels aux variables respectives
    largeur=width
    pygame.mixer.music.load("loop-menu.mp3")
    pygame.mixer.music.play(loops=-1)
    dem = tk.Canvas(fen, height=500, width=500, background="#2C3E50")  # Couleur élégante (bleu-gris foncé)
    dem.create_text(longueur * 0.5, largeur * 0.45, fill="black", text="Abalone", font=("Comic Sans MS", 50, "bold"),tag=['txt'])
    def apparitionCredit(longueur,largeur,dem,t):#on fait appraitre les crédits au bout d'un certain temps, temps pdt lequel le bouton start est désactivé
        if t>0:
            dem.after(1000,apparitionCredit,longueur,largeur,dem,t-1)
        else:
            dem.create_text(longueur * 0.5, largeur * 0.55, fill="black", text="Created by Nassim & Gabriel",font=("Comic Sans MS", 10), tag=['auteurs'])

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
    apparitionCredit(longueur,largeur,dem,1)
    logo(dem)

    dem.focus_set()
    start.bind("<Enter>",startBigger)
    start.bind("<Leave>",startSmaller)
    animeButton()
    dem.pack()


def resolution_window(): #fenêtre de demande de résolution

    def changeRes(): #met à jour la résolution de la fenêtre en fonction de la résolution sélectionnée
        res.destroy()
        fen.geometry(f"{choixVal.get()}")

    choix = ["1920x1080", "1280x720", "800x600", "640x480", "480x360", "320x240"]

    res = tk.Toplevel() # on crée une fenêtre "fille"
    res.geometry("300x150")
    res.resizable(False,False)
    choixVal = tk.StringVar()
    choixVal.set(choix[0])


    valide = tk.Button(res,text="valider",command=changeRes)
    label =tk.Label(res,text="Choisissez une résolution :")
    labtest = tk.Label(res,textvariable=choixVal)

    liste = ttk.Combobox(res,textvariable=choixVal, values=choix,state="readonly") # barre de séléction pour les résolutions

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

demarrage()




fen.mainloop()