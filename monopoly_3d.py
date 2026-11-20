from ursina import *
import random
import sys
import math
from casillas import crear_casillas

app = Ursina(title="Monopoly 3D - 3 Jugadores", borderless=False)

window.color = color.hex('#141c26')
base.win.setClearColor(Vec4(0.08, 0.11, 0.15, 1)) # type: ignore

# Base central del tablero 3D
tablero_base = Entity(
    model='cube',
    scale=(10.5, 0.3, 10.5),
    position=(0, -0.15, 0),
    color=color.hex('#26303e'),
    unlit=True
)

datos_casillas = crear_casillas()
casillas_3d = []
paso = 1.15
inicio = -4.6
colores_grupo = [
    color.green, color.brown, color.orange, color.brown,
    color.red, color.gray, color.azure, color.azure
]

for i in range(32):
    if i < 8:
        x, z = -inicio - i * paso, inicio
    elif i < 16:
        x, z = inicio, inicio + (i - 8) * paso
    elif i < 24:
        x, z = inicio + (i - 16) * paso, -inicio
    else:
        x, z = -inicio, -inicio - (i - 24) * paso

    bloque = Entity(
        model='cube',
        scale=(1.05, 0.25, 1.05),
        position=(x, 0.12, z),
        color=color.hex('#d8dde6'),
        texture='white_cube',
        unlit=True
    )
    Entity(
        parent=bloque,
        model='cube',
        scale=(0.95, 0.12, 0.25),
        position=(0, 0.52, 0.32),
        color=colores_grupo[i % len(colores_grupo)],
        unlit=True
    )

    info = datos_casillas[i]
    etiqueta = info["nombre"]
    if info["tipo"] == "propiedad":
        etiqueta += f"\n${info['precio']}"

    Text(
        parent=bloque,
        text=etiqueta,
        position=(0, 0.65, -0.08),
        rotation_x=90,
        scale=6.5,
        origin=(0, 0),
        color=color.black
    )
    casillas_3d.append(bloque)

# Crear los 3 jugadores con tus fotos
jugadores = [
    {"nombre": "J1 (Azul)",  "color": color.azure, "casilla": 0, "dinero": 1000, "offset": (-0.22, 0.22), "tex": "personaje1.png"},
    {"nombre": "J2 (Rojo)",  "color": color.red,   "casilla": 0, "dinero": 1000, "offset": (0.22, 0.22),  "tex": "personaje2.png"},
    {"nombre": "J3 (Verde)", "color": color.green, "casilla": 0, "dinero": 1000, "offset": (0, -0.22),    "tex": "personaje3.png"}
]

primera = casillas_3d[0]
for j in jugadores:
    cx, _, cz = primera.position
    ox, oz = j["offset"]

    # Base cilíndrica del color del jugador
    ficha = Entity(
        model='cylinder',
        scale=(0.48, 0.16, 0.48),
        position=(cx + ox, 0.32, cz + oz),
        color=j["color"],
        unlit=True
    )

    # Marco cuadrado con relieve del color del jugador
    Entity(
        parent=ficha,
        model='cube',
        position=(0, 0.52, 0),
        scale=(0.82, 0.08, 0.82),
        color=j["color"],
        unlit=True
    )

    # Foto centrada un poco más arriba para que sobresalga toda la orilla de color
    Entity(
        parent=ficha,
        model='quad',
        rotation_x=90,
        position=(0, 0.58, 0),
        scale=0.64,
        texture=j["tex"],
        unlit=True
    )
    j["entidad"] = ficha



# Dados 3D con puntos reales
def crear_dado_3d(posicion):
    dado = Entity(model='cube', scale=0.8, position=posicion, color=color.white, texture='white_cube', unlit=True)
    caras = {
        1: ((0, 0.51, 0), (90, 0, 0), [(0, 0)]),
        6: ((0, -0.51, 0), (-90, 0, 0), [(-0.25, -0.25), (0.25, -0.25), (-0.25, 0), (0.25, 0), (-0.25, 0.25), (0.25, 0.25)]),
        2: ((0, 0, 0.51), (0, 0, 0), [(-0.22, 0.22), (0.22, -0.22)]),
        5: ((0, 0, -0.51), (0, 180, 0), [(-0.24, 0.24), (0.24, 0.24), (0, 0), (-0.24, -0.24), (0.24, -0.24)]),
        3: ((0.51, 0, 0), (0, 90, 0), [(-0.24, 0.24), (0, 0), (0.24, -0.24)]),
        4: ((-0.51, 0, 0), (0, -90, 0), [(-0.22, 0.22), (0.22, 0.22), (-0.22, -0.22), (0.22, -0.22)])
    }
    for num, (pos_cara, rot_cara, puntos) in caras.items():
        contenedor = Entity(parent=dado, position=pos_cara, rotation=rot_cara)
        for px, py in puntos:
            Entity(parent=contenedor, model='circle', scale=0.17, position=(px, py, 0), color=color.black, double_sided=True, unlit=True)
    return dado

ROTACIONES_DADO = {
    1: (0, 0, 0),
    6: (180, 0, 0),
    2: (90, 0, 0),
    5: (-90, 0, 0),
    3: (0, 0, 90),
    4: (0, 0, -90)
}

dado1 = crear_dado_3d((-0.65, 0.7, 0))
dado2 = crear_dado_3d((0.65, 0.7, 0))
dado_girando = True
moviendo = False


# --- PANTALLA DE INTRO Y SELECCIÓN APARTE ---
estado_juego = "INTRO"
tiempo_intro = 0
sel_jugador = 0
sel_opcion = 0
opciones_personajes = [
    {"nombre": "Personaje 1", "tex": "personaje1.png"},
    {"nombre": "Personaje 2", "tex": "personaje2.png"},
    {"nombre": "Personaje 3", "tex": "personaje3.png"}
]

# Fondo negro/azul sólido que cubre toda la pantalla (tapa el tablero 3D)
pantalla_negra = Entity(parent=camera.ui, model='quad', scale=(2.5, 1.5), color=color.hex('#141c26'), z=-5)

# Textos de Intro
txt_intro_1 = Text("BIENVENIDO A MI PRIMER JUEGO", origin=(0, 0), y=0.08, scale=2.2, color=color.gold, z=-6)
txt_intro_2 = Text("PROGRAMADO EN PYTHON 3D", origin=(0, 0), y=-0.02, scale=1.6, color=color.azure, z=-6)
txt_intro_3 = Text("Presiona ESPACIO para continuar", origin=(0, 0), y=-0.20, scale=1.2, color=color.white, z=-6)

# Elementos de Selección de Personaje (ocultos al inicio)
txt_sel_titulo = Text("ELIGE TU PERSONAJE", origin=(0, 0), y=0.35, scale=2.0, color=color.gold, z=-6, enabled=False)
txt_sel_turno = Text("", origin=(0, 0), y=0.25, scale=1.3, z=-6, enabled=False)

marcos_sel = []
bordes_fotos = []
items_sel = []

for i, op in enumerate(opciones_personajes):
    x_pos = -0.45 + i * 0.45
    marco = Entity(parent=camera.ui, model='quad', scale=(0.36, 0.44), position=(x_pos, -0.02, -5.0), color=color.hex('#26303e'), enabled=False)

    # Orilla gruesa de color alrededor de la foto
    borde_foto = Entity(parent=camera.ui, model='quad', scale=0.265, position=(x_pos, 0.03, -5.5), color=color.azure, enabled=False)

    # Foto encima del borde
    foto = Entity(
        parent=camera.ui,
        model='quad',
        scale=0.22,
        position=(x_pos, 0.03, -6.0),
        texture=op["tex"],
        enabled=False
    )
    nombre_op = Text(op["nombre"], origin=(0, 0), position=(x_pos, -0.16, -6.0), scale=1.2, enabled=False)
    marcos_sel.append(marco)
    bordes_fotos.append(borde_foto)
    items_sel.extend([marco, borde_foto, foto, nombre_op])




# Cámara fija mirando al tablero desde el inicio (sin girar)
camera.position = (0, 16.5, -16.5)
camera.look_at((0, 0, -0.4))

turno = 0
texto_estado = Text(text="Turno de J1 (Azul) — Presiona ESPACIO para tirar", position=(-0.48, 0.44), scale=1.3, color=color.yellow, enabled=False)

def pasar_a_seleccion():
    global estado_juego
    estado_juego = "SELECCION"
    destroy(txt_intro_1)
    destroy(txt_intro_2)
    destroy(txt_intro_3)
    txt_sel_titulo.enabled = True
    txt_sel_turno.enabled = True
    for item in items_sel:
        item.enabled = True
    actualizar_visual_seleccion()

def actualizar_visual_seleccion():
    j = jugadores[sel_jugador]
    txt_sel_turno.text = f"Turno de {j['nombre']} — Usa FLECHAS y presiona ENTER"
    txt_sel_turno.color = j["color"]
    for i, m in enumerate(marcos_sel):
        m.color = color.hex('#324054') if i == sel_opcion else color.hex('#1e2633')
        bordes_fotos[i].color = j["color"] if i == sel_opcion else color.gray



def empezar_tablero():
    global estado_juego
    estado_juego = "JUGANDO"
    destroy(pantalla_negra)
    destroy(txt_sel_titulo)
    destroy(txt_sel_turno)
    for item in items_sel:
        destroy(item)
    texto_estado.enabled = True

def update():
    global tiempo_intro
    if estado_juego == "INTRO":
        tiempo_intro += time.dt
        txt_intro_3.visible = int(tiempo_intro * 2.5) % 2 == 0
        if tiempo_intro >= 4.5:
            pasar_a_seleccion()
        return

    if estado_juego == "JUGANDO" and dado_girando:
        dado1.rotation_x += 220 * time.dt
        dado1.rotation_y += 280 * time.dt
        dado2.rotation_x -= 250 * time.dt
        dado2.rotation_z += 210 * time.dt

def mover_paso_a_paso(jugador, pasos_restantes):
    global turno, dado_girando, moviendo

    if pasos_restantes <= 0:
        moviendo = False
        turno = (turno + 1) % 3
        texto_estado.text = f"Turno de {jugadores[turno]['nombre']} — Presiona ESPACIO para tirar"
        dado_girando = True
        return

    # Avanzar exactamente 1 casilla
    jugador["casilla"] = (jugador["casilla"] + 1) % len(casillas_3d)
    if jugador["casilla"] == 0:
        jugador["dinero"] += 200

    cx, _, cz = casillas_3d[jugador["casilla"]].position
    ox, oz = jugador["offset"]
    ent = jugador["entidad"]

    # Deslizar en X/Z y hacer un salto vertical en Y
    ent.animate_x(cx + ox, duration=0.22, curve=curve.linear)
    ent.animate_z(cz + oz, duration=0.22, curve=curve.linear)
    ent.animate_y(0.75, duration=0.11, curve=curve.out_quad)
    invoke(ent.animate_y, 0.32, duration=0.11, curve=curve.in_quad, delay=0.11)

    # Llamar al siguiente paso en 0.25 segundos
    invoke(mover_paso_a_paso, jugador, pasos_restantes - 1, delay=0.25)


def input(key):
    global turno, dado_girando, sel_jugador, sel_opcion, moviendo

    if estado_juego == "INTRO":
        if key in ('space', 'enter'):
            pasar_a_seleccion()
        return

    if estado_juego == "SELECCION":
        if key == 'left arrow':
            sel_opcion = (sel_opcion - 1) % 3
            actualizar_visual_seleccion()
        elif key == 'right arrow':
            sel_opcion = (sel_opcion + 1) % 3
            actualizar_visual_seleccion()
        elif key == 'enter':
            # Cambiar la foto de la ficha 3D por la que eligió el jugador
            tex_elegida = opciones_personajes[sel_opcion]["tex"]
            ficha_actual = jugadores[sel_jugador]["entidad"]
            for hijo in ficha_actual.children:
                hijo.texture = tex_elegida

            sel_jugador += 1
            if sel_jugador >= 3:
                empezar_tablero()
            else:
                actualizar_visual_seleccion()
        return

    if estado_juego == "JUGANDO" and key == 'space' and dado_girando and not moviendo:
        dado_girando = False
        moviendo = True
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        valor = d1 + d2

        dado1.rotation = ROTACIONES_DADO[d1]
        dado2.rotation = ROTACIONES_DADO[d2]

        j = jugadores[turno]
        texto_estado.text = f"{j['nombre']} sacó {d1} + {d2} = {valor}. Avanzando..."
        invoke(mover_paso_a_paso, j, valor, delay=0.45)



        

app.run()
