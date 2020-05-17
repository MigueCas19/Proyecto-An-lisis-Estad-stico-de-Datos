import pandas as Pandas

confusion = {'verdaderos':{'correcto':225,'fraudulento':151},'falsos':{'correcto':239,'fraudulento':178}}

matrizConfusion = Pandas.DataFrame(confusion)
exactitud = float(matrizConfusion['verdaderos'].sum())/float(matrizConfusion.values.sum())
recordacion = float(matrizConfusion['verdaderos']['correcto'])/float(matrizConfusion['verdaderos']['correcto']+matrizConfusion['falsos']['correcto'])
precision = float(matrizConfusion['verdaderos']['correcto'])/float(matrizConfusion['verdaderos'].sum())
FScore = 2*recordacion*precision/(precision+recordacion)                      
print("exactitud: ","%{:,.2f}".format(100*exactitud))
print("recordación: ","%{:,.2f}".format(100*recordacion))
print("precision: ","%{:,.2f}".format(100*precision))
print("F-Score: ","{:,.2f}".format(FScore))
print("Matriz de confusión")
print(matrizConfusion)