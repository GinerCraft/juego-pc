import pygame
import sys
from casillas import crear_casillas
from dado import GestorDados
from jugadores import crear_jugadores, procesar_casilla, comprar_propiedad
from movimiento import GestorMovimiento
from personajes import SelectorPersonajes, dibujar_vehiculo
from intro import PantallaIntro


pygame.init()
ANCHO, ALTO = 1100, 820
pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE | pygame.SCALED)

pygame.display.set_caption("Monopoly Modular - 3 Jugadores")
reloj = pygame.time.Clock()

f_titulo = pygame.font.SysFont("Arial", 32, bold=True)
f_med = pygame.font.SysFont("Arial", 20, bold=True)
f_chica = pygame.font.SysFont("Arial", 14, bold=True)
f_casilla = pygame.font.SysFont("Arial", 12, bold=True)

FONDO, CENTRO = (28, 34, 42), (38, 46, 56)
BLANCO, NEGRO, DORADO = (255, 255, 255), (20, 20, 20), (255, 215, 0)

tablero = crear_casillas()
jugadores = crear_jugadores()
dados = GestorDados()
movimiento = GestorMovimiento(jugadores, tablero)
selector = SelectorPersonajes()
intro = PantallaIntro(ANCHO, ALTO)
turno = 0
fase = "INTRO"
mensaje = "Turno de J1 (Azul): Presiona ESPACIO para tirar los dados"

def avanzar_turno():
    global turno, fase, mensaje
    activos = [j for j in jugadores if j["activo"]]
    if len(activos) == 1:
        fase = "FIN"
        mensaje = f"¡VICTORIA! {activos[0]['nombre']} gana la partida."
        return

    for _ in range(3):
        turno = (turno + 1) % 3
        if jugadores[turno]["activo"]:
            break

    dados.girando = True
    fase = "GIRANDO"
    mensaje = f"Turno de {jugadores[turno]['nombre']}: Presiona ESPACIO"
def obtener_acomodo_casilla(jugador, todos_jugadores):
    # Buscar qué jugadores activos están en esta misma casilla
    en_misma_casilla = [j for j in todos_jugadores if j["activo"] and j["casilla"] == jugador["casilla"]]
    cantidad = len(en_misma_casilla)

    if cantidad == 1:
        return (0, 4, 1.25)  # Solo: centrado y tamaño grande

    indice = en_misma_casilla.index(jugador)
    if cantidad == 2:
        posiciones = [(-16, 4), (16, 4)]  # Lado a lado
        return (posiciones[indice][0], posiciones[indice][1], 0.95)
    else:
        posiciones = [(-16, -2), (16, -2), (0, 14)]  # En triángulo
        return (posiciones[indice][0], posiciones[indice][1], 0.85)


while True:
    dt = reloj.tick(60)
    j_actual = jugadores[turno]

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        # Este bloque debe ir PRIMERO
        if fase == "INTRO":
            intro.manejar_evento(ev)
        elif fase == "SELECCION":
            selector.manejar_evento(ev, jugadores)
            if selector.completado:
                fase = "GIRANDO"
        elif ev.type == pygame.KEYDOWN:
            if fase == "GIRANDO" and ev.key == pygame.K_SPACE:
                total_dados = dados.frenar()
                movimiento.iniciar(total_dados)
                fase = "MOVIENDO"
                mensaje = f"¡Salió {total_dados}! Avanzando..."
            elif fase == "COMPRAR":
                if ev.key == pygame.K_c:
                    comprar_propiedad(j_actual, tablero)
                    avanzar_turno()
                elif ev.key == pygame.K_p:
                    avanzar_turno()

    # Pantalla de selección de vehículos
    if fase == "INTRO":
        intro.actualizar(dt)
        intro.dibujar(pantalla, f_titulo, f_med)
        if intro.terminada:
            fase = "SELECCION"
        pygame.display.flip()
        continue
    if fase == "SELECCION":
        selector.dibujar(pantalla, jugadores, f_titulo, f_med)
        pygame.display.flip()
        continue


    if fase == "GIRANDO":
        dados.actualizar(dt)
    elif fase == "MOVIENDO":
        termino = movimiento.actualizar(j_actual, tablero)
        if termino:
            siguiente_fase, mensaje = procesar_casilla(j_actual, jugadores, tablero)
            cx, cy = tablero[j_actual["casilla"]]["pos"]
            ox, oy = j_actual["offset"]
            j_actual["x"] = float(cx + ox)
            j_actual["y"] = float(cy + oy)

            if siguiente_fase == "COMPRAR":
                fase = "COMPRAR"
            else:
                avanzar_turno()

    pantalla.fill(FONDO)
    pygame.draw.rect(pantalla, CENTRO, (120, 100, 544, 544), border_radius=12)

    for c in tablero:
        cx, cy = c["pos"]
        pygame.draw.rect(pantalla, BLANCO, (cx - 40, cy - 40, 80, 80), border_radius=6)
        pygame.draw.rect(pantalla, NEGRO, (cx - 40, cy - 40, 80, 80), 2, border_radius=6)
        pygame.draw.rect(pantalla, c["color"], (cx - 38, cy - 38, 76, 16), border_top_left_radius=4, border_top_right_radius=4)

        txt = f_casilla.render(c["nombre"], True, NEGRO)
        pantalla.blit(txt, (cx - txt.get_width() // 2, cy - 19))

        if c["tipo"] == "propiedad":
            pr = f_casilla.render(f"${c['precio']}", True, (60, 60, 60))
            pantalla.blit(pr, (cx - pr.get_width() // 2, cy + 18))
            if c["dueno"] is not None:
                pygame.draw.rect(pantalla, jugadores[c["dueno"]]["color"], (cx - 30, cy + 9, 60, 7), border_radius=2)




        

    # Dibujar el vehículo elegido de cada jugador
    for i, j in enumerate(jugadores):
        if j["activo"]:
            paso_y = movimiento.obtener_balanceo() if (i == turno and fase == "MOVIENDO") else 0

            # Si está detenido, aplicar acomodo dinámico; si está caminando, usar su ruta suave
            if i == turno and fase == "MOVIENDO":
                px, py, escala = int(j["x"]), int(j["y"] + paso_y), 1.25
            else:
                cx, cy = tablero[j["casilla"]]["pos"]
                dx, dy, escala = obtener_acomodo_casilla(j, jugadores)
                px, py = cx + dx, cy + dy

            dibujar_vehiculo(pantalla, j["vehiculo"], px, py, j["color"], escala=escala)
            if i == turno and fase == "MOVIENDO":
                movimiento.dibujar_contador(pantalla, f_chica, px, py)


    t1 = f_titulo.render("MONOPOLY", True, DORADO)
    pantalla.blit(t1, (392 - t1.get_width() // 2, 310))
    dados.dibujar(pantalla, 392, 365)

    for i, j in enumerate(jugadores):
        yp = 60 + i * 210
        borde = j["color"] if (i == turno and fase != "FIN") else (60, 70, 85)
        pygame.draw.rect(pantalla, CENTRO, (780, yp, 280, 180), border_radius=10)
        pygame.draw.rect(pantalla, borde, (780, yp, 280, 180), 3, border_radius=10)

        pantalla.blit(f_med.render(j["nombre"], True, j["color"]), (800, yp + 20))
        dibujar_vehiculo(pantalla, j["vehiculo"], 1015, yp + 32, j["color"], escala=1.4)
        pantalla.blit(f_titulo.render(f"${j['dinero']}" if j["activo"] else "ELIMINADO", True, DORADO), (800, yp + 65))
        pantalla.blit(f_chica.render(f"Casilla: {tablero[j['casilla']]['nombre']}", True, BLANCO), (800, yp + 125))

    pygame.draw.rect(pantalla, (20, 24, 30), (0, 755, ANCHO, 65))
    msg = f_med.render(mensaje, True, BLANCO)
    pantalla.blit(msg, (ANCHO // 2 - msg.get_width() // 2, 775))

    pygame.display.flip()
