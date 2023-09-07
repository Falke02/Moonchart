import csv
import math

import pygame
import pygame_gui


class Moonchart(object):
    def __init__(self):
        pygame.init()

        self.load_assets()
        self.width, self.height = 800, 653
        self.manager = pygame_gui.UIManager((self.width, self.height))
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.year = int(self.dates[0][2])
        self.month = int(self.dates[0][1])
        self.day = int(self.dates[0][0])
        self.year_count = self.year * 336
        self.month_count = self.month * 28

        self.days_count = self.year_count + self.month_count + self.day

        # Circle parameters
        self.outer_center = (self.width // 2, self.height // 2)
        self.outer_radius = 240
        self.num_outer_segments = 36
        self.outer_angle_increment = 360 / self.num_outer_segments

        self.inner_radius = 190
        self.num_inner_segments = 28
        self.inner_angle_increment = 360 / self.num_inner_segments

        self.most_inner_radius = 150
        self.num_most_inner_segments = 8
        self.most_inner_angle_increment = 360 / self.num_most_inner_segments

        # Angel constant was chosen so that all moons are in full moon on 15/10/350
        self.outer_angle = 210 + (((self.days_count - 1) * 10) * -1)
        self.inner_angle = 90 + (((self.days_count - 1) * 12.8571428) * -1)
        self.most_inner_angle = 160 + (((self.days_count - 1) * 45) * -1)

        self.setup_pygame_gui()
        self.clock = pygame.time.Clock()
        self.running = True

    def setup_pygame_gui(self):
        pygame.display.set_caption("Krynn Mondkalender")

        self.left_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 30), (100, 40)),
                                                        text='+ 1 Tag', manager=self.manager)
        self.right_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((110, 30), (100, 40)),
                                                         text='- 1 Tag', manager=self.manager)

    def savedate(self, currentdate):
        data = currentdate

        with open('date.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data)

    # Loads the given assets for later usage.
    def load_assets(self):
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.calendar = pygame.image.load("moon2.jpg")

        file = open("date.csv")
        self.dates = list(csv.reader(file, delimiter=","))
        file.close()

    # Main pygame event and drawing loop
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                self.manager.process_events(event)

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.left_button:

                            # Logic for the left button for circle control
                            self.outer_angle -= self.outer_angle_increment
                            self.inner_angle -= self.inner_angle_increment
                            self.most_inner_angle -= self.most_inner_angle_increment
                            self.day += 1
                            if self.day == 29:
                                self.day = 1
                                self.month += 1
                            if self.month == 13:
                                self.month = 1
                                self.year += 1
                            if self.day == 0:
                                self.day = 28
                                self.month -= 1
                            if self.month == 0:
                                self.month = 12
                                self.year -= 1
                        elif event.ui_element == self.right_button:

                            # Logic for the right button for circle control
                            self.outer_angle += self.outer_angle_increment
                            self.inner_angle += self.inner_angle_increment
                            self.most_inner_angle += self.most_inner_angle_increment
                            self.day -= 1
                            if self.day == 0:
                                self.day = 28
                                self.month -= 1
                            if self.month == 0:
                                self.month = 12
                                self.year -= 1

            currentdate = [self.day, self.month, self.year]

            self.screen.fill((255, 255, 255))
            # Calculate the position of the point on the outer circle
            outer_point_x = self.outer_center[0] + self.outer_radius * math.cos(math.radians(self.outer_angle))
            outer_point_y = self.outer_center[1] + self.outer_radius * math.sin(math.radians(self.outer_angle))

            # Calculate the position of the point on the inner circle
            inner_point_x = self.outer_center[0] + self.inner_radius * math.cos(math.radians(self.inner_angle))
            inner_point_y = self.outer_center[1] + self.inner_radius * math.sin(math.radians(self.inner_angle))

            # Calculate the position of the point on the innermost circle
            most_inner_point_x = self.outer_center[0] + self.most_inner_radius * math.cos(
                math.radians(self.most_inner_angle))
            most_inner_point_y = self.outer_center[1] + self.most_inner_radius * math.sin(
                math.radians(self.most_inner_angle))

            calendar = pygame.transform.scale(self.calendar, (800, 653))
            self.screen.blit(calendar, (0, 0))

            # Draw the outer circle
            pygame.draw.circle(self.screen, (255, 255, 255), self.outer_center, self.outer_radius, -1)

            # Draw the inner circle
            pygame.draw.circle(self.screen, (0, 0, 0), (int(inner_point_x), int(inner_point_y)), 10)

            # Draw the innermost circle
            pygame.draw.circle(self.screen, (255, 255, 255), (int(most_inner_point_x), int(most_inner_point_y)), 10)

            # Draw the point on the outer circle
            pygame.draw.circle(self.screen, (255, 0, 0), (int(outer_point_x), int(outer_point_y)), 10)

            # Render the date string
            datum = ["Tag", self.day, "Monat", self.month, "Jahr", self.year]
            datum2 = ' '.join(map(str, datum))
            text = self.font.render(datum2, True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (120, 20)

            self.screen.blit(text, textRect)
            self.time_delta = self.clock.tick(10)
            self.manager.update(self.time_delta)
            self.manager.draw_ui(self.screen)
            self.savedate(currentdate)
            pygame.display.flip()

        pygame.quit()
