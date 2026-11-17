import os

# Carpeta donde tenemos guardadas las facturas
carpeta_facturas = "facturas"

# Obtener la lista de archivos de la carpeta
archivos = os.listdir(carpeta_facturas)

# Recorrer todos los archivos
for archivo in archivos:

    # Comprobar que el archivo termina en .txt
    if archivo.endswith(".txt"):

        # Crear la ruta del archivo
        ruta = os.path.join(carpeta_facturas, archivo)

        # Abrir y leer el contenido
        with open(ruta, "r", encoding="utf-8") as fichero:
            contenido = fichero.read()

        # Mostrar el nombre y el contenido
        print("Archivo:", archivo)
        print(contenido)
        print("------------------------")


def parse_ticket(contenido):
    """
    Extrae los datos generales y los productos de una factura.
    Recibe el contenido de un archivo TXT.
    """

    # Creamos un diccionario para guardar los datos
    ticket = {}

    # Separamos el contenido en líneas
    lineas = contenido.split("\n")

    # Recorremos todas las líneas
    for linea in lineas:

        # Buscamos la fecha y la hora
        if linea.startswith("Fecha:"):
            partes = linea.split()

            ticket["fecha"] = partes[1]
            ticket["hora"] = partes[3]

        # Buscamos el cajero
        elif linea.startswith("Cajero:"):
            partes = linea.replace("Cajero:", "").strip()
            codigo, nombre = partes.split(" - ")

            ticket["codigo_cajero"] = codigo
            ticket["nombre_cajero"] = nombre

        # Buscamos el número de ticket
        elif linea.startswith("Ticket:"):
            ticket["numero_ticket"] = linea.split(":")[1].strip()

    # Creamos una lista para guardar los productos
        # Creamos una lista para guardar los productos
    productos = []

    # Variable para saber si estamos leyendo los productos
    leyendo_productos = False

    # Recorremos las líneas de la factura
    for linea in lineas:

        # Buscamos la cabecera de los productos
        if "CANT" in linea and "DESCRIPCIÓN" in linea:
            leyendo_productos = True
            continue

        # Comprobamos si hemos llegado al final de los productos
        elif leyendo_productos and linea.strip().startswith("---"):

            # Si ya hemos encontrado productos, terminamos
            if len(productos) > 0:
                break

            # Si todavía no hay productos, saltamos la línea
            else:
                continue

        # Leemos las líneas que contienen productos
        elif leyendo_productos and linea.strip() != "":
            partes = linea.split()

            # Extraemos la cantidad, descripción e importe
            cantidad = partes[0]
            importe = partes[-2]
            descripcion = " ".join(partes[1:-2])

            # Guardamos el producto en un diccionario
            producto = {
                "cantidad": cantidad,
                "descripcion": descripcion,
                "importe": importe
            }

            # Añadimos el producto a la lista
            productos.append(producto)

    # Guardamos la lista de productos en el ticket
    ticket["productos"] = productos

    return ticket


# Abrimos la primera factura para hacer una prueba
ruta = os.path.join(carpeta_facturas, "factura_001.txt")

with open(ruta, "r", encoding="utf-8") as fichero:
    contenido = fichero.read()

# Llamamos a nuestra función
datos = parse_ticket(contenido)

# Mostramos los datos extraídos
print(datos)