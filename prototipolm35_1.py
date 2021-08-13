import serial,time
import pandas as pd
import csv

from sklearn.svm import SVC
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold
from matplotlib.colors import ListedColormap
import math

ard = serial.Serial('COM4',baudrate= 9600, timeout = 1)


train = pd.read_csv('nuevo_calibrado.csv',header=0)

SVM = SVC(kernel = 'rbf',C=0.5)
X_train = train.loc[:,train.columns != 'calibrado']
Y_train = train.calibrado
SVM.fit(X_train,Y_train)

datos = open("datos_evaluar.csv",'w')
datos.write("celsius,calibrado")

print("Temperatura(°C)")
i=0
while i <= 3:
    data = ard.readline().decode('ascii').rstrip()
    datos.write(data+"\n")
    print(data)
    time.sleep(1)
    i=i+1

ard.close()
time.sleep(0.2)
print ("Puerto cerrado")
datos.close()
time.sleep(1)

test = pd.read_csv('datos_evaluar.csv',header=0)
X_test = test[['celsius']]

pred = SVM.predict(X_test)

print("prediccion: ",pred)
print("Evaluacion de datos:" )

print("--------------------------")

pred1 = list(pred)



print("Datos calibrados: ",pred1.count(1))
print("Datos descalibrados: ",pred1.count(0))
print("--------------------------")

if(pred1.count(0)/len(pred1)*100 > 20 ):
    print("Existe un "+str(round(pred1.count(0)/len(pred1)*100),2)+
          "% de datos descalibrados")
    print("SE RECOMIENDA CAMBIAR DE SENSOR")
elif(pred1.count(1)/len(pred1)*100 == 100):
    print("FUNCIONAMIENTO DEL SENSOR OPTIMO")

else:
    print("Datos descalibrados estan por debajo del 20%")
    print("SENSOR EN BUENAS CONDICIONS")
    
    

