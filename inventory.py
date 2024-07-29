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
    def __init__(self, nombre, costo, precio, cantidad) -> None:
        self.__nombre = nombre
        self.__costo = costo
        self.__precio = precio
        self.__cantidad = cantidad

    
    #Getters
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