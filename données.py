# Attention, utilisation d'une syntaxe récente veiller à utiliser la version la plus récente de Python
# Ce programme garanti au minima l'affichage du jeu Abalone plus ou moins fonctionnel
# Dans le cas ou aucun n'affichage n'apparaît, merci de vérifier votre configuration
# En cas de non respect des instructions, nous nous tenons pas responsable de tout problème survenu
# Merci de votre comprehension

import math
global M,selectBouleList,team,out,matrice
selectBouleList=[]
multi_possibilites=[]
direction = [(-1,-1),(-1,1),(0,-1),(0,1),(1,-1),(1,1)]
out=[[],[],[],[],[],[]]
team=1

def setMat(mat): #définit la matrice
    global matrice
    matrice = mat

def setindiceMat(i,j,val):# on remplace assigne une valeur val a l'indice i,j de la matrice
    global matrice
    matrice[i][j]=val

def afficheMat(matrice): #affiche la matrice dans la console sous la forme de grille Abalone
    for i in range(5):
        print(" " * len(matrice[4-i]),matrice[i])
    for i in range(5,9):
        print(" " * len(matrice[12-i]),matrice[i])



def matNulle(): # creation de la grille vide du jeu
    global matrice
    matrice=[]
    for i in range(5,10):
        matrice.append([0 for j in range(0,i)])

    for i in range(8,3,-1):
        matrice.append([0 for j in range(0,i)])

    afficheMat(matrice)

def resetOut(): # remet à 0 la liste des boules hors jeu
    global out
    out=[[],[],[],[],[],[]]

def setOut(L): #définir la liste des boules qui sont hors jeu
    global out
    out=L

def moveToij(y1,x1,y2,x2): #déplace a partir des indices seulements
    global matrice
    #print(f"y1,x1 : {y1,x1} ,y2,x2 : {y2,x2}")
    matrice[y1][x1], matrice[y2][x2] = matrice[y2][x2], matrice[y1][x1]


def multiMove(directy,directx): #procède au déplacement d'un groupe de boules
    global selectBouleList
    for i in range(len(selectBouleList)): #on set a 0 l'endroit ou se situe les boules avant déplacement
        y,x=selectBouleList[i]
        setindiceMat(y,x,0)
    for i in range(len(selectBouleList)): #on set a 1/-1 le nouvel emplacement des boules
        y,x=selectBouleList[i]
        #print("y,x",y,x)
        realy,realx=quickDirection(directy,directx,selectBouleList[i][0])
        #print("real",realy,realx)
        setindiceMat(y+realy,x+realx,1)


def move(y,x,i,j,select=False): # déplace la boule aux coordonnées i,j dans la direction x,y
    global matrice
    zone = getZone(i)
    y, x = moveZ(y, x, zone)

    if select == False:
        matrice[i][j], matrice[i + y][j + x] = matrice[i + y][j + x], matrice[i][j]
    else:
        return y+i,x+j

def moveZ(y,x,zone):
    def moveZ0(y,x):  # donne les coordonnées relatif aux déplacements des boules qui se situent au milieu de la grille
        if x < 0 and y < 0:  # cas bas gauche
            return (1, -1)
        elif x > 0 and y < 0:  # cas bas droite
            return (1, 0)
        elif x < 0 and y > 0:  # cas haut gauche
            return (-1, -1)
        elif x > 0 and y > 0:  # cas haut droite
            return (-1, 0)


    def moveZ1(y,x):  # donne les coordonnées relatif aux déplacements des boules qui se situent en bas de la grille
        if x < 0 and y < 0:  # cas bas gauche
            return (1, -1)
        elif x > 0 and y < 0:  # cas bas droite
            return (1, 0)
        elif x < 0 and y > 0:  # cas haut gauche
            return (-1, 0)
        elif x > 0 and y > 0:  # cas haut droite
            return (-1, 1)


    def moveZ2(y,x):  # donne les coordonnées relatif aux déplacements des boules qui se situent en haut de la grille
        if x < 0 and y < 0:  # cas bas gauche
            return (1, 0)
        elif x > 0 and y < 0:  # cas bas droite
            return (1, 1)
        elif x < 0 and y > 0:  # cas haut gauche
            return (-1, -1)
        elif x > 0 and y > 0:  # cas haut droite
            return (-1, 0)
    if y==0:
        return (y,x)
    match zone:
        case 0:
            return moveZ0(y,x)
        case 1:
            return moveZ1(y,x)
        case -1:
            return moveZ2(y,x)


def isBoule(i,j,y=0,x=0): # Observe s'il y a une boule aux coordonées i,j de l'équipe "team"
    global matrice
    return matrice[i+y][j+x] == -1 or matrice[i+y][j+x] == 1



def getZone(i): # Donne la zone de la grille dans la quelle se situe la boule (haut:-1,milieu:0,bas:+1)
    if 0<= i <= 3:
        return -1
    elif i == 4:
        return 0
    else :
        return 1

def getMatrice():
    global matrice
    return matrice

def getSumitoList(i,j,x,y): # Donne la liste des éléments dans la direction x,y à partir de la position i,j
    L=[]
    while True:
        if 0<=i<=8 and 0<=j<=(len(matrice[i])-1): #verifie si on est dans la grille
            if matrice[i][j] != 0:# on ajoute toute type de boule a la liste
                L.append((i,j,matrice[i][j]))

            elif len(L) == 7: #si on a + de 6 boules + le cas on s'arrete
                break

            elif matrice[i][j]==0: # si on tombe sur une case vide on est dans le cas "empty"
                L.append("empty")
                break
        elif (i<0 or i > 8) or (j<0 or j>(len(matrice[i])-1)): # verifie si on est en dehors de la grille
            L.append("out") #si on se retrouve en dehors de la grille on est dans le cas out
            break

        i+=y
        j+=x
    return L



def sumitoCheck(L): #verifie à partir de la sumitoList si un sumito est detecté
    black=0
    white=0
    team=L[0][2]
    if L[len(L)-1]!= "out" and L[len(L)-1]!="empty": # si on n'est dans le cas d'une ejection ou de déplacement de boule alors on retourne Faux
        return False
    for i in range(len(L)-2):
        if L[i][2]==1: #lorsque qu'une boule blanche est trouvée on actualise son compteur
            white+=1
        elif L[i][2]==-1: #lorsque qu'une boule noir est trouvée on actualise so compteur
            black+=1
        if (L[i][2]==-team) and L[i+1][2] == team: #si une boule de l'équipe emettrice du sumito se situe après une boule noir alors pas de sumito (règle à verifier)
            return False
    if team == 1 and white>black: # si on l'équipe white est en superiorité numéique alors le sumito est confirmé dans le cas ou elle est l'emettrice de ce coup
        return True
    elif team == -1 and black>white: # si on l'équipe black est en superiorité numéique alors le sumito est confirmé dans le cas ou elle est l'emettrice de ce coup
        return True



def getSumitoCase(L): #permet de savoir si une boule va être éjecté ou si c'est un simple déplacement de plusieurs boules
    return L[len(L)-1]



def sumito(i,j,y,x): # effectue les déplacement en cas de sumito
    global matrice
    L=getSumitoList(i, j, y, x)
    if sumitoCheck(L): # verifie si on est dans un cas de sumito
        if getSumitoCase(L) == "out": # cas out
            addOut(y,x,L[0][2])
            matrice[L[-2][0]][L[-2][1]]=0
            for i in range(2,len(L)):
                a,b,c=L[-i]
                a1,b1,c1=L[-(i+1)]
                #print((a,b),(a1,b1))
                matrice[a][b],matrice[a1][b1]=matrice[a1][b1],matrice[a][b] # décale les positions des boules en cas de out

def addSelectBouleList(i,j):#on ajoute la boule séléctionné à la liste de boules sélectionnées
    global selectBouleList,possibilites
    selectBouleList.append((i,j)) # [(indicey,indicex),(etcy,etcx),...]
    possibilites=[]

def resetBouleList():
    global selectBouleList,multi_possibilites
    selectBouleList=[]
    multi_possibilites = []

def getBouleList():
    return selectBouleList

def getPossibilites(): # permet d'obtenir la liste des mouvements possible pour une boule selectionnée
    global possibilites,multi_possibilites
    sortBetween()
    def uniPosi(boule,nb): #donne les possibilités pour une boule donnée
        possi=[]
        global selectBouleList
        for i in range(-1, 2):
            for j in range(-1, 2):
                if j != 0:
                    zone = getZone(boule[0])
                    y, x = moveZ(i, j, zone)
                    if not (isOut(selectBouleList[nb][0] + y, selectBouleList[nb][1] + x)):
                        if (not (isBoule(selectBouleList[nb][0], selectBouleList[nb][1], y, x))) or (selectBouleList[nb][0] + y, selectBouleList[nb][1] + x) in selectBouleList :
                            #print((selectBouleList[nb][0] + y, selectBouleList[nb][1] + x))
                            possi.append((i, j))
                            #print(possi)
        #print(possi)
        return possi

    if len(selectBouleList)==1:
        return uniPosi(selectBouleList[0],0)
    else:
        #print(selectBouleList)
        multi_possibilites=[]
        possibilites = []
        for a in range(len(selectBouleList)):
            possi=[]
            possi=uniPosi(selectBouleList[a],a)
            multi_possibilites.append(possi)
        #print("possi",possi)
        #print("multi",multi_possibilites)

        for i in multi_possibilites[0]: # pour savoir les possibilités valides on regarde les possibilites que les boules de la selection ont en commun
            cpt=0 # on compte le nombre d'occurence des possibilités
            for j in range(1,len(multi_possibilites)):
                if i in multi_possibilites[j] and i not in possibilites:
                    cpt+=1
                    if cpt == len(multi_possibilites)-1:
                        possibilites.append(i)
        print("pas multi",possibilites)
    return possibilites



def possToShow(): # obtient la liste des possibilités a afficher pour chaque boules
    global possibilites,selectBouleList
    haut=[(1,1),(0,1),(0,-1),(1,-1)]
    mid=[(0,1),(0,-1)]
    bas=[(-1,1),(0,1),(0,-1),(-1,-1)]
    gauche=[(0,-1),(1,-1),(-1,-1),(1,1),(-1,1)]
    droite=[(0,1),(1,1),(-1,1),(1,-1),(-1,-1)]
    possibilitesShow=[[] for i in range(len(selectBouleList))]
    a,b=getAbsoluteDirection(selectBouleList[0][0],selectBouleList[0][1],selectBouleList[1][0],selectBouleList[1][1])
    print("a,b : ",a,b)
    if (a,b) != (0,1):
        y,x=quickDirection(a,b,selectBouleList[0][0])
        for i in bas:
            if i in possibilites:
                possibilitesShow[-1].append(i)
        for i in haut:
            if i in possibilites:
                possibilitesShow[0].append(i)

        if len(selectBouleList) == 3:
            for i in mid:
                if i in possibilites:
                    possibilitesShow[1].append(i)
    else:
        print("ok")
        y, x = quickDirection(a, b, selectBouleList[0][0])
        if selectBouleList[0][0] + y == selectBouleList[1][0] and selectBouleList[0][1] + x == selectBouleList[1][1]:
            for i in gauche:
                if i in possibilites:
                    possibilitesShow[0].append(i)
            for i in droite:
                if i in possibilites:
                    possibilitesShow[-1].append(i)
    return possibilitesShow

def quickDirection(i,j,y): # i,j correspond à la direction en langage naturel et y la position y de la case dans la matrice elle permet de determiner la zone:
    zone=getZone(y)
    y,x=moveZ(i,j,zone)
    return y,x # renvoie la traduction du déplacement selon la zone dans la matrice


def isSameDirection(posy,posx):# observe si une boule se situe dans le même ligne que deux autres boules
    global selectBouleList
    if len(selectBouleList) == 2:
        direction=getDirection(selectBouleList[0][0],selectBouleList[0][1],selectBouleList[1][0],selectBouleList[1][1]) #pour chaque boule sélect
        for h in range(len(selectBouleList)):
            zone=getZone(selectBouleList[h][0])
            a,b=moveZ(direction[0],direction[1],zone)
            if (selectBouleList[h][0]+a == posy and selectBouleList[h][1]+b == posx) or (selectBouleList[h][0]-a == posy and selectBouleList[h][1]-b == posx):
                return True
    return False

def getDirection(y,x,y2,x2): #obtenir la direction a partir des coordonnées de deux boules
        zone = getZone(y)
        direction = (None, None)
        for a in range(-1, 2):
            for b in range(-1, 2):
                if b != 0:
                    i,j = moveZ(a, b, getZone(y))
                    if (i + y, j + x) == (y2,x2):
                        return (a, b)

def getAbsoluteDirection(y,x,y2,x2): #obtenir la direction a partir des coordonnées de deux boules
        a,b=getDirection(y,x,y2,x2)
        return (abs(a),abs(b))


def sortBetween():  # permet de trier selectBouleList de sorte à ce que la boule qui se situe entre les deux autres corresponde au 2ème élément
    global selectBouleList
    if len(selectBouleList) >1:
        selectBouleList.sort(key=lambda coord: (coord[0], coord[1])) #on tri les tuples par i prioritairement puis par j




def isOut(y,x): # vérifie si on est toujours dans la grille
    if 0 <= y <= 8:
        match (y):
            case 0:
                return not (0 <= x <= 4)
            case 1:
                return not (0 <= x <= 5)
            case 2:
                return not (0 <= x <= 6)
            case 3:
                return not (0 <= x <= 7)
            case 4:
                return not (0 <= x <= 8)
            case 5:
                return not (0 <= x <= 7)
            case 6:
                return not (0 <= x <= 6)
            case 7:
                return not (0 <= x <= 5)
            case 8:
                return not (0 <= x <= 4)
            case _:
                return True
    return True




def addOut(y,x,couleur): #ajoute a une liste de liste les boules hors jeu
    global out
    if x<=0 and y<=0: #cas bas gauche
        out.append(couleur)
    elif x>=0 and y<=0: #cas bas droite
        out.append(couleur)
    elif x<0 and y>0: #cas haut gauche
        out.append(couleur)
    elif x>0 and y>0: #cas haut droite
        out.append(couleur)


def champsAction(i,j,i2,j2):# verifie si une boule est dans le champs d'action d'une autre boule
    global matrice
    if isBoule(i2,j2):
        zone=getZone(i)
        for a in range(-1,2):
            for b in range(-1,2):
                if b!=0:
                    y,x=moveZ(a,b,zone)
                    if (y+i,x+j) == (i2,j2):
                        return True
    return False

        
"""print(moveZ(1,0,-1))
creativeMove(4,4)"""


setMat([[-1, -1, -1, -1, -1],
           [-1, -1, -1, -1, -1, -1],
          [0, -1, -1, -1, -1, -1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
          [0, 1, 1, 1, 1, 1, 0],
           [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1]])
