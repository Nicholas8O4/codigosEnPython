a = 1
valor = int(input('Ingrese un valor: '))

while a==1:
    for i in range(1, valor+1):
        contador = 0
        for n in range(1,i+1):
            residuo = i%n
            if residuo == 0:
                contador = contador + 1
    if contador == 2: 
        print(f'{i} es un primo')
        print("\n")
    else:
        print(f'{i} no es un primo')
        print("\n")

    print('¿Quieres continuar?. Presiona 1 en tal caso: ')
    a = int(input())

    if a != 1:
        break

    valor = int(input('Ingrese un valor: '))