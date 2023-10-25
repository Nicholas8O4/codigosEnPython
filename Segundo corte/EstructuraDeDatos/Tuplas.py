miLista = ['Rojo','Azul','Amarillo','Naranja', 'Verde']
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
