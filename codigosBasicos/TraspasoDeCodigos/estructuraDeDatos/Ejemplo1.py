miLista = ['Rojo','Azul','Amarillo','Naranja', 'Verde']

print(miLista)
print(type(miLista))
print(miLista[0:3]) #Lista o rango de numeros

print("Tamaño de la lista", len(miLista))
print(miLista[0:2])
print(miLista[:2])

miLista.append('Blanco')
print(miLista)

miLista.extend(['Cafe', 'Rosado'])
print(miLista)

miLista.remove('Cafe')
print(miLista)

miLista.insert(8 , 'Cafe')
print(miLista)

print("Elemento: ", miLista.pop())
size = len(miLista)
print("tamaño = ", size)
#print(miLista.pop(size))

miLista3 = miLista*3
print(miLista3)


print("Sort:")
print()
listaOrdenada = sorted(miLista)
print(listaOrdenada)

NumList = [10, 9, 8, 7, 6 , 5 , 4, 3, 2, 1]
print("Odenando la lista de menor a mayor: ")
NumList.sort()
print(NumList)

print("Odenando la lista de menor a mayor: ")
NumList.sort(reverse = True)
print(NumList)


print()
print("Tuplas")

Tupla = tuple(miLista)
print()
print("mi tupla", Tupla)

#Evaluar si un elemento está contenido en la tupla (Devuelve un valor booleano)
print("Rojo" in Tupla)
print(Tupla.count('Rojo'))

TuplaUnitaria = ('Blanco')
print(TuplaUnitaria)

Tupla = 'pepe',5,5,2023
print(Tupla)

#Desempaquetado de tupla, se guardan los valores en orden de las variables
nombre, dia, mes, año = Tupla
print(nombre)
print(dia)
print(mes)
print(año)

print("Nombre: ", nombre, " - Dia:", dia, " - Mes: ", mes, "- Año: ", año)


#Convertir una tupla en una lista
Lista2=list(Tupla)
print(Lista2)