#Imports
import os
import platform

from inventory import (
    ProductoElectronico,
    ProductoAlimenticio,
    GestionProductos
)

def limpiar_pantalla():
    '''
    Limpiar la pantalla según OS
    '''
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def mostrar_menu():
    print('Menu de gestion de inventario')
    print('1. Crear producto electronico')
    print('2. Crear producto alimenticio')
    print('3. Buscar producto')
    print('4. Actualizar producto')
    print('5. Eliminar producto')
    print('6. Mostrar todos los productos')
    print('7. Salir')

def agregar_producto(gestion: GestionProductos, tipo_producto):
    '''
    Recibe una instancia de producto
    y los datos del producto
    '''
    try:
        codigo = input('Ingrese el codigo: ')
        nombre = input('Ingrese el nombre: ')
        costo = float(input('Ingrese el costo: '))
        precio = float(input('Ingrese el precio: '))
        cantidad = int(input('Ingrese la cantidad: '))

        if tipo_producto == '1':
            categoria = input('Ingrese categoria: ')
            producto = ProductoElectronico(codigo, nombre, costo, 
                                                precio, cantidad, categoria)
        elif tipo_producto == '2':
            vencimiento = input('Ingrese vencimiento: ')
            producto = ProductoAlimenticio(codigo, nombre, costo, 
                                                precio, cantidad, vencimiento)
        else:
            print('Opción inválida')
            return


        # Instancia
        gestion.crear_producto(producto)
        input('Presione enter para continuar...') #Por limpiado de pantalla 

    except ValueError as e:
        print(f'Error: {e}')
    except Exception as e:
        print(f'Error inesperado: {e}')
    
def buscar_producto_por_codigo(gestion: GestionProductos):
    codigo = input('Ingrese el codigo del producto a buscar: ')
    producto = gestion.leer_producto(codigo)
    if isinstance(producto, ProductoElectronico):
        print(producto)
    elif isinstance(producto, ProductoAlimenticio):
        print(producto)
    else:
        print(f'No se encontró producto con el código {codigo}')
    input('Presione una tecla para continuar...')

def actualizar_producto_por_codigo(gestion: GestionProductos):
    codigo = input('Ingrese el código del producto a actualizar: ')
    costo = float(input('Ingrese el nuevo costo del producto: '))
    precio = float(input('Ingrese el nuevo precio del producto: '))
    cantidad = int(input('Ingrese la nueva cantidad del producto: '))
    gestion.actualizar_producto(codigo, costo, precio, cantidad)
    input('Presione una tecla para continuar...')

def eliminar_producto_por_codigo(gestion: GestionProductos):
    codigo = input('Ingrese el codigo del producto a eliminar: ')
    gestion.eliminar_producto(codigo)
    input('Presione una tecla para continuar...')

def mostrar_todos_los_productos(gestion: GestionProductos):
    print('=== Listado completo de productos ===')
    
    try:
        productos = gestion.leer_todos_los_productos()
        for producto in productos:
            if isinstance(producto, ProductoElectronico):
                print(f'{producto.codigo} {producto.nombre} {producto.precio}')
            elif isinstance(producto, ProductoAlimenticio):
                print(f'{producto.codigo} {producto.nombre} {producto.precio}')
    except Exception as e:
        print(f'Error al mostrar todos los productos {e}')
        
    print('=== /// === /// ===')
    input('Presione una tecla para continuar')

if __name__ == '__main__':
    gestion_productos = GestionProductos() ### Instancia de la clase que implementa el CRUD

    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input('Seleccione una opción: ')

        if opcion == '1' or opcion == '2':
            agregar_producto(gestion_productos, opcion)
        if opcion == '3':
            buscar_producto_por_codigo(gestion_productos)
        if opcion == '4':
            actualizar_producto_por_codigo(gestion_productos)
        if opcion == '5':
            eliminar_producto_por_codigo(gestion_productos)
        if opcion == '6':
            mostrar_todos_los_productos(gestion_productos)
        if opcion == '7':
            print('Saliendo del programa...')
            break
        else:
            print('Opcion no válida. Seleccione una opción válida (1-7)')