# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 13:44:40 2020

@author: Mr ABBAS-TURKI
"""

import hashlib
import binascii
from PKCS import *

def decimalToBinary(n):
    return bin(n).replace("0b", "")
def home_mod_exponent(x,y,n): #exponentiation modulaire
    exposant_binaire=decimalToBinary(y)#je transforme le puissance en binaire
    r1=1
    r2=x
    while (len(exposant_binaire)>=1):
        if(exposant_binaire[-1]=='1'):#si le bit=1
            r1=(r1*r2)%n #update r1
        r2=(r2*r2)%n   # update r2
        exposant_binaire=exposant_binaire[0:-1] #je supprime le bit déja traité pour lire le bit suivant
    return r1 #je retourne r1
            
def privateKey(e,phi):
    return home_ext_euclide(phi,e)
   
def CRT(x1,x2,d,c):
    p,q=None,None
    if x1<x2:
        p,q=x1,x2
    else:
        p,q=x2,x1
    inv_q=home_ext_euclide(q,p)
    dq=d%(q-1)
    dp=d%(p-1)

    mq=home_mod_exponent(c,dq,q)
    mp=home_mod_exponent(c,dp,p)
    h=((mp-mq)*inv_q)%p
    m=(mq+h*q)%(x1*x2)
    return m

def home_ext_euclide(p,a):#inverse modulaire

    r1, r2 = a, p
    u1, u2 = 1, 0 #  uk
    v1, v2 = 0, 1 #  vk

    while r2 != 0:#quand le  dernier reste est 0 on arrête et on recupére le reste avant le dernier
        q = r1 // r2                # quotient         
        r1, r2 = r2, r1 - q * r2    # update r1 et r2
        u1, u2 = u2, u1 - q * u2    # update uk
        v1, v2 = v2, v1 - q * v2    # update vk

    if r1 == 1:                     # dernier reste avant que r=0
        return u1 % p
    else:
        return None

def home_pgcd(a,b): #recherche du pgcd
    if(b==0): 
        return a 
    else: 
        return home_pgcd(b,a%b)

def home_string_to_int(x): # pour transformer un string en int
    z=0
    for i in reversed(range(len(x))):
        z=int(ord(x[i]))*pow(2,(8*i))+z
    return(z)


def home_int_to_string(x): # pour transformer un int en string
    txt=''
    res1=x
    while res1>0:
        res=res1%(pow(2,8))
        res1=(res1-res)//(pow(2,8))
        txt=txt+chr(res)
    return txt

def mot10char(): #entrer le secret
    secret=input("donner un secret:")
    return(secret)

#voici les éléments de la clé d'Alice
x1a=637105457357217098121389895254439055566760698458516304611849 #p>>0
x2a=329518769797631194077806654294870961679098194587355930457539 #q>>0
na=x1a*x2a  #n
phia=((x1a-1)*(x2a-1))//home_pgcd(x1a-1,x2a-1)
ea=17 #exposant public
da=privateKey(ea,phia) #exposant privé

#voici les éléments de la clé de bob
x1b=987993420748147643369555129513253856353449121349142485798937 #p
x2b=848770671698055769948925708891126544705856067332145614461047 #q
nb=x1b*x2b # n
phib=((x1b-1)*(x2b-1))//home_pgcd(x1b-1,x2b-1)
eb=65573 # exposants public
db=privateKey(eb,phib) #exposant privé

print("Vous êtes Bob, vous souhaitez envoyer un secret à Alice")
print("voici votre clé publique que tout le monde a le droit de consulter")
print("n =",nb)
print("exposant :",eb)
print("voici votre précieux secret")
print("db =",db)
print("da =",da)

print("*******************************************************************")
print("Voici aussi la clé publique d'Alice que tout le monde peut conslter")
print("n =",na)
print("exposent :",ea)
print("*******************************************************************")
print("il est temps de lui envoyer votre secret ")
print("*******************************************************************")
x=input("appuyer sur entrer ")

secret=mot10char()
taille=10#choisir la taille du bloc
liste_blocks=blocks(secret,taille)#decomposition du message en blocs
print("*******************************************************************")
print("Liste des blocks avant le chiffrage:\n")
print(liste_blocks)
print("*******************************************************************")


print("*******************************************************************")
print("voici la listes des blocs de messages chiffrés avec la publique d'Alice : ")
liste_chif=[home_mod_exponent(home_string_to_int(block),ea,na) for block in liste_blocks]
print(liste_chif)
print("*******************************************************************")


print("*******************************************************************")
print("On utilise la fonction de hashage sha256 pour obtenir le hash du message",secret)
print(secret)
Bhachis0=hashlib.sha256(secret.encode(encoding='UTF-8',errors='strict')).digest() #SH256 du message
print("voici le hash en nombre décimal ")
Bhachis1=binascii.b2a_uu(Bhachis0)
Bhachis2=Bhachis1.decode() #en string
Bhachis3=home_string_to_int(Bhachis2)
print(Bhachis3)#le hash du message secret en decimale
print("voici la signature avec la clé privée de Bob du hachis")
signe=home_mod_exponent(Bhachis3, db, nb)#signature(chiffre par la cle prive de bob)
print("sigature:\n",signe)
print("*******************************************************************")
print("Bob envoie \n \t 1-la liste des blocks chiffrés avec la clé public d'Alice \n",liste_chif,"\n")
print("*******************************************************************")

x=input("appuyer sur entrer")

print("*******************************************************************")
print("Alice déchiffre le liste des message chiffré \n",liste_chif,"\nce qui donne ")
liste_dechif=[]
for dechiffrement in liste_chif:
    liste_dechif.append(home_int_to_string(CRT(x1a,x2a,da,dechiffrement)))
print(liste_dechif)
print("Puis elle elimine les 00‖02‖x‖00 pour obtenir les mi et concaténer l'ensemble de 𝑚𝑖 pour constituer le message initial.\n")
dechif=concat(liste_dechif)
print("resultat de la contenation:",dechif)
print("*******************************************************************")

print("\nAlice déchiffre la signature de Bob \n",signe,"\n ce qui donne  en décimal")
designe=home_mod_exponent(signe, eb, nb)#j'obtient le hashage du message car j'ai dechifré la signature
print(designe)
print("Alice vérifie si elle obtient la même chose avec le hash de ",dechif)
Ahachis0=hashlib.sha256(dechif.encode(encoding='UTF-8',errors='strict')).digest()
Ahachis1=binascii.b2a_uu(Ahachis0)
Ahachis2=Ahachis1.decode()
Ahachis3=home_string_to_int(Ahachis2)
print(Ahachis3)
print("La différence =",Ahachis3-int(designe))
if (Ahachis3-int(designe)==0):
    print("Alice : Bob m'a envoyé : ",dechif)
else:
    print("oups")