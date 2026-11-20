import pygame
import math

class GestorMovimiento:
    def __init__(self, jugadores, tablero):
        self.pasos_restantes = 0
        self.velocidad = 6.0
        self.distancia_recorrida = 0

        for j in jugadores:
            cx, cy = tablero[j["casilla"]]["pos"]
            ox, oy = j["offset"]
            j["x"] = float(cx + ox)
            j["y"] = float(cy + oy)

    def iniciar(self, pasos):
        self.pasos_restantes = pasos
        self.distancia_recorrida = 0

    def actualizar(self, jugador, tablero):
        if self.pasos_restantes <= 0:
            return True

        siguiente_indice = (jugador["casilla"] + 1) % len(tablero)
        tx, ty = tablero[siguiente_indice]["pos"]
        ox, oy = jugador["offset"]
        dest_x = tx + ox
        dest_y = ty + oy

        dx = dest_x - jugador["x"]
        dy = dest_y - jugador["y"]
        distancia = math.hypot(dx, dy)

        if distancia <= self.velocidad:
            jugador["x"] = float(dest_x)
            jugador["y"] = float(dest_y)
            jugador["casilla"] = siguiente_indice
            self.pasos_restantes -= 1

            if jugador["casilla"] == 0:
                jugador["dinero"] += 200
        else:
            jugador["x"] += (dx / distancia) * self.velocidad
            jugador["y"] += (dy / distancia) * self.velocidad
            self.distancia_recorrida += self.velocidad

        return self.pasos_restantes == 0

    def obtener_balanceo(self):
        if self.pasos_restantes > 0:
            return abs(math.sin(self.distancia_recorrida * 0.15)) * -4
        return 0

    def dibujar_contador(self, pantalla, fuente, x, y):
        if self.pasos_restantes > 0:
            burbuja = pygame.Rect(int(x) - 12, int(y) - 36, 24, 20)
            pygame.draw.rect(pantalla, (255, 215, 0), burbuja, border_radius=6)
            pygame.draw.rect(pantalla, (20, 20, 20), burbuja, 2, border_radius=6)
            txt = fuente.render(str(self.pasos_restantes), True, (20, 20, 20))
            pantalla.blit(txt, (burbuja.centerx - txt.get_width() // 2, burbuja.centery - txt.get_height() // 2))
