#########################################
# Planets Simulation using Newtons Laws #
#########################################

import pygame
import numpy as np
pygame.init()


w,h = 750,750
screen = pygame.display.set_mode((w,h))
pygame.display.set_caption("Planet Simulator")
clock = pygame.time.Clock()
FPS = 60

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)


G = 6.67*10**-11
AU = 1.496*10**11
dt = 1*24*36000    #1day in  seconds
scaleAU = 10
scale = scaleAU*AU

Mt = 5.9722*10**24
Ms = 332946*Mt

data = {"mercury": (0.387, 0.055, 47400), 
        "venus": (0.723, 0.815, 35020),
        "earth": (1,1, 29783),
        "mars": (1.52,0.107, 24077), 
        "jupiter": (5.2, 317.8, 13060), 
        "saturn": (9.57, 95.2, 9680), 
        "uranus": (19.17, 14.5, 6800),
        "neptune": (30.1, 17.15, 5430)}

def mapRange(value, a1, b1, a2, b2): #To map some value from a range to another range (de coordenadas a pixeles)
    return ((value - a1) / (b1 - a1) * (b2 - a2) + a2)

def rescale(x):
    a = -1.5
    res = (7.5/(np.log((a-10)/a)))*np.log((a-abs(x))/a)
    if x >= 0: return +res
    elif x < 0: return -res

def decompose(x,theta):
    return (x*np.cos(theta), x*np.sin(theta))

class Body():
    def __init__(self, x,y,r,M,color, sun = False):
        self.x,self.y = x*AU,y*AU
        self.pos = np.array([self.x,self.y])
        self.theta = np.arctan2(self.y,self.x)
        self.r = r
        self.M = M
        self.color = color

        self.cumf = 0
        self.fx,self.fy = 0,0
        self.vx,self.vy = 0,0

        self.d = 0

        self.sun = sun
    
    def draw(self, surf):

        # x,y = rescale(self.x/AU)*AU, rescale(self.y/AU)*AU
        x,y = self.x,self.y
        x = mapRange(x, -scale, scale, 0,w)
        y = mapRange(y, scale, -scale, 0,h)
        pygame.draw.circle(surf, self.color, (x,y), self.r)

    @staticmethod
    def distance(body1,body2):
        if body1 == body2: pass
        else: return np.linalg.norm(body1.pos-body2.pos)

    @staticmethod
    def force(body1,body2):
        if body1 == body2: pass
        else: return -G*body1.M*body2.M/Body.distance(body1,body2)**2

    def update(self):
        pass

    def stop(self):
        self.vx, self.vy, self.cumf, self.fx, self.fy = (0 for _ in range(5))


sun1 = Body(-3,0, 25, Ms, yellow, sun = True)
# sun2 = Body(3,0, 25, Ms, yellow, sun = True)
planets = []
for d,m,vx in list(data.values()):
    p = Body(0,d, mapRange(m, 0.3,300, 5, 20),m*Mt, np.random.randint(0,255,3))
    p.vx = vx
    planets.append(p)


running = True
while running:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    sun1.draw(screen)
    # sun2.draw(screen)
    for p1 in planets:
        fsun = Body.force(p1,sun1)
        p1.cumf += fsun
        for p2 in planets:
            if p1 == p2: continue
            else:
                f = Body.force(p1,p2)
                p1.cumf += f

        p1.theta = np.arctan2(p1.y,p1.x)
        p1.fx, p1.fy = decompose(p1.cumf,p1.theta)
        p1.vx += p1.fx*dt/p1.M
        p1.vy += p1.fy*dt/p1.M 
        p1.x += p1.vx*dt
        p1.y += p1.vy*dt

        p1.draw(screen)
        p1.cumf = 0
        p1.fx,p1.fy = 0,0

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()