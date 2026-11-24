import os # permite trabajar con carpetas y archivos.
import sys # permite recoger los argumentos que escribimos al ejecutar el programa en CMD.


# DATOS DEL SUPERMERCADO

# Guardamos datos de la sucursal que después introduciremos en la base de datos.
nombre_sucursal = "SUPERMERCADOS EL AHORRO"
direccion_sucursal = "Av. Principal #123 - Madrid"
cif_sucursal = "B12345678"
telefono_sucursal = "910123456"


# 1. LEER Y EXTRAER LOS DATOS DE UNA FACTURA

# def se utiliza para crear una función.
# Esta función recibe el contenido de una factura y extrae su información.
def parse_ticket(contenido):
    """
    Lee una factura y extrae sus datos.
    También guarda el número de línea de cada dato.
    """

    # Creamos un diccionario para guardar los datos de la factura.
    ticket = {
        "fecha": "",
        "hora": "",
        "codigo_cajero": "",
        "nombre_cajero": "",
        "numero_ticket": "",
        "subtotal": "",
        "iva": "",
        "total": "",
        "forma_pago": "",
        "autorizacion": "",
        "productos": [],
        "lineas_incorrectas": [],
        "lineas_datos": {}
    }

    # split("\n") separa el contenido cada vez que encuentra un salto de línea.
    lineas = contenido.split("\n")

    # Recorremos todas las líneas de la factura.
    # enumerate() también nos permite saber el número de línea.
    # start=1 hace que la primera línea sea la número 1.
    for numero_linea, linea in enumerate(lineas, start=1):  #Enumerate: contar las líneas de cada factura empezando desde la linea 1

        # strip() elimina los espacios que hay al principio y al final.
        linea = linea.strip()

        # startswith() comprueba si una línea empieza por el texto indicado.
        if linea.startswith("Fecha:"): # Si la línea contiene la fecha

            # split() separa el texto en diferentes partes.
            partes = linea.split()

            # len() cuenta cuántos elementos tiene la lista.
            if len(partes) >= 4: # Si hay suficientes partes
                ticket["fecha"] = partes[1]
                ticket["hora"] = partes[3]

                # Guardamos el número de línea donde aparecen la fecha y la hora.
                ticket["lineas_datos"]["fecha"] = numero_linea    #lineas_datos: Guarda el número de línea de cada dato, asi si encontramos un error sabemos en que línea está
                ticket["lineas_datos"]["hora"] = numero_linea

        elif linea.startswith("Cajero:"): # Si no es la fecha y sí contiene el cajero

            # replace() elimina el texto "Cajero:".
            # strip() elimina los espacios sobrantes.
            datos = linea.replace("Cajero:", "").strip()

            # Separamos el código y el nombre del cajero.
            # El 1 indica que solo queremos hacer una separación.
            partes = datos.split(" - ", 1)

            if len(partes) == 2: # Si hay código y nombre
                ticket["codigo_cajero"] = partes[0].strip()
                ticket["nombre_cajero"] = partes[1].strip()

                # Guardamos dónde aparecen los datos del cajero.
                ticket["lineas_datos"]["codigo_cajero"] = numero_linea #lineas_datos: Guarda el número de línea de cada dato, asi si encontramos un error sabemos en que línea está
                ticket["lineas_datos"]["nombre_cajero"] = numero_linea

        elif linea.startswith("Ticket:"): # Si no son los datos anteriores y sí contiene el ticket

            # Separamos el texto por los dos puntos.
            partes = linea.split(":", 1)

            if len(partes) == 2: # Si se pudo separar el número
                ticket["numero_ticket"] = partes[1].strip()
                ticket["lineas_datos"]["numero_ticket"] = numero_linea

        elif linea.startswith("SUBTOTAL"): # Si no son los datos anteriores y sí contiene el subtotal

            partes = linea.split()

            # [-2] obtiene el penúltimo elemento de la lista.
            if len(partes) >= 2: # Si hay un subtotal
                ticket["subtotal"] = partes[-2]
                ticket["lineas_datos"]["subtotal"] = numero_linea #lineas_datos: Guarda el número de línea de cada dato, asi si encontramos un error sabemos en que línea está

        elif linea.startswith("IVA"): # Si no son los datos anteriores y sí contiene el IVA

            partes = linea.split()

            if len(partes) >= 2: # Si hay un IVA
                ticket["iva"] = partes[-2]
                ticket["lineas_datos"]["iva"] = numero_linea #lineas_datos: Guarda el número de línea de cada dato, asi si encontramos un error sabemos en que línea está

        elif linea.startswith("TOTAL A PAGAR"): # Si no son los datos anteriores y sí contiene el total

            partes = linea.split()

            if len(partes) >= 2: # Si hay un total
                ticket["total"] = partes[-2]
                ticket["lineas_datos"]["total"] = numero_linea #lineas_datos: Guarda el número de línea de cada dato, asi si encontramos un error sabemos en que línea está

        elif linea.startswith("FORMA DE PAGO:"): # Si no son los datos anteriores y sí contiene la forma de pago

            partes = linea.split(":", 1)

            if len(partes) == 2: # Si se pudo separar la forma de pago
                ticket["forma_pago"] = partes[1].strip()
                ticket["lineas_datos"]["forma_pago"] = numero_linea #lineas_datos: Guarda el número de línea de cada dato, asi si encontramos un error sabemos en que línea está

        elif linea.startswith("Autorización:"): # Si no son los datos anteriores y sí contiene la autorización

            partes = linea.split(":", 1)

            if len(partes) == 2: # Si se pudo separar la autorización
                ticket["autorizacion"] = partes[1].strip()
                ticket["lineas_datos"]["autorizacion"] = numero_linea

    # Ahora buscamos los productos que aparecen en la factura.

    # Estas variables nos permiten saber si hemos llegado a la tabla de productos.
    leyendo_productos = False
    primera_linea = True

    # Volvemos a recorrer las líneas de la factura.
    for numero_linea, linea in enumerate(lineas, start=1): #Enumerate: contar las líneas de cada factura empezando desde la linea 1

        linea = linea.strip()

        # Detectamos la cabecera de la tabla de productos.
        if "CANT" in linea and "DESCRIPCIÓN" in linea:
            leyendo_productos = True

        elif leyendo_productos:

            # Ignoramos la primera línea de guiones que aparece debajo de la cabecera.
            if linea.startswith("---") and primera_linea:
                primera_linea = False

            # La siguiente línea de guiones indica que termina la tabla.
            elif linea.startswith("---"):
                break

            # Comprobamos que la línea no esté vacía.
            elif linea != "":

                # Separamos los datos del producto.
                partes = linea.split()

                if len(partes) >= 3: # Si la línea tiene suficientes datos

                    # El primer elemento es la cantidad.
                    cantidad = partes[0]

                    # El penúltimo elemento es el importe.
                    importe = partes[-2]

                    # Unimos las palabras que forman la descripción.
                    descripcion = " ".join(partes[1:-2])

                    # Si no hay descripción, guardamos la línea como incorrecta.
                    if descripcion == "":
                        ticket["lineas_incorrectas"].append(numero_linea)

                    else:
                        # Creamos un diccionario para guardar cada producto.
                        producto = {
                            "cantidad": cantidad,
                            "descripcion": descripcion,
                            "importe": importe,

                            # Guardamos el número de línea donde aparece el producto.
                            "numero_linea": numero_linea
                        }

                        # append() añade el producto a la lista de productos.
                        ticket["productos"].append(producto)

                else:
                    # Si faltan datos, guardamos el número de línea como incorrecto.
                    ticket["lineas_incorrectas"].append(numero_linea)

    # return devuelve el diccionario con toda la información extraída.
    return ticket


# 2. COMPROBAR SI UN DATO ES NUMÉRICO

# Esta función recibe un valor y comprueba si se puede convertir en número.
def es_numero(valor):
    """
    Comprueba si un valor es un número.
    """

    # Cambiamos la coma decimal por un punto.
    valor = valor.replace(",", ".")

    try: # Intenta ejecutar las instrucciones.

        # float() intenta convertir el valor en un número decimal.
        float(valor)

        # Si funciona, devolvemos True (verdadero).
        return True

    # except recoge el error si no se puede convertir.
    except ValueError:

        # Si no es un número válido, devolvemos False (falso).
        return False


# FUNCIÓN PARA GUARDAR LOS ERRORES

# Esta función guarda los errores encontrados en el archivo errorlog.txt.
def guardar_error(archivo, numero_linea, mensaje, valor):

    # Abrimos el archivo en modo "a" para añadir errores sin borrar los anteriores.
    # La letra "a" significa añadir y escribe al final del archivo.
    with open("errorlog.txt", "a", encoding="utf-8") as fichero:

        # str() convierte un dato en texto. Lo utilizamos porque el número de línea puede ser un número entero.
        # "\n" representa un salto de línea. Cada error se escribe en una línea diferente del archivo.
        # write() escribe el texto dentro del archivo.
        fichero.write("Factura: " + archivo + " , Línea: " + str(numero_linea) +
                      " , Error: " + mensaje + " . Valor encontrado: " + str(valor) + "\n")


# 3. VALIDAR LOS DATOS DE LA FACTURA

# Esta función comprueba que los datos extraídos sean correctos.
# También recibe el nombre del archivo para indicar dónde está el error.
def validar_ticket(ticket, archivo):
    """
    Comprueba que los datos de la factura sean correctos.
    Si encuentra errores, los guarda en errorlog.txt.
    """

    # Empezamos suponiendo que la factura es correcta.
    correcto = True

    # Comprobamos que no falten los datos obligatorios.
    campos = [
        "fecha",
        "hora",
        "codigo_cajero",
        "nombre_cajero",
        "numero_ticket",
        "subtotal",
        "iva",
        "total",
        "forma_pago"
    ]

    # Recorremos los datos obligatorios.
    for campo in campos:

        if ticket[campo] == "": # Si falta un dato

            # Guardamos el error en errorlog.txt.
            # str() no es necesario aquí porque el nombre del campo ya es texto.
            # Como falta el dato, no tenemos un número de línea concreto.
            guardar_error(archivo, "No disponible",
                          "Falta este dato en la factura: " + campo, "Dato ausente")

            correcto = False

    # Comprobamos que la fecha tenga tres partes separadas por barras.
    fecha = ticket["fecha"].split("/")

    if ticket["fecha"] != "":

        if len(fecha) != 3: # Si la fecha no tiene tres partes

            guardar_error(archivo, ticket["lineas_datos"]["fecha"],
                          "La fecha tiene un formato incorrecto", ticket["fecha"])

            correcto = False

        else:

            # Recorremos las partes de la fecha.
            for parte in fecha:

                # isdigit() comprueba si el texto contiene solamente números.
                if not parte.isdigit():

                    guardar_error(archivo, ticket["lineas_datos"]["fecha"],
                                  "La fecha tiene un formato incorrecto", ticket["fecha"])

                    correcto = False
                    break

    # Comprobamos que la hora tenga dos partes separadas por dos puntos.
    hora = ticket["hora"].split(":")

    if ticket["hora"] != "":

        if len(hora) != 2: # Si la hora no tiene dos partes

            guardar_error(archivo, ticket["lineas_datos"]["hora"],
                          "La hora tiene un formato incorrecto", ticket["hora"])

            correcto = False

        else:

            for parte in hora:

                if not parte.isdigit():

                    guardar_error(archivo, ticket["lineas_datos"]["hora"],
                                  "La hora tiene un formato incorrecto", ticket["hora"])

                    correcto = False
                    break

    # Comprobamos que el subtotal, el IVA y el total sean números.
    importes = ["subtotal", "iva", "total"]

    for campo in importes:

        if ticket[campo] != "":

            if not es_numero(ticket[campo]):

                guardar_error(archivo, ticket["lineas_datos"][campo],
                              "El " + campo + " no es correcto", ticket[campo])

                correcto = False

    # len() cuenta los productos.
    # Si hay 0, significa que la factura no tiene productos.
    if len(ticket["productos"]) == 0:

        guardar_error(archivo, "No disponible",
                      "La factura no tiene productos", "No se encontraron productos")

        correcto = False

    # Comprobamos si hay líneas de productos incorrectas.
    for numero_linea in ticket["lineas_incorrectas"]:

        guardar_error(archivo, numero_linea,
                      "La línea del producto está incompleta", "Datos incompletos")

        correcto = False

    # Recorremos todos los productos para comprobar sus datos.
    for producto in ticket["productos"]:

        # Recuperamos el número de línea donde aparece el producto.
        numero_linea = producto["numero_linea"]

        if not es_numero(producto["cantidad"]): # Si la cantidad no es numérica

            guardar_error(archivo, numero_linea,
                          "La cantidad del producto no es correcta", producto["cantidad"])

            correcto = False

        if not es_numero(producto["importe"]): # Si el importe no es numérico

            guardar_error(archivo, numero_linea,
                          "El importe del producto no es correcto", producto["importe"])

            correcto = False

    # Devolvemos True si todo está correcto o False si hay algún error.
    return correcto


# 4. PREPARAR LOS TEXTOS PARA SQL

# Esta función prepara los textos antes de introducirlos en SQL.
def escapar_sql(texto):
    """
    Evita errores con las comillas simples en SQL.
    """

    # Duplicamos las comillas simples para evitar problemas al generar SQL.
    # Por ejemplo: O'Brien se convierte en O''Brien.
    return texto.replace("'", "''")


# 5. CAMBIAR EL FORMATO DE FECHA Y HORA

def convertir_fecha(fecha):
    """
    Cambia la fecha al formato que utiliza MySQL.
    """

    # Separamos el día, el mes y el año.
    partes = fecha.split("/")

    # MySQL utiliza el formato año-mes-día.
    return partes[2] + "-" + partes[1] + "-" + partes[0]


# Esta función añade los segundos a la hora.
def convertir_hora(hora):
    """
    Añade los segundos al formato de la hora.
    """

    # Separamos las horas y los minutos.
    partes = hora.split(":")

    # Devolvemos la hora añadiendo los segundos :00.
    return partes[0] + ":" + partes[1] + ":00"


# 6. LEER LAS FACTURAS Y GENERAR EL ARCHIVO SQL

# Esta función lee todas las facturas de una carpeta y genera el archivo SQL.
def generar_sql_para_carpeta(carpeta):
    """
    Lee todas las facturas de una carpeta y genera el archivo SQL.
    """

    # Creamos el archivo de errores vacío al comenzar el programa.
    # Abrirlo en modo "w" crea el archivo si no existe.
    # Si ya existe, borra su contenido anterior para empezar de cero.
    with open("errorlog.txt", "w", encoding="utf-8") as fichero: # sirve para crear el archivo si no existe o vaciarlo si ya existe

        # pass indica que no tenemos que ejecutar ninguna instrucción aquí.
        # Solo queremos crear el archivo o vaciarlo.
        pass

    # os.path.isdir() comprueba si la carpeta existe.
    if not os.path.isdir(carpeta):
        print("Error: no se encuentra la carpeta", carpeta)
        return

    # os.listdir() obtiene los nombres de los archivos de la carpeta.
    archivos = os.listdir(carpeta)

    # sort() ordena los nombres de los archivos.
    archivos.sort()

    # Creamos una lista vacía para guardar las facturas correctas.
    tickets = []

    # Recorremos todos los archivos de la carpeta.
    for archivo in archivos:

        # lower() convierte el nombre a minúsculas.
        # endswith() comprueba si el archivo termina en .txt.
        if archivo.lower().endswith(".txt"):

            # os.path.join() une la carpeta y el nombre del archivo para crear su ruta.
            ruta = os.path.join(carpeta, archivo)

            # try intenta abrir y leer el archivo.
            try:

                # open() abre el archivo en modo lectura ("r").
                # encoding="utf-8" permite leer correctamente caracteres como las tildes.
                # with cierra el archivo automáticamente al terminar.
                with open(ruta, "r", encoding="utf-8") as fichero:

                    # read() lee todo el contenido del archivo.
                    contenido = fichero.read()

                # strip() permite comprobar si el archivo está vacío.
                if contenido.strip() == "":

                    guardar_error(archivo, "No disponible",
                                  "La factura está vacía", "No hay contenido")

                else:

                    # Extraemos los datos de la factura.
                    datos = parse_ticket(contenido)

                    # Comprobamos si los datos extraídos son correctos.
                    # También enviamos el nombre del archivo para identificar los errores.
                    if validar_ticket(datos, archivo):  #validar_ticket(): utiliza esa información y pueda indicar el archivo, la línea y el dato que contiene el error.

                        # Si es correcta, la guardamos en la lista de tickets.
                        tickets.append(datos)

            # OSError recoge errores relacionados con la lectura del archivo.
            except OSError:

                guardar_error(archivo, "No disponible",
                              "No se ha podido leer el archivo", "Error de lectura")

    # Si no hay facturas correctas, no generamos el archivo SQL.
    if len(tickets) == 0:
        print("No hay facturas correctas para generar el SQL")
        return

    # Creamos listas para no guardar empleados ni productos repetidos.
    codigos_empleados = []
    descripciones_productos = []

    # Creamos listas donde guardaremos las instrucciones SQL.
    inserts_empleados = []
    inserts_productos = []
    inserts_tickets = []
    inserts_lineas = []
    inserts_pagos = []

    # PREPARAR EMPLEADOS Y PRODUCTOS.

    # Recorremos todas las facturas correctas.
    for ticket in tickets:

        codigo = ticket["codigo_cajero"]

        # Comprobamos si el empleado ya está guardado en nuestra lista.
        if codigo not in codigos_empleados:

            # Añadimos el código para no repetir al empleado.
            codigos_empleados.append(codigo)

            # Preparamos los textos para utilizarlos en SQL.
            codigo_sql = escapar_sql(codigo)
            nombre_sql = escapar_sql(ticket["nombre_cajero"])

            # Creamos la instrucción SQL para insertar al empleado.
            # INSERT IGNORE evita errores si el registro ya existe.
            sentencia = (
                "INSERT IGNORE INTO empleado (codigo, nombre) "
                "VALUES ('" + codigo_sql + "', '" + nombre_sql + "');"
            )

            # Guardamos la instrucción SQL en la lista de empleados.
            inserts_empleados.append(sentencia)

        # Recorremos los productos de cada factura.
        for producto in ticket["productos"]:

            descripcion = producto["descripcion"]

            # Comprobamos si el producto ya está guardado.
            if descripcion not in descripciones_productos:

                # Guardamos la descripción para no repetirla.
                descripciones_productos.append(descripcion)

                descripcion_sql = escapar_sql(descripcion)

                # Creamos la instrucción SQL para insertar el producto.
                sentencia = (
                    "INSERT IGNORE INTO producto (descripcion) "
                    "VALUES ('" + descripcion_sql + "');"
                )

                # Guardamos la instrucción en la lista de productos.
                inserts_productos.append(sentencia)

    # PREPARAR TICKETS, LÍNEAS Y PAGOS.

    # Recorremos de nuevo las facturas correctas.
    for ticket in tickets:

        # Preparamos el número del ticket y el código del empleado para SQL.
        numero = escapar_sql(ticket["numero_ticket"])
        codigo = escapar_sql(ticket["codigo_cajero"])

        # Convertimos la fecha y la hora al formato de MySQL.
        fecha = convertir_fecha(ticket["fecha"])
        hora = convertir_hora(ticket["hora"])

        # Cambiamos las comas decimales por puntos.
        subtotal = ticket["subtotal"].replace(",", ".")
        iva = ticket["iva"].replace(",", ".")
        total = ticket["total"].replace(",", ".")

        # INSERT del ticket.
        # SELECT permite obtener los identificadores de la sucursal y del empleado.
        sentencia = (
            "INSERT IGNORE INTO ticket "
            "(numero_ticket, fecha, hora, subtotal, iva, total, id_sucursal, id_empleado) "
            "SELECT '" + numero + "', '" + fecha + "', '" + hora + "', "
            + subtotal + ", " + iva + ", " + total + ", "
            "sucursal.id_sucursal, empleado.id_empleado "
            "FROM sucursal, empleado "
            "WHERE sucursal.cif = '" + escapar_sql(cif_sucursal) + "' "
            "AND empleado.codigo = '" + codigo + "';"
        )

        # Guardamos la instrucción SQL del ticket.
        inserts_tickets.append(sentencia)

        # INSERT de cada línea del ticket.
        # Una línea representa un producto comprado dentro de una factura.
        for producto in ticket["productos"]:

            # Preparamos los datos del producto para SQL.
            descripcion = escapar_sql(producto["descripcion"])
            cantidad = producto["cantidad"].replace(",", ".")
            importe = producto["importe"].replace(",", ".")

            # Creamos la instrucción SQL para insertar las líneas del ticket.
            sentencia = (
                "INSERT INTO ticket_linea "
                "(id_ticket, id_producto, cantidad, importe) "
                "SELECT ticket.id_ticket, producto.id_producto, "
                + cantidad + ", " + importe + " "
                "FROM ticket, producto "
                "WHERE ticket.numero_ticket = '" + numero + "' "
                "AND producto.descripcion = '" + descripcion + "' "
                "AND NOT EXISTS ("
                "SELECT 1 FROM ticket_linea "
                "WHERE ticket_linea.id_ticket = ticket.id_ticket "
                "AND ticket_linea.id_producto = producto.id_producto"
                ");"
            )

            # Guardamos la instrucción de la línea.
            inserts_lineas.append(sentencia)

        # Comprobamos si la factura tiene código de autorización.
        if ticket["autorizacion"] == "":

            # Si no hay autorización, utilizamos NULL en SQL.
            autorizacion = "NULL"

        else:
            # Si existe, preparamos el texto para SQL y añadimos las comillas.
            autorizacion = "'" + escapar_sql(ticket["autorizacion"]) + "'"

        forma_pago = escapar_sql(ticket["forma_pago"])

        # INSERT del pago.
        sentencia = (
            "INSERT IGNORE INTO pago (id_ticket, forma_pago, autorizacion) "
            "SELECT id_ticket, '" + forma_pago + "', " + autorizacion + " "
            "FROM ticket "
            "WHERE numero_ticket = '" + numero + "';"
        )

        # Guardamos la instrucción del pago.
        inserts_pagos.append(sentencia)

    # JUNTAR TODAS LAS INSTRUCCIONES SQL.

    # Creamos una lista vacía donde reuniremos todo el contenido del archivo SQL.
    sql = []

    # Añadimos comentarios para identificar el archivo y la base de datos.
    sql.append("-- Archivo SQL generado desde las facturas TXT")
    sql.append("-- Base de datos: supermercado")
    sql.append("")

    # Indicamos la codificación de los textos en MySQL.
    sql.append("SET NAMES utf8mb4;")
    sql.append("")

    # Añadimos la sucursal.
    sql.append("-- 1. SUCURSAL")

    # Esta instrucción inserta la sucursal si todavía no existe.
    sql.append(
        "INSERT INTO sucursal (nombre, direccion, cif, telefono) "
        "SELECT '" + escapar_sql(nombre_sucursal) + "', "
        "'" + escapar_sql(direccion_sucursal) + "', "
        "'" + escapar_sql(cif_sucursal) + "', "
        "'" + escapar_sql(telefono_sucursal) + "' "
        "WHERE NOT EXISTS ("
        "SELECT 1 FROM sucursal WHERE cif = '" + escapar_sql(cif_sucursal) + "'"
        ");"
    )

    sql.append("")

    # Añadimos las instrucciones de los empleados.
    sql.append("-- 2. EMPLEADOS")

    # Recorremos la lista y añadimos cada instrucción al SQL.
    for sentencia in inserts_empleados:
        sql.append(sentencia)

    sql.append("")

    # Añadimos las instrucciones de los productos.
    sql.append("-- 3. PRODUCTOS")

    for sentencia in inserts_productos:
        sql.append(sentencia)

    sql.append("")

    # Añadimos las instrucciones de los tickets.
    sql.append("-- 4. TICKETS")

    for sentencia in inserts_tickets:
        sql.append(sentencia)

    sql.append("")

    # Añadimos las instrucciones de las líneas de los tickets.
    sql.append("-- 5. LINEAS DE TICKETS")

    for sentencia in inserts_lineas:
        sql.append(sentencia)

    sql.append("")

    # Añadimos las instrucciones de los pagos.
    sql.append("-- 6. PAGOS")

    for sentencia in inserts_pagos:
        sql.append(sentencia)

    # CREAR Y ESCRIBIR EL ARCHIVO SQL.

    # try intenta crear y escribir el archivo.
    try:

        # Abrimos el archivo en modo escritura ("w").
        # Si no existe, se crea. Si ya existe, se sustituye su contenido.
        # encoding="utf-8" permite guardar correctamente las tildes y otros caracteres.
        with open("InsertUnderlineTicket.sql", "w", encoding="utf-8") as fichero:

            # Recorremos todas las instrucciones SQL.
            for linea in sql:

                # write() escribe cada instrucción en el archivo.
                # "\n" añade un salto de línea después de cada una.
                fichero.write(linea + "\n")

        # Mostramos un resumen cuando termina correctamente.
        # No mostramos los nombres de las facturas para evitar mensajes repetidos.
        print("")
        print("Proceso terminado correctamente")
        print("Facturas correctas:", len(tickets))
        print("Empleados diferentes:", len(codigos_empleados))
        print("Productos diferentes:", len(descripciones_productos))
        print("Archivo generado: InsertUnderlineTicket.sql")

    # Si ocurre un error al crear o escribir el archivo, lo mostramos.
    except OSError:
        print("Error: no se ha podido crear el archivo SQL")


# 7. PROGRAMA PRINCIPAL

# sys.argv contiene los argumentos que escribimos al ejecutar el programa en CMD.
# sys.argv[0] es el nombre del archivo Python.
# sys.argv[1] sería el nombre de la carpeta que queremos procesar.

# len() cuenta los elementos que hay en sys.argv.
if len(sys.argv) > 1:

    # Si hemos escrito una carpeta en CMD, utilizamos esa carpeta.
    carpeta_facturas = sys.argv[1]

else:
    # Si no indicamos ninguna carpeta, utilizamos "facturas" por defecto.
    carpeta_facturas = "facturas"

# Llamamos a la función principal para empezar a procesar las facturas.
generar_sql_para_carpeta(carpeta_facturas)
