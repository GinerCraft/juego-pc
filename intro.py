import pygame
import random

class PantallaIntro:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.alpha = 0           # Transparencia del texto (0 = invisible, 255 = sólido)
        self.tiempo = 0
        self.terminada = False

        # Partículas decorativas en el fondo
        self.particulas = [
            [random.randint(0, ancho), random.randint(0, alto), random.uniform(0.5, 2.0), random.randint(2, 5)]
            for _ in range(35)
        ]

    def manejar_evento(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_SPACE, pygame.K_RETURN):
                self.terminada = True

    def actualizar(self, dt):
        self.tiempo += dt

        # Efecto de aparición suave (fade-in)
        if self.alpha < 255:
            self.alpha = min(255, self.alpha + 3)

        # Mover partículas hacia arriba
        for p in self.particulas:
            p[1] -= p[2]
            if p[1] < 0:
                p[1] = self.alto
                p[0] = random.randint(0, self.ancho)

        # Avanzar automáticamente después de 4.5 segundos (4500 ms)
        if self.tiempo >= 4500:
            self.terminada = True

    def dibujar(self, pantalla, f_titulo, f_med):
        pantalla.fill((20, 24, 32))

        # 1. Dibujar partículas doradas flotando
        for px, py, _, radio in self.particulas:
            pygame.draw.circle(pantalla, (60, 75, 100), (int(px), int(py)), radio)

        # 2. Crear superficie con transparencia para el título principal
        txt_linea1 = f_titulo.render("BIENVENIDO A MI PRIMER JUEGO", True, (255, 215, 0))
        txt_linea2 = f_titulo.render("PROGRAMADO EN PYTHON", True, (0, 190, 255))

        txt_linea1.set_alpha(self.alpha)
        txt_linea2.set_alpha(self.alpha)

        # Efecto de leve desplazamiento hacia arriba al aparecer
        desplazamiento_y = int((255 - self.alpha) * 0.12)

        pantalla.blit(txt_linea1, (self.ancho // 2 - txt_linea1.get_width() // 2, 310 + desplazamiento_y))
        pantalla.blit(txt_linea2, (self.ancho // 2 - txt_linea2.get_width() // 2, 365 + desplazamiento_y))

        # 3. Texto parpadeante abajo cuando ya apareció el título
        if self.alpha >= 200 and (self.tiempo // 400) % 2 == 0:
            txt_saltar = f_med.render("Presiona ESPACIO para continuar", True, (180, 190, 210))
            pantalla.blit(txt_saltar, (self.ancho // 2 - txt_saltar.get_width() // 2, 520))
