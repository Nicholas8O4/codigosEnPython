import time
inicio = time.time()

for i in range(1,32): #i toma los valores del rango
    contador = 0 #Un numero primo tiene modulo cero en dos ocaciones
    for n in range(1,i+1): #n toma los valores de i hasta uno posterio i+1
        residuo = i%n   #dividimos ii entre iV hasta aqui ii tiene un valor pero iv hira cambiando hasta terminar el rango
        if residuo == 0: #si aldidiri un numero entre todos los numeros del rango alguno tiene residuo cero entonce se le suma 1 al contador
            contador = contador +1
    if contador == 2:  #Si el contador es 2 significa que el numero tiene unicamente dos divisires 
        #print(str(i) + "Es un primo")
        print (f'{i} es un primo')
        print("\n")

fin = time.time()
print("t = ", (fin - inicio)*1000)