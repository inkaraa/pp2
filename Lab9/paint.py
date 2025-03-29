import pygame, sys, time


pygame.init()

BLUE = (0,255,255)
WHITE = (255,255,255)
WIDTH, HEIGHT = 1080, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
    
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas = canvas.convert()
canvas.fill(WHITE)
    
clock = pygame.time.Clock()

# Current tool options: "pencil", "rectangle", "circle", "eraser"
current_tool = "pencil"
# Default drawing color (blue)
current_color = BLUE
# Brush (or pen) thickness; also used as the outline width for shapes
brush_radius = 15
# Flags and positions used during drawing
drawing = False         # True when mouse button is held down
start_pos = None        # Starting point for shape drawing (rectangle or circle)
last_pos = None         # Last recorded position for continuous free drawing
while True:
    
    pressed_keys = pygame.key.get_pressed()
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
                
        if event.type == pygame.KEYDOWN:
            # Tool Selection via number keys:
            #   1: Pencil, 2: Rectangle, 3: Circle, 4: Eraser
            if event.key == pygame.K_1:
                current_tool = "pencil"
            elif event.key == pygame.K_2:
                current_tool = "rectangle"
            elif event.key == pygame.K_3:
                current_tool = "circle"
            elif event.key == pygame.K_4:
                current_tool = "eraser"
            elif event.key == pygame.K_5:
                current_tool = "square"
            elif event.key == pygame.K_6:
                current_tool = "right_triangle"
            elif event.key == pygame.K_7:
                current_tool = "equilateral_triangle"
            elif event.key == pygame.K_8:
                current_tool = "rhombus"
            
                    
            # Color Selection via letter keys:
            #   R for red, G for green, B for blue, Y for yellow,
            #   C for cyan, M for magenta.
            if event.key == pygame.K_r:
                current_color = (255, 0, 0)    # Red
            elif event.key == pygame.K_g:
                current_color = (0, 255, 0)    # Green
            elif event.key == pygame.K_b:
                current_color = (0, 0, 255)    # Blue
            elif event.key == pygame.K_y:
                current_color = (255, 255, 0)  # Yellow
            elif event.key == pygame.K_c:
                current_color = (0, 255, 255)  # Cyan
            elif event.key == pygame.K_m:
                current_color = (255, 0, 255)  # Magenta
                    
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Left click increases brush size; right click decreases it.
            if event.button == 1:
                brush_radius = min(200, brush_radius + 1)
            elif event.button == 3:
                brush_radius = max(1, brush_radius - 1)
                    
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Begin drawing on left mouse button press
                drawing = True
                start_pos = event.pos  # Record the starting point for shapes
                last_pos = event.pos   # For free drawing, track the last position
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if drawing:
                end_pos = event.pos
                x1, y1 = start_pos
                x2, y2 = end_pos

                # rectangle
                if current_tool == "rectangle":
                    rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
                    pygame.draw.rect(canvas, current_color, rect, brush_radius)

                # circle
                elif current_tool == "circle":
                    radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
                    pygame.draw.circle(canvas, current_color, start_pos, radius, brush_radius)

                # square
                elif current_tool == "square":
                    side = min(abs(x2 - x1), abs(y2 - y1))
                    rect = pygame.Rect(x1, y1, side * (1 if x2 > x1 else -1), side * (1 if y2 > y1 else -1))
                    rect.normalize()
                    pygame.draw.rect(canvas, current_color, rect, brush_radius)

                # right triangle
                elif current_tool == "right_triangle":
                    points = [start_pos, (x1, y2), (x2, y2)]
                    pygame.draw.polygon(canvas, current_color, points, brush_radius)

                # equilateral triangle
                elif current_tool == "equilateral_triangle":
                    base = abs(x2 - x1)
                    height = int(base * (3 ** 0.5) / 2)
                    direction = -1 if y2 < y1 else 1
                    points = [
                        ((x1 + x2) // 2, y1 + direction * height),
                        (x1, y1),
                        (x2, y1)
                    ]
                    pygame.draw.polygon(canvas, current_color, points, brush_radius)

                # rhombus
                elif current_tool == "rhombus":
                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                    dx, dy = abs(x2 - x1) // 2, abs(y2 - y1) // 2
                    points = [
                        (cx, cy - dy),
                        (cx + dx, cy),
                        (cx, cy + dy),
                        (cx - dx, cy)
                    ]
                    pygame.draw.polygon(canvas, current_color, points, brush_radius)

                    # For pencil and eraser, drawing is handled continuously during mouse motion.
                drawing = False
                start_pos = None
                last_pos = None
                    
        if event.type == pygame.MOUSEMOTION:
            if drawing:
                if current_tool == "pencil":
                    # Draw continuous freehand lines on the canvas.
                    pygame.draw.line(canvas, current_color, last_pos, event.pos, brush_radius)
                    last_pos = event.pos
                elif current_tool == "eraser":
                    # Eraser: draw with white color (matching the canvas background)
                    pygame.draw.line(canvas, (255, 255, 255), last_pos, event.pos, brush_radius)
                    last_pos = event.pos

    # Create a temporary copy of the canvas to show a preview while dragging.
    preview = canvas.copy()
    if drawing and current_tool in ["rectangle", "circle", "square", "right_triangle", "equilateral_triangle", "rhombus"]:
        current_pos = pygame.mouse.get_pos()
        x1, y1 = start_pos
        x2, y2 = current_pos

        if current_tool == "rectangle":
            rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
            pygame.draw.rect(preview, current_color, rect, brush_radius)

        elif current_tool == "circle":
            radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
            pygame.draw.circle(preview, current_color, start_pos, radius, brush_radius)

        elif current_tool == "square":
            side = min(abs(x2 - x1), abs(y2 - y1))
            rect = pygame.Rect(x1, y1, side * (1 if x2 > x1 else -1), side * (1 if y2 > y1 else -1))
            rect.normalize()
            pygame.draw.rect(preview, current_color, rect, brush_radius)

        elif current_tool == "right_triangle":
            points = [start_pos, (x1, y2), (x2, y2)]
            pygame.draw.polygon(preview, current_color, points, brush_radius)

        elif current_tool == "equilateral_triangle":
            base = abs(x2 - x1)
            height = int(base * (3 ** 0.5) / 2)
            direction = -1 if y2 < y1 else 1
            points = [
                ((x1 + x2) // 2, y1 + direction * height),
                (x1, y1),
                (x2, y1)
            ]
            pygame.draw.polygon(preview, current_color, points, brush_radius)

        elif current_tool == "rhombus":
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            dx, dy = abs(x2 - x1) // 2, abs(y2 - y1) // 2
            points = [
                (cx, cy - dy),
                (cx + dx, cy),
                (cx, cy + dy),
                (cx - dx, cy)
            ]
            pygame.draw.polygon(preview, current_color, points, brush_radius)

    screen.blit(preview, (0, 0))
        
    # display current tool and color information for user reference.
    info_font = pygame.font.SysFont(None, 24)
    tool_text = info_font.render("Tool: " + current_tool, True, (0, 0, 0))
    color_text = info_font.render("Color: " + str(current_color), True, (0, 0, 0))
    screen.blit(tool_text, (10, 10))
    screen.blit(color_text, (10, 30))
        
    pygame.display.flip()
    clock.tick(60)

