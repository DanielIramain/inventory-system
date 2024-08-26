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

import mysql.connector
from mysql.connector import Error
from decouple import config

# Clase base
class Producto():
    def __init__(self, codigo, nombre, costo, precio, cantidad) -> None:
        self.__codigo = self.validar_codigo(codigo)
        self.__nombre = self.validar_nombre(nombre)
        self.__costo = self.validar_costo(costo)
        self.__precio = self.validar_precio(precio)
        self.__cantidad = self.validar_cantidad(cantidad)

    ##Getters
    @property
    def codigo(self):
        return self.__codigo

    @property
    def nombre(self):
        return self.__nombre
    
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
    def codigo(self, nuevo_codigo):
        self.__codigo = self.validar_codigo(nuevo_codigo)

    @nombre.setter
    def nombre(self, nuevo_nombre):
        self.__nombre = self.validar_nombre(nuevo_nombre)

    @costo.setter
    def costo(self, nuevo_costo):
        self.__costo = self.validar_costo(nuevo_costo)
    
    @precio.setter
    def precio(self, nuevo_precio):
        self.__precio = self.validar_precio(nuevo_precio)
    
    @cantidad.setter
    def cantidad(self, nueva_cantidad):
        self.__cantidad = self.validar_cantidad(nueva_cantidad)

    def validar_codigo(self, codigo):
        try: 
            nuevo_codigo = int(codigo)
                        
            return nuevo_codigo
        except ValueError:
            print('El código debe ser un número entero')
            input('Presione enter para volver a intentarlo...')
            
            return nuevo_codigo
    
    def validar_nombre(self, nombre):
        try:
            nuevo_nombre = str(nombre)
            if nuevo_nombre == '':
                raise ValueError('El nombre no puede estar vacío')
            
            return nuevo_nombre
        except ValueError:
            print('El nombre debe ser alfanumerico')

            return nuevo_nombre

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

# Clases derivadas
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

# Clase de gestion
class GestionProductos():
    def __init__(self) -> None:
        self.host = config('DB_HOST')
        self.name = config('DB_NAME')
        self.user = config('DB_USER')
        self.password = config('DB_PASS')
        self.port = config('DB_PORT')

    def connect(self):
        '''
        Establece la conexión con la BBDD
        '''
        try:
            connection = mysql.connector.connect(
                host = self.host,
                database = self.name,
                user = self.user,
                password = self.password,
                port = self.port
            )

            if connection.is_connected:
                return connection
        except Error as e:
            print(f'Error al conectarse a la base de datos: {e}')
            return None
###
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
###    
    def crear_producto(self, producto):
        '''
        Este método va a recibir una instancia de Producto cuando llamemos desde main.py. Es decir, recibirá un input del usuario
        Dicha instancia será un producto electrónico o alimenticio
        Ese objeto con esos datos pasa a este método para crear el producto en la BBDD
        (El parámetro producto del método es a su vez una instancia de las subclases)
        '''
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    ### Verificamos si existe el codigo
                    cursor.execute('SELECT codigo FROM producto WHERE codigo = %s ', (producto.codigo,))
                    
                    if cursor.fetchone():
                        print('Ya existe un producto con ese código')
                        return
                    
                    ### Insertar producto
                    query = '''
                    INSERT INTO producto (codigo, nombre, costo, precio, cantidad) 
                    VALUES (%s, %s, %s, %s, %s)
                    '''
                    cursor.execute(query, (producto.codigo, producto.nombre, producto.costo, producto.precio, producto.cantidad))

                    ### Luego insertar producto por tipo
                    if isinstance(producto, ProductoElectronico):
                        query = '''
                        INSERT INTO productoelectronico (codigo, categoria)
                        VALUES (%s, %s)
                        '''
                    
                        cursor.execute(query, (producto.codigo, producto.categoria))
                    
                    elif isinstance(producto, ProductoAlimenticio):
                        query = '''
                        INSERT INTO productoalimenticio(codigo, vencimiento)
                        VALUES (%s, %s)
                        '''

                        cursor.execute(query, (producto.codigo, producto.vencimiento))
                    
                    ### Guardar cambios
                    connection.commit()
                    print(f'Producto {producto.nombre} creado exitosamente')
        except Exception as e:
            print(f'Error inesperado al crear producto: {e}')
    
    def leer_producto(self, codigo):
        '''
        Buscar producto por código
        '''
        try:
            connection = self.connect()
            if connection:
                with connection.cursor(dictionary=True) as cursor: ### Con ese parametro en True devuelve las consultas en dicc.
                    cursor.execute('SELECT * FROM producto WHERE codigo = %s', (codigo,))
                    datos_producto = cursor.fetchone()
                
                    if datos_producto:
                        cursor.execute('SELECT categoria FROM productoelectronico WHERE codigo = %s', (codigo,))
                        categoria = cursor.fetchone()

                        if categoria: ### Si es un producto de tipo electronico
                            datos_producto['categoria'] = categoria['categoria'] ### Asigna el valor de categoria obtenido en fetch a una nueva key (categoria) en el dicc de datos_productos
                            producto = ProductoElectronico(**datos_producto)
                        else: ### No es de tipo electronico si no alimenticio (no tiene categoría)
                            cursor.execute('SELECT vencimiento FROM productoalimenticio WHERE codigo = %s', (codigo,))
                            vencimiento = cursor.fetchone()
                            if vencimiento:
                                datos_producto['vencimiento'] = vencimiento['vencimiento']
                                producto = ProductoAlimenticio(**datos_producto)
                            else: ### Caso (hipotetico) donde no es electronico ni alimenticio
                                producto = Producto(**datos_producto)

                        print(f'Producto encontrado: {producto.nombre}')

                    else:
                        print(f'No se encontró ningún producto con el código ingresado')
        except Error as e:
            print(f'Error al leer producto: {e}')
        finally:
            if connection.is_connected():
                connection.close()

    def actualizar_producto(self, codigo, nuevo_costo, nuevo_precio, nueva_cantidad):
        '''
        Modificar los datos de los productos en la BBDD
        '''
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    ## Verificar si existe el código
                    cursor.execute('SELECT * FROM producto WHERE codigo = %s', (codigo,))
                    if not cursor.fetchone():
                        print(f'Producto de código {codigo} inexistente')
                        return
                    
                    ## Actualizar los datos si existe el código
                    query = '''
                    UPDATE producto SET costo = %s, precio = %s, cantidad = %s WHERE codigo = %s
                    '''
                    cursor.execute(query ,(nuevo_costo, nuevo_precio, nueva_cantidad, codigo))

                    if cursor.rowcount > 0:
                        connection.commit()
                        print('Los datos se guardaron correctamente')
                    else:
                        print(f'No se encontró producto de código {codigo}')
        except Error as e:
            print(f'Error al actualizar el producto: {e}')
        finally:
            if connection.is_connected():
                connection.close()

    def eliminar_producto(self, codigo):
        '''
        Busca un producto por código
        y lo elimina de la BBDD
        '''
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                   # Verificar si el producto con el dni ingresado existe
                    cursor.execute('SELECT * FROM producto WHERE codigo = %s', (codigo,))
                    if not cursor.fetchone():
                        print(f'No se encontro producto con codigo {codigo}')
                        return 

                    # Eliminar el producto
                    cursor.execute('DELETE FROM productoelectronico WHERE codigo = %s', (codigo,))
                    cursor.execute('DELETE FROM productoalimenticio WHERE codigo = %s', (codigo,))
                    cursor.execute('DELETE FROM producto WHERE codigo = %s', (codigo,))
                    if cursor.rowcount > 0:
                        connection.commit()
                        print(f'Producto de codigo: {codigo} eliminado correctamente')
                    else:
                        print(f'No se encontró producto con codigo: {codigo}')
        except Exception as e:
            print(f'Error al eliminar el producto: {e}')
        finally:
            if connection.is_connected():
                connection.close()

    def leer_todos_los_productos(self):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute('SELECT * FROM producto')
                    productos_data = cursor.fetchall()

                    productos = []
                    
                    for producto_data in productos_data:
                        codigo = producto_data['codigo']

                        cursor.execute('SELECT categoria FROM productoelectronico WHERE codigo = %s', (codigo,))
                        categoria = cursor.fetchone()

                        if categoria:
                            producto_data['categoria'] = categoria['categoria']
                            producto = ProductoElectronico(**producto_data)
                        else:
                            cursor.execute('SELECT vencimiento FROM productoalimenticio WHERE codigo = %s', (codigo,))
                            vencimiento = cursor.fetchone()
                            producto_data['vencimiento'] = vencimiento['vencimiento']
                            producto = ProductoAlimenticio(**producto_data)

                        productos.append(producto)

        except Exception as e:
            print(f'Error al mostrar todos los productos: {e}')
        else:
            return productos
        finally:
            if connection.is_connected():
                connection.close()
