class Facade:
    pass

facade_1 = Facade()     #Se declaro un objeto
facade_1_type  = type(facade_1)
print(facade_1_type)


class Circulo: #Sin constructor
    pi = 3.14
    def area(self, radio):
        return Circulo.pi * radio **2
    
circulo = Circulo()
Area = circulo.area(6)
print(Area)

class Circulo1:
    pi = 3.141516
    def __init__(self, diametro): #Constructor de la clase
        print('Nuevo circulo con diametro: {}'.format(diametro))
    def area(self, radio):
        return Circulo.pi * radio **2
    
circle1= Circulo1(2)
print(circle1.area(1))

class Circulo2:
    pi = 3.141516
    
    def __init__(self, diametro2):
        print('Nuevo cálculo de círculo: {d}'.format(d=diametro2))
        self.radio = diametro2 / 2 #Creacion dinamica de atributo

    def perimetro(self):
        return 2 * self.pi * self.radio

circulo2 = Circulo2(4)
perimetro = circulo2.perimetro()
print(f'El perimetro del circulo es: {perimetro}')