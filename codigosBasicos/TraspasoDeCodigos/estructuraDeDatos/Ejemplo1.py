miLista = ['Rojo','Azul','Amarillo','Naranja', 'Verde']

print(miLista)
print(type(miLista))
print(miLista[0:3]) #Lista o rango de numeros

print("Tamaño de la lista", len(miLista))
print(miLista[0:2])
print(miLista[:2])

#agrega al final directamente
miLista.append('Blanco')
print(miLista)

#agrega los elementos de otro vector a el mismo
miLista.extend(['Cafe', 'Rosado'])
print(miLista)

#Busca el elemento cafe y lo elimina
miLista.remove('Cafe')
print(miLista)

#Agrega un elemento en una posicion especifica de la lista
miLista.insert(5 , 'Cafe')
print(miLista)

#Nos devuelve un elemnto aleatorio de la lista
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
