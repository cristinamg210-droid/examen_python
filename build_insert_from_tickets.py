import os
import sys


# DATOS DEL SUPERMERCADO

nombre_sucursal = "SUPERMERCADOS EL AHORRO"
direccion_sucursal = "Av. Principal #123 - Madrid"
cif_sucursal = "B12345678"
telefono_sucursal = "910123456"


# 1. LEER Y EXTRAER LOS DATOS DE UNA FACTURA

def parse_ticket(contenido):
    """
    Lee una factura y extrae sus datos.
    """

    # Diccionario donde guardamos los datos de la factura.
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
        "lineas_incorrectas": []
    }

    # Separamos el contenido en líneas.
    lineas = contenido.split("\n")

    # Recorremos las líneas para extraer los datos generales.
    for linea in lineas:

        linea = linea.strip()

        if linea.startswith("Fecha:"):
            partes = linea.split()

            if len(partes) >= 4:
                ticket["fecha"] = partes[1]
                ticket["hora"] = partes[3]

        elif linea.startswith("Cajero:"):
            datos = linea.replace("Cajero:", "").strip()
            partes = datos.split(" - ", 1)

            if len(partes) == 2:
                ticket["codigo_cajero"] = partes[0].strip()
                ticket["nombre_cajero"] = partes[1].strip()

        elif linea.startswith("Ticket:"):
            partes = linea.split(":", 1)

            if len(partes) == 2:
                ticket["numero_ticket"] = partes[1].strip()

        elif linea.startswith("SUBTOTAL"):
            partes = linea.split()

            if len(partes) >= 2:
                ticket["subtotal"] = partes[-2]

        elif linea.startswith("IVA"):
            partes = linea.split()

            if len(partes) >= 2:
                ticket["iva"] = partes[-2]

        elif linea.startswith("TOTAL A PAGAR"):
            partes = linea.split()

            if len(partes) >= 2:
                ticket["total"] = partes[-2]

        elif linea.startswith("FORMA DE PAGO:"):
            partes = linea.split(":", 1)

            if len(partes) == 2:
                ticket["forma_pago"] = partes[1].strip()

        elif linea.startswith("Autorización:"):
            partes = linea.split(":", 1)

            if len(partes) == 2:
                ticket["autorizacion"] = partes[1].strip()

    # Ahora buscamos los productos de la factura.
    leyendo_productos = False
    primera_linea = True

    for linea in lineas:

        linea = linea.strip()

        # Detectamos la cabecera de la tabla de productos.
        if "CANT" in linea and "DESCRIPCIÓN" in linea:
            leyendo_productos = True

        elif leyendo_productos:

            # Ignoramos la primera línea de guiones.
            if linea.startswith("---") and primera_linea:
                primera_linea = False

            # La siguiente línea de guiones indica el final.
            elif linea.startswith("---"):
                break

            elif linea != "":

                partes = linea.split()

                if len(partes) >= 3:

                    cantidad = partes[0]
                    importe = partes[-2]
                    descripcion = " ".join(partes[1:-2])

                    if descripcion == "":
                        ticket["lineas_incorrectas"].append(linea)

                    else:
                        producto = {
                            "cantidad": cantidad,
                            "descripcion": descripcion,
                            "importe": importe
                        }

                        ticket["productos"].append(producto)

                else:
                    ticket["lineas_incorrectas"].append(linea)

    return ticket


# 2. COMPROBAR SI UN DATO ES NUMÉRICO

def es_numero(valor):
    """
    Comprueba si un valor es un número.
    """

    # Cambiamos la coma decimal por un punto.
    valor = valor.replace(",", ".")

    try:
        float(valor)
        return True

    except ValueError:
        return False


# 3. VALIDAR LOS DATOS DE LA FACTURA

def validar_ticket(ticket):
    """
    Comprueba que los datos de la factura sean correctos.
    """

    correcto = True

    # Comprobamos que no falten datos.
    if ticket["fecha"] == "":
        print("Falta la fecha")
        correcto = False

    if ticket["hora"] == "":
        print("Falta la hora")
        correcto = False

    if ticket["codigo_cajero"] == "":
        print("Falta el código del cajero")
        correcto = False

    if ticket["nombre_cajero"] == "":
        print("Falta el nombre del cajero")
        correcto = False

    if ticket["numero_ticket"] == "":
        print("Falta el número del ticket")
        correcto = False

    if ticket["subtotal"] == "":
        print("Falta el subtotal")
        correcto = False

    if ticket["iva"] == "":
        print("Falta el IVA")
        correcto = False

    if ticket["total"] == "":
        print("Falta el total")
        correcto = False

    if ticket["forma_pago"] == "":
        print("Falta la forma de pago")
        correcto = False

    # Comprobamos el formato de la fecha.
    fecha = ticket["fecha"].split("/")

    if len(fecha) != 3:
        print("La fecha tiene un formato incorrecto")
        correcto = False

    else:
        for parte in fecha:
            if not parte.isdigit():
                print("La fecha tiene un formato incorrecto")
                correcto = False

    # Comprobamos el formato de la hora.
    hora = ticket["hora"].split(":")

    if len(hora) != 2:
        print("La hora tiene un formato incorrecto")
        correcto = False

    else:
        for parte in hora:
            if not parte.isdigit():
                print("La hora tiene un formato incorrecto")
                correcto = False

    # Comprobamos los importes.
    if not es_numero(ticket["subtotal"]):
        print("El subtotal no es correcto")
        correcto = False

    if not es_numero(ticket["iva"]):
        print("El IVA no es correcto")
        correcto = False

    if not es_numero(ticket["total"]):
        print("El total no es correcto")
        correcto = False

    # Comprobamos que haya productos.
    if len(ticket["productos"]) == 0:
        print("La factura no tiene productos")
        correcto = False

    # Comprobamos que no haya líneas incorrectas.
    if len(ticket["lineas_incorrectas"]) > 0:
        print("Hay líneas de productos incorrectas")
        correcto = False

    # Comprobamos las cantidades e importes de los productos.
    for producto in ticket["productos"]:

        if not es_numero(producto["cantidad"]):
            print("Hay una cantidad incorrecta")
            correcto = False

        if not es_numero(producto["importe"]):
            print("Hay un importe de producto incorrecto")
            correcto = False

    return correcto


# 4. PREPARAR LOS TEXTOS PARA SQL

def escapar_sql(texto):
    """
    Evita errores con las comillas simples en SQL.
    """

    # Duplicamos las comillas simples.
    return texto.replace("'", "''")


# 5. CAMBIAR EL FORMATO DE FECHA Y HORA

def convertir_fecha(fecha):
    """
    Cambia la fecha al formato que utiliza MySQL.
    """

    partes = fecha.split("/")

    # MySQL utiliza el formato año-mes-día.
    return partes[2] + "-" + partes[1] + "-" + partes[0]


def convertir_hora(hora):
    """
    Añade los segundos al formato de la hora.
    """

    partes = hora.split(":")

    return partes[0] + ":" + partes[1] + ":00"


# 6. LEER LAS FACTURAS Y GENERAR EL ARCHIVO SQL

def generar_sql_para_carpeta(carpeta):
    """
    Lee las facturas de una carpeta y genera el archivo SQL.
    """

    # Comprobamos que exista la carpeta.
    if not os.path.isdir(carpeta):
        print("Error: no se encuentra la carpeta", carpeta)
        return

    # Obtenemos los nombres de los archivos.
    archivos = os.listdir(carpeta)
    archivos.sort()

    tickets = []

    # Leemos todos los archivos TXT.
    for archivo in archivos:

        if archivo.lower().endswith(".txt"):

            ruta = os.path.join(carpeta, archivo)

            print("Leyendo:", archivo)

            try:
                with open(ruta, "r", encoding="utf-8") as fichero:
                    contenido = fichero.read()

                if contenido.strip() == "":
                    print("Error: la factura está vacía")

                else:
                    datos = parse_ticket(contenido)

                    if validar_ticket(datos):
                        tickets.append(datos)
                        print("Factura correcta:", datos["numero_ticket"])

                    else:
                        print("La factura tiene errores")

            except OSError:
                print("Error al leer el archivo:", archivo)

            print("-----------------------------")

    # Si no hay facturas válidas, no generamos el SQL.
    if len(tickets) == 0:
        print("No hay facturas correctas para generar el SQL")
        return

    # Listas para evitar repetir empleados y productos.
    codigos_empleados = []
    descripciones_productos = []

    # Listas para guardar las instrucciones SQL.
    inserts_empleados = []
    inserts_productos = []
    inserts_tickets = []
    inserts_lineas = []
    inserts_pagos = []

    # PREPARAR EMPLEADOS Y PRODUCTOS.

    for ticket in tickets:

        codigo = ticket["codigo_cajero"]

        # Comprobamos si el empleado ya está guardado.
        if codigo not in codigos_empleados:

            codigos_empleados.append(codigo)

            codigo_sql = escapar_sql(codigo)
            nombre_sql = escapar_sql(ticket["nombre_cajero"])

            sentencia = (
                "INSERT IGNORE INTO empleado (codigo, nombre) "
                "VALUES ('" + codigo_sql + "', '" + nombre_sql + "');"
            )

            inserts_empleados.append(sentencia)

        # Recorremos los productos de la factura.
        for producto in ticket["productos"]:

            descripcion = producto["descripcion"]

            if descripcion not in descripciones_productos:

                descripciones_productos.append(descripcion)

                descripcion_sql = escapar_sql(descripcion)

                sentencia = (
                    "INSERT IGNORE INTO producto (descripcion) "
                    "VALUES ('" + descripcion_sql + "');"
                )

                inserts_productos.append(sentencia)

    # PREPARAR TICKETS, LÍNEAS Y PAGOS.

    for ticket in tickets:

        numero = escapar_sql(ticket["numero_ticket"])
        codigo = escapar_sql(ticket["codigo_cajero"])

        fecha = convertir_fecha(ticket["fecha"])
        hora = convertir_hora(ticket["hora"])

        subtotal = ticket["subtotal"].replace(",", ".")
        iva = ticket["iva"].replace(",", ".")
        total = ticket["total"].replace(",", ".")

        # INSERT del ticket.
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

        inserts_tickets.append(sentencia)

        # INSERT de cada línea del ticket.
        for producto in ticket["productos"]:

            descripcion = escapar_sql(producto["descripcion"])
            cantidad = producto["cantidad"].replace(",", ".")
            importe = producto["importe"].replace(",", ".")

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

            inserts_lineas.append(sentencia)

        # Comprobamos si hay código de autorización.
        if ticket["autorizacion"] == "":
            autorizacion = "NULL"

        else:
            autorizacion = "'" + escapar_sql(ticket["autorizacion"]) + "'"

        forma_pago = escapar_sql(ticket["forma_pago"])

        # INSERT del pago.
        sentencia = (
            "INSERT IGNORE INTO pago (id_ticket, forma_pago, autorizacion) "
            "SELECT id_ticket, '" + forma_pago + "', " + autorizacion + " "
            "FROM ticket "
            "WHERE numero_ticket = '" + numero + "';"
        )

        inserts_pagos.append(sentencia)

    # JUNTAR TODAS LAS INSTRUCCIONES SQL.

    sql = []

    sql.append("-- Archivo SQL generado desde las facturas TXT")
    sql.append("-- Base de datos: supermercado")
    sql.append("")

    sql.append("SET NAMES utf8mb4;")
    sql.append("")

    # Añadimos la sucursal.
    sql.append("-- 1. SUCURSAL")

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

    # Añadimos los empleados.
    sql.append("-- 2. EMPLEADOS")

    for sentencia in inserts_empleados:
        sql.append(sentencia)

    sql.append("")

    # Añadimos los productos.
    sql.append("-- 3. PRODUCTOS")

    for sentencia in inserts_productos:
        sql.append(sentencia)

    sql.append("")

    # Añadimos los tickets.
    sql.append("-- 4. TICKETS")

    for sentencia in inserts_tickets:
        sql.append(sentencia)

    sql.append("")

    # Añadimos las líneas de los tickets.
    sql.append("-- 5. LINEAS DE TICKETS")

    for sentencia in inserts_lineas:
        sql.append(sentencia)

    sql.append("")

    # Añadimos los pagos.
    sql.append("-- 6. PAGOS")

    for sentencia in inserts_pagos:
        sql.append(sentencia)

    # CREAR Y ESCRIBIR EL ARCHIVO SQL.

    try:

        # Creamos el archivo en modo escritura.
        with open("InsertUnderlineTicket.sql", "w", encoding="utf-8") as fichero:

            # Escribimos cada línea del SQL en el archivo.
            for linea in sql:
                fichero.write(linea + "\n")

        print("")
        print("Proceso terminado correctamente")
        print("Facturas correctas:", len(tickets))
        print("Empleados diferentes:", len(codigos_empleados))
        print("Productos diferentes:", len(descripciones_productos))
        print("Archivo generado: InsertUnderlineTicket.sql")

    except OSError:
        print("Error: no se ha podido crear el archivo SQL")


# 7. PROGRAMA PRINCIPAL

# sys.argv contiene los datos escritos en CMD.
if len(sys.argv) > 1:

    carpeta_facturas = sys.argv[1]

else:
    carpeta_facturas = "facturas"

# Empezamos a ejecutar el programa.
generar_sql_para_carpeta(carpeta_facturas)
