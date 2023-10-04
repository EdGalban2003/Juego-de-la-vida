import pygame
import numpy as np

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
width, height = 1500, 900
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Juego de la Vida")

# Variables para el juego
cell_size = 20
rows, cols = height // cell_size, width // cell_size
grid = np.zeros((rows, cols), dtype=int)  # Inicialmente, todas las celdas están muertas
running = True
drawing = False  # Indica si el usuario está dibujando en la cuadrícula

# Variables para el control del tiempo
auto_advance = False
auto_advance_interval = 150  # Intervalo de 1 segundo en milisegundos
last_advance_time = pygame.time.get_ticks()

# Variables para el contador de generación
generation = 0

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)  # Gris para el contador de generación

# Fuente para el contador de generación
font = pygame.font.Font(None, 36)

# Función para dibujar la cuadrícula
def draw_grid():
    for row in range(rows):
        for col in range(cols):
            # Define el color de las celdas
            cell_color = WHITE if grid[row][col] == 1 else BLACK
            pygame.draw.rect(screen, cell_color, (col * cell_size, row * cell_size, cell_size, cell_size))
            
            # Define el color de las líneas de la cuadrícula
            line_color = (9, 9, 9)  # Gris oscuro (puedes ajustar los valores RGB según tu preferencia)
            pygame.draw.rect(screen, line_color, (col * cell_size, row * cell_size, cell_size, cell_size), 1)

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
            if event.button == 1:  # Click izquierdo para dibujar o borrar
                x, y = pygame.mouse.get_pos()
                col = x // cell_size
                row = y // cell_size
                grid[row][col] = 1 - grid[row][col]  # Alternar entre vivo y muerto
                drawing = True
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                grid = next_generation()  # Avanzar 1 generación con la barra espaciadora
                generation += 1  # Incrementar el contador de generación
            elif event.key == pygame.K_c:
                grid = np.zeros((rows, cols), dtype=int)  # Limpiar la cuadrícula con la tecla 'C'
                generation = 0  # Reiniciar el contador de generación
            elif event.key == pygame.K_v:
                auto_advance = not auto_advance  # Alternar avance automático con la tecla 'V'

    if auto_advance and current_time - last_advance_time >= auto_advance_interval:
        grid = next_generation()
        last_advance_time = current_time
        generation += 1  # Incrementar el contador de generación

    screen.fill(BLACK)
    draw_grid()
    
    # Dibujar el contador de generación
    text = font.render("Generación: " + str(generation), True, WHITE)
    screen.blit(text, (10, height - 40))  # Posición del contador
    
    pygame.display.flip()

# Salir del juego
pygame.quit()
