###################################################
# Gas movement following Lennard-Jones Potential. #
###################################################


import pygame
import numpy as np

pygame.init()

w,h = 500,500
screen = pygame.display.set_mode((w,h))
clock = pygame.time.Clock()

white = (255,255,255)

mol = 6.022*10**-23
u=1.6605402*10**-27
mass = 40000000000000000*u #40000000000000000,120,0.15 

e,s=120,0.3   #e=0.185kcal/mol s=3.04nm #disminuir s hace que Rmin disminuya
A,B=4*e*s**12,4*e*s**6

n=50
r=10

def map_range(value, a1, b1, a2, b2):
    #To map some value from a range to another range (velocity to colour)
    if value >= b1:
        return int(b2)
    else:
        return int((value - a1) / (b1 - a1) * (b2 - a2) + a2)

def vector(p1,p2): #Vector r entre dos puntos
    return p2.r-p1.r #devuelve np.array

def module(v): #Módulo de un vector
    return float(np.linalg.norm(v))

def unit(v): #Vector unidad
    return v/module(v)

def distance(p1,p2):
    return np.sqrt((p1.x-p2.x)**2 + (p1.y-p2.y)**2)

def potential(p1,p2): #potencial truncado a distancia
    if distance(p1,p2) <= 30:
        d = 30
    else:
        d = distance(p1,p2)
    return (A/(d**12)) - (B/(d**6))

def force(p1,p2):
    return potential(p1,p2)/distance(p1,p2) * unit(vector(p1,p2))

def acceleration(p1,p2):
    return force(p1,p2)/mass

def velocity(p1,p2):
    if p1 == p2:
        pass
    # elif module(acceleration(p1,p2))<=10:
    #     return list(np.array([p1.dx,p1.dy]))
    else:
        return list(np.array([p1.dx,p1.dy]) + acceleration(p1,p2))

def collision(p1,p2): #mejorar sistema de colision, csegun por donde se acerce particula
    if p1 == p2:    
        pass
    elif pygame.Rect.colliderect(p1.rect,p2.rect):
        return True
    else:
        return False


class particula():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.r = np.array([self.x,self.y])
        self.dx = np.random.uniform(-1,1) # 0.1
        self.dy = np.random.uniform(-1,1)
        self.v = module(np.array([self.dx,self.dy]))
        self.m = mass
        self.color = white #np.random.randint(0,255,3)
        self.rect = pygame.draw.circle(screen,self.color, (self.x,self.y),r)

        
    def show(self):
        self.rect=pygame.draw.circle(screen,self.color, (self.x,self.y),r)
        
    def paint(self):
        c=map_range(self.v,0,8,255,0)
        self.color = (255,c,c)



#particles=[particula(250,300), particula(350,300)]    #for i in range(2)
particles=[]
for i in range(int(n/10)):
    for j in range(10):
        x,y=int((w/10*j)+(w/20)),int(h/(n/10)*i + (h/(2*n/10)))
        x += np.random.uniform(-2*w/50,2*w/50)
        y += np.random.uniform(-4*h/n,4*h/n)
        particles.append(particula(x,y))

# particles=[]
# for i in range(n):
#     x,y=np.random.randint(10,w-10,2)
#     particles.append(particula(x,y))
veltest,distest=[],[]
vel,dist,distt=[],[],[]
running = True
while running:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    
    for p in particles:
    
        #Borders
        if p.x<=0 or p.x>=w:
            #p.x = 0
            p.dx = -p.dx
        if p.y<=0 or p.y>=h:
            #p.y = 0
            p.dy = -p.dy

        #p.dx, p.dy = np.random.uniform(-1,1), np.random.uniform(-1,1) ###
        p.x += p.dx
        p.y += p.dy
        p.r = np.array([p.x,p.y])
        
        dist_pp=[]
        for i in particles:
            if i == p or distance(p,i)>=100:
                pass
            # elif module(np.array(velocity(p,i)))>=20:
            #     p.dx,p.dy = p.dx, p.dy
            else:
                p.dx,p.dy = velocity(p,i)
                p.v = module(np.array(p.dx,p.dy))

        p.show() #ha de ir antes del collision, porque crea el rectangulo
        p.paint()
        veltest.append(p.v)


    vel.append(max(veltest))
    veltest = []
    pygame.display.update()
    clock.tick(60)
