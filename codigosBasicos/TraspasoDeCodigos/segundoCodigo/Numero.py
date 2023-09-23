import random
from matplotlib import pyplot as plt #Se instala una nueva libreria con el comando pip install matplotlib en el CMD

numeros1 = range(1, 13)
numeros2 = [random.randint(1,1000) for i in range(12)] #Se generara una lista de 12 numeros aleatorias el ciclo for me determina hasta el limite
plt.plot(numeros1,numeros2) #Genera una grafica en el que el eje x son los valores de la lista 1 y en y los valores de la lista 2
plt.show() # Muestra en una pestaña aparte la grafica generada previamente
