for i in range (1,21): #Este ciclo for se detiene cuando recorre todos los elementos iterables (elementos no a uno)
    residuo = i%2
    if residuo == 0:
        print (f'{i} es par') 
    else:
        print (str(i) + 'es impar')

