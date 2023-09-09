import time
inicio = time.time()

def identificacacion(C1,C2):
    variable = []
    for i in range(C1,C2+1): #i toma los numeros
        contador = 0
        for n in range(1, i+1): #Es una cota abierta por lo que no incluye los extremos por eso se le suma 1 para aunmentar la cota 
            residue = i%n #Necesitamos el modulo de dividir cada numero por el mismo y por 1 y debe de cumplirse 
            if residue == 0:
                contador = contador + 1
                
        if contador == 2:
            #Elementos.append(i)
            variable.append(i)
            #print(f'{i} es un primo')
    return variable



Lim_inferior = int(input(print("Ingrese el primer numero del rango: ")))
Lim_sup = int(input(print("Ingrese el segundo numero del rango: ")))
numeros = identificacacion(Lim_inferior,Lim_sup)
print(numeros)
