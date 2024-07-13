import random

import pygame


class PygameTutorial:

    def __init__(self):
        self.height = 600
        self.width = 800
        self.x_road = 200
        self.y_road = 0
        self.finish_score = 5000
        self.level_up_score = 500

    def create_simple_game(self):
        global screen_display
        global image_car_loc
        global score
        global level
        global speed_level
        score = 0
        level = 1
        speed_level = 1
        # initialize game
        pygame.init()
        # put screen display using the set_mode
        screen_display = pygame.display.set_mode((self.width, self.height))
        # change title
        pygame.display.set_caption("My first game")
        # change icon of image
        icon = pygame.image.load("pictures/farming.png")
        background = pygame.image.load("pictures/background.jpeg")
        pygame.display.set_icon(icon)
        # set font and label for score
        font = pygame.font.SysFont(name="Arial", size=24, bold=True)
        label_score = font.render("SCORE", 1, (0, 0, 0), (255, 255, 255))
        font_int = pygame.font.SysFont(name="Arial", size=26, bold=True)
        label_score_int = font_int.render(str(score), 1, (0, 0, 0), (255, 255, 255))
        # set font and label for level
        font_level = pygame.font.SysFont(name="Arial", size=20, bold=True)
        label_level = font_level.render("LEVEL " + str(level), 1, (57, 71, 139), (255, 255, 255))
        # set font and label for replay game
        font_game_over = pygame.font.SysFont(name="Arial", size=18, bold=True)
        label_replay = font_game_over.render("Press SPACE to restart", 1, (230, 95, 117),
                                             (49, 119, 203))
        # set font and label for speed
        speed_level_font = pygame.font.SysFont(name="Arial", size=20, bold=True)
        label_speed_level = speed_level_font.render("SPEED " + str(speed_level), 1, (57, 71, 139), (255, 255, 255))
        # set font and label for game winner
        game_winner_font = pygame.font.SysFont(name="Arial", size=36, bold=True)
        label_game_winner = game_winner_font.render("WINNER!!", 1, (128, 255, 0), (127, 127, 127))
        x_initial = 428
        y_initial = 455
        x_change = 0
        x_offset = 2  # offset needs to be low
        y_offset_car = 0.5
        x_value_car_enemy = self.define_random_x_value()
        y_value_car_enemy = 100  # we will add it every time at the top of the screen
        # flag to increase
        increase_score = True
        speed = 0.15
        # game loop - if press x (pygame.QUIT), window will close
        running = True
        while running:
            # stop game in case of losing
            '''
            here we use that 125 because in this case there will be a collision just when the cars crashes at center
            '''
            if y_value_car_enemy > y_initial - 125 and x_initial == x_value_car_enemy:
                print("You lost!")
                #we use this in order to quit in case of replay and collision
                pygame.quit()
                break
            '''
            create some kind of a score tracking and when a score is reached we will increase the speed on y for car
            do this also in our while loop maybe if we can
            '''
            # if we pass the enemy car then we want a new car to appear
            if y_value_car_enemy > self.width - 75:
                # if our car is passes we will increment the score
                score += 100
                label_score_int = font_int.render(str(score), 1, (0, 0, 0), (255, 255, 255))
                x_value_car_enemy = self.define_random_x_value()
                y_value_car_enemy = random.randint(0, 200)  # we want to appear at least top of screen
            # check if we have passed a multiple of 1000 then we can go a level up - increase score is used to not continously increase level when at multiple of 1000
            if score % self.level_up_score == 0 and score != 0 and increase_score is True:
                level += 1
                speed_level += 1
                random_colors = self.get_random_color_level()
                label_level = font_level.render("LEVEL " + str(level), 1, random_colors, (255, 255, 255))
                label_speed_level = speed_level_font.render("SPEED " + str(speed_level), 1, random_colors,
                                                            (255, 255, 255))
                y_offset_car += speed
                increase_score = False
            elif score % self.level_up_score != 0:
                # we need to have it again True in order to increase at a multiple of 1000
                increase_score = True
            # get events
            # screen_display.fill((0, 255, 0))
            screen_display.blit(background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # add condition if key is pressed
                if event.type == pygame.KEYDOWN:
                    '''check now that we have left arrow pressed'''
                    if event.key == pygame.K_LEFT:
                        print("Left arrow pressed")
                        x_change -= x_offset
                    '''check now that we have left arrow pressed'''
                    if event.key == pygame.K_RIGHT:  # on the left side
                        print("Right arrow pressed")
                        x_change += x_offset
                    '''
                    replay game if you want but just if you finished game
                    need to create a variable that game finished
                    '''
                    if event.key == pygame.K_SPACE:
                        self.create_simple_game()
                # CHECK IF THE KEY IS RELEASED
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        print("Key is released")
                        # here we need to add logic to stop car moving
                        x_change = 0  # car will stay on same position

            # change the screen fill using the created screen display
            '''
            x_value = width(from left to right)
            y_value =height (from top to bottom)
            '''
            # now we need first to update the initial_x to display the car
            self.load_road("pictures/road.jpeg", self.x_road, self.y_road, 445, 800)
            x_initial += x_change
            # print(x_initial)
            # PUT BOUNDARIES TO NOT CROSS THE ROAD ON LEFT OR RIGHT
            # WE CAN SIMPLY PUT THE BOUNDARIES ON THE KEY PRESS to check the initial_x
            if x_initial >= 428:  # boundary right side
                x_initial = 428
            if x_initial <= 328:  # boundary left side
                x_initial = 328
            # we need to change the y in order for the enemy car to move down
            y_value_car_enemy += y_offset_car
            self.load_car("pictures/red_car.png", x_initial, y_initial)
            self.load_car_enemy_image("pictures/enemy_car.jpeg", x_value_car_enemy, y_value_car_enemy)
            # display labels on screen
            screen_display.blit(label_score, (202, 45))
            screen_display.blit(label_score_int, (215, 70))
            screen_display.blit(label_level, (202, 130))
            screen_display.blit(label_speed_level, (202, 190))
            '''
                     CREATE A LABEL AND PUT IN MIDDLE OF SCREEN IF FINISH SCORE IS REACHED
             '''
            if score == self.finish_score:
                screen_display.blit(label_score, (202, 45))
                screen_display.blit(label_score_int, (215, 70))
                screen_display.blit(label_game_winner, (355, 270))
                y_value_car_enemy = 0
                self.load_car_enemy_image("pictures/enemy_car.jpeg", x_value_car_enemy, y_value_car_enemy)
                screen_display.blit(label_replay, (345, 320))
            pygame.display.update()

    @staticmethod
    def load_car(picture, x_value, y_value):
        image_car = pygame.image.load(picture)
        image_car_transformed = pygame.transform.scale(image_car, (90, 118))
        # screen_display.blit(image_car_transformed, (x_value, y_value))
        image_car_transformed_location = image_car_transformed.get_rect()
        image_car_transformed_location.center = x_value + 50, y_value + 50
        screen_display.blit(image_car_transformed, image_car_transformed_location)

    @staticmethod
    def load_road(picture, x_value, y_value, wanted_width, wanted_height):
        image_road = pygame.image.load(picture)
        # make the road to have the whole image width
        image_road_transformed = pygame.transform.scale(image_road, (wanted_width, wanted_height))
        screen_display.blit(image_road_transformed, (x_value, y_value))

    @staticmethod
    def load_car_enemy_image(picture, x_value, y_value):
        image_car = pygame.image.load(picture)
        image_car_transformed = pygame.transform.scale(image_car, (90, 118))
        screen_display.blit(image_car_transformed, (x_value, y_value))

    # random function to put random x value for another car
    @staticmethod
    def define_random_x_value():
        x = random.randint(0, 1)
        if x == 0:
            return 428
        else:
            return 328

    @staticmethod
    def get_random_color_level():
        x = random.randint(25, 225)
        y = random.randint(25, 255)
        z = random.randint(25, 255)
        return x,y,z
