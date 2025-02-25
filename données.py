import math
global M,selectBouleList,team,out,matrice
selectBouleList=[]
multi_possibilites=[]

out=[[],[],[],[],[],[]]
team=1

def setMat(mat):
    global matrice
    matrice = mat


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

def moveWithij(x1,y1,x2,y2): #déplace a partir des indices seulements
    global matrice
    matrice[y1][x1], matrice[y2][x2] = matrice[y2][x2], matrice[y1][x1]



def move(x,y,i,j,select=False): # déplace la boule aux coordonnées i,j dans la direction x,y
    global matrice
    zone = getZone(i)
    x, y = moveZ(x, y, zone)
    """if isBoule(i, j, x, y):
        sumito(i, j, x, y)"""
    if select == False:
        matrice[i][j], matrice[i + y][j + x] = matrice[i + y][j + x], matrice[i][j]
    else:
        return x+j,y+i


def creativeMove(i,j) :#permet de déplacer une boule librement afin de tester les différentes fonctionnalités
    global matrice
    x = int(input("déplacement x: "))
    y = int(input("déplacement y:"))
    possible = True
    afficheMat(matrice)
    while x != 0 or y!=0:

        zone=getZone(i)
        x,y = moveZ(x,y,zone)
        if isBoule(i, j, x, y):
            sumito(i,j,x,y)
        matrice[i][j],matrice[i+y][j+x]=matrice[i+y][j+x],matrice[i][j]
        resetBouleList()
        addSelectBouleList(i+y,j+x)
        getPossibilites()
        print(possibilites)
        j=j+x
        i=i+y
        afficheMat(matrice)

        x = int(input("déplacement x: "))
        y = int(input("déplacement y:"))
        
def moveZ(x,y,zone):
    def moveZ0(x,y):  # donne les coordonnées relatif aux déplacements des boules qui se situent au milieu de la grille
        if x < 0 and y < 0:  # cas bas gauche
            return (-1, 1)
        elif x > 0 and y < 0:  # cas bas droite
            return (0, 1)
        elif x < 0 and y > 0:  # cas haut gauche
            return (-1, -1)
        elif x > 0 and y > 0:  # cas haut droite
            return (0, -1)


    def moveZ1(x,y):  # donne les coordonnées relatif aux déplacements des boules qui se situent en bas de la grille
        if x < 0 and y < 0:  # cas bas gauche
            return (-1, 1)
        elif x > 0 and y < 0:  # cas bas droite
            return (0, 1)
        elif x < 0 and y > 0:  # cas haut gauche
            return (0, -1)
        elif x > 0 and y > 0:  # cas haut droite
            return (1, -1)


    def moveZ2(x,y):  # donne les coordonnées relatif aux déplacements des boules qui se situent en haut de la grille
        if x < 0 and y < 0:  # cas bas gauche
            return (0, 1)
        elif x > 0 and y < 0:  # cas bas droite
            return (1, 1)
        elif x < 0 and y > 0:  # cas haut gauche
            return (-1, -1)
        elif x > 0 and y > 0:  # cas haut droite
            return (0, -1)
    if y==0:
        return (x,y)
    match zone:
        case 0:
            return moveZ0(x,y)
        case 1:
            return moveZ1(x,y)
        case -1:
            return moveZ2(x,y)


def isBoule(i,j,x=0,y=0): # Observe s'il y a une boule aux coordonées i,j de l'équipe "team"
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


    
def sumito(i,j,x,y): # effectue les déplacement en cas de sumito
    global matrice
    L=getSumitoList(i, j, x, y)
    if sumitoCheck(L): # verifie si on est dans un cas de sumito
        if getSumitoCase(L) == "out": # cas out
            addOut(x,y,L[0][2])
            matrice[L[-2][0]][L[-2][1]]=0
            for i in range(2,len(L)):
                a,b,c=L[-i]
                a1,b1,c1=L[-(i+1)]
                print((a,b),(a1,b1))
                matrice[a][b],matrice[a1][b1]=matrice[a1][b1],matrice[a][b] # décale les positions des boules en cas de out            
        else:
            for i in range(2,len(L)):
                a,b,c=L[-i]
                a1,b1,c1=L[-(i+1)]
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
    global possibilites,selectBouleList,multi_possibilites
    if len(selectBouleList)==1:
        for i in range(-1,2):
            for j in range(-1,2):
                if j!=0:
                    zone=getZone(selectBouleList[0][0])
                    x,y=moveZ(j,i,zone)
                    if not(isOut(selectBouleList[0][1] + x, selectBouleList[0][0] + y)):
                        if not(isBoule(selectBouleList[0][0],selectBouleList[0][1],x,y)) :
                            possibilites.append((i,j))
    else:
        multi_possibilites=[]
        sortBetween()
        for a in range(len(selectBouleList)):
            possibilites=[]
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if j != 0:
                        zone = getZone(selectBouleList[a][0])
                        x, y = moveZ(j, i, zone)
                        if not (isOut(selectBouleList[a][1] + x, selectBouleList[a][0] + y)):
                            if (not (isBoule(selectBouleList[a][0], selectBouleList[a][1], x, y)) or ((selectBouleList[a][0]+y,selectBouleList[a][1]+x) in selectBouleList)):
                                possibilites.append((i, j))
            multi_possibilites.append(possibilites)
        print(multi_possibilites)

        possibilites=[]
        for i in multi_possibilites[0]:
            cpt=0 # on compte le nombre d'occurence des possibilités
            for j in range(1,len(multi_possibilites)):
                if i in multi_possibilites[j] and i not in possibilites:
                    cpt+=1
                    if cpt == len(multi_possibilites)-1:
                        possibilites.append(i)
        print(possibilites)
        return possibilites
    return possibilites



def quickDirection(i,j,y): # i,j correspond à la direction en langage naturel et y la position y de la case dans la matrice elle permet de determiner la zone:
    zone=getZone(y)
    print("putain :" ,i,j)
    x,y=moveZ(i,j,zone)
    return y,x


def isSameDirection(posy,posx):# observe si une boule se situe dans le même ligne que deux autres boules
    global selectBouleList
    if len(selectBouleList) == 2:
        direction=getDirection(selectBouleList[0][1],selectBouleList[0][0],selectBouleList[1][1],selectBouleList[1][0]) #pour chaque boule sélect
        for h in range(len(selectBouleList)):
            zone=getZone(selectBouleList[h][0])
            b,a=moveZ(direction[1],direction[0],zone)
            if (selectBouleList[h][0]+a == posy and selectBouleList[h][1]+b == posx) or (selectBouleList[h][0]-a == posy and selectBouleList[h][1]-b == posx):
                return True
    return False

def getDirection(x,y,x2,y2): #obtenir la direction a partir des coordonnées de deux boules
        zone = getZone(y)
        direction = (None, None)
        for a in range(-1, 2):
            for b in range(-1, 2):
                if b != 0:
                    j, i = moveZ(b, a, getZone(y))
                    if (i + y, j + x) == (y2,x2):
                        return (a, b)

def getAbsoluteDirection(x,y,x2,y2): #obtenir la direction a partir des coordonnées de deux boules
        zone = getZone(y)
        direction = (None, None)
        for a in range(-1, 2):
            for b in range(-1, 2):
                if b != 0:
                    j, i = moveZ(b, a, getZone(y))
                    if (i + y, j + x) == (y2,x2):
                        return (abs(a), abs(b))

def sortBetween(): #permet de trier selectBouleList de sorte à ce que la boule qui se situe entre les deux autres corresponde au 2ème élément
    global selectBouleList
    if len(selectBouleList) == 3:
        #print("test")
        y,x=getDirection(selectBouleList[0][1],selectBouleList[0][0],selectBouleList[1][1],selectBouleList[1][0])
        #print(y,x)
        i0,j0 = selectBouleList[0][0],selectBouleList[0][1]
        i1,j1 = selectBouleList[1][0],selectBouleList[1][1]
        i2,j2 = selectBouleList[2][0],selectBouleList[2][1]

        if ((i0+y,j0+x) == (i1,j1) or (i0-y,j0-x) == (i1,j1)) and ((i0+y,j0+x) == (i2,j2) or (i0-y,j0-x) == (i2,j2)):
            selectBouleList[0],selectBouleList[1]=selectBouleList[1],selectBouleList[0]
        elif ((i1+y,j1+x) == (i0,j0) or (i1-y,j1-x) == (i0,j0)) and ((i1+y,j1+x) == (i2,j2) or (i1-y,j1-x) == (i2,j2)):
            selectBouleList[0],selectBouleList[1]=selectBouleList[1],selectBouleList[0]
        elif ((i2+y,j2+x) == (i0,j0) or (i2-y,j2-x) == (i0,j0)) and ((i2+y,j2+x) == (i1,j1) or (i2-y,j2-x) == (i1,j1)):
            selectBouleList[2],selectBouleList[1]=selectBouleList[1],selectBouleList[2]




def isOut(x,y): # vérifie si on est toujours dans la grille
    if 0 <= y <= 8:
        if y == 0:
            return not (0 <= x <= 4)
        elif y == 1:
            return not (0 <= x <= 5)
        elif y == 2:
            return not (0 <= x <= 6)
        elif y == 3:
            return not (0 <= x <= 7)
        elif y == 4:
            return not (0 <= x <= 8)
        elif y == 5:
            return not (0 <= x <= 7)
        elif y == 6:
            return not (0 <= x <= 6)
        elif y == 7:
            return not (0 <= x <= 5)
        elif y == 8:
            return not (0 <= x <= 4)
    return True




def addOut(x,y,couleur): #ajoute a une liste de liste les boules hors jeu
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
                    x,y=moveZ(b,a,zone)
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
