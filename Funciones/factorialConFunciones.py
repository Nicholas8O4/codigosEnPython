
def FuncionFactorial (a):
    while True:
        fact = 1
        
        for i in range (1, a+1):
            fact = fact*i
        return fact

def IngresarNumero ():
    numero = int (input("Ingrese el numero para calcular su factorial: "))
    b = isinstance(numero, int) 

    while b==False or numero<0:
        numero = int(input("Reingrese el numero: "))

    print( f"El factorial de {numero} es {FuncionFactorial (numero)}")



IngresarNumero()

