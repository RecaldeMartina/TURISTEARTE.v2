import os
import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS
from PIL import Image

# Configurar la conexión a la base de datos SQLite
DATABASE = 'inventario.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Crear la tabla 'destinos' si no existe
def create_table():
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
    conn = sqlite3.connect(DATABASE)
    conn.close()
    create_table()

# Programa principal
# Crear la base de datos y la tabla si no existen
create_database()

class Destino:
    # Definimos el constructor e inicializamos los atributos de instancia
    def __init__(self, codigo, descripcion, cantidad, precio, imagen):
        self.codigo = codigo           # Código 
        self.descripcion = descripcion # Descripción
        self.cantidad = cantidad       # Cantidad de pasajes disponibles
        self.precio = precio           # Precio 
        self.imagen = Image.open(imagen) #Imagen

    # Este método permite modificar un destino.
    def modificar(self, nueva_cantidad, nuevo_precio):
        self.cantidad = nueva_cantidad        # Modifica la cantidad
        self.precio = nuevo_precio            # Modifica el precio

imagenCataratas = 'destinos/cataratas.jpg'
imagenBariloche = 'destinos/bariloche.jpg'
imagenCordoba = 'destinos/cordoba.jpg'

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
            return jsonify({'message': 'Ya existe un Destino con ese código.'}), 400
        sql = f'INSERT INTO destinos VALUES ({codigo}, "{descripcion}", {cantidad}, {precio}, "{imagen}");'
        self.cursor.execute(sql)
        self.conexion.commit()
        return jsonify({'message': 'Destino agregado correctamente.'}), 200
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
        return None
    
    # Este método permite modificar datos de destinos que están en el inventario
    # Utiliza el método consultar_destino del inventario y modificar del destino.
    def modificar_destino(self, codigo, nueva_cantidad, nuevo_precio):
        destino = self.consultar_destino(codigo)
        if destino:
            destino.modificar(nueva_cantidad, nuevo_precio)
            sql = f'UPDATE destinos SET cantidad = {nueva_cantidad}, precio = {nuevo_precio} WHERE codigo = {codigo};' 
            self.cursor.execute(sql)
            self.conexion.commit()
            return jsonify({'message': 'Destino modificado correctamente.'}), 200
        return jsonify({'message': 'Destino no encontrado.'}), 404
            

    # Este método elimina el destino indicado por codigo de la lista mantenida en el inventario.
    def eliminar_destino(self, codigo):
            sql = f'DELETE FROM destinos WHERE codigo = {codigo};' 
            self.cursor.execute(sql)
            if self.cursor.rowcount > 0:
                self.conexion.commit()
                return jsonify({'message': 'Destino eliminado correctamente.'}), 200
            return jsonify({'message': 'Destino no encontrado.'}), 404

    # Este método imprime en la terminal una lista con los datos de los destinos que figuran en el inventario.
    def listar_destinos(self):
        self.cursor.execute("SELECT * FROM destinos")
        rows = self.cursor.fetchall()
        destinos = []
        for row in rows:
            codigo, descripcion, cantidad, precio, imagen = row
            destino = {'codigo': codigo, 'descripcion': descripcion, 'cantidad': cantidad, 'precio': precio, 'imagen': imagen}
            destinos.append(destino)
        return jsonify(destinos), 200

class Carrito:
    # Definimos el constructor e inicializamos los atributos de instancia
    def __init__(self):
        self.conexion = get_db_connection()
        self.cursor = self.conexion.cursor()
        self.items = []
      # Lista de items en el carrito (variable de clase)

    # Este método permite agregar destinos del inventario al carrito.
    def agregar(self, codigo, cantidad, inventario):
        destino = inventario.consultar_destino(codigo)
        if destino is None:
            return jsonify({'message': 'El destino no existe.'}), 404
        if destino.cantidad < cantidad:
            return jsonify({'message': 'Cantidad en stock insuficiente.'}), 400

        for item in self.items:
            if item.codigo == codigo:
                item.cantidad += cantidad
                sql = f'UPDATE destinos SET cantidad = cantidad - {cantidad}  WHERE codigo = {codigo};'
                self.cursor.execute(sql)
                self.conexion.commit()
                return jsonify({'message': 'destino agregado al carrito correctamente.'}), 200
       
        def agregar_imagen (descripcion):
            if descripcion == 'Cataratas del Iguazu' or descripcion == 'cataratas del Iguazu':
                return imagenCataratas
            if descripcion == 'Bariloche' or descripcion == 'bariloche':
                return imagenBariloche
            if descripcion == 'Cordoba' or descripcion == 'cordoba':
                return imagenCordoba
            
        # Si no existe en el carrito, lo agregamos como un nuevo item.
        
        nuevo_item = Destino(codigo, destino.descripcion, cantidad, destino.precio, imagen = agregar_imagen(destino.descripcion))
        self.items.append(nuevo_item)
        sql = f'UPDATE destinos SET cantidad = cantidad - {cantidad}  WHERE codigo = {codigo};'
        self.cursor.execute(sql)
        self.conexion.commit()
        return jsonify({'message': 'Destino agregado al carrito correctamente.'}), 200
        
    # Este método quita unidades de un elemento del carrito, o lo elimina.
    def quitar(self, codigo, cantidad, inventario):
        for item in self.items:
            if item.codigo == codigo:
                if cantidad > item.cantidad:
                    return jsonify({'message': 'Cantidad a quitar mayor a la cantidad en el carrito.'}), 400
                item.cantidad -= cantidad
                if item.cantidad == 0:
                    self.items.remove(item)
                sql = f'UPDATE destinos SET cantidad = cantidad + {cantidad} WHERE codigo = {codigo};'
                self.cursor.execute(sql)
                self.conexion.commit()
                return jsonify({'message': 'Destino quitado del carrito correctamente.'}), 200
            return jsonify({'message': 'El destino no se encuentra en el carrito.'}), 404

    def mostrar(self):
        destinos_carrito = []
        for item in self.items:
            destino = {'codigo': item.codigo, 'descripcion': item.descripcion, 'cantidad': item.cantidad, 'precio': item.precio, 'imagen': item.imagen}
            destinos_carrito.append(destino)
        return jsonify(destinos_carrito), 200
    
app = Flask(__name__)
CORS(app)

carrito = Carrito()         # Instanciamos un carrito
inventario = Inventario()   # Instanciamos un inventario

# Ruta para obtener los datos de un destino según su código
@app.route('/destinos/<int:codigo>', methods=['GET'])
def obtener_destino(codigo):
    destino = inventario.consultar_destino(codigo)
    if destino:
        return jsonify({
            'codigo': destino.codigo,
            'descripcion': destino.descripcion,
            'cantidad': destino.cantidad,
            'precio': destino.precio,
            'imagen': destino.imagen
        }), 200
    return jsonify({'message': 'destino no encontrado.'}), 404

# Ruta para obtener la lista de destinos del inventario
@app.route('/')
def index():
    return 'API de Inventario' #codigo HTML de la pag principal que presente a la api

# Ruta para obtener la lista de destinos del inventario
@app.route('/destinos', methods=['GET'])
def obtener_destinos():
    return inventario.listar_destinos()

# Ruta para agregar un Destino al inventario
@app.route('/destinos', methods=['POST'])
def agregarDestino():
    codigo = request.json.get('codigo')
    descripcion = request.json.get('descripcion')
    cantidad = request.json.get('cantidad')
    precio = request.json.get('precio')
    imagen = request.json.get('imagen')
    return inventario.agregar_destino(codigo, descripcion, cantidad, precio, imagen)

# Ruta para modificar un Destino del inventario
@app.route('/destinos/<int:codigo>', methods=['PUT'])
def modificarDestino(codigo):
    nueva_cantidad = request.json.get('cantidad')
    nuevo_precio = request.json.get('precio')
    return inventario.modificar_destino(codigo, nueva_cantidad, nuevo_precio)

# Ruta para eliminar un Destino del inventario
@app.route('/destinos/<int:codigo>', methods=['DELETE'])
def eliminarDestino(codigo):
    return inventario.eliminar_destino(codigo)

# Ruta para agregar un Destino al carrito
@app.route('/carrito', methods=['POST'])
def agregar_carrito():
    codigo = request.json.get('codigo')
    cantidad = request.json.get('cantidad')
    inventario = Inventario()
    return carrito.agregar(codigo, cantidad, inventario)

# Ruta para quitar un Destino del carrito
@app.route('/carrito', methods=['DELETE'])
def quitar_carrito():
    codigo = request.json.get('codigo')
    cantidad = request.json.get('cantidad')
    inventario = Inventario()
    return carrito.quitar(codigo, cantidad, inventario)

# Ruta para obtener el contenido del carrito
@app.route('/carrito', methods=['GET'])
def obtener_carrito():
    return carrito.mostrar()

# Finalmente, si estamos ejecutando este archivo, lanzamos app.
if __name__ == '__main__':
    app.run()