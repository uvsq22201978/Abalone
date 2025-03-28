import random
import tkinter
from tkinter import Radiobutton

from modele import *


global selected,selectedOnClick,height,width,selectedOnClick


nbselected=0 # nombre de boule en séléction
selectedOnClick=False # click gauche définit a false
height=500
width=500

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





def makeLogo(canvas): # affiche le logo
    canvas.create_polygon(250, 25, 325, 62, 325, 137, 250, 175, 175, 137, 175, 62, fill="#582900", outline="black",width=2, tag=['logo'])
    canvas.create_oval(225, 35, 275, 85, fill="white", tag=['logo'])
    canvas.create_oval(225, 115, 275, 165, fill="black", tag=['logo'])


def calculer_points_hexagone(centre_x, centre_y, rayon, rotation=0): #fabrication hexagone
    points = []
    for i in range(6):
        angle_deg = 60 * i - 30 + rotation
        angle_rad = math.radians(angle_deg)
        x = centre_x + rayon * math.cos(angle_rad)
        y = centre_y + rayon * math.sin(angle_rad)
        points.append((x, y))
    return points

def getSizeBoule():
    points = calculer_points_hexagone(width / 2, width / 2, width / 2.5, 90)
    occupationxEspace = 0.5  # pourcentage d'espace alloué à l'espacement
    occupationxCarre = 0.5  # pourcentage d'espace alloué aux formes
    Lminmax = [(points[3], points[4]), (points[2], points[5]), (points[1], points[0])]  # contient le coordonnées min et max de x et y trié dans l'ordre et par couple (x,y)
    minX = Lminmax[0][0][0]
    maxX = Lminmax[0][1][0]
    linesize = maxX - minX

    espacementx = occupationxEspace * (linesize / 4)
    taillexcarre = occupationxCarre * (linesize / 5)

    Ymin = Lminmax[0][0][1]
    Ymax = Lminmax[2][1][1]
    linesizey = Ymax - Ymin
    espacementy = linesizey / 20.78
    return (espacementx, espacementy, taillexcarre,minX)

def placHole(canvas,points): # creation des emplacements des boules en fonction de la taille du plateau (maxX,maxY)
    global long,larg,caseXY
    caseXY=[[]for i in range(9)]
    espacementx,espacementy,taillexcarre,minX=getSizeBoule()

    for j in range(5):
        y1 = (larg/5.4)+j*(taillexcarre+espacementy)
        y2 = (larg/5.4)+j*(taillexcarre+espacementy)+taillexcarre
        if j!=0: # décalage
            minX-=(espacementx+taillexcarre)/2 # on décale de la moitié de la taille d'un cercle

        for i in range(5+j):
            x1=minX+(espacementx+taillexcarre)*i
            x2=minX+(espacementx+taillexcarre)*i+taillexcarre
            canvas.create_oval(x1,y1,x2,y2,fill="brown",outline="black",tags=("case",f"case_{j}_{i}"))
            caseXY[j].append((x1,y1,x2,y2))
    cpt = 0
    for j in range(5,9):
        y1 = (larg/5.4) + j * (taillexcarre + espacementy)
        y2 = (larg/5.4) + j * (taillexcarre + espacementy) + taillexcarre
        if j != 0:  # decalage
            minX += (espacementx + taillexcarre) / 2

        for i in range((8-cpt)):
            x1 = minX + (espacementx + taillexcarre) * i
            x2 = minX + (espacementx + taillexcarre) * i + taillexcarre
            canvas.create_oval(x1, y1, x2, y2, fill="brown", outline="black",tags=("case",f"case_{j}_{i}"))
            caseXY[j].append((x1, y1, x2, y2))
        cpt+=1


def affScore():
    global larg,long,canvas
    score=getOut()

    espacementx, espacementy, taillexcarre, minX = getSizeBoule()
    minX -= (espacementx + taillexcarre) / 2
    y1 = (larg / 5.4) + -1.5 * (taillexcarre + espacementy)
    y2 = (larg / 5.4) + -1.5 * (taillexcarre + espacementy) + taillexcarre
    for i in range(5,5-len(score[1]),-1): #affichage invérsé pour les boules noirs on part de droite vers la gauche
        x1 = minX + (espacementx + taillexcarre) * i
        x2 = minX + (espacementx + taillexcarre) * i + taillexcarre
        canvas.create_oval(x1,y1,x2,y2,fill="white",outline="white",tag=("plateau","score"))
        lableft.config(text="Score Noir : "+str(len(score[1])))
    y1 = (larg / 5.4) + 9.5 * (taillexcarre + espacementy)
    y2 = (larg / 5.4) + 9.5 * (taillexcarre + espacementy) + taillexcarre
    for i in range(len(score[0])):
        x1 = minX + (espacementx + taillexcarre) * i
        x2 = minX + (espacementx + taillexcarre) * i + taillexcarre
        canvas.create_oval(x1, y1, x2, y2, fill="black", outline="white",tag=("plateau","score") )
        labright.config(text="Score Blanc : "+str(len(score[0])))

def aff(M,event=None):
    try: #on efface les cases s'ils elles existent
        canvas.delete("case")
    except: #sinon on ne lève pas d'erreur
        pass
    finally: # quoi qu'il arrive on affichera les éléments suivants
        emptygrid()
        for i in range(len(M)):
            for j in range(len(M[i])):
                if M[i][j]==1:
                    canvas.create_oval(caseXY[i][j][0],caseXY[i][j][1],caseXY[i][j][2],caseXY[i][j][3],fill="white",outline="black",tags=("case","black","plateau"))
                elif M[i][j]==0:
                    canvas.create_oval(caseXY[i][j][0],caseXY[i][j][1],caseXY[i][j][2],caseXY[i][j][3],fill="brown",outline="black",tags=("case","plateau"))
                else:
                    canvas.create_oval(caseXY[i][j][0],caseXY[i][j][1],caseXY[i][j][2],caseXY[i][j][3],fill="black",outline="black",tags=("case","white","plateau"))
    afficheMat(getMatrice())
def getCoord(i,j): #renvoie les coordonnées de la case (x,y)
    return caseXY[i][j]

def resetScore():
    resetOut()
    affScore()
    lableft.config(text="Score Noir : 0")
    labright.config(text="Score Blanc : 0")
    canvas.delete("score")

def aff_pos(event):
    print(event.x,event.y)

def emptygrid(): #vide la grille du jeu
    points = calculer_points_hexagone(width / 2, width / 2, width / 2.5, 90)
    canvas.create_polygon(points, fill="#582900")
    placHole(canvas, points)

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
    return (-1,-1)


def mainCanvas(fen,longueur,largeur): # creation du plateau de jeu
    global canvas,height,width,labright,lableft


    messages=["Vous pouvez suivre l'avancement du projet via ce lien : https://github.com/uvsq22201978/Abalone","Le saviez vous, cette banderole vous fera perdre de précieuses secondes","la raison pour laquelle cette banderole est présente c'est uniquement pour justifier d'une évolution entre deux rendus mais elle est pas cool quand même ?","Si vous trouvez un seul bug Gabriel s'engage à vous payer un repas","Si un joueur tappe sur C puis H puis T, il aura automatiquement gagné                                                                          attendez... vous n'avez quand même pas essayé ?","Nous n'avons pas fait de glisser déposer à cause de l'inexistance de transparence des formes dans tkinter","là j'ai plus d'inspi","je pourrais perdre des heures à écrire tout et n'importe quoi"]
    texte = (random.choice(messages))
    vitesse, delai = int(longueur/320), int(longueur/106) #la vitesse correspond au nombre de pixel de déplacement a chaque tour de boucle, le delai correspond à la vitesse de répétition de la boucle en ms
    height=longueur
    width=largeur


    def deplacer(canvas, text_item, vitesse, largeur, text_width, delai):
        canvas.move(text_item, -vitesse, 0) # déplacement du text
        x1, y1, x2, y2 = canvas.bbox(text_item)
        if x2 < 0: # quand le texte est intégralement arrivé a gauche on recrée un texte à droite de l'écran
            text_item = canvas.create_text(largeur, largeur // 20, text=random.choice(messages), anchor='w',fill="white",
                                           font=("Arial", int(largeur/30), "bold"))
            canvas.move(text_item, largeur + text_width, 0) # on fait en sorte que l'intégralité du texte soit bien hors de l'ecran

        canvas.after(delai, deplacer, canvas, text_item, vitesse, largeur, text_width, delai)


    canvas = tk.Canvas(fen,height=largeur,width=largeur,background="black")
    points=calculer_points_hexagone(largeur/2,largeur/2,largeur/2.5,90)
    canvas.create_polygon(points,fill="#582900")
    placHole(canvas,points)
    frameright = tk.Frame(fen,bg=main_bg)
    frameleft = tk.Frame(fen, bg=main_bg)
    text_item = canvas.create_text(largeur, largeur // 2, text=texte, anchor='w', font=("Arial", 20, "bold"))
    canvas.update()
    bbox = canvas.bbox(text_item)
    text_width = bbox[2] - bbox[0]

    deplacer(canvas, text_item, vitesse, largeur, text_width, delai)

    replay = tk.Button(frameright,text="rejouer",command=rejouer)
    labright = tk.Label(frameright,text="Score Blanc : 0",bg=main_bg,font=("Comic Sans MS", int(width/60)))
    lableft = tk.Label(frameleft,text="Score Noir : 0",bg=main_bg,font=("Comic Sans MS", int(width/60)))
    bt =tk.Button(frameright,text="Quitter",command=fen.destroy)
    bt.pack(side="bottom",fill="both")
    replay.pack(side="bottom",fill="both")
    labright.pack(side="top", anchor="center")
    lableft.pack(side="top")
    frameright.pack(side="right",fill="both",expand=True)
    frameleft.pack(side="left",fill="both",expand=True)
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
            canvas.create_oval(x1-1,y1-1,x2+1,y2+1,outline="red",width=2,tags=("selection","plateau"))
            canvas.tag_lower("selection", "case") #mise en arrière plan du cercle de selection afin d'éviter les conflits entre leave et enter, et éviter les plantages de tkinter

        except:
            pass


def supprimerSelection(event): # supprime le cercle de sélection s'il existe
    global selected
    if selected:
        selected=False
        canvas.delete("selection")


def createPos(event): #on crée les emplacements possibles
    possibilites=getPossibilites()
    if len(getBouleList()) == 1:
        for i in range(len(possibilites)):
            indicei, indicej = getCase(event)
            y,x=move(possibilites[i][0],possibilites[i][1],indicei,indicej,True)
            x1,y1,x2,y2=getCoord(y,x)
            canvas.create_oval(x1-1,y1-1,x2+1,y2+1,outline="orange",fill="brown",width=2,tags=("possibilites","plateau"))
    else:
        possibilites=possToShow()

        canvas.delete("possibilites")
        cpt=0
        for i in range(len(possibilites)):
            for j in range(len(possibilites[i])):
                indicei,indicej=getBouleList()[i]
                zone=getZone(indicei)
                y,x = moveZ(possibilites[i][j][0],possibilites[i][j][1],zone)
                cpt += 1
                #print(possibilites[i][j][0]+indicei,possibilites[i][j][1]+indicej)
                if getMatrice()[indicei+y][indicej+x] != 1:
                    x1, y1, x2, y2 = getCoord(y+indicei, x+indicej)
                    #print(f"poss : {possibilites[i][j]}, coord : {y},{x} , boule : {données.getBouleList()[i]}")
                    canvas.create_oval(x1 - 1, y1 - 1, x2 + 1, y2 + 1, outline="orange", fill="brown", width=2,tags=("possibilites", "plateau"))
        liste=getBouleList()
        y,x=getDirection(liste[0][0],liste[0][1],liste[1][0],liste[1][1])
        L1 = getSumitoList(liste[-1][0],liste[-1][1],-y,-x)
        L2 = getSumitoList(liste[0][0],liste[0][1],y,x)

        if sumitoCheck(L1):
            zone = getZone(liste[0][0])
            realy, realx = moveZ(-y, -x, zone)
            x1, y1, x2, y2 = getCoord(liste[0][0]+realy,liste[0][1]+realx)
            canvas.create_oval(x1 - 1, y1 - 1, x2 + 1, y2 + 1, outline="orange", fill="violet", width=2,tags=("sumito", "plateau"))

        if sumitoCheck(L2):
            zone = getZone(liste[-1][0])
            realy, realx = moveZ(y, x, zone)
            x1, y1, x2, y2 = getCoord(liste[-1][0] + realy, liste[-1][1] + realx)
            canvas.create_oval(x1 - 1, y1 - 1, x2 + 1, y2 + 1, outline="orange", fill="violet", width=2,tags=("sumito", "plateau"))

def checkClickOut(event):
    y,x=getCase(event)
    if isOut(y,x):
        delOnClick(event)

def onClick(event): # creation du cercle de selection avec clique
    global nbselected
    y,x=getCase(event)
    if isBoule(y, x) and getMatrice()[y][x] == getTeam():
        if nbselected<=2:
            if nbselected==0:
                canvas.delete("selection", "possibilites")
                (i, j) = getCase(event)
                x1, y1, x2, y2 = getCoord(i, j)
                canvas.create_oval(x1 - 1, y1 - 1, x2 + 1, y2 + 1, outline="green", width=2, tags=("selectionClick","plateau"))
                canvas.tag_lower("selectionClick","case")
                addSelectBouleList(i,j)
                createPos(event)
                nbselected+=1
            elif nbselected==1:
                canvas.delete("selection", "possibilites")
                (i, j) = getCase(event)

                if champsAction(getBouleList()[0][0],getBouleList()[0][1],i,j):
                    x1, y1, x2, y2 = getCoord(i, j)
                    canvas.create_oval(x1 - 1, y1 - 1, x2 + 1, y2 + 1, outline="green", width=2, tags=("selectionClick","plateau"))
                    canvas.tag_lower("selectionClick","case")
                    addSelectBouleList(i,j)
                    createPos(event)
                    nbselected+=1
                else:

                    canvas.delete("selection", "possibilites")
            elif nbselected==2:
                canvas.delete("selection", "possibilites")
                (i, j) = getCase(event)
                if isSameDirection(i,j):
                    x1, y1, x2, y2 = getCoord(i, j)
                    canvas.create_oval(x1 - 1, y1 - 1, x2 + 1, y2 + 1, outline="green", width=2,tags=("selectionClick", "plateau"))
                    canvas.tag_lower("selectionClick", "case")
                    addSelectBouleList(i, j)
                    createPos(event)
                    nbselected += 1
                else:
                    canvas.delete("selection", "possibilites")

        else:
            delOnClick(event)


def askMove(event): #fait le liens avec les fontions de mouvement et la position de la boule
    global nbselected
    liste=getBouleList()
    if len(liste) == 1:
        x_initiale,y_initiale=liste[0][1],liste[0][0]
        y_final,x_final=getCase(event)
        canvas.delete("plateau")
        moveToij(y_initiale,x_initiale,y_final,x_final)
        aff(getMatrice(),event)
        resetBouleList()
        nbselected=0
    else:
        poss=possToShow()
        canvas.delete("plateau")
        found = False
        for i in range(len(liste)):
            y_final,x_final=getCase(event)
            for a in range(-1,2):
                if found:
                    break
                for b in range(-1,2):
                    if found:
                        break
                    if b!=0:
                        yreal,xreal=moveZ(a,b,getZone(liste[i][0]))
                        if (liste[i][0]+yreal,liste[i][1]+xreal) == (y_final,x_final) and (a,b) in poss[i]:
                            #print("lol",yreal,xreal)
                            found=True
                            direcy,direcx=a,b
            if found:
                break
        for i in range(len(liste)):
            #print("direc",direcy,direcx)
            multiMove(direcy,direcx)
        canvas.delete("plateau")
        aff(getMatrice(), event)
        resetBouleList()
        nbselected = 0
    changeTeam()



def askSumitoMove(event):
    global nbselected
    def move(L,y,x): #effectue le déplacement
        if sumitoCheck(L):
            multiSumitoMove(L,y,x)
            changeTeam()
            affScore()


    liste=getBouleList()
    y, x = getDirection(liste[0][0], liste[0][1], liste[1][0], liste[1][1])
    L1 = getSumitoList(liste[-1][0], liste[-1][1], -y, -x)
    L2 = getSumitoList(liste[0][0], liste[0][1], y, x)
    move(L1, -y, -x)
    move(L2,y,x)
    resetBouleList()
    nbselected = 0
    canvas.delete("selectionClick", "possibilites", "sumito")
    aff(getMatrice(),event)
    if winCheck() != 0:
        winScreen(winCheck())



def delOnClick(event=None): #supression du cercle de selection avec clique
    global nbselected
    nbselected=0
    canvas.delete("selectionClick","possibilites","sumito")
    resetBouleList()

def selectActive(): #active la selection en survol autour des cases
    canvas.tag_bind("case","<Enter>",aff_selection)
    canvas.tag_bind("case","<Leave>",supprimerSelection)
    canvas.tag_bind("possibilites", "<Button-1>", askMove)
    canvas.tag_bind("case","<Button-1>",onClick)
    canvas.bind("<Button-3>",delOnClick) # le clicque droit annule la selection du moment qu'il est fait au niveau du canvas
    canvas.tag_bind("sumito","<Button-1>",askSumitoMove)
    canvas.bind("<Button-1>",checkClickOut)


def winScreen(gagnant):
    selectInactive()
    if gagnant == 1:
        joueur = "blancs"
    else:
        joueur = "noirs"
    canvas.create_text(width / 2, height / 2, text=f"les {joueur} ont gagnés", font=("Comic Sans MS", int(width/15), "bold"),fill="green", justify="center")


def selectInactive():
    canvas.tag_unbind("case","<Enter>")
    canvas.tag_unbind("case","<Leave>")
    canvas.tag_unbind("possibilites", "<Button-1>")
    canvas.tag_unbind("case","<Button-1>")
    canvas.unbind("<Button-3>")
    canvas.tag_unbind("sumito","<Button-1>")
    canvas.unbind("<Button-1>")


def resolutionWindow(debbug=False): #fenêtre de demande de résolution
    global value
    if not debbug:

        def changeRes(): #met à jour la résolution de la fenêtre en fonction de la résolution sélectionnée

            global long, larg
            long=int(choixVal.get().split("x")[0])
            larg=int(choixVal.get().split("x")[1])
            res.destroy()
            fen.geometry(f"{choixVal.get()}")
            mainCanvas(fen,int(choixVal.get().split("x")[1]),int(choixVal.get().split("x")[1]))

            aff(getMatrice())
            print(value.get())
            if int(value.get())==0:
                randTurn()
            else:
                play()

        choix = ["1920x1080", "1280x720", "800x600", "640x480", "480x360"]

        res = tk.Toplevel() # on crée une fenêtre "fille"
        res.geometry("300x150")
        res.resizable(False,False)
        choixVal = tk.StringVar()
        value = tk.StringVar()
        value.set(1)
        choixVal.set(choix[1])
        lab = tk.LabelFrame(res, text="êtes vous épileptique ?")
        yes = Radiobutton(lab,text="Oui",variable=value,value=1)
        non = Radiobutton(lab,text="Non",variable=value,value=0)
        lab.pack()
        yes.grid(row=0,column=0)
        non.grid(row=0,column=1)
        valide = tk.Button(res,text="valider",command=changeRes)
        label =tk.Label(res,text="Choisissez une résolution :")
        labtest = tk.Label(res,textvariable=choixVal)

        liste = ttk.Combobox(res,textvariable=choixVal, values=choix,state="readonly") # barre de séléction pour les résolutions

        valide.pack(side="bottom")
        label.pack(side="top")
        liste.pack()
        labtest.pack()
        res.mainloop()
    else:
        global long, larg
        long = 1280
        larg = 720
        fen.geometry(f"1280x720")

        mainCanvas(fen, 1280, 720)
        aff(getMatrice())
        play()


def randTurn(delai=1000,r=0,color="white"):
    canvas.delete("rand")
    turn = randTeam()
    pts = calculer_points_hexagone(width/2, width/2, width/4, r)
    canvas.create_polygon(pts, fill=color, tag="rand")
    if delai % 40 == 0:
        if turn==1:
            canvas.create_polygon(pts,fill="white",tag="rand")
            color="white"
        else:
            canvas.create_polygon(pts,fill="black",tag="rand")
            color="black"
    if delai>0:
        canvas.after(10, randTurn,delai-1, r+1,color)
    if delai == 0:
        setTeam(turn)
        canvas.create_text(width / 2, height / 2,text=f"Tour de {color}",font=("Comic Sans MS",int(width/30)),fill="red",tag="rand")
        canvas.after(1000, play)


def play():
    canvas.delete("rand")
    selectActive()
    if value.get()==1: #inactif
        setTeam(1)

def rejouer():
    delOnClick()
    setMat([[-1, -1, -1, -1, -1],
           [-1, -1, -1, -1, -1, -1],
          [0, -1, -1, -1, -1, -1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
          [0, 1, 1, 1, 1, 1, 0],
           [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1]])
    aff(getMatrice())
    resetScore()
    if value.get()==0:
        randTurn()
    else:
        randTurn()




#resolutionWindow(True)

