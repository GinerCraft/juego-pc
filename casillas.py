def crear_casillas():
    datos = [
        {"nombre": "SALIDA",     "tipo": "salida",    "color": (80, 200, 120)},
        {"nombre": "Casilla 1",  "tipo": "propiedad", "color": (150, 90, 50),   "precio": 80,  "alquiler": 25},
        {"nombre": "SUERTE",     "tipo": "suerte",    "color": (255, 180, 50)},
        {"nombre": "Casilla 3",  "tipo": "propiedad", "color": (150, 90, 50),   "precio": 100, "alquiler": 30},
        {"nombre": "IMPUESTO",   "tipo": "impuesto",  "color": (230, 70, 70),   "monto": 100},
        {"nombre": "Tren Sur",   "tipo": "propiedad", "color": (100, 100, 100), "precio": 200, "alquiler": 50},
        {"nombre": "Casilla 6",  "tipo": "propiedad", "color": (100, 200, 255), "precio": 120, "alquiler": 35},
        {"nombre": "Casilla 7",  "tipo": "propiedad", "color": (100, 200, 255), "precio": 140, "alquiler": 40},

        {"nombre": "CÁRCEL",     "tipo": "libre",     "color": (160, 160, 160)},
        {"nombre": "Casilla 9",  "tipo": "propiedad", "color": (230, 100, 180), "precio": 160, "alquiler": 45},
        {"nombre": "ARCA",       "tipo": "suerte",    "color": (100, 220, 255)},
        {"nombre": "Casilla 11", "tipo": "propiedad", "color": (230, 100, 180), "precio": 180, "alquiler": 50},
        {"nombre": "Tren Oeste", "tipo": "propiedad", "color": (100, 100, 100), "precio": 200, "alquiler": 50},
        {"nombre": "Casilla 13", "tipo": "propiedad", "color": (255, 140, 40),  "precio": 200, "alquiler": 60},
        {"nombre": "SUERTE",     "tipo": "suerte",    "color": (255, 180, 50)},
        {"nombre": "Casilla 15", "tipo": "propiedad", "color": (255, 140, 40),  "precio": 220, "alquiler": 65},

        {"nombre": "PARKING",    "tipo": "libre",     "color": (160, 160, 160)},
        {"nombre": "Casilla 17", "tipo": "propiedad", "color": (230, 60, 60),   "precio": 240, "alquiler": 75},
        {"nombre": "IMPUESTO",   "tipo": "impuesto",  "color": (230, 70, 70),   "monto": 120},
        {"nombre": "Casilla 19", "tipo": "propiedad", "color": (230, 60, 60),   "precio": 260, "alquiler": 80},
        {"nombre": "Tren Norte", "tipo": "propiedad", "color": (100, 100, 100), "precio": 200, "alquiler": 50},
        {"nombre": "Casilla 21", "tipo": "propiedad", "color": (240, 210, 40),  "precio": 280, "alquiler": 90},
        {"nombre": "ARCA",       "tipo": "suerte",    "color": (100, 220, 255)},
        {"nombre": "Casilla 23", "tipo": "propiedad", "color": (240, 210, 40),  "precio": 300, "alquiler": 100},

        {"nombre": "IR CÁRCEL",  "tipo": "ir_carcel", "color": (220, 50, 50)},
        {"nombre": "Casilla 25", "tipo": "propiedad", "color": (50, 180, 90),   "precio": 320, "alquiler": 110},
        {"nombre": "SUERTE",     "tipo": "suerte",    "color": (255, 180, 50)},
        {"nombre": "Casilla 27", "tipo": "propiedad", "color": (50, 180, 90),   "precio": 340, "alquiler": 120},
        {"nombre": "Tren Este",  "tipo": "propiedad", "color": (100, 100, 100), "precio": 200, "alquiler": 50},
        {"nombre": "Casilla 29", "tipo": "propiedad", "color": (50, 100, 230),  "precio": 360, "alquiler": 135},
        {"nombre": "IMPUESTO",   "tipo": "impuesto",  "color": (230, 70, 70),   "monto": 150},
        {"nombre": "Casilla 31", "tipo": "propiedad", "color": (50, 100, 230),  "precio": 400, "alquiler": 160}
    ]

    por_lado = len(datos) // 4
    paso = 78
    x_izq, x_der = 65, 65 + por_lado * paso
    y_arr, y_aba = 45, 45 + por_lado * paso


    for i, c in enumerate(datos):
        if c["tipo"] == "propiedad":
            c["dueno"] = None
        if i < por_lado:
            c["pos"] = (x_der - i * paso, y_aba)
        elif i < por_lado * 2:
            c["pos"] = (x_izq, y_aba - (i - por_lado) * paso)
        elif i < por_lado * 3:
            c["pos"] = (x_izq + (i - por_lado * 2) * paso, y_arr)
        else:
            c["pos"] = (x_der, y_arr + (i - por_lado * 3) * paso)
    return datos
