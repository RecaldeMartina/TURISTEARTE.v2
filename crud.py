from PIL import Image

class Destino:
    # Definimos el constructor e inicializamos los atributos de instancia
    def __init__(self, codigo, descripcion, cantidad, precio, imagen):
        self.codigo = codigo           # Código 
        self.descripcion = descripcion # Descripción
        self.cantidad = cantidad       # Cantidad de pasajes disponibles
        self.precio = precio           # Precio 
        self.imagen = Image.open()

    # Este método permite modificar un destino.
    def modificar(self, nueva_descripcion, nueva_cantidad, nuevo_precio):
        self.descripcion = nueva_descripcion  # Modifica la descripción
        self.cantidad = nueva_cantidad        # Modifica la cantidad
        self.precio = nuevo_precio            # Modifica el precio

# Programa principal
destino = Destino(1, 'Cataratas del Iguazu', 10, 7500, Image.open('cataratas.jpg'))
# Accedemos a los atributos del objeto
print(f'{destino.codigo} | {destino.descripcion} | {destino.cantidad} | {destino.precio} | {destino.imagen}')
# Modificar los datos del destino
destino.modificar('Cataratas del Iguazu', 20, 9800) 
print(f'{destino.codigo} | {destino.descripcion} | {destino.cantidad} | {destino.precio}')
