import time

cadena = 'Python'

for letra in cadena: #como cadena es una cadena de caracteres podemos iterar entre cada eslabon 
    if letra == 't': #Si uno de los eslabones de la cadena es igual a t enotnces el codigo continura sin hacer nada
        continue
    print(letra) #Las demas letras si se imprimiran
    time.sleep(1) 