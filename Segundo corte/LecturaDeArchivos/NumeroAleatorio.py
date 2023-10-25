import random
import csv

# Especifica el nombre del archivo CSV en el que deseas escribir los números
nombre_archivo_csv = 'numeros.csv'

while True:
    # Genera un número pseudoaleatorio en el rango (0, 1)
    numero_pseudoaleatorio = random.uniform(0, 1)

    # Abre el archivo CSV en modo de escritura y agrega el número generado
    with open(nombre_archivo_csv, 'a', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerow([numero_pseudoaleatorio])

    print(f'Se ha añadido el número {numero_pseudoaleatorio} al archivo {nombre_archivo_csv}.')
