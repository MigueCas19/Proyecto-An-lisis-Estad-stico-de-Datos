#!/usr/bin/env python
# coding: utf-8

# In[14]:


import pandas as Pandas
import matplotlib.pyplot as PyPlot
import seaborn as SeaBorn
import random


# In[133]:


dataset1 = Pandas.read_csv(r'dataset2.csv',sep=';',names=['x','y','clase'])
dataset_train = dataset1.sample(50)
dataset_train


# In[134]:


clasesDict=dict(dataset_train['clase'].value_counts())
clasesDict


# In[135]:


SeaBorn.scatterplot(data=dataset_train,x='x',y='y',hue='clase')


# In[136]:


#vamos a iniciar los centroides con un punto aleatoriamente por clase
centroides ={}
for clase in clasesDict.keys():
    puntoDataSet = dataset_train.loc[dataset_train['clase']==clase].sample(1)
    x = puntoDataSet.iloc[0]['x']
    y = puntoDataSet.iloc[0]['y']
    centroides[clase] = [x,y]
print(centroides)


# In[125]:


#ahora vamos a asignar el cluster usando una función de distancia para cada punto, 
#podemos escoger entre varias funciones
def distanciaEuclidea(p1,p2):
    return (p1[0]-p2[0])**2+(p1[1]-p2[1])**2
def distanciaSupremo(p1,p2):
    return max(abs(p1[0]-p2[0]),abs(p1[1]-p2[1]))


# In[126]:


def claseMasCercana(p,centrosDict,funcionDistancia):
    claseMasApropiada = -1
    distancia = 1000000000
    for clase in centrosDict.keys():
        if funcionDistancia(p,centrosDict[clase]) < distancia:
            claseMasApropiada = clase
            distancia = funcionDistancia(p,centrosDict[clase])
    return claseMasApropiada


# In[139]:


#ahora, la invariante del algoritmo es mientras que la variación de los centroides sea alta
parar ={}
numEncontrados ={}
for clase in centroides.keys():
    parar[clase] = False
    numEncontrados[clase] = 1
def pararAlgoritmo():
    pararTodo = True
    for clase in parar.keys():
        pararTodo = pararTodo and parar[clase]
    return pararTodo

indexPunto = 0
tolerancia = 0.001
while indexPunto < len(dataset_train) and pararAlgoritmo()==False:
    x = dataset_train.iloc[indexPunto]['x']
    y = dataset_train.iloc[indexPunto]['y']
    claseCercana = claseMasCercana([x,y],centroides,distanciaEuclidea)
    if claseCercana != -1:
        nuevoCentroide = [(x+centroides[claseCercana][0])/numEncontrados[claseCercana],                          (y+centroides[claseCercana][1])/numEncontrados[claseCercana]]
        parar[claseCercana] = distanciaEuclidea(centroides[claseCercana],nuevoCentroide)<tolerancia
        centroides[claseCercana] = nuevoCentroide
        numEncontrados[claseCercana] += 1
    indexPunto += 1
print("iteraciones para converger:",indexPunto)


# In[140]:


#ahora vamos a probar nuestros centroides encontrados con un sample de prueba
dataset_test = dataset1.sample(200)
dataset_test
correctos = 0
for index, fila in dataset_test.iterrows():
    x = fila['x']
    y = fila['y']
    claseOriginal = fila['clase']
    claseEncontrada = claseMasCercana([x,y],centroides,distanciaEuclidea)
    if claseOriginal == claseEncontrada:
        correctos +=1

print("correctos:",correctos)


# In[ ]:





# In[ ]:




