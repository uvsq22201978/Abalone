global M
ex=    [[0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 1, -1],
         [0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]]


M=          [[0, 0, 0, 0, -1],
           [0, 0, 0, 0, -1, 0],
          [0, 0, 0, 0, 1, 0, 0],
         [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1,-1, -1],
         [0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]]


global team,out,matrice
out=[[],[],[],[],[],[]]
team=1



def setMat(M):
    global matrice
    matrice = M
    
setMat(M)

def afficheMat(matrice): #affiche la matrice dnas la console sous la forme de grille Abalone
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

        
#obsolète / a mettre à jour
def move(x,y,i,j): # déplace la boule aux coordonnées i,j dans la direction x,y
    global matrice
    if y == 0: # cas déplacement lattérale
        if x == 1:
            matrice[i][j+1],matrice[i][j]=matrice[i][j],matrice[i][j+1]
        elif x == -1:
            matrice[i][j-1],matrice[i][j]=matrice[i][j],matrice[i][j-1]
    else:
        zone=getZone(i)
        if zone==0:
            x,y = moveZ0(x,y)
            matrice[i+y][j+x],matrice[i][j]=matrice[i][j],matrice[i+y][j+x]
            i,j=i+y,j+x
        elif zone==1:
            x,y = moveZ1(x,y)
            matrice[i+y][j+x],matrice[i][j]=matrice[i][j],matrice[i+y][j+x]
            i,j=i+y,j+x
        elif zone==-1:
            x,y = moveZ2(x,y)
            matrice[i+y][j+x],matrice[i][j]=matrice[i][j],matrice[i+y][j+x]
            i,j=i+y,j+x
        
    afficheMat(matrice)


def creativeMove(i,j) :#permet de déplacer une boule librement afin de tester les différentes fonctionnalités
    
    x = int(input("déplacement x: "))
    y = int(input("déplacement y:"))
    afficheMat(matrice)
    while x != 0 or y!=0:
        
        if y == 0: # cas déplacement lattérale
        
            if x == 1:
                
                if isBoule(i, j, x, y):
                    sumito(i,j,x,y)
                j+=1
                
            elif x == -1:
                if isBoule(i, j, x, y):
                    sumito(i,j,x,y)
                j-=1
                
                
        else: # déplacement digonal
            zone=getZone(i)
            
            if zone==0: #milieu
                x,y = moveZ0(x,y)
                if isBoule(i, j, x, y):
                    sumito(i,j,x,y)
                i,j=i+y,j+x
                
            elif zone==1:
                x,y = moveZ1(x,y)
                if isBoule(i, j, x, y):
                    sumito(i,j,x,y)
                i,j=i+y,j+x
                
                
            elif zone==-1:
                x,y = moveZ2(x,y)
                if isBoule(i, j, x, y):
                    sumito(i,j,x,y)
                i,j=i+y,j+x
                
                
        afficheMat(matrice)
                
            

        x = int(input("déplacement x: "))
        y = int(input("déplacement y:"))
        

        
def moveZ0(x,y): # donne les coordonnées relatif aux déplacements des boules qui se situent au milieu de la grille        
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
            return (x,-1)
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
            return (0,-1)

                
        
        
def isBoule(i,j,x,y,): # Observe s'il y a une boule aux coordonées i,j de l'équipe "team"
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


"""def sumito(i,j,x,y,white,black): #vérifie s'il y a un sumito, x,y représente le sens de déplacement de la boule aux coo i,j 
    global sx,sy #coo de la dernière boule
    if matrice[i][j] == 1: # actualise les compteur en fonction des boules trouvées
        white+=1
    else:
        black+=1
    
    if (team == 1 and black != 0) and matrice[i][j] == 1: #si on tombe sur une boule de notre équipe suite à un enchainement de boule adverse alors le sumito est faux
        return False
    elif (team == -1 and white != 0) and matrice[i][j] == -1:
        return False
    else:
        if (i+y<0 or i+y>8) or (x+j<0 or x+j>(len(matrice[i])-1)): # si une boule se retrouve out
            if white<=3 and black<white and team==1:
                return True
            elif black<=3 and black>white and team==-1:
                return True
            else:
                return False
        elif (i+y>=0 or i+y<=8) or (x+j>=0 and x+j<=(len(matrice[i])-1)): #on est bien dans la grille
            if matrice[i+y][j+x] == 0 and (white<=3 and black<white and team==1) and black!=0: #on tombe sur une case vide
            
                return True
            elif matrice[i+y][j+x] == 0 and (black<=3 and black>white and team==-1) and white!=0:
                return True
            else: #cas par défaut on tombe sur une autre boule
                return sumito(i+y,j+x,x,y,white,black)"""
            
            
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
 

           
def getSumitoCase(L): #permet de savoir si une boule va être éjecté si c'est un simple déplacement de plusieurs boules
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
        
        

#creativeMove(4,4)

setMat([[0, 0, 0, 0, -1],
           [0, 0, 0, 0, -1, 0],
          [0, 0, 0, 0, 1, 0, 0],
         [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1,-1, 1],
         [0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]])