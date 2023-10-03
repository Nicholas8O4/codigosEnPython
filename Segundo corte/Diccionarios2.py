diccionario = { "Nombre": 'Victor', "Apellido" : 'Zaun'}.get("Apodo") #Solo nos devuelve o mostrora lo que el get este identificando
print(diccionario)

diccionario2 = { 1:'Hola', 'two' : True, '3':[1,2,3], 'Four': ['fun', 'ask']}

#Podemos actulizar los datos de un diccionario con otro diccionario si conciden dos palabras clave se intercabiara pero si no se agregara un nuevo espacio
diccionario3 = {'Color': 'Morado', 'forma': ' Circulo'}
print(diccionario3)
diccionario4 = {'Color': 'Rosado', 'numero': 3}
print(diccionario4)
diccionario3.update(diccionario4)
print(diccionario3)

#podemos obtner las palbras clave y lo valores de las palbaras clave de un diccionario
print(diccionario3.keys())
print(diccionario3.values())

diccionario3.items()