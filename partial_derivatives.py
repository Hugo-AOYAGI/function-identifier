
import math
import numpy as np

premier_ordre = lambda t, q: q[0]*(1 - math.exp(-t/q[1]))

premier_ordre_dK = lambda t, q, y: 2*(premier_ordre(t, q) - y)*(-math.exp(-t/q[1]) + 1)
premier_ordre_dK_dK = lambda t, q, y: 2*(-math.exp(-t/q[1]) + 1)**2

premier_ordre_dT = lambda t, q, y: -(2*math.exp(-t/q[1])*t*q[0]*(premier_ordre(t, q) - y))/(q[1]**2)
premier_ordre_dT_dT = lambda t, q, y: -(2*q[0]*t*(-2*math.exp(-t/q[1]) + math.exp(-t/q[1])*q[0]*t - math.exp(-t/q[1])*t*y -(2*math.exp(-t/q[1])*t*q[0]*(premier_ordre(t, q) - y))))/(q[1]**4)

premier_ordre_dK_dT = lambda t, q, y: 2*(2*math.exp(-2*t/q[1])*q[0]*t - 2*math.exp(-t/q[1])*q[0]*t + math.exp(-t/q[1])*t*y)/(q[1]**2)

second_ordre = lambda t, q: q[0]*(1 - math.exp(-q[1]*q[2]*t)*(math.cos(q[2]*t*math.sqrt(1 - q[1]**2)) + (q[1]/math.sqrt(1-q[1]**2)*math.sin(q[2]*t*math.sqrt(1-q[1]**2)))))

second_ordre_dK = lambda t, q, y: 2*(1-math.exp(-t*q[2]*q[1])*((q[1]*math.sin(t*q[2]*math.sqrt(1-q[1]**2)))/math.sqrt(1-q[1]**2)+math.cos(t*q[2]*math.sqrt(1-q[1]**2))))*((1-math.exp(-t*q[2]*q[1])*((q[1]*math.sin(t*q[2]*math.sqrt(1-q[1]**2)))/math.sqrt(1-q[1]**2)+math.cos(t*q[2]*math.sqrt(1-q[1]**2))))*q[0]-y)
second_ordre_dK_dK = lambda t, q, y: 2*(1-math.exp(-t*q[2]*q[1])*((q[1]*math.sin(t*q[2]*math.sqrt(1-q[1]**2)))/math.sqrt(1-q[1]**2)+math.cos(t*q[2]*math.sqrt(1-q[1]**2))))**2

second_ordre_dz = lambda t, q, y: (2*q[0]*math.exp(-2*t*q[2]*q[1])*(q[0]*q[1]*math.sin(t*q[2]*math.sqrt(1-q[1]**2))+q[0]*math.sqrt(1-q[1]**2)*math.cos(t*q[2]*math.sqrt(1-q[1]**2))+(y-q[0])*math.sqrt(1-q[1]**2)*math.exp(t*q[2]*q[1]))*((q[1]**2-1)*math.sin(t*q[2]*math.sqrt(1-q[1]**2))+t*q[2]*(1-q[1]**2)**(3/2)*math.cos(t*q[2]*math.sqrt(1-q[1]**2))))/(q[1]**2-1)**3
second_ordre_dz_dz = lambda t, q, y: (2*q[0]*math.exp(-2*t*q[2]*q[1])*(q[0]*t*q[2]*q[1]*math.sin(t*q[2]*math.sqrt(1-q[1]**2))+q[0]*math.sin(t*q[2]*math.sqrt(1-q[1]**2))-(q[0]*t*q[2]*q[1]**2*math.cos(t*q[2]*math.sqrt(1-q[1]**2)))/math.sqrt(1-q[1]**2)-(q[0]*q[1]*math.cos(t*q[2]*math.sqrt(1-q[1]**2)))/math.sqrt(1-q[1]**2)+t*q[2]*(y-q[0])*math.sqrt(1-q[1]**2)*math.exp(t*q[2]*q[1])-((y-q[0])*q[1]*math.exp(t*q[2]*q[1]))/math.sqrt(1-q[1]**2))*((q[1]**2-1)*math.sin(t*q[2]*math.sqrt(1-q[1]**2))+t*q[2]*(1-q[1]**2)**(3/2)*math.cos(t*q[2]*math.sqrt(1-q[1]**2))))/(q[1]**2-1)**3-(4*q[0]*t*q[2]*math.exp(-2*t*q[2]*q[1])*(q[0]*q[1]*math.sin(t*q[2]*math.sqrt(1-q[1]**2))+q[0]*math.sqrt(1-q[1]**2)*math.cos(t*q[2]*math.sqrt(1-q[1]**2))+(y-q[0])*math.sqrt(1-q[1]**2)*math.exp(t*q[2]*q[1]))*((q[1]**2-1)*math.sin(t*q[2]*math.sqrt(1-q[1]**2))+t*q[2]*(1-q[1]**2)**(3/2)*math.cos(t*q[2]*math.sqrt(1-q[1]**2))))/(q[1]**2-1)**3-(12*q[0]*q[1]*math.exp(-2*t*q[2]*q[1])*(q[0]*q[1]*math.sin(t*q[2]*math.sqrt(1-q[1]**2))+q[0]*math.sqrt(1-q[1]**2)*math.cos(t*q[2]*math.sqrt(1-q[1]**2))+(y-q[0])*math.sqrt(1-q[1]**2)*math.exp(t*q[2]*q[1]))*((q[1]**2-1)*math.sin(t*q[2]*math.sqrt(1-q[1]**2))+t*q[2]*(1-q[1]**2)**(3/2)*math.cos(t*q[2]*math.sqrt(1-q[1]**2))))/(q[1]**2-1)**4+(2*q[0]*math.exp(-2*t*q[2]*q[1])*(q[0]*q[1]*math.sin(t*q[2]*math.sqrt(1-q[1]**2))+q[0]*math.sqrt(1-q[1]**2)*math.cos(t*q[2]*math.sqrt(1-q[1]**2))+(y-q[0])*math.sqrt(1-q[1]**2)*math.exp(t*q[2]*q[1]))*(t**2*q[2]**2*q[1]*(1-q[1]**2)*math.sin(t*q[2]*math.sqrt(1-q[1]**2))+2*q[1]*math.sin(t*q[2]*math.sqrt(1-q[1]**2))-3*t*q[2]*q[1]*math.sqrt(1-q[1]**2)*math.cos(t*q[2]*math.sqrt(1-q[1]**2))-(t*q[2]*q[1]*(q[1]**2-1)*math.cos(t*q[2]*math.sqrt(1-q[1]**2)))/math.sqrt(1-q[1]**2)))/(q[1]**2-1)**3

second_ordre_dw = lambda t, q, y: (2*q[0]*t*math.exp(-2*t*q[1]*q[2])*math.sin(t*math.sqrt(1-q[1]**2)*q[2])*(q[0]*q[1]*math.sin(t*math.sqrt(1-q[1]**2)*q[2])+q[0]*math.sqrt(1-q[1]**2)*math.cos(t*math.sqrt(1-q[1]**2)*q[2])+(y-q[0])*math.sqrt(1-q[1]**2)*math.exp(t*q[1]*q[2])))/(q[1]**2-1)
second_ordre_dw_dw = lambda t, q, y: -(2*q[0]*t**2*math.exp(-2*t*q[1]*q[2])*((q[0]*q[1]**2+q[0])*math.sin(t*math.sqrt(1-q[1]**2)*q[2])**2+(y-q[0])*q[1]*math.sqrt(1-q[1]**2)*math.exp(t*q[1]*q[2])*math.sin(t*math.sqrt(1-q[1]**2)*q[2])+(q[0]*q[1]**2-q[0])*math.cos(t*math.sqrt(1-q[1]**2)*q[2])**2+((y-q[0])*q[1]**2-y+q[0])*math.exp(t*q[1]*q[2])*math.cos(t*math.sqrt(1-q[1]**2)*q[2])))/(q[1]**2-1)

second_ordre_dK_dz = lambda t, q, y: (2*math.exp(-2*t*q[2]*q[1])*(2*q[0]*q[1]*math.sin(t*q[2]*math.sqrt(1-q[1]**2))+2*q[0]*math.sqrt(1-q[1]**2)*math.cos(t*q[2]*math.sqrt(1-q[1]**2))+(y-2*q[0])*math.sqrt(1-q[1]**2)*math.exp(t*q[2]*q[1]))*((q[1]**2-1)*math.sin(t*q[2]*math.sqrt(1-q[1]**2))+t*q[2]*(1-q[1]**2)**(3/2)*math.cos(t*q[2]*math.sqrt(1-q[1]**2))))/(q[1]**2-1)**3
second_ordre_dK_dw = lambda t, q, y: (2*t*math.exp(-2*t*q[1]*q[2])*math.sin(t*math.sqrt(1-q[1]**2)*q[2])*(2*q[0]*q[1]*math.sin(t*math.sqrt(1-q[1]**2)*q[2])+2*q[0]*math.sqrt(1-q[1]**2)*math.cos(t*math.sqrt(1-q[1]**2)*q[2])+(y-2*q[0])*math.sqrt(1-q[1]**2)*math.exp(t*q[1]*q[2])))/(q[1]**2-1)

second_ordre_dz_dw = lambda t, q, y: -(2*q[0]*t*math.exp(-2*t*q[1]*q[2])*(((q[0]*t*q[1]**5-2*q[0]*t*q[1]**3+q[0]*t*q[1])*q[2]+q[0]*q[1]**4-q[0])*math.sin(t*math.sqrt(1-q[1]**2)*q[2])**2+(((math.sqrt(1-q[1]**2)*(q[0]*t*q[1]**4-2*q[0]*t*q[1]**2+q[0]*t)+(1-q[1]**2)**(3/2)*(q[0]*t*q[1]**2+q[0]*t))*q[2]-q[0]*q[1]*(1-q[1]**2)**(3/2))*math.cos(t*math.sqrt(1-q[1]**2)*q[2])+(math.sqrt(1-q[1]**2)*((t*y-q[0]*t)*q[1]**4+(2*q[0]*t-2*t*y)*q[1]**2+t*y-q[0]*t)*q[2]+math.sqrt(1-q[1]**2)*((y-q[0])*q[1]**3+(q[0]-y)*q[1]))*math.exp(t*q[1]*q[2]))*math.sin(t*math.sqrt(1-q[1]**2)*q[2])+(q[0]*t*q[1]**5-2*q[0]*t*q[1]**3+q[0]*t*q[1])*q[2]*math.cos(t*math.sqrt(1-q[1]**2)*q[2])**2+((t*y-q[0]*t)*q[1]**5+(2*q[0]*t-2*t*y)*q[1]**3+(t*y-q[0]*t)*q[1])*q[2]*math.exp(t*q[1]*q[2])*math.cos(t*math.sqrt(1-q[1]**2)*q[2])))/(q[1]**2-1)**3

droite = lambda t, q: q[0]*t + q[1]

droite_da = lambda t, q, y: 2*t*(t*q[0]-y+q[1])
droite_da_da = lambda t, q, y: 2*t**2

droite_db = lambda t, q, y: 2*(q[1]-y+q[0]*t)
droite_db_db = lambda t, q, y: 2

droite_da_db = lambda t, q, y: 2*t


def MatriceJacobiennePremierOrdre(q, listet, listey):
    dK = 0; dT = 0
    for i, t in enumerate(listet):
        dK += premier_ordre_dK(t, q, listey[i])
        dT += premier_ordre_dT(t, q, listey[i])
    return np.array([[dK], [dT]])

def MatriceJacobiennePremierOrdreDerivee(q, listet, listey):
    dTdT = 0; dTdK = 0; dKdK = 0
    for i, t in enumerate(listet):
        y = listey[i]
        dTdT += premier_ordre_dT_dT(t, q, y)
        dTdK += premier_ordre_dK_dT(t, q, y)
        dKdK += premier_ordre_dK_dK(t, q, y)
    return np.array([[dKdK, dTdK], [dTdK, dTdT]])


def MatriceJacobienneSecondOrdre(q, listet, listey):
    dz = 0; dw = 0; dK = 0
    for i, t in enumerate(listet):
        y = listey[i]
        dK += second_ordre_dK(t, q, y)
        dw += second_ordre_dw(t, q, y)
        dz += second_ordre_dz(t, q, y)
    return np.array([[dK], [dz], [dw]])

def MatriceJacobienneSecondOrdreDerivee(q, listet, listey):
    dzdz = 0; dwdw = 0; dKdK = 0; dKdw = 0; dKdz = 0; dzdw = 0
    for i, t in enumerate(listet):
        y = listey[i]
        dKdK += second_ordre_dK_dK(t, q, y)
        dzdz += second_ordre_dz_dz(t, q, y)
        dwdw += second_ordre_dw_dw(t, q, y)
        dKdw += second_ordre_dK_dw(t, q, y)
        dKdz += second_ordre_dK_dz(t, q, y)
        dzdw += second_ordre_dz_dw(t, q, y)  
    return np.array([[dKdK, dKdz, dKdw], [dKdz, dzdz, dzdw], [dKdw, dzdw, dwdw]])

def MatriceJacobienneDroite(q, listet, listey):
    da = 0; db = 0
    for i, t in enumerate(listet):
        da += droite_da(t, q, listey[i])
        db += droite_db(t, q, listey[i])
    return np.array([[da], [db]])

def MatriceJacobienneDroiteDerivee(q, listet, listey):
    dada = 0; dbdb = 0; dadb = 0
    for i, t in enumerate(listet):
        y = listey[i]
        dada += droite_da_da(t, q, y)
        dbdb += droite_db_db(t, q, y)
        dadb += droite_da_db(t, q, y)
    return np.array([[dada, dadb], [dadb, dbdb]])


def ApproxParametresPremierOrdre(listet, listey):
    # Estimation du gain K en effectuant une moyenne
    moy = listey[-1]
    i = len(listey) - 1
    while abs(moy - listey[i])/moy < 0.03:
        i -= 1
        moy = moy*(i-1)/i + listey[i]/i
    K = moy
    # Mesure du temps de réponse à 63%
    while abs(K-listey[i])/K < 0.37:
        i -= 1
    tau = listet[i+1]
    
    return [K, tau]

def ApproxParametresSecondOrdre(listet, listey):

    # Estimation du gain K en effectuant une moyenne
    moy = listey[-1]
    i = len(listey) - 1
    while abs(moy - listey[i])/moy < 0.02:
        i -= 1
        moy = moy*(i-1)/i + listey[i]/i
    K = moy

    # Mesure du premier dépassement et calcul de ksi
    d1 = (max(listey)-K)/K
    z = math.sqrt((math.log(d1)**2)/(math.pi**2 + math.log(d1)**2))

    # Mesure de la période
    i1 = listey.index(max(listey))
    d2 = min(listey[i1::])
    i2 = listey.index(d2)
    T = 2*(listet[i2] - listet[i1])

    # En déduire la pulsation propre
    w = (2*math.pi)/(T*math.sqrt(1-z**2))*1.1

    
    return [K, z, w]



premier_ordre_latex_template = r"K(1 - e^{-\frac{t}{tau}})"
premier_ordre_py_template = "K*(1 - math.exp(-t/tau))"

second_ordre_latex_template = r"K(1 - e^{-z.w t}(cos(w t \sqrt{1 - z^2}) + (\frac{z}{\sqrt{1-z^2}} sin(w t \sqrt{1-z^2}))))"
second_ordre_py_template = "K*(1 - math.exp(-z*w*t)*(math.cos(w*t*math.sqrt(1 - z**2)) + (z/math.sqrt(1-z**2)*math.sin(w*t*math.sqrt(1-z**2)))))"

droite_latex_template = r"ax + b"
droite_py_template = "a*x + b"