"""Plantilla del juego Arkanoid para el hito M2.

Completa los métodos marcados con TODO respetando las anotaciones de tipo y la
estructura de la clase. El objetivo es construir un prototipo jugable usando
pygame que cargue bloques desde un fichero de nivel basado en caracteres.
"""
from arkanoid_core import *
# --------------------------------------------------------------------- #
# Métodos a completar por el alumnado
# --------------------------------------------------------------------- #

@arkanoid_method
def cargar_nivel(self) -> list[str]:
    ruta = Path(self.level_path)

    if not ruta.exists():
        raise FileNotFoundError("No se encontro el nivel" + str(ruta))
    
    texto = ruta.read_text(encoding="utf-8")
    filas = texto.splitlines()

    filas_sin_vacias =[]
    for fila in filas:
        if fila.strip() != "":
            filas_sin_vacias.append(fila)
    if len(filas_sin_vacias) == 0:
        raise ValueError("El nivel esta vacio")
    ancho = len(filas_sin_vacias[0])

    for fila in filas_sin_vacias:
        if len(fila) != ancho:
            raise ValueError("Todas las filas deben de tener el mismo ancho")

    self.layout = filas_sin_vacias
    return filas_sin_vacias;    

@arkanoid_method
def preparar_entidades(self) -> None:
    ancho = self.PADDLE_WIDTH 
    alto = self.PADDLE_HEIGHT

    x = self.WIDTH // 2 - ancho // 2 
    y = self.HEIGHT - alto - 20

    self.paddle = self.crear_rect(x, y, ancho, alto)

    self.score = 0
    self.lives = self.LIVES
    self.end_message = ""

    self.ball_pos = Vector2(0, 0)
    self.reiniciar_bola()

@arkanoid_method
def crear_bloques(self) -> None:
    """Genera los rectángulos de los bloques en base a la cuadrícula."""
    self.blocks.clear()
    self.block_colors.clear()
    self.block_symbols.clear()

    for fila_idx, fila in enumerate(self.layout):
        for col_idx, simbolo in enumerate(fila):
            if simbolo == '.':
                continue
            rect = self.calcular_posicion_bloque(fila_idx, col_idx)
            self.blocks.append(rect)
            self.block_colors.append(self.BLOCK_COLORS.get(simbolo, (200, 200, 200)))
            self.block_symbols.append(simbolo)

@arkanoid_method
def procesar_input(self) -> None:
   teclas = self.obtener_estado_teclas()
    desplazamiento = 0

    if teclas[self.KEY_LEFT] or teclas[self.KEY_A]:
        desplazamiento -= self.PADDLE_SPEED
    if teclas[self.KEY_RIGHT] or teclas[self.KEY_D]:
        desplazamiento += self.PADDLE_SPEED

    self.paddle.x += desplazamiento

    # Limitar dentro de la pantalla
    if self.paddle.left < 0:
        self.paddle.left = 0
    if self.paddle.right > self.SCREEN_WIDTH:
        self.paddle.right = self.SCREEN_WIDTH


@arkanoid_method
def actualizar_bola(self: ArkanoidGame) -> None:
    # 1) Mover la bola según su velocidad actual
    self.ball_pos += self.ball_velocity

    # Rectángulo de la bola para comprobar colisiones
    ball_rect = self.obtener_rect_bola()

    # 2) Rebote con paredes izquierda y derecha
    if ball_rect.left <= 0 or ball_rect.right >= self.SCREEN_WIDTH:
        self.ball_velocity.x *= -1  # invertimos la velocidad horizontal

        # Recolocamos la bola dentro de la pantalla para que no se quede pegada
        if ball_rect.left < 0:
            self.ball_pos.x = self.BALL_RADIUS
        elif ball_rect.right > self.SCREEN_WIDTH:
            self.ball_pos.x = self.SCREEN_WIDTH - self.BALL_RADIUS

        ball_rect = self.obtener_rect_bola()

    # 3) Rebote con el techo
    if ball_rect.top <= 0:
        self.ball_velocity.y *= -1  # invertimos la velocidad vertical
        self.ball_pos.y = self.BALL_RADIUS
        ball_rect = self.obtener_rect_bola()

    # 4) Si la bola se cae por abajo: perdemos una vida
    if ball_rect.top >= self.SCREEN_HEIGHT:
        self.lives -= 1
        if self.lives > 0:
            self.reiniciar_bola()
        else:
            self.running = False
            self.end_message = "GAME OVER"
        return  # ya no seguimos comprobando colisiones en este frame

    # 5) Colisión con la paleta
    if self.paddle is not None and ball_rect.colliderect(self.paddle):
        # Colocamos la bola justo encima de la paleta
        self.ball_pos.y = self.paddle.top - self.BALL_RADIUS - 1
        self.ball_velocity.y *= -1  # rebote vertical

        # (Opcional) Pequeño efecto según dónde golpee en la paleta
        offset = (ball_rect.centerx - self.paddle.centerx) / (self.paddle.width / 2)
        self.ball_velocity.x += offset  # ajusta ligeramente vx

        ball_rect = self.obtener_rect_bola()

    # 6) Colisión con bloques
    indice_golpeado = -1

    for i, rect_bloque in enumerate(self.blocks):
        if ball_rect.colliderect(rect_bloque):
            indice_golpeado = i
            # Rebote simple: invertimos la velocidad vertical
            self.ball_velocity.y *= -1
            break

    # 7) Si hemos golpeado un bloque, lo eliminamos y sumamos puntos
    if indice_golpeado != -1:
        simbolo = self.block_symbols[indice_golpeado]

        # Usamos la tabla de puntos definida en ArkanoidGame
        puntos = self.BLOCK_POINTS.get(simbolo, 0)
        self.score += puntos

        # Eliminamos el bloque y su información asociada
        self.blocks.pop(indice_golpeado)
        self.block_colors.pop(indice_golpeado)
        self.block_symbols.pop(indice_golpeado)

@arkanoid_method
def dibujar_escena(self) -> None:
    """Renderiza fondo, bloques, paleta, bola y HUD."""
    # - Rellena el fondo y dibuja cada bloque con `self.dibujar_rectangulo`.
    # - Pinta la paleta y la bola con las utilidades proporcionadas.
    # - Muestra puntuación, vidas y mensajes usando `self.dibujar_texto`.
    raise NotImplementedError

@arkanoid_method
def run(self) -> None:
    """Ejecuta el bucle principal del juego."""
    # - Inicializa recursos (`self.inicializar_pygame`, `self.cargar_nivel`, etc.).
    # - Procesa eventos de `self.iterar_eventos()` y llama a los métodos de actualización/dibujo.
    # - Refresca la pantalla con `self.actualizar_pantalla()` y cierra con `self.finalizar_pygame()`.
    raise NotImplementedError


def main() -> None:
    """Permite ejecutar el juego desde la línea de comandos."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Plantilla del hito M2: Arkanoid con pygame.",
    )
    parser.add_argument(
        "level",
        type=str,
        help="Ruta al fichero de nivel (texto con # para bloques y . para huecos).",
    )
    args = parser.parse_args()

    game = ArkanoidGame(args.level)
    game.run()


if __name__ == "__main__":
    main()
