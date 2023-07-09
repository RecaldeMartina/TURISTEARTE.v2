import os
from PIL import Image

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

# Programa principal
cataratas = Destino(1, 'Cataratas del Iguazu', 10, 7500, imagenCataratas)
# Accedemos a los atributos del objeto
print(f'{cataratas.codigo} | {cataratas.descripcion} | {cataratas.cantidad} | ${cataratas.precio} | {cataratas.imagen}')
# Modificar los datos del objeto
cataratas.modificar(20, 9800) 
print(f'{cataratas.codigo} | {cataratas.descripcion} | {cataratas.cantidad} | ${cataratas.precio} | {cataratas.imagen}')

bariloche = Destino(2, 'Bariloche', 15, 45000, imagenBariloche)
print(f'{bariloche.codigo} | {bariloche.descripcion} | {bariloche.cantidad} | ${bariloche.precio} | {bariloche.imagen}')

bariloche.modificar(20, 50000)
print(f'{bariloche.codigo} | {bariloche.descripcion} | {bariloche.cantidad} | ${bariloche.precio} | {bariloche.imagen}')

cordoba = Destino(3, 'Cordoba', 7, 5000, imagenCordoba)
print(f'{cordoba.codigo} | {cordoba.descripcion} | {cordoba.cantidad} | ${cordoba.precio} | {cordoba.imagen}')

cordoba.modificar(10, 5500)
print(f'{cordoba.codigo} | {cordoba.descripcion} | {cordoba.cantidad} | ${cordoba.precio} | {cordoba.imagen}')

class Inventario:
    # Definimos el constructor e inicializamos los atributos de instancia
    def __init__(self):
        self.destinos = []  # Lista de destinos en el inventario (variable de clase)

    # Este método permite crear objetos de la clase "destino" y agregarlos al inventario.
    def agregar_destino(self, codigo, descripcion, cantidad, precio, imagen):
        nuevo_destino = Destino(codigo, descripcion, cantidad, precio, imagen)
        self.destinos.append(nuevo_destino)  # Agrega un nuevo destino a la lista

    # Este método permite consultar datos de destinos que están en el inventario
    # Devuelve el destino correspondiente al código proporcionado o False si no existe.
    def consultar_destino(self, codigo):
        for destino in self.destinos:
            if destino.codigo == codigo:
                return destino # Retorna un objeto
        return False

    # Este método permite modificar datos de destinos que están en el inventario
    # Utiliza el método consultar_destino del inventario y modificar del destino.
    def modificar_destino(self, codigo, nueva_cantidad, nuevo_precio):
        destino = self.consultar_destino(codigo)
        if destino:
            destino.modificar(nueva_cantidad, nuevo_precio)

    # Este método elimina el destino indicado por codigo de la lista mantenida en el inventario.
    def eliminar_destino(self, codigo):
        eliminar = False
        for destino in self.destinos:
            if destino.codigo == codigo:
                eliminar = True
                destino_eliminar = destino       
        if eliminar == True:
            self.destinos.remove(destino_eliminar)
            print(f'destino {codigo} eliminado.')
        else:
            print(f'destino {codigo} no encontrado.')

    # Este método imprime en la terminal una lista con los datos de los destinos que figuran en el inventario.
    def listar_destinos(self):
        print("-"*50)
        print("Lista de destinos en el inventario:")
        print("Código\tDescripción\t\tCant\tPrecio\tImagen")
        for destino in self.destinos:
            print(f'{destino.codigo}\t{destino.descripcion}\t{destino.cantidad}\t{destino.precio}\t{destino.imagen}')
        print("-"*50)

# Programa principal
# Crear una instancia de la clase Inventario
mi_inventario = Inventario() 

# Agregar Destinos 
mi_inventario.agregar_destino(1, 'Cataratas del Iguazu', 10, 7500, imagenCataratas)
mi_inventario.agregar_destino(2, 'Bariloche', 15, 45000, imagenBariloche)
mi_inventario.agregar_destino(3, 'Cordoba', 7, 5000, imagenCordoba)


# Consultar un destino 
destino = mi_inventario.consultar_destino(3)
if destino != False:
    print(f'Destino encontrado:\nCódigo: {destino.codigo}\nDescripción: {destino.descripcion}\nCantidad Pasajes: {destino.cantidad}\nPrecio: {destino.precio}\n{destino.imagen}')  
else:
    print("Destino no encontrado.")

# Modificar un destino 
mi_inventario.modificar_destino(3, 10, 5500)

# Listar todos los Destinos
mi_inventario.listar_destinos()

# Eliminar un destino 
mi_inventario.eliminar_destino(2)

# Confirmamos que haya sido eliminado
mi_inventario.listar_destinos()

class Carrito:
    # Definimos el constructor e inicializamos los atributos de instancia
    def __init__(self):
        self.items = []  # Lista de items en el carrito (variable de clase)

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
                destino = inventario.consultar_destino(codigo)
                destino.modificar(destino.cantidad - cantidad, destino.precio)
                return True

        # Si no existe en el carrito, lo agregamos como un nuevo item.
        def agregar_imagen (descripcion):
            if descripcion == 'Cataratas del Iguazu':
                return imagenCataratas
            if descripcion == 'Bariloche':
                return imagenBariloche
            if descripcion == 'Cordoba':
                return imagenCordoba

        nuevo_item = Destino(codigo, destino.descripcion, cantidad, destino.precio, imagen = agregar_imagen(destino.descripcion))
        self.items.append(nuevo_item)
        # Actualizamos la cantidad en el inventario
        destino = inventario.consultar_destino(codigo)
        destino.modificar(destino.cantidad - cantidad, destino.precio)
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
                destino = inventario.consultar_destino(codigo)
                destino.modificar(destino.cantidad + cantidad, destino.precio)
                return True

        # Si el bucle finaliza sin novedad, es que ese destino NO ESTA en el carrito.
        print("El destino no se encuentra en el carrito.")
        return False

    def mostrar(self):
        print("-"*50)
        print("Lista de productos en el carrito:")
        print("Código\tDescripción\t\tCant\tPrecio")
        for item in self.items:
            print(f'{item.codigo}\t{item.descripcion}\t{item.cantidad}\t{item.precio}')
        print("-"*50)

# Programa principal

# ---------------------------------------------------------------------
# Ejemplo de uso de las clases y objetos definidos antes:
# ---------------------------------------------------------------------

# Crear una instancia de la clase Inventario
mi_inventario = Inventario()

# Crear una instancia de la clase Carrito
mi_carrito = Carrito()

# Crear 3 productos y agregarlos al inventario
mi_inventario.agregar_destino(1, 'Cataratas del Iguazu', 10, 7500, imagenCataratas)
mi_inventario.agregar_destino(2, 'Bariloche', 15, 45000, imagenBariloche)
mi_inventario.agregar_destino(3, 'Cordoba', 7, 5000, imagenCordoba)

# Listar todos los productos del inventario
mi_inventario.listar_destinos()

# Agregar 2 productos al carrito
mi_carrito.agregar(1, 2, mi_inventario) # Agregar 2 unidades del producto con código 1 al carrito
mi_carrito.agregar(3, 4, mi_inventario) # Agregar 1 unidad del producto con código 3 al carrito
mi_carrito.quitar (1, 1, mi_inventario) # Quitar 1 unidad del producto con código 1 al carrito
# Listar todos los productos del carrito
mi_carrito.mostrar()
# Quitar 1 producto al carrito
mi_carrito.quitar (1, 1, mi_inventario) # Quitar 1 unidad del producto con código 1 al carrito
# Listar todos los productos del carrito
mi_carrito.mostrar()
# Mostramos el inventario
mi_inventario.listar_destinos()



    

