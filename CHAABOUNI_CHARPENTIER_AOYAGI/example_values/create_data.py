

import numpy as np
import os
import math
import matplotlib.pyplot as plt

premier_ordre = lambda t, q: q[0]*(1 - math.exp(-t/q[1]))
second_ordre = lambda t, q: q[0]*(1 - math.exp(-q[1]*q[2]*t)*(math.cos(q[2]*t*math.sqrt(1 - q[1]**2)) + (q[1]/math.sqrt(1-q[1]**2)*math.sin(q[2]*t*math.sqrt(1-q[1]**2)))))
parabole = lambda t, q: q[0]*t**2 + q[1]*t + q[2]
droite = lambda t, q: q[0]*t + q[1]

path = input("Entrez le nom du fichier : ")
sepa = input("Séparateur : ")

print("\nArguments : ")
n = int(input(" - n (nombre de points) : "))
inf = int(input(" - inf (borne inférieure): "))
sup = int(input(" - sup (borne supérieure): "))

print("\n Les types disponibles sont : \n'second ordre sous-amorti',\n'premier ordre',\n'parabole',\n'droite' ")
type = input("  - type de fonction : ")

print("\Paramètres : ")
if type == "second ordre sous-amorti":
    K = float(input(" - Gain : "))
    z = float(input(" - Coefficient de frottement : "))
    w = float(input(" - Pulsation propre : "))
    q = (K, z, w)
    f = second_ordre

elif type == "premier ordre":
    K = float(input(" - Gain : "))
    T = float(input(" - Temps de réponse : "))
    q = (K, T)
    f = premier_ordre

elif type == "parabole":
    a = float(input(" - a : "))
    b = float(input(" - b : "))
    c = float(input(" - c : "))
    q = (a, b, c)
    f = parabole

elif type == "droite":
    a = float(input(" - a : "))
    b = float(input(" - b : "))
    q = (a, b)
    f = droite

listet = np.linspace(inf, sup, n)

listey = [f(t, q) for t in listet]

with open(os.path.join(os.path.dirname(__file__), path), "w") as f:
    for i in range(len(listet)):
        line = "{}{} {}\n".format(listet[i], sepa, listey[i])
        f.write(line)

plt.plot(listet, listey)
plt.show()


