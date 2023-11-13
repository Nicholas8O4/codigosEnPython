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

# Obtener una clave
# Puedes acceder a los valores en un diccionario proporcionando la clave:

alturas_edificios = {"Burj Khalifa": 828, "Torre de Shanghai": 632, "Abraj Al Bait": 601, "Ping An": 599, "Lotte World Tower": 554.5, "One World Trade": 541.3}
print(alturas_edificios["Burj Khalifa"]) # Imprime 828
print(alturas_edificios["Ping An"]) # Imprime 599

elementos_zodiaco = {"agua": ["Cáncer", "Escorpio", "Piscis"], "fuego": ["Aries", "Leo", "Sagitario"], "tierra": ["Tauro", "Virgo", "Capricornio"], "aire": ["Géminis", "Libra", "Acuario"]}
print(elementos_zodiaco["tierra"])
print(elementos_zodiaco["fuego"])

# Obtener una clave inválida

alturas_edificios = {"Burj Khalifa": 828, "Torre de Shanghai": 632, "Abraj Al Bait": 601, "Ping An": 599, "Lotte World Tower": 554.5, "One World Trade": 541.3}
#print(alturas_edificios["Landmark 81"]) #Genera error al obtener un valo invalido

# Una forma de evitar este error es verificar primero si la clave existe en el diccionario:
clave_a_verificar = "Landmark 81"  

if clave_a_verificar in alturas_edificios:
    print(alturas_edificios["Landmark 81"])

elementos_zodiaco = {"agua": ["Cáncer", "Escorpio", "Piscis"], "fuego": ["Aries", "Leo", "Sagitario"], "tierra": ["Tauro", "Virgo", "Capricornio"], "aire": ["Géminis", "Libra", "Acuario"]}

elementos_zodiaco["energía"] = "No es un elemento del zodiaco"

if "energía" in elementos_zodiaco:
    print(elementos_zodiaco["energía"])

# Obtener una clave de manera segura

alturas_edificios = {"Burj Khalifa": 828, "Torre de Shanghai": 632, "Abraj Al Bait": 601, "Ping An": 599, "Lotte World Tower": 554.5, "One World Trade": 541.3}

# Esta línea devolverá 632:
alturas_edificios.get("Torre de Shanghai")

# Esta línea devolverá None:
alturas_edificios.get("Mi Casa")

identificadores_usuario = {"teraCoder": 100019, "pythonGuy": 182921, "samTheJavaMaam": 123112, "lyleLoop": 102931, "keysmithKeith": 129384}
identificadores_usuario.get("teraCoder")

if identificadores_usuario.get("teraCoder") == None:
    tc_id = 1000
else:
    tc_id = identificadores_usuario.get("teraCoder")

print(tc_id)

if identificadores_usuario.get("superStackSmash") == None:
    stack_id = 100000

print(stack_id)

# Eliminar una clave
# .pop() funciona para eliminar elementos de un diccionario cuando se conoce el valor de la clave.
sorteo = {223842: "Osito de Peluche", 872921: "Entradas para Concierto", 320291: "Canasta de Regalo", 412123: "Collar", 298787: "Hacedor de Pasta"}
print(sorteo.pop(320291, "Sin Premio")) # Imprime "Canasta de Regalo"
print(sorteo) # Imprime {223842: "Osito de Peluche", 872921: "Entradas para Concierto", 412123: "Collar", 298787: "Hacedor de Pasta"}
print(sorteo.pop(100000, "Sin Premio")) # Imprime "Sin Premio"
print(sorteo) # Imprime {223842: "Osito de Peluche", 872921: "Entradas para Concierto", 412123: "Collar", 298787: "Hacedor de Pasta"}
print(sorteo.pop(872921, "Sin Premio")) # Imprime "Entradas para Concierto"
print(sorteo) # Imprime {223842: "Osito de Peluche", 412123: "Collar", 298787: "Hacedor de Pasta"}

items_disponibles = {"poción de salud": 10, "pastel de la cura": 5, "elixir verde": 20, "sándwich de fuerza": 25, "granos de resistencia": 15, "guiso de poder": 30}
puntos_salud = 20

puntos_salud += items_disponibles.pop("granos de resistencia", 0)
puntos_salud += items_disponibles.pop("guiso de poder", 0)
puntos_salud += items_disponibles.pop("pan místico", 0)

print(items_disponibles)
print(puntos_salud)

# Obtener todas las claves
puntuaciones_prueba = {"Grace": [80, 72, 90], "Jeffrey": [88, 68, 81], "Sylvia": [80, 82, 84], "Pedro": [98, 96, 95], "Martin": [78, 80, 78], "Dina": [64, 60, 75]}
print(list(puntuaciones_prueba)) # Imprime ["Grace", "Jeffrey", "Sylvia", "Pedro", "Martin", "Dina"]

for estudiante in puntuaciones_prueba.keys():
    print(estudiante)

identificadores_usuario = {"teraCoder": 100019, "pythonGuy": 182921, "samTheJavaMaam": 123112, "lyleLoop": 102931, "keysmithKeith": 129384}
num_ejercicios = {"funciones": 10, "sintaxis": 13, "flujo de control": 15, "bucles": 22, "listas": 19, "clases": 18, "diccionarios": 18}

usuarios = identificadores_usuario.keys()
lecciones = num_ejercicios.keys()

print(usuarios)
print(lecciones)

# Obtener todos los valores
puntuaciones_prueba = {"Grace": [80, 72, 90], "Jeffrey": [88, 68, 81], "Sylvia": [80, 82, 84], "Pedro": [98, 96, 95], "Martin": [78, 80, 78], "Dina": [64, 60, 75]}

for lista_puntuaciones in puntuaciones_prueba.values():
    print(lista_puntuaciones)

num_ejercicios = {"funciones": 10, "sintaxis": 13, "flujo de control": 15, "bucles": 22, "listas": 19, "clases": 18, "diccionarios": 18}

total_ejercicios = 0

for ejercicios in num_ejercicios.values():
    total_ejercicios += ejercicios
print(total_ejercicios)

# Obtener todos los elementos
grandes_marcas = {"Apple": 184, "Google": 141.7, "Microsoft": 80, "Coca-Cola": 69.7, "Amazon": 64.8}

for empresa, valor in grandes_marcas.items():
    print(empresa + " tiene un valor de " + str(valor) + " mil millones de dólares.")

porcentaje_mujeres_en_ocupacion = {"CEO": 28, "Gerente de Ingeniería": 9, "Farmacéutico": 58, "Médico": 40, "Abogado": 37, "Ingeniero Aeroespacial": 9}

for ocupacion, porcentaje in porcentaje_mujeres_en_ocupacion.items():
    print("Las mujeres representan el " + str(porcentaje) + " por ciento de los " + ocupacion + ".")
