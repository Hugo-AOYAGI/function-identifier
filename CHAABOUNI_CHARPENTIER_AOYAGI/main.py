
# IMPORTS
import tkinter as tk

import tkinter.filedialog as fd
import tkinter.messagebox as mb

import matplotlib
import matplotlib.pyplot as plt



import json # Permet de lire le fichier contenant les éléments de style de la fenetre.
import os # Pour lire ou d'écrire des fichiers texte
from ctypes import windll # Permet de rendre la fenetre moins floue

import numpy as np # Permet le traitement des valeurs
import math # Pour d'avoir accès aux fonctions mathématiques de base
import random # Permet la création de bruit

dir_= input("Entrez le chemin du dossier : ")

os.chdir(dir_)

print("La fenetre pour exporter l'équation ne fonctionne pas sur pyzo.")
pyzo = input("Utilisez vous Pyzo ? (O/N) : ")
if pyzo != "O": 
    # Permet d'intégrer matplotlib dans tkinter
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    matplotlib.use('TkAgg')

# Importation des matrices jacobiennes et fonctions
import partial_derivatives as pd

# Application Class
class TkinterApp:
    
    # Constructor
    def __init__(self):
        
        # Creation de la fenetre principale
        self.root = tk.Tk()
        
        # Paramètres de la fenetre principale
        self.root.title("Projet Info n°22")
        self.root.geometry("1600x900+0+0")

        # Rend la fenetre moins floue
        windll.shcore.SetProcessDpiAwareness(1)
        self.root.tk.call('tk', 'scaling', 2)

        self.root.tk_setPalette(background="#F9F9F9", foreground="#000000")
        
        # Variables de la fenetre
        self.window_widgets = {} # Nom du Widget --> Widget 
        self.tkinter_variables = {} # Nom de la Variable --> Variable Tkinter
        self.style_sheet = {} # Nom du Widget --> Style

        # Choix du thème
        self.theme = "light"

        # Chemins des fichiers auxquels on ajoute le bruit ou que l'on identifie
        self.identifyPath = ""
        self.noisePath = ""

        # Variables pour les cycles de l'algorithme par seconde
        self.cycles_per_second = tk.IntVar()        
        self.cycles_per_second.set(1)  

        self.isCycling = False
        self.cycles_count = 0
        
        # Variable pour le séparateur des valeurs dans les fichiers de courbes
        self.separator = tk.StringVar()
        self.separator.set("")

        # Variable pour l'intensité du bruit
        self.noiseIntensity = tk.DoubleVar()
        self.noiseIntensity.set(0)

        # Appel des fonctions de démarrage
        self.loadStyleSheet()

        self.mainMenuSetup()
        self.noiseMenuSetup()
        self.identifyMenuSetup()
        self.resultMenuSetup()

        # Affichage du menu principal
        self.mainMenu.lift()

    # Chargement du fichier contenant les éléments de style des widgets
    def loadStyleSheet(self):
        path = os.path.join(dir_, "sheet.json")
        
        # Ouverture du fichier json
        with open(path, "r") as sheet:
            data = json.load(sheet)
            self.style_sheet =  data

    def mainMenuSetup(self):	
        # Création du Widget 'mainMenu'
        self.mainMenu = tk.Frame(self.root, self.style_sheet["mainMenu"])
        self.mainMenu.place(relx=0, rely=0, relwidth=1, relheight=1)
            

        # Création du Widget 'mm_title'
        lbl = tk.Label(self.mainMenu, self.style_sheet["mm_title"])
        lbl.place(relx=0, rely=0, relwidth=1, relheight=0.2)
        self.window_widgets.update({"mm_title": lbl}) # On garde toujours une référence des widgets construits si ceux ci doivent être utilisés ultérieurement


        # Création du Widget 'mm_identify_btn'
        btn = tk.Button(self.mainMenu, self.style_sheet["mm_identify_btn"], command=lambda: self.identifyMenu.lift())
        btn.place(relx=0.3, rely=0.4, relwidth=0.4, relheight=0.1)
        self.window_widgets.update({"mm_identify_btn": btn})


        # Création du Widget 'mm_noise_btn'
        btn = tk.Button(self.mainMenu, self.style_sheet["mm_noise_btn"], command=lambda: self.noiseMenu.lift())
        btn.place(relx=0.3, rely=0.51, relwidth=0.4, relheight=0.1)
        self.window_widgets.update({"mm_noise_btn": btn})

        # Création du Widget 'mm_theme_btn'
        btn = tk.Button(self.mainMenu, self.style_sheet["mm_theme_btn"], command=self.changeTheme)
        btn.place(relx=0, rely=0.95, relwidth=0.1, relheight=0.05)
        self.window_widgets.update({"mm_theme_btn": btn})
    
    def changeTheme(self):
        if self.theme == "light":
            self.root.tk_setPalette(background="#595959", foreground="#E9E9E9")
        else:
            self.root.tk_setPalette(background="#F9F9F9", foreground="#000000")
        self.theme = "light" if self.theme == "dark" else "dark"            
        
    
    def noiseMenuSetup(self):	
        # Création du Widget 'noiseMenu'
        self.noiseMenu = tk.Frame(self.root, self.style_sheet["noiseMenu"])
        self.noiseMenu.place(relx=0, rely=0, relwidth=1, relheight=1)
            

        # Création du Widget 'nm_back_btn'
        btn = tk.Button(self.noiseMenu, self.style_sheet["nm_back_btn"], command=lambda: self.mainMenu.lift())
        btn.place(relx=0, rely=0.9, relwidth=0.2, relheight=0.1)
        self.window_widgets.update({"nm_back_btn": btn})


        # Création du Widget 'nm_title_lbl'
        lbl = tk.Label(self.noiseMenu, self.style_sheet["nm_title_lbl"])
        lbl.place(relx=0, rely=0, relwidth=1, relheight=0.2)
        self.window_widgets.update({"nm_title_lbl": lbl})


        # Création du Widget 'nm_selected_lbl'
        lbl = tk.Label(self.noiseMenu, self.style_sheet["nm_selected_lbl"])
        lbl.place(relx=0.3, rely=0.3, relwidth=0.15, relheight=0.075)
        self.window_widgets.update({"nm_selected_lbl": lbl})

        # Création du Widget 'nm_selected_btn', permet de choisir un fichier sur lequel ajouter du bruit
        self.nm_selected_btn = tk.Button(self.noiseMenu, self.style_sheet["nm_selected_btn"], command=self.openFileToAddNoise)
        self.nm_selected_btn.place(relx=0.45, rely=0.3, relwidth=0.25, relheight=0.075)
            

        # Création du Widget 'nm_intensity_lbl'
        lbl = tk.Label(self.noiseMenu, self.style_sheet["nm_intensity_lbl"])
        lbl.place(relx=0.3, rely=0.55, relwidth=0.15, relheight=0.075)
        self.window_widgets.update({"nm_intensity_lbl": lbl})

        # Création du Widget 'nm_intensity_input', choix de l'intensité du bruit
        self.nm_intensity_input = tk.Spinbox(self.noiseMenu, self.style_sheet["nm_intensity_input"], textvariable=self.noiseIntensity)
        self.nm_intensity_input.place(relx=0.45, rely=0.55, relwidth=0.25, relheight=0.075)
            

        # Création du Widget 'nm_prob_law_lbl'
        lbl = tk.Label(self.noiseMenu, self.style_sheet["nm_prob_law_lbl"])
        lbl.place(relx=0.3, rely=0.65, relwidth=0.25, relheight=0.075)
        self.window_widgets.update({"nm_prob_law_lbl": lbl})

        self.prob_law = tk.StringVar()

        # Création du Widget 'nm_prob_law_input', choix de la loi de probabilité
        self.nm_prob_law_input = tk.OptionMenu(self.noiseMenu, self.prob_law, 'uniforme',' normale')
        self.nm_prob_law_input.configure(self.style_sheet["nm_prob_law_input"])
        self.nm_prob_law_input.place(relx=0.55, rely=0.65, relwidth=0.15, relheight=0.075)


        # Création du Widget 'nm_confirm_btn'
        btn = tk.Button(self.noiseMenu, self.style_sheet["nm_confirm_btn"], command=self.addNoise)
        btn.place(relx=0.4, rely=0.8, relwidth=0.2, relheight=0.1)
        self.window_widgets.update({"nm_confirm_btn": btn})


        # Création du Widget 'nm_separator_lbl'
        lbl = tk.Label(self.noiseMenu, self.style_sheet["nm_separator_lbl"])
        lbl.place(relx=0.3, rely=0.4, relwidth=0.2, relheight=0.075)
        self.window_widgets.update({"nm_separator_lbl": lbl})

        # Création du Widget 'nm_separator_input', choix du séparateur dans le fichier texte, (par exemple un espace ou une virgule pour séparer les valeurs)
        self.nm_separator_input = tk.Entry(self.noiseMenu, self.style_sheet["nm_separator_input"], textvariable=self.separator)
        self.nm_separator_input.place(relx=0.5, rely=0.4, relwidth=0.2, relheight=0.075)
            
    # Ouverture du fichier où ajouter du bruit par l'utilisateur
    def openFileToAddNoise(self): 
        path = fd.askopenfilename()
        self.nm_selected_btn["text"] = path.split("/")[-1]
        self.noisePath = path

    def addNoise(self):
        
        listet, listey = [], []
        
        try:
            # Création des listes x et y pour les traiter ensuite
            with open(self.noisePath, "r") as f:
                lines = f.readlines()
                for line in lines:
                    # On coupe la liste en fonction du séparateur chosis
                    vals = line.split(self.separator.get())
                    t, y = vals[0], vals[1]
                    listet.append(float(t)); listey.append(float(y))
        except:
            mb.showwarning("Erreur", "Le fichier ou chemin est invalide.")
            return
        
        # Choix du bruit selon la loi selectionnée
        if self.prob_law.get() == "uniforme":
            # loi Uniforme
            listey = [y + self.noiseIntensity.get()*random.random()*(-1 if random.random() < 0.5 else 1) for y in listey]
        else:
            # loi Normale
            listey = [y + self.noiseIntensity.get()*random.gauss(0, 3) for y in listey]

        # Sauvegarde du fichier
        path = fd.asksaveasfilename()

        try:
            with open(path, "w") as f:
                for i in range(len(listey)):
                    line = "{}{} {}\n".format(listet[i], self.separator.get(), listey[i])
                    f.write(line)
        except:
            mb.showwarning("Erreur", "Le fichier ou chemin est invalide.")
            return
        
        self.mainMenu.lift()
    

    def identifyMenuSetup(self):

        # Ce menu suit la même structure que le menu de bruit.
        
        # Création du Widget 'identifyMenu'
        self.identifyMenu = tk.Frame(self.root, self.style_sheet["identifyMenu"])
        self.identifyMenu.place(relx=0, rely=0, relwidth=1, relheight=1)
            

        # Création du Widget 'im_back_btn'
        btn = tk.Button(self.identifyMenu, self.style_sheet["im_back_btn"], command=lambda: self.mainMenu.lift())
        btn.place(relx=0, rely=0.9, relwidth=0.2, relheight=0.1)
        self.window_widgets.update({"im_back_btn": btn})


        # Création du Widget 'im_title_lbl'
        lbl = tk.Label(self.identifyMenu, self.style_sheet["im_title_lbl"])
        lbl.place(relx=0, rely=0, relwidth=1, relheight=0.2)
        self.window_widgets.update({"im_title_lbl": lbl})


        # Création du Widget 'im_selected_lbl'
        lbl = tk.Label(self.identifyMenu, self.style_sheet["im_selected_lbl"])
        lbl.place(relx=0.3, rely=0.3, relwidth=0.15, relheight=0.075)
        self.window_widgets.update({"im_selected_lbl": lbl})

        # Création du Widget 'im_selected_input'
        self.im_selected_input = tk.Button(self.identifyMenu, self.style_sheet["im_selected_input"], command=self.openFileToIdentify)
        self.im_selected_input.place(relx=0.45, rely=0.3, relwidth=0.25, relheight=0.075)
            

        # Création du Widget 'im_separator_lbl'
        lbl = tk.Label(self.identifyMenu, self.style_sheet["im_separator_lbl"])
        lbl.place(relx=0.3, rely=0.4, relwidth=0.2, relheight=0.075)
        self.window_widgets.update({"im_separator_lbl": lbl})


        # Création du Widget 'im_separator_input'
        entry = tk.Entry(self.identifyMenu, self.style_sheet["im_separator_input"], textvariable=self.separator)
        entry.place(relx=0.5, rely=0.4, relwidth=0.2, relheight=0.075)
        self.window_widgets.update({"im_separator_input": entry})


        # Création du Widget 'im_type_lbl'
        lbl = tk.Label(self.identifyMenu, self.style_sheet["im_type_lbl"])
        lbl.place(relx=0.3, rely=0.55, relwidth=0.15, relheight=0.075)
        self.window_widgets.update({"im_type_lbl": lbl})

        # Permet de savoir si l'utilisateur veut identifier un premier ordre, un second ordre, ..etc
        self.func_type = tk.StringVar()

        # Création du Widget 'nm_type_input'
        self.nm_type_input = tk.OptionMenu(self.identifyMenu, self.func_type, 'second ordre sous-amorti','premier ordre', 'droite')
        self.nm_type_input.configure(self.style_sheet["nm_type_input"])
        self.nm_type_input.place(relx=0.45, rely=0.55, relwidth=0.25, relheight=0.075)


        # Création du Widget 'im_confirm_btn'
        btn = tk.Button(self.identifyMenu, self.style_sheet["im_confirm_btn"], command=self.identifier)
        btn.place(relx=0.4, rely=0.7, relwidth=0.2, relheight=0.1)
        self.window_widgets.update({"im_confirm_btn": btn})

    # Récupération des données du fichier selectionné
    def identifier(self):
        listet, listey = [], []

        # Ouverture du fichier texte et récupération des valeurs
        try:
            with open(self.identifyPath, "r") as f:
                lines = f.readlines()
                for line in lines:
                    vals = line.split(self.separator.get())
                    t, y = vals[0], vals[1]
                    listet.append(float(t)); listey.append(float(y))
        except:
            mb.showwarning("Erreur", "Le fichier ou chemin est invalide.")
            return
            
        # Création d'un objet identificateur
        self.identificateur = Identificateur(listet, listey, self.func_type.get(), self)

        self.resultMenu.lift()

    # Ouverture du popup pour choisir un fichier à identifier
    def openFileToIdentify(self): 
        path = fd.askopenfilename()
        self.im_selected_input["text"] = path.split("/")[-1]
        self.identifyPath = path

    def resultMenuSetup(self):	
        # Création du Widget 'resultMenu'
        self.resultMenu = tk.Frame(self.root, self.style_sheet["resultMenu"])
        self.resultMenu.place(relx=0, rely=0, relwidth=1, relheight=1)
            
        # Création du Widget 'rm_title_lbl'
        lbl = tk.Label(self.resultMenu, self.style_sheet["rm_title_lbl"])
        lbl.place(relx=0, rely=0, relwidth=0.8, relheight=0.2)
        self.window_widgets.update({"rm_title_lbl": lbl})

        # Création du Widget 'rm_error_lbl'
        lbl = tk.Label(self.resultMenu, self.style_sheet["rm_error_lbl"])
        lbl.place(relx=0.8, rely=0, relwidth=0.2, relheight=0.1)
        self.window_widgets.update({"rm_error_lbl": lbl})

        # Création du Widget 'rm_error_val'
        lbl = tk.Label(self.resultMenu, self.style_sheet["rm_error_val"])
        lbl.place(relx=0.8, rely=0.1, relwidth=0.2, relheight=0.1)
        self.window_widgets.update({"rm_error_val": lbl})

        # Création du Widget 'graphCanv', permet d'afficher le graphique du modèle et des valeurs réelles
        self.graphCanv = tk.Canvas(self.resultMenu, self.style_sheet["graphCanv"])
        self.graphCanv.place(relx=0.2, rely=0.2, relwidth=0.8, relheight=0.7)

        # Création du Widget 'rm_cycles_lbl', permet d'afficher le nombre de cycles effectués
        lbl = tk.Label(self.resultMenu, self.style_sheet["rm_cycles_lbl"])
        lbl.place(relx=0.84, rely=0.21, relwidth=0.15, relheight=0.05)
        self.window_widgets.update({"rm_cycles_lbl": lbl})

        # Création du Widget 'rm_back_btn'
        btn = tk.Button(self.resultMenu, self.style_sheet["rm_back_btn"], command=lambda: self.backToMain())
        btn.place(relx=0, rely=0.9, relwidth=0.2, relheight=0.1)
        self.window_widgets.update({"rm_back_btn": btn})

        # Création du Widget 'rm_forward_btn', permet de faire 10 cycles d'un coup
        btn = tk.Button(self.resultMenu, self.style_sheet["rm_forward_btn"], command=lambda :self.identificateur.cycle(10))
        btn.place(relx=0.352, rely=0.9, relwidth=0.075, relheight=0.1)
        self.window_widgets.update({"rm_forward_btn": btn})


        # Création du Widget 'rm_next_btn', permet de faire un seul cycle
        btn = tk.Button(self.resultMenu, self.style_sheet["rm_next_btn"], command=lambda :self.identificateur.cycle())
        btn.place(relx=0.277, rely=0.9, relwidth=0.075, relheight=0.1)
        self.window_widgets.update({"rm_next_btn": btn})


        # Création du Widget 'rm_pause_btn'
        btn = tk.Button(self.resultMenu, self.style_sheet["rm_pause_btn"], command=lambda: self.cyclesStart())
        btn.place(relx=0.202, rely=0.9, relwidth=0.075, relheight=0.1)
        self.window_widgets.update({"rm_pause_btn": btn})


        # Création du Widget 'rm_cps_lbl'
        lbl = tk.Label(self.resultMenu, self.style_sheet["rm_cpm_lbl"])
        lbl.place(relx=0.43, rely=0.9, relwidth=0.2, relheight=0.05)
        self.window_widgets.update({"rm_cps_lbl": lbl})


        # Création du Widget 'rm_cps_input', choix du nombre de cycles par secondes à effectuer
        entry = tk.Entry(self.resultMenu, self.style_sheet["rm_cps_input"], textvariable=self.cycles_per_second)
        entry.place(relx=0.43, rely=0.95, relwidth=0.2, relheight=0.05)
        self.window_widgets.update({"rm_cps_input": entry})


        # Création du Widget 'rm_export_btn', permet d'ouvrir une fenetre où l'on peut exporter la fonction en python ou en latex
        btn = tk.Button(self.resultMenu, self.style_sheet["rm_export_btn"], command = lambda: self.exportEquationWindow())
        btn.place(relx=0.6325, rely=0.9, relwidth=0.2, relheight=0.1)
        self.window_widgets.update({"rm_export_btn": btn})


        # Création du Widget 'rm_reset_btn'
        btn = tk.Button(self.resultMenu, self.style_sheet["rm_reset_btn"], command=lambda: self.reset())
        btn.place(relx=0.835, rely=0.9, relwidth=0.165, relheight=0.1)
        self.window_widgets.update({"rm_reset_btn": btn})

    # Retour au menu principal
    def backToMain(self):
        self.cyclesStop()
        self.cycles_count = 0
        self.mainMenu.lift()

    # Démarage des cycles par secondes
    def cyclesStart(self):
        # Actualisation du bouton pause
        self.window_widgets["rm_pause_btn"]["text"] = "▶"
        self.window_widgets["rm_pause_btn"]["command"] = lambda: self.cyclesStop()

        self.isCycling = True

        self.cycling()

    # Execution d'un cycle d'identification
    def cycling(self):
        if self.isCycling:
            try:
                self.identificateur.cycle(1)
                # Effectue des cycles en fonction du nombre de cycles par secondes choisis par l'utilisateur
                self.root.after(int((1/self.cycles_per_second.get())*1000), self.cycling)
                # .after permet d'appeller une fonction après une durée prédéterminée, ici on appelle la fonction en elle même
            except:
                self.cyclesStop()

    # Arret des cycles par secondes
    def cyclesStop(self):
        # Affichage du bouton pause
        self.window_widgets["rm_pause_btn"]["text"] = "l l"
        self.window_widgets["rm_pause_btn"]["command"] = lambda: self.cyclesStart()

        self.isCycling = False
 
    def reset(self):
        self.identificateur.q =  [0.1442, 0.24, 70] # Valeurs aléatoires éloignées pour mieux tester le programme
        self.identificateur.drawModel()

    # Tracé du graphe
    def drawGraph(self, listex, listey, fill_="black", max_val = False, min_val = False, points = False):

        self.window_widgets["rm_cycles_lbl"]["text"] = "Cycles : " + str(self.cycles_count)
        
        w, h = int(self.root.winfo_screenwidth()), int(self.root.winfo_screenheight())

        # Récupération des valeurs extrèmes pour adapter l'échelle
        max_y = max(listey) if not max_val else max_val
        max_x = max(listex)
        min_y = min(listey) if not min_val else min_val
        min_x = min(listex)

        # Choix entre tracé de points et de lignes
        if not points:
            for i in range(len(listex) - 1):
                # Remise à l'échelle de tous les points
                x1, y1 = ((listex[i] - min_x)/(max_x - min_x))*w, h - (((listey[i] - min_y)/(max_y - min_y))*0.7*h + 0.2*h)
                x2, y2 = ((listex[i+1] - min_x)/(max_x - min_x))*w, h - (((listey[i+1] - min_y)/(max_y - min_y))*0.7*h + 0.2*h)
                self.graphCanv.create_line(x1, y1, x2 , y2, fill=fill_, width=3)
        else:
            for i in range(len(listex)):
                # Remise à l'échelle de tous les points
                x1, y1 = ((listex[i] - min_x)/(max_x - min_x))*w, h - (((listey[i] - min_y)/(max_y - min_y))*0.7*h + 0.2*h)
                self.graphCanv.create_oval(x1-2, y1-2, x1+2, y1+2, fill=fill_, width=3)


        return max_y, min_y

    # Affichage de la fenetre pour exporter l'équation
    def exportEquationWindow(self):
        
        if pyzo == "O":
            return

        win = tk.Toplevel(self.root)
        win.geometry("800x400")
        win.title("Exporter l'équation")

        # Création des widgets de la fenetre
        title_lbl = tk.Label(win, text="Exporter l'équation", font=("Arial", 20))
        title_lbl.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        # Création du Widget "canvas_lbl", permet d'afficher l'équation en Latex
        canvas_lbl = tk.Label(win, relief="groove")
        canvas_lbl.place(relx=0.025, rely=0.15, relwidth=0.95, relheight=0.15)

        # Utilisation de la librairie pour intégrer une figure matplotlib dans tkinter pour afficher le latex
        canvas = FigureCanvasTkAgg(fig, master=canvas_lbl)
        canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)
        canvas._tkcanvas.place(relx=0, rely=0, relwidth=1, relheight=1)

        ax.axis('off')

        # Récupération des codes latex ou python de l'équation
        # Pour un second ordre
        if self.identificateur.type_ == "second ordre sous-amorti":
            latex_string = pd.second_ordre_latex_template.replace("K", str(round(self.identificateur.q[0], 5))).replace("z", str(round(self.identificateur.q[1], 5))).replace("w", str(round(self.identificateur.q[2], 5)))
            python_string = pd.second_ordre_py_template.replace("K", str(round(self.identificateur.q[0], 5))).replace("z", str(round(self.identificateur.q[1], 5))).replace("w", str(round(self.identificateur.q[2], 5)))
        # Pour un premier ordre
        elif self.identificateur.type_ == "premier ordre":
            latex_string = pd.premier_ordre_latex_template.replace("K", str(round(self.identificateur.q[0], 5))).replace("tau", str(round(self.identificateur.q[1], 5)))
            python_string = pd.premier_ordre_py_template.replace("K", str(round(self.identificateur.q[0], 5))).replace("tau", str(round(self.identificateur.q[1], 5)))
        # Pour une droite
        elif self.identificateur.type_ == "droite":
            latex_string = pd.droite_latex_template.replace("a", str(round(self.identificateur.q[0], 5))).replace("b", str(round(self.identificateur.q[1], 5)))
            python_string = pd.droite_py_template.replace("a", str(round(self.identificateur.q[0], 5))).replace("b", str(round(self.identificateur.q[1], 5)))

        # Affichage de l'équation en latex
        ax.text(0.5, 0.5, "$" + latex_string + "$", fontsize = 11, horizontalalignment="center", verticalalignment="center")  
        canvas.draw()

        # Affichage de l'équation en python
        lbl_py = tk.Label(win, text="En Python :", font=("Arial", 14))
        lbl_py.place(relx=0.02, rely=0.4, relwidth=0.2, relheight=0.1)

        txt_py = tk.Text(win)
        txt_py.insert(tk.INSERT, python_string)
        txt_py.place(relx=0.25, rely=0.4, relwidth=0.7, relheight=0.2)

        # Rend l'entrée de texte en lecture seule
        txt_py.config(state=tk.DISABLED)

        # Affichage de l'équation en Latex
        lbl_tex = tk.Label(win, text="En Latex :", font=("Arial", 14))
        lbl_tex.place(relx=0.02, rely=0.7, relwidth=0.2, relheight=0.1)

        txt_tex = tk.Text(win)
        txt_tex.insert(tk.INSERT, latex_string)
        txt_tex.place(relx=0.25, rely=0.7, relwidth=0.7, relheight=0.2)

        # Rend l'entrée de texte en lecture seule
        txt_tex.config(state=tk.DISABLED)

        # Démarrage de la fenêtre popup
        win.mainloop()

class Identificateur:

    def __init__(self, listex, listey, type_, app):
        self.listet, self.listey = listex, listey

        # Contient le type de la fonction (premier ordre, second ordre)
        self.type_ = type_
        # Contient une référence à la fenetre parente
        self.app = app

        # Valeurs et noms des arguments de la fonction
        self.q_names_lbls = []
        self.q_vals_lbls = []

        # Appel des fonctions de démarrage
        self.setType()
        self.setupArgsLabels()
        self.drawModel()

    def setupArgsLabels(self):
        # Affichage en temps réel des valeurs des arguments
        for i, q in enumerate(self.q_names):
            # Création du label du titre : ex "Gain K"
            lbl = tk.Label(self.app.resultMenu, self.app.style_sheet["rm_arg_lbl"], text=q)
            lbl.place(relx=0, rely=0.2 + 0.175*i, relwidth=0.2, relheight=0.075)
            self.q_names_lbls.append(lbl)
            # Création du label de la valeur de l'argument
            lbl = tk.Label(self.app.resultMenu, self.app.style_sheet["rm_arg_val_lbl"], text=str(self.q[i] + 0.0000001)[0:7])
            lbl.place(relx=0, rely=0.275 + 0.175*i, relwidth=0.2, relheight=0.1)
            self.q_vals_lbls.append(lbl)

    # Affichage du modèle et des points réels
    def drawModel(self):
        modele = [self.f(t, self.q) for t in self.listet]

        self.app.graphCanv.delete("all")

        # On récupère les points mins et max pour adapter l'échelle aux points réels
        max, min = self.app.drawGraph(self.listet, self.listey, "black", points=True)
        self.app.drawGraph(self.listet, modele, "red", max, min)

        # Calcul et affichage de l'erreur relative
        self.app.window_widgets["rm_error_val"]["text"] = str(round(self.erreurRelative(), 5))

    def setType(self):
        # Définition des propriétés (matrices, noms des arguments ..etc) selon le type choisis par l'utilisateur
        if self.type_ == "premier ordre":
            # Récupération des matrices jacobiennes
            self.matriceJacobienne = lambda q, listet, listey: pd.MatriceJacobiennePremierOrdre(q, listet, listey)
            self.matriceJacobienneDerivee = lambda  q, listet, listey: pd.MatriceJacobiennePremierOrdreDerivee(q, listet, listey)
            # Récupération de la fonction
            self.f = pd.premier_ordre
            # Définition des arguments
            self.q_names = ["Gain K", '\u03C4']
            self.q = pd.ApproxParametresPremierOrdre(self.listet, self.listey)
            
        elif self.type_ == "second ordre sous-amorti":
            # Récupération des matrices jacobiennes
            self.matriceJacobienne = lambda  q, listet, listey: pd.MatriceJacobienneSecondOrdre(q, listet, listey)
            self.matriceJacobienneDerivee = lambda  q, listet, listey: pd.MatriceJacobienneSecondOrdreDerivee(q, listet, listey)
            # Récupération de la fonction
            self.f = pd.second_ordre
            # Définition des arguments
            self.q_names = ["Gain K", '\u03BE', '\u03C9']
            self.q = pd.ApproxParametresSecondOrdre(self.listet, self.listey)
            
        elif self.type_ == "droite":
            # Récupération des matrices jacobiennes
            self.matriceJacobienne = lambda  q, listet, listey: pd.MatriceJacobienneDroite(q, listet, listey)
            self.matriceJacobienneDerivee = lambda  q, listet, listey: pd.MatriceJacobienneDroiteDerivee(q, listet, listey)
            # Récupération de la fonction
            self.f = pd.droite
            # Définition des arguments
            self.q_names = ["a", 'b']
            self.q = [0.3, 2]
    
    # Cycle d'identification (calcul d'un certain dq)
    def cycle(self, n=1):

        # Actualisation du nombre de cycles effectués
        self.app.cycles_count += n
        
        for i in range(n):

            # Récupération des matrices jacobiennes
            F = self.matriceJacobienne(self.q, self.listet, self.listey)
            dF = self.matriceJacobienneDerivee(self.q, self.listet, self.listey)

            # Calcul de la solution du système linéaire
            dq = -np.linalg.solve(dF,F).transpose()[0]
            
            # Modification de q et des labels
            for k in range(len(dq)):
                self.q[k] += dq[k]
                self.q_vals_lbls[k]["text"] = str(self.q[k] + 0.0000001)[0:7]

        self.drawModel()

    def erreurRelative(self):
        # Calcul de l'erreur relative
        modele = [self.f(t, self.q) for t in self.listet]
        s1 = 0
        s2 = 0
        for k in range(len(self.listey)):
            s1 = s1 + (modele[k]-self.listey[k])**2
            s2 = s2 + self.listey[k]**2
        return s1/s2



# Running the Application
if __name__ == "__main__":
    app = TkinterApp()
    app.root.mainloop()
    

