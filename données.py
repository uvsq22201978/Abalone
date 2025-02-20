global M,selectBouleList,team,out,matrice
selectBouleList=[]

out=[[],[],[],[],[],[]]
team=1
ex=          [[0, 0, 0, 0, -1],
           [0, 0, 0, 0, -1, 0],
          [0, 0, 0, 0, 1, 0, 0],
         [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1,-1, -1],
         [0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]]




def setMat(M):
    global matrice
    matrice = M
    
setMat([[0, 0, 0, 0, -1],
           [0, 0, 0, 0, 0, 0],
          [0, 0, 1, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0,0,0],
         [0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]])

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


def move(x,y,i,j,select=False): # déplace la boule aux coordonnées i,j dans la direction x,y
    global matrice
    #afficheMat(matrice)
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



"""def moveZ0(x,y): # donne les coordonnées relatif aux déplacements des boules qui se situent au milieu de la grille
        if x<0 and y<0: #cas bas gauche
            return (-1,1)
        elif x>0 and y<0: #cas bas droite
            return (-1,1)
        elif x<0 and y>0: #cas haut gauche
            return (-1,-1)
        elif x>0 and y>0: #cas haut droite
            return (0,-1)
        
        
def moveZ1(x,y): # donne les coordonnées relatif aux déplacements des boules qui se situent en bas de la grille        
        if x<0 and y<0: #cas bas gauche
            return (-1,1)
        elif x>0 and y<0: #cas bas droite
            return (0,1)
        elif x<0 and y>0: #cas haut gauche
            return (0,-1)
        elif x>0 and y>0: #cas haut droite
            return (1,-1)
        
def moveZ2(x,y): # donne les coordonnées relatif aux déplacements des boules qui se situent en haut de la grille
        if x<0 and y<0: #cas bas gauche
            return (0,1)
        elif x>0 and y<0: #cas bas droite
            return (1,1)
        elif x<0 and y>0: #cas haut gauche
            return (-1,-1)
        elif x>0 and y>0: #cas haut droite
            return (0,-1)"""


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
    
    
#ancienne version



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
    selectBouleList.append((i,j)) # [(cordy,cordx),(etcy,etcx),...]
    possibilites=[]

def resetBouleList():
    global selectBouleList
    selectBouleList=[]

def getPossibilites(): # permet d'obtenir la liste des mouvements possible pour une boule selectionnée
    global possibilites,select_BouleList
    if len(selectBouleList)==1:
        for i in range(-1,2):
            for j in range(-1,2):
                if j!=0:
                    zone=getZone(selectBouleList[0][0])
                    x,y=moveZ(j,i,zone)
                    if not(isOut(selectBouleList[0][1] + x, selectBouleList[0][0] + y)):
                        if not(isBoule(selectBouleList[0][0],selectBouleList[0][1],x,y)) :
                            possibilites.append((i,j))
    return possibilites



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
        
"""print(moveZ(1,0,-1))
creativeMove(4,4)"""



