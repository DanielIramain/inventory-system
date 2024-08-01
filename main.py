#Imports
from inventory import (
    ProductoElectronico,
    ProductoAlimenticio,
    GestionProductos
)

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
    Recibe una instancia de colaborador 
    (necesitamos los datos del colaborador)
    '''
    try:
        codigo = int(input('Ingrese el codigo: '))
        nombre = input('Ingrese el nombre: ')
        costo = float(input('Ingrese el costo: '))
        precio = float(input('Ingrese edad: '))
        cantidad = int(input('Ingrese salario: '))

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