import random

def crear_jugadores():
    return [
        {"id": 0, "nombre": "J1 (Azul)",  "color": (0, 190, 255), "casilla": 0, "dinero": 1000, "activo": True, "offset": (0, 4), "vehiculo": "Auto"},
        {"id": 1, "nombre": "J2 (Rojo)",  "color": (255, 75, 75), "casilla": 0, "dinero": 1000, "activo": True, "offset": (0, 4), "vehiculo": "Barco"},
        {"id": 2, "nombre": "J3 (Verde)", "color": (70, 230, 100),"casilla": 0, "dinero": 1000, "activo": True, "offset": (0, 4), "vehiculo": "Helicóptero"}
    ]


def verificar_bancarrota(jugador, tablero):
    if jugador["dinero"] <= 0:
        jugador["dinero"] = 0
        jugador["activo"] = False
        for c in tablero:
            if c.get("dueno") == jugador["id"]:
                c["dueno"] = None

def procesar_casilla(jugador, jugadores, tablero):
    """Evalúa la casilla donde cayó el jugador y devuelve (siguiente_fase, mensaje)."""
    c = tablero[jugador["casilla"]]
    tipo = c["tipo"]

    if tipo == "propiedad":
        if c["dueno"] is None:
            if jugador["dinero"] >= c["precio"]:
                return "COMPRAR", f"¿Comprar {c['nombre']} por ${c['precio']}?  [C] Comprar  |  [P] Pasar"
            return "SIGUIENTE", f"{jugador['nombre']} no tiene dinero para {c['nombre']}."

        elif c["dueno"] != jugador["id"]:
            dueno = jugadores[c["dueno"]]
            jugador["dinero"] -= c["alquiler"]
            dueno["dinero"] += c["alquiler"]
            verificar_bancarrota(jugador, tablero)
            return "SIGUIENTE", f"{jugador['nombre']} pagó ${c['alquiler']} a {dueno['nombre']}."

        return "SIGUIENTE", f"{jugador['nombre']} cayó en su propia propiedad."

    elif tipo == "impuesto":
        jugador["dinero"] -= c["monto"]
        verificar_bancarrota(jugador, tablero)
        return "SIGUIENTE", f"{jugador['nombre']} pagó ${c['monto']} de impuestos."

    elif tipo == "suerte":
        premio = random.choice([-100, -50, 50, 100, 200])
        jugador["dinero"] += premio
        verificar_bancarrota(jugador, tablero)
        accion = "ganó" if premio > 0 else "perdió"
        return "SIGUIENTE", f"¡SUERTE! {jugador['nombre']} {accion} ${abs(premio)}."

    elif tipo == "ir_carcel":
        jugador["casilla"] = len(tablero) // 4
        return "SIGUIENTE", f"¡{jugador['nombre']} fue enviado directo a la CÁRCEL!"

    return "SIGUIENTE", f"{jugador['nombre']} descansa en {c['nombre']}."

def comprar_propiedad(jugador, tablero):
    c = tablero[jugador["casilla"]]
    jugador["dinero"] -= c["precio"]
    c["dueno"] = jugador["id"]
