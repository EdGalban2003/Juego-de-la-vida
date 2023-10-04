import pygame
import numpy as np

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Juego de la Vida")

# Variables para el juego
cell_size = 20  # Tamaño de las cuadrículas
rows, cols = height // cell_size, width // cell_size
grid = np.zeros((rows, cols), dtype=int)  # Inicialmente, todas las celdas están muertas
running = True

# Variables para el control del tiempo
auto_advance = False
auto_advance_interval = 150  # Intervalo de 150 milisegundos
last_advance_time = pygame.time.get_ticks()

auto_retrocede = False
auto_retrocede_interval = 150  # Intervalo de 150 milisegundos
last_retrocede_time = pygame.time.get_ticks()

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200, 70)  # Transparencia agregada (70 en este caso)

# Historial de generaciones para retroceder
history = [grid.copy()]
current_generation = 0

# Variable para controlar si se ha avanzado alguna vez
has_advanced = False

# Función para dibujar la cuadrícula
def draw_grid():
    screen.fill(BLACK)
    for row in range(rows):
        for col in range(cols):
            color = WHITE if grid[row][col] == 1 else BLACK
            pygame.draw.rect(screen, color, (col * cell_size, row * cell_size, cell_size, cell_size))
            pygame.draw.rect(screen, GRAY, (col * cell_size, row * cell_size, cell_size, cell_size), 1)

    # Dibujar contador de generaciones
    font = pygame.font.Font(None, 36)
    text = font.render(f"Generación: {current_generation}", True, WHITE)
    screen.blit(text, (10, 10))

# Función para calcular la siguiente generación del Juego de la Vida
def next_generation():
    new_grid = np.zeros((rows, cols), dtype=int)
    for row in range(rows):
        for col in range(cols):
            neighbors = np.sum(grid[row - 1:row + 2, col - 1:col + 2]) - grid[row][col]
            if grid[row][col] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[row][col] = 0
                else:
                    new_grid[row][col] = 1
            else:
                if neighbors == 3:
                    new_grid[row][col] = 1
    return new_grid

# Ciclo principal del juego
while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Click izquierdo para colocar o quitar cuadritos
                x, y = pygame.mouse.get_pos()
                col = x // cell_size
                row = y // cell_size
                grid[row][col] = 1 - grid[row][col]  # Alternar entre vivo y muerto
                has_advanced = False  # Restablecer el contador

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                grid = next_generation()  # Avanzar 1 generación con la barra espaciadora
                current_generation += 1
                history.append(grid.copy())
                has_advanced = True  # Se ha avanzado al menos una vez
            elif event.key == pygame.K_c:
                grid = np.zeros((rows, cols), dtype=int)  # Limpiar todas las celdas
                current_generation = 0  # Restablecer el contador a 0
                history = [grid.copy()]
                has_advanced = False  # Restablecer el contador
            elif event.key == pygame.K_v:
                auto_advance = not auto_advance  # Alternar avance automático con la tecla 'V'
            elif event.key == pygame.K_b:
                if current_generation > 0:
                    current_generation -= 1  # Retroceder 1 generación con la tecla 'B'
                    grid = history[current_generation].copy()
                    has_advanced = True  # Se ha avanzado al menos una vez
            elif event.key == pygame.K_n:
                auto_retrocede = not auto_retrocede  # Alternar retroceso automático con la tecla 'N'

    if auto_advance and current_time - last_advance_time >= auto_advance_interval:
        grid = next_generation()
        current_generation += 1
        history.append(grid.copy())
        last_advance_time = current_time
        has_advanced = True  # Se ha avanzado al menos una vez

    if auto_retrocede and current_time - last_retrocede_time >= auto_retrocede_interval:
        if current_generation > 0:
            current_generation -= 1  # Retroceder 1 generación automáticamente
            grid = history[current_generation].copy()
        last_retrocede_time = current_time
        has_advanced = True  # Se ha avanzado al menos una vez

    draw_grid()
    pygame.display.flip()

# Salir del juego
pygame.quit()
