import pygame
import time
cities = []
with open('cities1.txt') as d:
    for i in d:
        i = i.strip()
        i = i.split(',')
        x = float(i[0])
        y = float(i[1])
        cities.append((x,y))

routes = []        
with open('60_citiesevo.txt') as f:
    for line in f.readlines():
        route = []
        line = line.split(';')
        for city in line[:-1]:
            city = city.strip()
            city = city.split(',')
            x = float(city[0])
            y = float(city[1])
            route.append((x,y))
        routes.append(route)

def score(route):
    ret = 0
    for x in range(len(route)):
        if x == len(route) - 1:
            ret += ((route[0][0] - route[x][0])**2 + (route[0][1] - route[x][1])**2) ** (1/2) 
        else:
            ret += ((route[x][0] - route[x+1][0])**2 + (route[x][1] - route[x+1][1])**2) ** (1/2) 
    return ret        
pygame.init()

width = 900
height = 900
running = True
screen = pygame.display.set_mode((width, height))
x = 0
base_font = pygame.font.Font(None, 80)

while running:
    if x != len(routes):
        route = routes[x]
        x += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255,255,255))
    for city in cities:
        pygame.draw.circle(screen, (0,0,0), (city[0]*8 + 20,city[1]*8 +20 ), 6)
    for i in range(len(route)):
        if i == len(route) - 1:
            start = (route[i][0] * 8 +20, route[i][1] * 8 + 20)
            end = (route[0][0] * 8 +20, route[0][1] * 8 + 20)
        else:
            start = (route[i][0] * 8 +20, route[i][1] * 8 + 20)
            end = (route[i+ 1][0] * 8 +20, route[i + 1][1] * 8 + 20)
        pygame.draw.line(screen, (0,0,0), start, end, width=3)
    game_text = base_font.render(f'Score: {score(route)}', True, 'black')
    textrect1 = game_text.get_rect( center= ((width/2-10),25))
    screen.blit(game_text, textrect1) 
    pygame.display.flip()
    time.sleep(1.2)