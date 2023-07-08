import os
from PIL import Image

class Destino:
    # Definimos el constructor e inicializamos los atributos de instancia
    def __init__(self, codigo, descripcion, cantidad, precio, imagen):
        self.codigo = codigo           # Código 
        self.descripcion = descripcion # Descripción
        self.cantidad = cantidad       # Cantidad de pasajes disponibles
        self.precio = precio           # Precio 
        ruta_absoluta = os.path.join(os.getcwd(), imagen)
        self.imagen = Image.open(ruta_absoluta)

    # Este método permite modificar un destino.
    def modificar(self, nueva_cantidad, nuevo_precio):
        self.cantidad = nueva_cantidad        # Modifica la cantidad
        self.precio = nuevo_precio            # Modifica el precio

# Programa principal
cataratas = Destino(1, 'Cataratas del Iguazu', 10, 7500, imagen="destinos/cataratas.jpg")
# Accedemos a los atributos del objeto
print(f'{cataratas.codigo} | {cataratas.descripcion} | {cataratas.cantidad} | ${cataratas.precio} | {cataratas.imagen}')
# Modificar los datos del objeto
cataratas.modificar(20, 9800) 
print(f'{cataratas.codigo} | {cataratas.descripcion} | {cataratas.cantidad} | ${cataratas.precio} | {cataratas.imagen}')

bariloche = Destino(2, 'Bariloche', 15, 45000, imagen="destinos/bariloche.jpg")
print(f'{bariloche.codigo} | {bariloche.descripcion} | {bariloche.cantidad} | ${bariloche.precio} | {bariloche.imagen}')

bariloche.modificar(20, 50000)
print(f'{bariloche.codigo} | {bariloche.descripcion} | {bariloche.cantidad} | ${bariloche.precio} | {bariloche.imagen}')

cordoba = Destino(3, 'Cordoba', 7, 5000, imagen="destinos/cordoba.jpg")
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
mi_inventario.agregar_destino(1, 'Cataratas del Iguazu', 10, 7500, imagen="destinos/cataratas.jpg")
mi_inventario.agregar_destino(2, 'Bariloche', 15, 45000, imagen="destinos/bariloche.jpg")
mi_inventario.agregar_destino(3, 'Cordoba', 7, 5000, imagen="destinos/cordoba.jpg")


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


