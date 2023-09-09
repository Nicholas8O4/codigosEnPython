def suma (a,b):
    return a+b #No es los mismo imprimir que retornar

A = int(input("Ingrese el primer valor: "))
B = int(input('Ingrese el segundo valor: '))
resultado = suma(A,B)
print(resultado)

def multiplicacion(x,y):
    return x*y

X = int(input("Ingrese el primer factor: "))
Y = int(input("Ingrese el segundo factor: "))
producto = multiplicacion(X,Y)
print(producto)
print(type(producto))

#Para los codigos de primos y factorial estrucurarlo con funciones