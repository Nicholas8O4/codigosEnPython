from shutil import copyfile


Ruta = 'E:\Proyectos\LecturaDeArchivos\Archivo.txt' #Ubacion o ruta en la se encuentra el archivo requerido
archivo = open(Ruta, 'r') #almacenanos los datos del archivo declarando que solo vamos a leer el archivo con 'r'

print(archivo.read()) #Utilizamos el metodo read() para imprimir todos los datos del archivo
archivo.seek(0) #Debido a que la lectura que hace python de los archivos es siguiendo un "cursor" debemos de indicarle
                #que regrese el cursor a la primera posicion del archivo para pueda leer nuevamente los datos desde esa posicion.
print(archivo.readline()) #podemos hacer la lectura de una sola linea 
print(archivo.readline()) #Si ejecutamos la misma sentencia dos veces cambiamos de renglon o linea
archivo.seek(0)
print(archivo.readlines()) #Presentamos los datos del archivo en forma de una lista
archivo.close() #Cerramos el archivo

print()

Contenido = "java, C++, C, C#, PHP, JAVASCRIPT"
RutaDeUbicacion = 'E:\Proyectos\LecturaDeArchivos\ArchivoGenerado.txt'  # Usa doble barra invertida para rutas de Windows
Datos = open(RutaDeUbicacion, 'r+')  # Generamos una variable(objeto) que se encargará de leer y escribir los datos que queramos en un archivo
Datos.write(Contenido)
Datos.seek(0)
print(Datos.read())
Datos.seek(0)

for lines in Datos.readlines(): 
    print(lines)

Datos.close()  # No te olvides de cerrar el archivo después de trabajar con él

print()

#con la libreria shutil podemos realizar copias de difretes archivos
copyfile('E:\Proyectos\LecturaDeArchivos\ArchivoGenerado.txt','E:\Proyectos\LecturaDeArchivos\ArchivoGenerado2.txt' )
