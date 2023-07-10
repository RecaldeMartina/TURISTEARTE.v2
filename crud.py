import os
import sqlite3
from flask import Flask, jsonify, request
from PIL import Image

# Configurar la conexión a la base de datos SQLite
DATABASE = 'inventario.db'

def get_db_connection():
    print("Obteniendo conexión...") # Para probar que se ejecuta la función
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Crear la tabla 'destinos' si no existe
def create_table():
    print("Creando tabla destinos...") # Para probar que se ejecuta la función
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS destinos (
            codigo INTEGER PRIMARY KEY,
            descripcion TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            imagen BLOB 
        ) ''')
    conn.commit()
    cursor.close()
    conn.close()

# Verificar si la base de datos existe, si no, crearla y crear la tabla
def create_database():
    print("Creando la BD...") # Para probar que se ejecuta la función
    conn = sqlite3.connect(DATABASE)
    conn.close()
    create_table()

# # Programa principal
# # Crear la base de datos y la tabla si no existen
# create_database()


class Destino:
    # Definimos el constructor e inicializamos los atributos de instancia
    def __init__(self, codigo, descripcion, cantidad, precio, imagen):
        self.codigo = codigo           # Código 
        self.descripcion = descripcion # Descripción
        self.cantidad = cantidad       # Cantidad de pasajes disponibles
        self.precio = precio           # Precio 
        self.imagen = Image.open(imagen)

    # Este método permite modificar un destino.
    def modificar(self, nueva_cantidad, nuevo_precio):
        self.cantidad = nueva_cantidad        # Modifica la cantidad
        self.precio = nuevo_precio            # Modifica el precio

imagenCataratas = 'destinos/cataratas.jpg'
imagenBariloche = 'destinos/bariloche.jpg'
imagenCordoba = 'destinos/cordoba.jpg'

# # Programa principal
# cataratas = Destino(1, 'Cataratas del Iguazu', 10, 7500, imagenCataratas)
# # Accedemos a los atributos del objeto
# print(f'{cataratas.codigo} | {cataratas.descripcion} | {cataratas.cantidad} | ${cataratas.precio} | {cataratas.imagen}')
# # Modificar los datos del objeto
# cataratas.modificar(20, 9800) 
# print(f'{cataratas.codigo} | {cataratas.descripcion} | {cataratas.cantidad} | ${cataratas.precio} | {cataratas.imagen}')

# bariloche = Destino(2, 'Bariloche', 15, 45000, imagenBariloche)
# print(f'{bariloche.codigo} | {bariloche.descripcion} | {bariloche.cantidad} | ${bariloche.precio} | {bariloche.imagen}')

# bariloche.modificar(20, 50000)
# print(f'{bariloche.codigo} | {bariloche.descripcion} | {bariloche.cantidad} | ${bariloche.precio} | {bariloche.imagen}')

# cordoba = Destino(3, 'Cordoba', 7, 5000, imagenCordoba)
# print(f'{cordoba.codigo} | {cordoba.descripcion} | {cordoba.cantidad} | ${cordoba.precio} | {cordoba.imagen}')

# cordoba.modificar(10, 5500)
# print(f'{cordoba.codigo} | {cordoba.descripcion} | {cordoba.cantidad} | ${cordoba.precio} | {cordoba.imagen}')

class Inventario:
    # Definimos el constructor e inicializamos los atributos de instancia
    def __init__(self):
        self.conexion = get_db_connection()
        self.cursor = self.conexion.cursor() 
         # Lista de destinos en el inventario (variable de clase)

    # Este método permite crear objetos de la clase "destino" y agregarlos al inventario.
    def agregar_destino(self, codigo, descripcion, cantidad, precio, imagen):
        destino_existente = self.consultar_destino(codigo)
        if destino_existente:
            print("Ya existe un Destino con ese código.")
            return False
        #nuevo_destino = Destino(codigo, descripcion, cantidad, precio, imagen)
        sql = f'INSERT INTO destinos VALUES ({codigo}, "{descripcion}", {cantidad}, {precio}, "{imagen}");'
        self.cursor.execute(sql)
        self.conexion.commit()
        return True
        # Agrega un nuevo destino a la lista

    # Este método permite consultar datos de destinos que están en el inventario
    # Devuelve el destino correspondiente al código proporcionado o False si no existe.
    def consultar_destino(self, codigo):
        sql = f'SELECT * FROM destinos WHERE codigo = {codigo};'
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        if row:
            codigo, descripcion, cantidad, precio, imagen = row
            return Destino(codigo, descripcion, cantidad, precio, imagen)
        return False
    
    # Este método permite modificar datos de destinos que están en el inventario
    # Utiliza el método consultar_destino del inventario y modificar del destino.
    def modificar_destino(self, codigo, nueva_cantidad, nuevo_precio):
        destino = self.consultar_destino(codigo)
        if destino:
            destino.modificar(nueva_cantidad, nuevo_precio)
            sql = f'UPDATE destinos SET cantidad = {nueva_cantidad}, precio = {nuevo_precio} WHERE codigo = {codigo};' 
            self.cursor.execute(sql)
            self.conexion.commit()

    # Este método elimina el destino indicado por codigo de la lista mantenida en el inventario.
    def eliminar_destino(self, codigo):
        sql = f'DELETE FROM destinos WHERE codigo = {codigo};' 
        self.cursor.execute(sql)
        if self.cursor.rowcount > 0:
            print(f'Destino {codigo} eliminado.')
            self.conexion.commit()
        else:
            print(f'Destino {codigo} no encontrado.')

    # Este método imprime en la terminal una lista con los datos de los destinos que figuran en el inventario.
    def listar_destinos(self):
        print("-"*50)
        print("Lista de destinos en el inventario:")
        print("Código\tDescripción\tCant\tPrecio")
        self.cursor.execute("SELECT * FROM destinos")
        rows = self.cursor.fetchall()
        for row in rows:
            codigo, descripcion, cantidad, precio, imagen = row
            print(f'{codigo}\t{descripcion}\t{cantidad}\t{precio}\t{imagen}')
        print("-"*50)



# # Programa principal
# # Crear una instancia de la clase Inventario
# mi_inventario = Inventario() 

# # Agregar Destinos 
# mi_inventario.agregar_destino(1, 'Cataratas del Iguazu', 10, 7500, imagenCataratas)
# mi_inventario.agregar_destino(2, 'Bariloche', 15, 45000, imagenBariloche)
# mi_inventario.agregar_destino(3, 'Cordoba', 7, 5000, imagenCordoba)


# # Consultar un destino 
# destino = mi_inventario.consultar_destino(3)
# if destino != False:
#     print(f'Destino encontrado:\nCódigo: {destino.codigo}\nDescripción: {destino.descripcion}\nCantidad Pasajes: {destino.cantidad}\nPrecio: {destino.precio}\n{destino.imagen}')  
# else:
#     print("Destino no encontrado.")

# # Modificar un destino 
# mi_inventario.modificar_destino(3, 10, 5500)

# # Listar todos los Destinos
# mi_inventario.listar_destinos()

# # Eliminar un destino 
# mi_inventario.eliminar_destino(2)

# # Confirmamos que haya sido eliminado
# mi_inventario.listar_destinos()

class Carrito:
    # Definimos el constructor e inicializamos los atributos de instancia
    def __init__(self):
        self.conexion = sqlite3.connect('inventario.db')  # Conexión a la BD
        self.cursor = self.conexion.cursor()
        self.items = []
      # Lista de items en el carrito (variable de clase)

    # Este método permite agregar destinos del inventario al carrito.
    def agregar(self, codigo, cantidad, inventario):
        # Nos aseguramos que el destino esté en el inventario
        destino = inventario.consultar_destino(codigo)
        if destino is False: 
            print("El destino no existe.")
            return False

        # Verificamos que la cantidad en stock sea suficiente
        if destino.cantidad < cantidad:
            print("Cantidad en stock insuficiente.")
            return False

        # Si existe y hay stock, vemos si ya existe en el carrito.
        for item in self.items:
            if item.codigo == codigo:
                item.cantidad += cantidad
                # Actualizamos la cantidad en el inventario
                sql = f'UPDATE destinos SET cantidad = cantidad - {cantidad}  WHERE codigo = {codigo};'
                self.cursor.execute(sql)
                self.conexion.commit()
                return True
       
        def agregar_imagen (descripcion):
            if descripcion == 'Cataratas del Iguazu':
                return imagenCataratas
            if descripcion == 'Bariloche':
                return imagenBariloche
            if descripcion == 'Cordoba':
                return imagenCordoba
            
        # Si no existe en el carrito, lo agregamos como un nuevo item.
        nuevo_item = Destino(codigo, destino.descripcion, cantidad, destino.precio, imagen = agregar_imagen(destino.descripcion))
        self.items.append(nuevo_item)
        # Actualizamos la cantidad en el inventario
        sql = f'UPDATE destinos SET cantidad = cantidad - {cantidad}  WHERE codigo = {codigo};'
        self.cursor.execute(sql)
        self.conexion.commit()
        return True

        
    # Este método quita unidades de un elemento del carrito, o lo elimina.
    def quitar(self, codigo, cantidad, inventario):
        for item in self.items:
            if item.codigo == codigo:
                if cantidad > item.cantidad:
                    print("Cantidad a quitar mayor a la cantidad en el carrito.")
                    return False
                item.cantidad -= cantidad
                if item.cantidad == 0:
                    self.items.remove(item)
                # Actualizamos la cantidad en el inventario
                sql = f'UPDATE destinos SET cantidad = cantidad + {cantidad} WHERE codigo = {codigo};'
                self.cursor.execute(sql)
                self.conexion.commit()
                return True
        # Si el bucle finaliza sin novedad, es que ese destino NO ESTA en el carrito.
        print("El destino no se encuentra en el carrito.")
        return False

    def mostrar(self):
        print("-"*50)
        print("Lista de Destinos en el carrito:")
        print("Código\tDescripción\t\tCant\tPrecio")
        for item in self.items:
            print(f'{item.codigo}\t{item.descripcion}\t{item.cantidad}\t{item.precio}\t{item.imagen}')
        print("-"*50)

# Programa principal

# ---------------------------------------------------------------------
# Crear la base de datos y la tabla si no existen
create_database()

# Crear una instancia de la clase Inventario
mi_inventario = Inventario()

# # Crear una instancia de la clase Carrito
# mi_carrito = Carrito()

# # Crear 3 Destinos y agregarlos al inventario
# mi_inventario.agregar_destino(1, 'Cataratas del Iguazu', 10, 7500, imagenCataratas)
# mi_inventario.agregar_destino(2, 'Bariloche', 15, 45000, imagenBariloche)
# mi_inventario.agregar_destino(3, 'Cordoba', 7, 5000, imagenCordoba)

# # Listar todos los Destinos del inventario
# mi_inventario.listar_destinos()

# # Agregar 2 Destinos al carrito
# mi_carrito.agregar(1, 2, mi_inventario) # Agregar 2 unidades del Destino con código 1 al carrito
# mi_carrito.agregar(3, 4, mi_inventario) # Agregar 1 unidad del Destino con código 3 al carrito
# mi_carrito.quitar (1, 1, mi_inventario) # Quitar 1 unidad del Destino con código 1 al carrito
# # Listar todos los Destinos del carrito
# mi_carrito.mostrar()
# # Quitar 1 Destino al carrito
# mi_carrito.quitar (1, 1, mi_inventario) # Quitar 1 unidad del Destino con código 1 al carrito
# # Listar todos los Destinos del carrito
# mi_carrito.mostrar()
# # Mostramos el inventario
# mi_inventario.listar_destinos()

# Agregar productos al inventario
mi_inventario.agregar_destino(1, 'Cataratas del Iguazu', 10, 7500, imagenCataratas)
mi_inventario.agregar_destino(2, 'Bariloche', 15, 45000, imagenBariloche)
mi_inventario.agregar_destino(3, 'Cordoba', 7, 5000, imagenCordoba)

# Consultar algún producto del inventario
print(mi_inventario.consultar_destino(3)) #Existe, se muestra la dirección de memoria
print(mi_inventario.consultar_destino(4)) #No existe, se muestra False

# Listar los productos del inventario
mi_inventario.listar_destinos()

# Modificar un destino 
mi_inventario.modificar_destino(3, 10, 5500)

# Listar todos los Destinos
mi_inventario.listar_destinos()

# Eliminar un destino 
mi_inventario.eliminar_destino(2)

# Confirmamos que haya sido eliminado
mi_inventario.listar_destinos()

# Crear una instancia de la clase Carrito
mi_carrito = Carrito()

# Crear 2 Destinos y agregarlos al inventario
mi_carrito.agregar(1, 2, mi_inventario)
mi_carrito.agregar(3, 7, mi_inventario)

# Listar todos los Destinos del inventario
mi_carrito.mostrar()
mi_inventario.listar_destinos()

# Quitar 1 unidad del producto con código 1 al carrito y 1 unidad del producto con código 2 al carrito
mi_carrito.quitar(1, 1, mi_inventario)
mi_carrito.quitar(3, 1, mi_inventario)

# Mostrar el contenido del carrito y del inventario
mi_carrito.mostrar()
mi_inventario.listar_destinos()



