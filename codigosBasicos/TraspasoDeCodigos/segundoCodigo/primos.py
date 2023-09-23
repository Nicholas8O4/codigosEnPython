import time
inicio = time.time()

for i in range(0,31):
    contador = 0 #Cada que inicia este ciclo este contador vuelve a cero
    for n in range(1, i+1):
        residuo = i%n
        if residuo == 0:
            contador = contador + 1
    if contador == 2: #Si el conador es dos significa que ya se dividieron 1 y el numero por lo que efectivamente el numero es primo
        print (f'{i} es primo')

fin = time.time() 
print("t = ", (fin - inicio)*1000)