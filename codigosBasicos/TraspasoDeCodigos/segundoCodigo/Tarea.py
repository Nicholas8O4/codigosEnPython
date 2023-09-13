#Ingresamos los vlaores de dos numeros y enseguida los definimos como enteros
a = input("Ingrese el numero a: ")
a = int(a)
b = input("Ingrese el numero b: ")
b = float(b)
c = a+b

if a == b:
    print("Iguales")
else:
    print("Diferentes")

print("El tipo de dato que es a es: ", type(a))
print("El tipo de dato que es b es: ", type(b))
print("c = ", c)

if type(a) == type(b):
    print("a y b son del mismo tipo")
else: 
    print("a y b son de diferente tipo")