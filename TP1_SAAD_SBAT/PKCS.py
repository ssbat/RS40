from random import *
def prefix(k,mi):
    i=len(mi)#i c'est la taille du message
    x=""
    for j in range(k-i-3):#generation de k-j-3 nombre aleatoire non nul
       x+=str(randint(255,263)%255+1)
    return str(0x00)+str(0x02)+x+str(0x00)+mi #00‖02‖x‖00‖m

def blocks(message,k=10):#k repésente la taille du bloc
    nbchar=(k//2)-1 #taille du message<(taille du bloc)/2
    taille=len(message)
    d=taille//nbchar #nombre des blocks de messages complets
    r=taille-d*nbchar #nb des octets qui construient pas un blocs de message complets
    liste=[]
    c=0
    j=0
    block=""
    while c<len(message):#découpage du message
        if(j<nbchar):
            block+=message[c]
            j+=1
            c+=1
        if j==nbchar :
            liste.append(block)
            block=""
            j=0
    if r!=0:
        liste.append(block)
    for l in range(len(liste)):
        liste[l]=prefix(k,liste[l])#concatenation de 00‖02‖x‖00 avec Mi
    return liste


#Elimination de 00‖02‖𝑥‖00 de chaque bloc pour obtenir 𝑚𝑖
def concat(liste):
    string=""
    for i in range(len(liste)):
        bloc=liste[i]
        j=1
        while bloc[j]!='0':
            j+=1
        string+=bloc[j+1:]
    return string

    
# liste_blocks=blocks("aaaaaaaaaaa",10)
# print("Liste_blocks:",liste_blocks,end="\n")
# print("Elimination de 00‖02‖x‖00:",concat(liste_blocks))

