class Facade:
    pass

facade_1 = Facade()     #Se declaro un objeto
facade_1_type  = type(facade_1)
print(facade_1_type)

class Grade:
    minimun_passing=65

class Rules:
    def washing_brushes(self):
        return 'Prueba de funcionamiento'


class Circulo: #Sin constructor
    pi = 3.14
    def area(self, radio):
        return Circulo.pi * radio **2
    
circulo = Circulo()
area_pizza= circulo.area(12/2)
table_area = circulo.area(36/2)
room_area= circulo.area(11460/2) 
Area = circulo.area(6)
print(area_pizza)
print(table_area)
print(room_area)
print(Area)

print()

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


media_pizza= Circulo2(12)
teaching_table = Circulo2(36)
round_room=Circulo2(11460)
circulo2 = Circulo2(4)

print(f'El perimetro de la pizza es aproximadamente: {round(media_pizza.perimetro())}')
print(f'El perimetro de la tabla es aproximadamente: {round(teaching_table.perimetro())}')
print(f'El perimetro del round_room es aproximadamente: {round(round_room.perimetro())}')
print(f'El perimetro del circulo es aproximadamente: {round(circulo2.perimetro())}')
