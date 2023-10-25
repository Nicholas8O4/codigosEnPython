#Como Leer un archivos en phyton
#Se debieron de haber creado con anterioridad los archivos.txt para poder realizar la apertura del mismo
with open("Welcom.txt") as text_file:
    text_data= text_file.read()
#Leer mediante lineas
with open ("how_many_lines.text") as line_doc:
    for line in line_doc.readlines():
        print(line)
#Escribir dentro de un archivo txt ya exitente
with open("bad_hands.txt","w") as bad_hands_doc:
    bad_hands_doc.write("Air buddy")

with open("cool_dogs.txt") as cool_dogs_file:
    cool_dogs_file.write("Perro de la cuadra")

with open("fun_file.txt") as file1:
    setup= file1.readline()
    punchline= file1.readline()
    print(setup)
    print(punchline)
    print(file1.readline())
