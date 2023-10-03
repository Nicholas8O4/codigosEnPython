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

