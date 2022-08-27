import pygame,pymunk #PyGame para visualizar PyMunk para calculos de física

#Creamos espacio que se va actualizando, con la fisica que queremos.
#Body == objeto que es afectado por fisica (no material)
    #Puede ser Static, Dynamic o Kinematic
#Shape == area alrededor de Body que lo vuelve material (puede colisionar)

def create_apple(space,pos): #Creamos body/shape manzana dinamica
    body = pymunk.Body(1, 10, body_type=pymunk.Body.DYNAMIC) #creamos cuerpo (mass,inertia,tipo)
    body.position = pos #Asignamos posicion inicial con pixeles (x,y)
    shape = pymunk.Circle(body, 80) #Creamos area para que el body pueda colisionar (body, radio)
    space.add(body,shape) #añadimos body y shape al espacio
    return shape

def draw_apples(apples): # Dibuja manzanas en screen (apples == list)
    for apple in apples:
        x = int(apple.body.position.x)
        y = int(apple.body.position.y) #Posiciones como integers
        apple_rect = apple_surface.get_rect(center = (x,y))
        screen.blit(apple_surface, apple_rect)
        
def static_ball(space,x,y): #Creamos body/shape de cuerpo estático
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (x,y)
    shape = pymunk.Circle(body, 55)
    space.add(body,shape)
    return shape

def draw_static_ball(balls): # Dibuja manzanas en screen (apples == list)
    for ball in balls:
        x = int(ball.body.position.x)
        y = int(ball.body.position.y) #Posiciones como integers
        pygame.draw.circle(screen, (0,0,0), (x,y), 50) #Dibujamos circulo en el centro de la manzana (screen, color, posicion, radio)


pygame.init() #Iniciar PyGame
screen = pygame.display.set_mode((800,800)) #Crea superficie de pantalla
clock = pygame.time.Clock() #Crea reloj/tiempo
space = pymunk.Space() #Creamos espacio (universo)
space.gravity = (0,250) #añadimos la fisica que queremos (x,y)(numeros arbitrarios)
apple_surface = pygame.image.load("C:/DOCUMENTOS DIEGO/DOWNLOADS/VS Images/apple_red.png") 
    #Cargamos imagen como superficie. Dirección completa con \\ o un solo /. 

apples = []

balls = []
balls.append(static_ball(space,500,500))
balls.append(static_ball(space,200,700))

running = True
while running: #Loop para el juego
    for event in pygame.event.get(): #Comprobar inputs del usuario
        if event.type == pygame.QUIT: #si la input es cerrar el juego
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
           apples.append(create_apple(space, event.pos)) 
    screen.fill((217,217,217)) #Color de fondo
    draw_apples(apples)
    draw_static_ball(balls)
    space.step(1/50) #Actualiza fisica
    pygame.display.update() #Renderizar el frame
    clock.tick(120) #Limitar frames/s a 120
    #Mantener carateristicas iguales durante el juego
