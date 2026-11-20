import pygame
import os

OPCIONES = ["Personaje 1", "Personaje 2", "Personaje 3"]
CACHE_FICHAS = {}

def cargar_ficha_circular(ruta, radio, color_borde, modo="centro"):
    clave = (ruta, radio, color_borde, modo)
    if clave in CACHE_FICHAS:
        return CACHE_FICHAS[clave]

    tam = radio * 2
    superficie = pygame.Surface((tam, tam), pygame.SRCALPHA)

    if os.path.exists(ruta):
        img = pygame.image.load(ruta).convert_alpha()
        ancho_img, alto_img = img.get_size()

        if modo == "zoom_abajo":
            lado = int(min(ancho_img, alto_img) * 0.42)
            x_recorte = int(ancho_img * 0.46) - lado // 2
            y_recorte = int(alto_img * 0.62) - lado // 2
        elif modo == "derecha":
            lado = min(ancho_img, alto_img)
            x_recorte = ancho_img - lado
            y_recorte = 0
        else:
            lado = min(ancho_img, alto_img)
            x_recorte = (ancho_img - lado) // 2
            y_recorte = 0

        x_recorte = max(0, min(ancho_img - lado, x_recorte))
        y_recorte = max(0, min(alto_img - lado, y_recorte))

        img_cuadrada = img.subsurface((x_recorte, y_recorte, lado, lado))
        img_escalada = pygame.transform.smoothscale(img_cuadrada, (tam, tam))

        mascara = pygame.Surface((tam, tam), pygame.SRCALPHA)
        pygame.draw.circle(mascara, (255, 255, 255, 255), (radio, radio), radio - 2)
        superficie.blit(img_escalada, (0, 0))
        superficie.blit(mascara, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    else:
        pygame.draw.circle(superficie, color_borde, (radio, radio), radio - 2)

    pygame.draw.circle(superficie, color_borde, (radio, radio), radio - 1, max(2, radio // 8))
    CACHE_FICHAS[clave] = superficie
    return superficie

def dibujar_vehiculo(pantalla, tipo, cx, cy, color, escala=1.0):
    radio = max(10, int(14 * escala))

    if tipo == "Personaje 1":
        ficha = cargar_ficha_circular("personaje1.png", radio, color, "centro")
    elif tipo == "Personaje 2":
        ficha = cargar_ficha_circular("personaje2.png", radio, color, "derecha")
    else:
        ficha = cargar_ficha_circular("personaje3.png", radio, color, "zoom_abajo")

    pantalla.blit(ficha, (int(cx - radio), int(cy - radio)))

class SelectorPersonajes:
    def __init__(self):
        self.jugador_actual = 0
        self.indice_opcion = 0
        self.completado = False

    def manejar_evento(self, evento, jugadores):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                self.indice_opcion = (self.indice_opcion - 1) % len(OPCIONES)
            elif evento.key == pygame.K_RIGHT:
                self.indice_opcion = (self.indice_opcion + 1) % len(OPCIONES)
            elif evento.key == pygame.K_RETURN:
                jugadores[self.jugador_actual]["vehiculo"] = OPCIONES[self.indice_opcion]
                self.jugador_actual += 1
                if self.jugador_actual >= len(jugadores):
                    self.completado = True

    def dibujar(self, pantalla, jugadores, f_titulo, f_med):
        pantalla.fill((28, 34, 42))
        j = jugadores[self.jugador_actual]

        titulo = f_titulo.render("ELIGE TU PERSONAJE", True, (255, 215, 0))
        turno_txt = f_med.render(f"Turno de {j['nombre']} — Usa FLECHAS y presiona ENTER", True, j["color"])
        pantalla.blit(titulo, (550 - titulo.get_width() // 2, 100))
        pantalla.blit(turno_txt, (550 - turno_txt.get_width() // 2, 160))

        for i, nombre_op in enumerate(OPCIONES):
            cx = 270 + i * 280
            cy = 380
            seleccionado = (i == self.indice_opcion)
            borde = j["color"] if seleccionado else (60, 70, 85)

            pygame.draw.rect(pantalla, (38, 46, 56), (cx - 110, cy - 110, 220, 220), border_radius=14)
            pygame.draw.rect(pantalla, borde, (cx - 110, cy - 110, 220, 220), 4 if seleccionado else 2, border_radius=14)

            dibujar_vehiculo(pantalla, nombre_op, cx, cy - 15, j["color"], escala=3.5)
            txt = f_med.render(nombre_op, True, (255, 255, 255))
            pantalla.blit(txt, (cx - txt.get_width() // 2, cy + 60))
