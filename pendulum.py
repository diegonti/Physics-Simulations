import pygame
import numpy as np
from scipy.integrate import solve_ivp

pygame.init()

w,h = 750,500
screen = pygame.display.set_mode((w,h))
clock = pygame.time.Clock()
FPS = 60

font32 = pygame.font.Font("freesansbold.ttf",32)
font16 = pygame.font.Font("freesansbold.ttf",16)

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)


def percent(p,n): #devuelve el porcentaje p% de un numero n
    return int(np.round((p/100)*n)) #el int quitarlo en otros casos, aqui me intersesa only int

origin = (percent(50,w),percent(5,h)) #origin pixel coordinates 

def map_range(value, a1, b1, a2, b2): #To map some value from a range to another range (de coordenadas a pixeles)
    return ((value - a1) / (b1 - a1) * (b2 - a2) + a2)

def distance(p1,p2): #en pixeles
    return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def draw_line_dashed(surface, color, start_pos, end_pos, width = 1, dash_length = 10, exclude_corners = True):
    start_pos = np.array(start_pos)
    end_pos   = np.array(end_pos)
    length = np.linalg.norm(end_pos - start_pos) #distance between start_pos and end_pos
    dash_amount = int(length / dash_length) #get amount of pieces that line will be split up in (half of it are amount of dashes)

    # x-y-value-pairs of where dashes start (and on next, will end)
    dash_knots = np.array([np.linspace(start_pos[i], end_pos[i], dash_amount) for i in range(2)]).transpose()

    [pygame.draw.line(surface, color, tuple(dash_knots[n]), tuple(dash_knots[n+1]), width)
        for n in range(int(exclude_corners), dash_amount - int(exclude_corners), 2)]

def draw_background():
    pygame.draw.line(screen, black,(percent(10,w),percent(5,h)),(percent(90,w),percent(5,h)),5)
    draw_line_dashed(screen,black,origin,(percent(50,w),percent(90,h)),1,10)

def draw_finish():
    finish_surface = pygame.Surface((percent(50,w),percent(20,w)))
    finish_surface.fill(black)
    finish_rect = finish_surface.get_rect(center = (percent(50,w),percent(60,h)))
    screen.blit(finish_surface, finish_rect)

    text32 = font32.render("SIMULATION OVER", True, (255,255,255))
    text16 = font16.render("Click anywere to restart from that position", True, (255,255,255))
    screen.blit(text32, text32.get_rect(center = (percent(50,w),percent(55,h))))
    screen.blit(text16, text16.get_rect(center = (percent(50,w),percent(65,h))))

def draw_data(l,m,theta,x,y,t):
    left, top = 10, 35
    screen.blit(font16.render(f"l = {l:.2f}m", True, black), (left,0+top))
    screen.blit(font16.render(f"m = {m:.0f}kg", True, black), (left,16+top))
    screen.blit(font16.render(f"θ = {theta/np.pi:.2f}π rad", True, black), (left,32+top))
    screen.blit(font16.render(f"x,y = ({x:.2f},{y:.2f})m", True, black), (left,48+top))
    screen.blit(font16.render(f"t = {t:.2f}s", True, black), (left,64+top))

def draw_pendulum(x,y):
    pygame.draw.line(screen,black,origin,(x,y),3)
    pygame.draw.circle(screen,black,(x,y),r)

def equations(t,theta): #equacion del péndulo convertida a EDO de primer orden
    dtheta2 = (-b/m)*theta[1] + (-g/l)*np.sin(theta[0])
    dtheta1 = theta[1]
    return [dtheta1,dtheta2]

###Pendulum Parameters
g = 9.81 #Gravity
l = 1 #Lenght (m)
m = 1 #Mass (kg)
b = 0.2 #Damping factor
r = map_range(m, 1,100, 10,50) #Radio bola péndulo

theta1_o = 0.3 #ángulo inicial
theta2_o = 0 #velocidad angular inicial
theta_o = [theta1_o,theta2_o]

dt = 1/FPS #time step
to,tf = 0,20
t_range = [to,tf+dt] #rango de tiempo que integra
t = np.arange(to,tf+dt,dt) #lista con todos los puntos de tiempo a calcular 
# len = np.arange(0,len(t),1) #puntos de simulacion (longitud simulación)

theta12 = solve_ivp(equations,t_range,theta_o,t_eval=t) #integral numérica
theta1 = theta12.y[0] #valores de angulo
#theta2 = theta12.y[1][0] #valores de velocidad

i = 0
running = True
while running:
    screen.fill(white)
    draw_background()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN: #solo si velocidad es baja?
            mpx,mpy = event.pos
            draw_pendulum(mpx,mpy)

            mx = map_range(mpx,percent(10,w),percent(90,w),-1,1)
            my = map_range(mpy,percent(5,h),percent(45,w),0,-1)
            l = distance((0,0),(mx,my)) #Cambia longitud 

            if mx>0: theta2_o = -theta2_o
            elif mx<0: theta2_o = theta2_o

            theta_o = [np.arcsin(mx/l), theta2_o]
            theta12 = solve_ivp(equations,t_range,theta_o,t_eval=t) #integral numérica
            theta1 = theta12.y[0] #valores de angulo  
            i = 0

           
    x = l*np.sin(theta1[i])
    y = -l*np.cos(theta1[i])
    px = map_range(x,-1,1,percent(10,w),percent(90,w))
    py = map_range(y,0,-1,percent(5,h),percent(45,w))
    
    draw_pendulum(px,py)
    draw_data(l,m, theta1[i], x,y, t[i])

    if i >= len(theta1)-1:
        draw_finish()
    else: i += 1
    

    pygame.display.update()
    clock.tick(FPS)

