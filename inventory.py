'''
Sistema de gestión de productos

Objetivo: Desarrollar un sistema para manejar productos en un inventario.

1. Crear una clase base Producto con atributos como nombre, precio, cantidad en stock, etc.
2. Definir al menos 2 clases derivadas para diferentes categorías de productos (por ejemplo, ProductoElectronico, ProductoAlimenticio) con atributos y métodos específicos.
3. Implementar operaciones CRUD para gestionar productos del inventario.
4. Manejar errores con bloques try-except para validar entradas y gestionar excepciones.
5. Persistir los datos en archivo JSON.
'''

class Producto():
    def __init__(self, codigo, nombre, costo, precio, cantidad) -> None:
        self.__codigo = codigo
        self.__nombre = nombre
        self.__costo = self.validar_costo(costo)
        self.__precio = self.validar_precio(precio)
        self.__cantidad = self.validar_cantidad(cantidad)

    #Getters
    @property
    def codigo(self):
        return self.__codigo

    @property
    def nombre(self):
        return self.__nombre.capitalize()
    
    @property
    def costo(self):
        return self.__costo
    
    @property
    def precio(self):
        return self.__precio
    
    @property
    def cantidad(self):
        return self.__cantidad
    
    #Setters
    @codigo.setter
    def codigo(self):
        pass

    @nombre.setter
    def nombre(self):
        '''
        No incluir nombres repetidos
        '''
        pass
    
    @costo.setter
    def costo(self, nuevo_costo):
        self.__costo = self.validad_costo(nuevo_costo)
    
    @precio.setter
    def precio(self, nuevo_precio):
        self.__precio = self.validad_precio(nuevo_precio)
    
    @cantidad.setter
    def cantidad(self, nueva_cantidad):
        self.__cantidad = self.validar_cantidad(nueva_cantidad)

    def validar_costo(self, costo):
        try:
            costo_num = float(costo)
            if costo_num <= 0:
                raise ValueError('El costo del producto no puede ser negativo o cero')
            return costo_num
        except ValueError:
            print('El costo debe ser numérico')

    def validar_precio(self, precio):
        try:
            precio_num = float(precio)
            if precio_num <= 0:
                raise ValueError('El precio del producto no puede ser negativo o cero')
            return precio_num
        except ValueError:
            print('El precio debe ser numérico')
        
    def validar_cantidad(self, cantidad):
        try:
            cantidad_num = int(cantidad)
            if cantidad < 0:
                raise ValueError('La cantidad no puede ser menor a 0')
            return cantidad_num
        except ValueError:
            print('La cantidad debe ser un número entero')
    
    def to_dict(self):
        '''
        método para devolver un dicc porque vamos a trasladarlo a JSON
        '''
        return {
            'codigo': self.codigo,
            'nombre': self.nombre,
            'costo': self.costo,
            'precio': self.precio,
            'cantidad': self.cantidad
        }

    def __str__(self) -> str:
        return f'{self.codigo} {self.nombre}'
    
class ProductoElectronico(Producto):
    def __init__(self, codigo, nombre, costo, precio, cantidad, categoria) -> None:
        super().__init__(codigo, nombre, costo, precio, cantidad)
        self.__categoria = categoria

    #Getters
    @property
    def categoria(self):
        return self.__categoria
    
    def to_dict(self):
        data = super().to_dict()
        data['categoria'] = self.categoria
        
        return data
    
    def __str__(self) -> str:
        return f'{super().__str__()} - categoria: {self.categoria}'
    
class ProductoAlimenticio(Producto):
    def __init__(self, codigo, nombre, costo, precio, cantidad, vencimiento) -> None:
        super().__init__(codigo, nombre, costo, precio, cantidad)
        self.__vencimiento = vencimiento

    #Getters
    @property
    def vencimiento(self):
        return self.__vencimiento
        
    def to_dict(self):
        data = super().to_dict()
        data['vencimiento'] = self.vencimiento
        
        return data
    
    def __str__(self) -> str:
        return f'{super().__str__()} - vencimiento: {self.vencimiento}' 
