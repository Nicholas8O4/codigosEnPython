controlador = True

while True:
    valor = int(input("Introduzca un numero entero positivo: "))
    print ("Valor: ", valor)
    a = isinstance(valor, int) #si valor es tipo entero a se vuelve True
    if a == True and valor > 0:
        fact = 1
        for i in range (1, valor + 1):
            fact = fact*i
        print(f'El factorial de {valor} es: ', fact) #Podemos combinar texto con valores progresivos del codigo
    else:
        print("Porfavor, ingrese un numero entero positivo")