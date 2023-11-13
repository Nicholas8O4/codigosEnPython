sensors =  {"living room": 21, "kitchen": 23, "bedroom": 20, "pantry": 22} #Son palbaras clabe, que se le asigna a cada uno un valor ditintivo
num_cameras = {"backyard": 6,  "garage": 2, "driveway": 1}

print(sensors)

translations = {"mountain":	"orod", "bread":	"bass", "friend":	"mellon", "horse":	"roch" } #Los distintivos (valores) no necesariamente deben ser numeros 
print(translations)
#powers = {[1, 2, 4, 8, 16]: 2, [1, 3, 9, 27, 81]: 3}

subtotal_to_total = {20: 24, 10: 12, 5: 6, 15: 18}
print(subtotal_to_total)


students_in_classes = {"software design": ["Aaron", "Delila", "Samson"], "cartography": ["Christopher", "Juan", "Marco"], "philosophy": ["Frederica", "Manuel"], "Fisica" :["Maxwell", "Einstein"]}    #Los distintivos (valores) puedes ser lisan pero las palabras clabe no
print(students_in_classes)

#Cambia los elementos de la plabra clabe por los selccionados
students_in_classes["Fisica"]=["Pepe", "Papa"]
print(students_in_classes)
#Agrega un elemento al final de lal diccionario
students_in_classes["Filosofia"]=["Nietchz", "Rudolf"]
print(students_in_classes)

#Podemos combinar los distintivos (Valores) entre numeros o cadenas de caracteres 
students_in_classes = {"software design": ["Aaron", "Delila", "Samson"], "cartography": ["Christopher", "Juan", "Marco"], "philosophy": ["Frederica", "Manuel"], "Fisica" : 2}    #Los distintivos (valores) puedes ser lisan pero las palabras clabe no
print(students_in_classes)

Diccionario ={}
print(Diccionario)
Diccionario = {"Vaca" : 1, "Perro":2}
Diccionario["Gato"] = 3
print(Diccionario)
#Elimina un elemento en particular del diccionario
del Diccionario["Vaca"]
print(Diccionario)

#actualizacion de datos , esto nos permite cambiar varios datos de un diccionarios al tiempo enves de realizar el cambia de un solo valor al momento
user_ids = {"teraCoder": 9018293, "proProgrammer": 119238}
print(user_ids)
user_ids.update({"theLooper": 138475, "stringQueen": 85739})
print(user_ids)


oscar_winners = {"Best Picture": "La La Land", "Best Actor": "Casey Affleck", "Best Actress": "Emma Stone", "Animated Feature": "Zootopia"}
print(oscar_winners)
oscar_winners.update({"Supporting Actress": "Viola Davis", "Animated Feature": "Pinocho"})
oscar_winners["Best Picture"] = "Moonlight"
print(oscar_winners)

print()

#creacion de un diccionario
bebidas = ["Agua","Gaseosa", "Malteadas", "Cafe"]
Azucares = [0,50,40,20]
zipbebidas = zip(bebidas,Azucares)

bebidasYazucares = {key:value for key, value in zipbebidas}
print(bebidasYazucares)
print()
print()


# Listas de nombres y alturas en pulgadas
nombres = ['Jenny', 'Alexus', 'Sam', 'Grace']
alturas = [61, 70, 67, 64]

# Se crea un diccionario que relaciona nombres con alturas usando comprensión de diccionarios
estudiantes = {llave: valor for llave, valor in zip(nombres, alturas)}
# estudiantes es ahora {'Jenny': 61, 'Alexus': 70, 'Sam': 67, 'Grace': 64}

# Listas de bebidas y contenido de cafeína
bebidas = ["espresso", "chai", "decaf", "drip"]
contenido_cafeina = [64, 40, 0, 120]

# Se utiliza zip() para combinar las listas en un iterador de tuplas con elementos de las listas emparejados
bebidas_a_contenido = {llave: valor for llave, valor in zip(bebidas, contenido_cafeina)}

# Listas de canciones y número de reproducciones
canciones = ["Like a Rolling Stone", "Satisfaction", "Imagine", "What's Going On", "Respect", "Good Vibrations"]
repeticiones = [78, 29, 44, 21, 89, 5]

print()

# Se crea un diccionario que relaciona canciones con el número de reproducciones
reproducciones = {llave: valor for llave, valor in zip(canciones, repeticiones)}
print(reproducciones)  # Muestra el diccionario de canciones y reproducciones

print()

# Se actualizan las reproducciones de dos canciones existentes y se añade una nueva
reproducciones.update({"Purple Haze": 1})
reproducciones.update({"Respect": 94})
print("Después: ", reproducciones)  # Muestra el diccionario actualizado de reproducciones

print()

# Se crea un diccionario llamado 'biblioteca' que contiene los diccionarios de reproducciones y otro vacío
biblioteca = {"Las Mejores Canciones": reproducciones, "Sentimientos de Domingo": {}}
print(biblioteca)  # Muestra el contenido de la biblioteca
