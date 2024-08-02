'''
Sistema de gestión de productos

Objetivo: Desarrollar un sistema para manejar productos en un inventario.

1. Crear una clase base Producto con atributos como nombre, precio, cantidad en stock, etc.
2. Definir al menos 2 clases derivadas para diferentes categorías de productos (por ejemplo, ProductoElectronico, ProductoAlimenticio) con atributos y métodos específicos.
3. Implementar operaciones CRUD para gestionar productos del inventario.
4. Manejar errores con bloques try-except para validar entradas y gestionar excepciones.
5. Persistir los datos en archivo JSON.
'''
# Librerías necesarias
import json


class Producto():
    def __init__(self, codigo, nombre, costo, precio, cantidad) -> None:
        self.__codigo = codigo
        self.__nombre = nombre
        self.__costo = self.validar_costo(costo)
        self.__precio = self.validar_precio(precio)
        self.__cantidad = self.validar_cantidad(cantidad)

    ##Getters
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
    
    ##Setters
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

    ##Getters
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

    ##Getters
    @property
    def vencimiento(self):
        return self.__vencimiento
        
    def to_dict(self):
        data = super().to_dict()
        data['vencimiento'] = self.vencimiento
        
        return data
    
    def __str__(self) -> str:
        return f'{super().__str__()} - vencimiento: {self.vencimiento}'

#Gestion
class GestionProductos():
    def __init__(self, archivo) -> None:
        self.archivo = archivo
    
    def leer_datos(self):
        '''
        Trae los datos del JSON
        '''
        try:
            with open(self.archivo, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            return {}
        except Exception as e:
            raise Exception(f'Error al leer datos del archivo: {e}')
        else:
            return data
        
    def guardar_datos(self, data):
        try:
            with open(self.archivo, 'w') as file:
                json.dump(data, file, indent=4)
        except IOError as e:
            print(f'Error al intentar guardar los datos en {self.archivo} - error: {e}')
        except Exception as e:
            print(f'Error inesperado: {e}')
    
    def crear_producto(self, producto):
        '''
        Este método va a recibir una instancia de Producto cuando llamemos desde main.py. Es decir, recibirá un input desde el usuario
        Dicha instancia será un producto electrónico o alimenticio
        Ese objeto con esos datos pasa a este método para crear el producto
        En resumen: el parámetro producto del método es a su vez una instancia de las subclases
        '''
        try:
            datos = self.leer_datos() ### Lee todo lo que contiene el JSON en ese momento
            codigo = producto.codigo ### Validacion con codigo
            if not str(codigo) in datos.keys(): ### Si no existe en datos, se crea
                datos[codigo] = producto.to_dict() ### Trae todos los campos de la instancia de la subclase
                self.guardar_datos(datos) ### Todos los datos junto con lo que agregamos ahora
                print(f'Guardado exitoso')
            else:
                print(f'{producto.codigo} ya existente')
        except Exception as e:
            print(f'Error inesperado al crear colaborador: {e}')
    
    def leer_producto(self, codigo):
        '''
        Método para buscar producto por código
        Lee los datos (del JSON) y busca una key con ese codigo
        Si la encuentra, crea una variable para guardar los datos 
        Evalua si está presente categoria, si es así, crea una 
        instancia de ProductoElectronico, de lo contrario es una instancia
        de ProductoAlimenticio
        '''
        data = self.leer_datos()
        if codigo in data:
            producto_data = data[codigo]
            if 'categoria' in producto_data:
                producto = ProductoElectronico(**producto_data) ##Desempaquetador (es un diccionario)
            else:
                producto = ProductoAlimenticio(**producto_data)
            print(f'Producto encontrado con codigo: {codigo}')
        else:
            print(f'Producto no encontrado con el código: {codigo}')

    def actualizar_producto(self, codigo, nuevo_costo, nuevo_precio, nueva_cantidad):
        '''
        Método para modificar los datos de los productos
        Si existe el codigo, accedemos a los datos 
        y los sobreescribimos para luego guardarlos.
        '''
        try:
            datos = self.leer_datos()
            if str(codigo) in datos.keys():
                datos[codigo]['costo'] = nuevo_costo
                datos[codigo]['precio'] = nuevo_precio
                datos[codigo]['cantidad'] = nueva_cantidad
                self.guardar_datos(datos)
                print(f'Datos actualizados correctamente para el producto {codigo}')
            else:
                print(f'No se encontró el producto {codigo}')
        except Exception as e:
            print(f'Error al actualizar el producto: {e}')

    def eliminar_producto(self, codigo):
        pass
