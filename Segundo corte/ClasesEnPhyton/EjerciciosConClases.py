class Circulo2:
    pi = 3.141516
    
    def __init__(self, diametro2):
        print('Nuevo cálculo de círculo: {d}'.format(d=diametro2))
        self.radio = diametro2 / 2 #Creacion dinamica de atributo

    def perimetro(self):
        return 2 * self.pi * self.radio

    def area(self):
        return self.pi * (self.radio**2)


pepe1 = Circulo2(4)
perimetro = pepe1.perimetro()
area = pepe1.area()
print(f'El perimetro del circulo es: {perimetro} y su area es igual a: {area}')

print()
print()


class Cuadrado:

    def __init__(self, lado):
        self.lado = lado
        print('Se ha creado un nuevo cudrado de lado: {l}'.format(l=lado))

    def area(self):
        return self.lado**2
    
    def perimetro(self):
        return self.lado*4
    

cuadrado1 = Cuadrado(3)
print(f'El perimetro del cuadrado es: {cuadrado1.perimetro()} y su area es igual a: {cuadrado1.area()}')

print()
print()

class Rectangulo:
    def __init__(self, altura, largo):
        self.altura = altura
        self.largo = largo
        print('Se ha creado un nuevo rectangulo de largo: {l}'.format(l=largo), 'Y de altura: {a}'.format(a=altura))

    def area(self):
        return self.altura*self.largo
    
    def perimetro(self):
        return (self.altura*2)+(self.largo*2)
    

rectangulo1 = Rectangulo(2,2)
print(f'El perimetro del rectangulo es: {rectangulo1.perimetro()} y su area es igual a: {rectangulo1.area()}')

print()
print()

from math import sqrt

class TrianguloRectangulo:
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura
        self.hipotenusa = sqrt(self.base**2 + self.altura**2)
        print(f'Se ha creado un nuevo triángulo rectángulo de base: {self.base}, altura: {self.altura}, y hipotenusa: {self.hipotenusa}')

    def area(self): # Fórmula de Herón
        s = (self.base + self.altura + self.hipotenusa) / 2
        return sqrt(s * (s - self.base) * (s - self.altura) * (s - self.hipotenusa))

    def perimetro(self):
        return self.base + self.altura + self.hipotenusa

triangulo1 = TrianguloRectangulo(5, 2)
print(f'El perímetro del triángulo es: {triangulo1.perimetro()} y su área es igual a: {triangulo1.area()}')
