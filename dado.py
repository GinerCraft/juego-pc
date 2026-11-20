import pygame
import random

class GestorDados:
    def __init__(self):
        self.d1 = 1
        self.d2 = 1
        self.girando = True
        self.timer = 0

    def actualizar(self, dt):
        if self.girando:
            self.timer += dt
            if self.timer >= 65:
                self.d1 = random.randint(1, 6)
                self.d2 = random.randint(1, 6)
                self.timer = 0

    def frenar(self):
        self.d1 = random.randint(1, 6)
        self.d2 = random.randint(1, 6)
        self.girando = False
        return self.d1 + self.d2

    def dibujar(self, pantalla, cx, cy):
        self._dibujar_uno(pantalla, cx - 64, cy, self.d1)
        self._dibujar_uno(pantalla, cx + 8, cy, self.d2)

    def _dibujar_uno(self, pantalla, x, y, valor):
        if self.girando:
            x += random.randint(-4, 4)
            y += random.randint(-4, 4)

        rect = pygame.Rect(x, y, 56, 56)
        pygame.draw.rect(pantalla, (255, 255, 255), rect, border_radius=10)
        borde = (255, 215, 0) if self.girando else (20, 20, 20)
        pygame.draw.rect(pantalla, borde, rect, 3, border_radius=10)

        cx, cy = x + 28, y + 28
        izq, der = x + 14, x + 42
        arr, aba = y + 14, y + 42

        puntos = {
            1: [(cx, cy)],
            2: [(izq, arr), (der, aba)],
            3: [(izq, arr), (cx, cy), (der, aba)],
            4: [(izq, arr), (der, arr), (izq, aba), (der, aba)],
            5: [(izq, arr), (der, arr), (cx, cy), (izq, aba), (der, aba)],
            6: [(izq, arr), (der, arr), (izq, cy), (der, cy), (izq, aba), (der, aba)]
        }
        for px, py in puntos[valor]:
            pygame.draw.circle(pantalla, (20, 20, 20), (px, py), 5)
