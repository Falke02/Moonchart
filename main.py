# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pygame
import math
import pygame_gui as pgui
import csv



# Initialisierung
pygame.init()
manager = pgui.UIManager((800, 653))
# Bildschirmgröße
width, height = 800, 653
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Krynn Mondkalender")
font = pygame.font.Font('freesansbold.ttf', 20)

#calenderbackground
calendar=pygame.image.load("images/moon2.jpg")

# Farben
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

#Tagesbestimmer

file = open("date.csv", "r")
datum = list(csv.reader(file, delimiter=","))
file.close()

year = int(datum[0] [2])
month = int(datum[0] [1])
day = int(datum[0] [0])

y = year * 336
m = month * 28
d = day

dayscount = y+m+d


# Kreisparameter
outer_center = (width // 2, height // 2)
outer_radius = 240
num_outer_segments = 36
outer_angle_increment = 360 / num_outer_segments

inner_radius = 190
num_inner_segments = 28
inner_angle_increment = 360 / num_inner_segments

most_inner_radius = 150
num_most_inner_segments = 8
most_inner_angle_increment = 360 / num_most_inner_segments

#Angel Konstante wurde so gewählt, dass alle Monde im Full Moon am 15.10.350 stehen

outer_angle = 210 + (((dayscount-1)*10)*-1)
inner_angle = 90 + (((dayscount-1)*12.8571428)*-1)
most_inner_angle = 160 + (((dayscount-1)*45)*-1)

running = True
clock = pygame.time.Clock()

def savedate(currentdate):
        
        data = currentdate


        with open('date.csv', 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(data)
                
left_button = pgui.elements.UIButton(relative_rect=pygame.Rect((10, 30), (100, 40)),
                                      text='+ 1 Tag', manager=manager)
right_button = pgui.elements.UIButton(relative_rect=pygame.Rect((110, 30), (100, 40)),
                                       text='- 1 Tag', manager=manager)



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        manager.process_events(event)

        if event.type == pygame.USEREVENT:
            if event.user_type == pgui.UI_BUTTON_PRESSED:
                if event.ui_element == left_button:
                    # Logik für den linken Button für die Kreissteuerung
                    outer_angle -= outer_angle_increment
                    inner_angle -= inner_angle_increment
                    most_inner_angle -= most_inner_angle_increment
                    day += 1
                    if day == 29:
                        day = 1
                        month += 1
                    if month == 13:
                        month = 1
                        year += 1
                    if day == 0:
                        day = 28
                        month -= 1
                    if month == 0:
                        month = 12
                        year -= 1
                elif event.ui_element == right_button:
                    # Logik für den rechten Button für die Kreissteuerung
                    outer_angle += outer_angle_increment
                    inner_angle += inner_angle_increment
                    most_inner_angle += most_inner_angle_increment
                    day -= 1
                    if day == 0:
                        day = 28
                        month -= 1
                    if month == 0:
                        month = 12
                        year -= 1
                      
    currentdate = [day,month,year]    
    
    screen.fill(white)
    # Berechne die Position des Punktes auf dem äußeren Kreis
    outer_point_x = outer_center[0] + outer_radius * math.cos(math.radians(outer_angle))
    outer_point_y = outer_center[1] + outer_radius * math.sin(math.radians(outer_angle))

    # Berechne die Position des Punktes auf dem inneren Kreis
    inner_point_x = outer_center[0] + inner_radius * math.cos(math.radians(inner_angle))
    inner_point_y = outer_center[1] + inner_radius * math.sin(math.radians(inner_angle))

    # Berechne die Position des Punktes auf dem innersten Kreis
    most_inner_point_x = outer_center[0] + most_inner_radius * math.cos(math.radians(most_inner_angle))
    most_inner_point_y = outer_center[1] + most_inner_radius * math.sin(math.radians(most_inner_angle))

    
    calendar = pygame.transform.scale(calendar, (800,653))
    screen.blit(calendar, (0,0))
 
    # Zeichne den äußeren Kreis
    pygame.draw.circle(screen, white, outer_center, outer_radius, -1)

    # Zeichne den inneren Kreis
    pygame.draw.circle(screen, black, (int(inner_point_x), int(inner_point_y)), 10)

    # Zeichne den innersten Kreis
    pygame.draw.circle(screen, white, (int(most_inner_point_x), int(most_inner_point_y)), 10)

# Zeichne den Punkt auf dem äußeren Kreis
    pygame.draw.circle(screen, red, (int(outer_point_x), int(outer_point_y)), 10)

# Rendere den Datumstext
    datum = ["Tag",day,"Monat",month,"Jahr",year]
    datum2 = ' '.join(map(str,datum))
    text = font.render(datum2, True, black)
    textRect = text.get_rect()
    textRect.center=(120,20)



# pygame display stuff
    screen.blit(text, textRect) 
    time_delta = clock.tick(10)
    manager.update(time_delta)
    manager.draw_ui(screen)
    savedate(currentdate)
    pygame.display.flip()
pygame.quit()