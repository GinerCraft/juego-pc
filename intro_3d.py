from ursina import *
import math

class IntroCinematica3D:
    def __init__(self, al_terminar):
        self.al_terminar = al_terminar
        self.activa = True
        self.tiempo = 0
        self.angulo_camara = 0

        # 1. Dado 3D gigante flotando en el aire durante la intro
        self.dado_promo = Entity(
            model='cube',
            scale=1.6,
            position=(0, 3.2, 0),
            color=color.gold,
            texture='white_cube',
            unlit=True
        )

        # 2. Textos flotantes sobre la escena 3D
        self.titulo1 = Text(
            text="BIENVENIDO A MI PRIMER JUEGO",
            parent=camera.ui,
            origin=(0, 0),
            y=0.32,
            scale=2.2,
            color=color.gold
        )
        self.titulo2 = Text(
            text="MONOPOLY 3D EN PYTHON",
            parent=camera.ui,
            origin=(0, 0),
            y=0.23,
            scale=1.7,
            color=color.azure
        )
        self.aviso = Text(
            text="Presiona ESPACIO para comenzar",
            parent=camera.ui,
            origin=(0, 0),
            y=-0.38,
            scale=1.3,
            color=color.white
        )

    def actualizar(self, dt):
        if not self.activa:
            return

        self.tiempo += dt
        self.angulo_camara += dt * 0.65

        # Efecto 1: La cámara orbita suavemente alrededor del tablero 3D
        radio = 17.5
        cam_x = math.sin(self.angulo_camara) * radio
        cam_z = -math.cos(self.angulo_camara) * radio
        camera.position = (cam_x, 12.5, cam_z)
        camera.look_at((0, 0.5, 0))

        # Efecto 2: El dado dorado gira y flota arriba y abajo
        self.dado_promo.rotation_y += 110 * dt
        self.dado_promo.rotation_x += 75 * dt
        self.dado_promo.y = 3.2 + math.sin(self.tiempo * 3) * 0.35

        # Efecto 3: Parpadeo del aviso inferior
        self.aviso.visible = int(self.tiempo * 2.5) % 2 == 0

        # Terminar automáticamente a los 6 segundos si no presionan tecla
        if self.tiempo >= 6.0:
            self.finalizar()

    def manejar_tecla(self, key):
        if self.activa and key in ('space', 'enter'):
            self.finalizar()
            return True
        return False

    def finalizar(self):
        if not self.activa:
            return
        self.activa = False

        # Ocultar elementos de la intro
        destroy(self.dado_promo)
        destroy(self.titulo1)
        destroy(self.titulo2)
        destroy(self.aviso)

        # Devolver la cámara suavemente a su posición de juego
        camera.animate_position((0, 16.5, -16.5), duration=0.8, curve=curve.out_quad)
        invoke(camera.look_at, (0, 0, -0.4), delay=0.81)
        self.al_terminar()
