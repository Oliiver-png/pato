import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((640, 610))
clock = pygame.time.Clock()
running = True
dt = 0.1

duck_img = pygame.image.load('duck.png').convert() 

duck_img = pygame.transform.scale(duck_img,
                                    (duck_img.get_width() *  2,
                                     duck_img.get_height() * 2))

duck_img.set_colorkey((0, 0, 0))

player_pos = pygame.Vector2(0, 152) #Posición inicial del pato
#Donde mira el pato, por defecto mira a la derecha
duck_right = duck_img 
duck_left = pygame.transform.flip(duck_right, True, False)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    screen.blit(duck_img, (player_pos.x, player_pos.y))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 200 * dt
    if keys[pygame.K_s]:
        player_pos.y += 200 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 200 * dt
        duck_img = duck_left
    if keys[pygame.K_d]:
        player_pos.x += 200 * dt
        duck_img = duck_right
        
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    pygame.display.flip()
    dt = clock.tick(60) / 1000
    dt = max(0.001, min(0.1, dt))
pygame.quit()