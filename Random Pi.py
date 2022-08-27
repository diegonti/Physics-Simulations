##################################
# Montecarlo aproximation of PI. #
##################################

import random,pygame

pygame.init()
clock = pygame.time.Clock()

w,h = 600,600
screen = pygame.display.set_mode((w,h))
screen.fill((0,0,0))

def map_range(value, a1, b1, a2, b2):
    #To map some value from a rangwe to another range ((-1,1) to pixels)
    return (value - a1) / (b1 - a1) * (b2 - a2) + a2

pygame.draw.circle(screen,(255,255,255),(w/2,h/2),w/2)
pygame.draw.line(screen, (0,0,0), (w/2,0), (w/2,h),1)
pygame.draw.line(screen, (0,0,0), (0,h/2), (w,h/2),1)

n_square, n_circle = 0,0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    x,y = random.uniform(-10,10), random.uniform(-10,10)

    r = (x**2 + y**2)**0.5 #radio desde el centro
    if r < 10: #si el punto esta dentro del circulo
        n_circle += 1
        n_square += 1
        color = (0,255,0)
    else: #si el punto esta fuera
        n_square += 1
        color = (255,0,0)

    px,py = map_range(x,-10,10,0,w), map_range(y,-10,10,h,0) #cambio a pixeles
    pygame.draw.circle(screen,color,(px,py),1)
    
    pi = 4 * n_circle/n_square
    print(pi)

    pygame.display.update()
    #clock.tick(60)