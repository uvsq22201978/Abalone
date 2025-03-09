# Attention, utilisation d'une syntaxe récente veiller à utiliser la version la plus récente de Python
# Ce programme garanti au minima l'affichage du jeu Abalone plus ou moins fonctionnel
# Dans le cas ou aucun n'affichage n'apparaît, merci de vérifier votre configuration
# En cas de non-respect des instructions, nous ne nous tenons pas responsable de tout problème survenu
# Merci de votre comprehension


from ihm import *
from modele import *


def demarrage(): #lance le menu de démarrage
    global animStart
    animStart=True # statut de l'animation du bouton start #cette manip est inutile mais, si supprimée penser à modifier les appels aux variables respectives
    try:
        pygame.mixer.music.load("loop-menu.mp3")
        pygame.mixer.music.play(loops=-1)
    except:
        pass
    finally:
        dem = tk.Canvas(fen, height=500, width=500, background="#2C3E50")  # Couleur élégante (bleu-gris foncé)
        dem.create_text(height * 0.5, width * 0.45, fill="black", text="Abalone", font=("Comic Sans MS", 50, "bold"),tag=['txt'])
        def apparitionCredit(height,width,dem,t):#on fait appraitre les crédits au bout d'un certain temps, temps pdt lequel le bouton start est désactivé
            if t>0:
                dem.after(1000,apparitionCredit,height,width,dem,t-1)
            else:
                dem.create_text(height * 0.5, width * 0.55, fill="black", text="Created by Nassim & Gabriel",font=("Comic Sans MS", 10), tag=['auteurs'])

                start.config(state="normal")


    def commandStart(): #commande du bouton start
        global animStart
        try:
            bruitage = pygame.mixer.Sound("interface.mp3")
            bruitage.play()
        except:
            pass
        finally:
            defilCredit(dem)
            animStart = False
            start.destroy()
            fen.after(1000,dem.destroy)
            resolutionWindow()

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
        try:
            bruitage = pygame.mixer.Sound("pop.mp3")
            bruitage.play()
        except:
            pass
        finally:
            start.config(font=("Arial", 16, "bold"),pady=20,padx=30)

    def startSmaller(event): #on réduit la taille du bouton
        start.config(font=("Arial", 12, "bold"),pady=10,padx=20)


    start = tk.Button(fen,state="disabled", text="Start", padx=20, pady=10, bg="#3498DB", fg="white", font=("Arial", 12, "bold"), bd=2,relief="raised", activebackground="#16A085", activeforeground="white", command=commandStart)
    dem.create_window(250, 350, window=start,tag=['start'])
    apparitionCredit(height,width,dem,1)
    makeLogo(dem)

    dem.focus_set()
    start.bind("<Enter>",startBigger)
    start.bind("<Leave>",startSmaller)
    animeButton()
    dem.pack()


try:
    pygame.mixer.init()
except:
    pass

demarrage()
fen.mainloop()