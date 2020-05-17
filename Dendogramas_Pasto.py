#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pandas as Pandas
import seaborn as SeaBorn
import matplotlib.pyplot as PyPlot

year = '2016'
# In[9]:


cols_drop=['Departamento','Municipio','País de nacimiento','Profesión','Código DANE','Cantidad','Zona']
variablesNominales = ['Clase de sitio','Arma empleada','Móvil Agresor','Móvil Victima','Sexo','Estado civil','Clase de empleado','Escolaridad']
variablesNumericas = ['Fecha','Día','Hora','Edad']
def creardatasetPastoDesdeArchivo(nomArchivo,tipoDelito):
    hoja = Pandas.read_excel(nomArchivo)
    dataset = hoja[hoja['Municipio']=='PASTO (CT)']
    dataset = dataset.drop(columns=cols_drop)
    dataset['Delito'] = tipoDelito
    return dataset


# In[10]:


#vamos a combinar 4 archivos en principio
archivosYDelitos = { 'homicidio':"Datasets/"+year+"/homicidios-"+year+".xlsx",
                     'hurto persona':"Datasets/"+year+"/hurto-personas-"+year+".xlsx",
                     'hurto residencia':"Datasets/"+year+"/hurto-residencias-"+year+".xlsx",
                     'amenaza':"Datasets/"+year+"/amenazas-"+year+".xlsx",
                     'lesiones personales':"Datasets/"+year+"/lesiones-personales-"+year+".xlsx"}

datasets = []
for delito in archivosYDelitos.keys():
    data = creardatasetPastoDesdeArchivo(archivosYDelitos[delito],delito)
    datasets.append(data)
datasetPasto = Pandas.concat(datasets,sort=False)

	
#Debido al tamaño de los datos usaremos únicamente un sample de 100 muestras
datasetPasto = datasetPasto.sample(100)


# In[11]:


#creamos los barrios de pasto sin repetidos
Barrios_pastico = list(set(datasetPasto['Barrio'].tolist()))
#aislemos los tipos de delito
delitos = list(archivosYDelitos.keys())
#para una columna del dataset vamos a extraer sus valores como una lista
def extraerCategoriasVariableNominal(nomVariableNominal):
    return list(dict(datasetPasto[nomVariableNominal].value_counts()).keys())


# In[12]:


#vamos a hacer diccionario de categorias de variables
categoriasVariables = {}
for varNominal in variablesNominales:
    categoriasVariables[varNominal] = extraerCategoriasVariableNominal(varNominal)
categoriasVariables['Delito'] = extraerCategoriasVariableNominal('Delito')


# In[13]:


#vamos a hacer un procedimiento para que para una variable nos construya un dataset que
#para una variable en específico nos muestre cómo queda cada localidad con respecto a esas categorías
def subDataCategoriasVariable(nomVariable):
    infoDataFrame = []
    for barrio in Barrios_pastico:
        rowInfo = [barrio]
        subDataFrame = datasetPasto.loc[datasetPasto['Barrio'] == barrio]
        for categoria in categoriasVariables[nomVariable]:
            numObservaciones = subDataFrame.loc[subDataFrame[nomVariable]==categoria]
            rowInfo.append(len(numObservaciones))
        infoDataFrame.append(rowInfo)
    return Pandas.DataFrame(data=infoDataFrame,columns=['Barrio']+categoriasVariables[nomVariable])

#veamos la variable 'Estado civil'
dataframeEstadoCivil = subDataCategoriasVariable('Estado civil')
dataframeEstadoCivil


# In[14]:


from scipy.cluster.hierarchy import dendrogram,linkage


# In[19]:


#vamos a construir una matriz de distancias para este dataframe
def matrizDistanciaCategoriaVariable(nomVariable,nomCategoria):
    subData = subDataCategoriasVariable(nomVariable)
    matrizDist = []
    for esta_1 in Barrios_pastico:
        filaMatriz=[]
        val1 = subData[subData['Barrio'] == esta_1][nomCategoria].values[0]
        for esta_2 in Barrios_pastico:
            val2 = subData[subData['Barrio'] == esta_2][nomCategoria].values[0]
            filaMatriz.append(abs(val1-val2))
        matrizDist.append(filaMatriz)
    return matrizDist

def crearGraficoMatrizDeDistancia(nomVariable,categoria):
    matriz = matrizDistanciaCategoriaVariable(nomVariable,categoria)
    SeaBorn.heatmap(matriz,fmt='d',xticklabels=Barrios_pastico,yticklabels=Barrios_pastico,cbar=False,cmap="viridis")

def crearGraficosParaVariable(nomVariable):
    for categoria in categoriasVariables[nomVariable]:
        PyPlot.figure(figsize=(5,5))
        PyPlot.title(categoria)
        crearGraficoMatrizDeDistancia(nomVariable,categoria)
        PyPlot.savefig("Imagenes/"+year+"/"+categoria+".png")


# In[ ]:


#veamos cómo se ven algunos clusters
crearGraficosParaVariable('Estado civil')

# In[ ]:


def dendrogramaVariable(nomVariable,umbralDeDivision):
    infoVar = subDataCategoriasVariable(nomVariable)
    infoVar = infoVar.set_index('Barrio')
    labels = [ind for ind in infoVar.index]
    #create dendrograma
    PyPlot.figure(figsize=(10,10))
    dendrogram(linkage(infoVar,'ward'),labels=labels,
           leaf_rotation=0, orientation="left", 
           color_threshold=umbralDeDivision, 
           above_threshold_color='grey')
    PyPlot.savefig("Imagenes/"+year+"/"+nomVariable+"_den.png")

dendrogramaVariable('Sexo',1000)
dendrogramaVariable('Estado civil',1000)


# In[27]:


# def generarScatterPlotVariable(varDataFrame,cat1,cat2):
#     PyPlot.figure(figsize=(6,6))
#     SeaBorn.scatterplot(data=varDataFrame,x=cat1,y=cat2,hue='Barrio',cmap='viridis')
#     PyPlot.legend(bbox_to_anchor=(1.05,1),loc=2,borderaxespad=0.)
# categoriasEdoCivil = categoriasVariables['Estado civil']
# infoEstadoCivil = subDataCategoriasVariable('Estado civil')
# for cat1 in categoriasEdoCivil:
#     for cat2 in categoriasEdoCivil:
#         generarScatterPlotVariable(infoEstadoCivil,cat1,cat2)


# In[ ]:




