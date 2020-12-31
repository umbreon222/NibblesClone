import math
import pygame
import os
import pathlib
from pygame.color import THECOLORS


class Display:
    """
    Represents the logic that draws frames to the screen for a nibbles game instance
    """
    STATS_BAR_HEIGHT = 2

    def __init__(self, nibbles, display_scale, refresh_rate):
        """
        Initializes the pygame window

        :param: nibbles: The game instance to display
        :param: display_scale: The multiplier to apply to the game board resolution to obtain the display resolution
        :param: refresh_rate: How many times a second the display should be updated
        """
        self.use_alternate_border_animation = False
        self.nibbles = nibbles
        self.display_scale = display_scale
        self.refresh_rate = refresh_rate
        self.display_width = self.nibbles.board_width * self.display_scale
        self.display_height = (self.nibbles.board_height + self.STATS_BAR_HEIGHT) * self.display_scale
        self.pixel_size = self.calculate_game_coordinate_size()
        pygame.init()
        self.display = pygame.display.set_mode((self.display_width, self.display_height), 0, 32)
        self.display.fill(THECOLORS['black'])

    @property
    def refresh_rate(self):
        return self._refresh_rate

    @refresh_rate.setter
    def refresh_rate(self, refresh_rate):
        if not isinstance(refresh_rate, int):
            raise ValueError("refresh rate must be an integer")
        if refresh_rate < 1:
            raise ValueError("refresh rate must be greater than 0")
        self._refresh_rate = refresh_rate

    @property
    def display_scale(self):
        return self._display_scale

    @display_scale.setter
    def display_scale(self, display_scale):
        if not isinstance(display_scale, int):
            raise ValueError("display scale must be an integer")
        if display_scale < 1:
            raise ValueError("display scale must greater than 0")
        self._display_scale = display_scale

    def calculate_game_coordinate_size(self):
        """
        Calculates the size in pixels that each game coordinate should be

        :return: The size in pixels that each game coordinate should be
        """
        pixel_size = self.display_width / self.nibbles.board_width
        if math.floor(pixel_size) != pixel_size:
            raise RuntimeError("calculated pixel size is not an integer")
        return pixel_size
        
    def draw_frame(self):
        """
        The main loop that draws the game state to the screen
        """
        self.draw_play_area()
        if self.nibbles.loaded_level:
            self.draw_barriers()
            self.draw_snakes()
            self.draw_food()
            self.draw_game_stats()
        if self.nibbles.paused:
            if self.nibbles.intro:
                self.draw_intro_screen()
            elif len(self.nibbles.killed_snakes) == 0:
                self.draw_game_paused()
            else:
                self.draw_snake_death()
        pygame.display.update()

    def draw_play_area(self):
        """
        Draws the play area and edge barriers for the given game
        """
        self.display.fill(THECOLORS['black'])
        pygame.draw.rect(self.display, THECOLORS['blue'], (0,
                                                           self.pixel_size * self.STATS_BAR_HEIGHT,
                                                           self.display_width,
                                                           self.display_height))

    def draw_game_stats(self):
        """
        Draws the stats of the given game to the top portion of the game window
        """
        text = ""
        if self.STATS_BAR_HEIGHT <= 0:
            return
        font_size = math.floor(self.STATS_BAR_HEIGHT / self.nibbles.board_height * self.display_height)
        font = pygame.font.Font('freesansbold.ttf', font_size)
        stat_format_text = 'Player {0} Score: {1} Lives: {2}'
        for snake in self.nibbles.snakes:
            if snake.player_number:
                text_to_display = stat_format_text.format(snake.player_number, snake.score, snake.lives, snake.color)
                text = font.render(text_to_display, True, snake.color, THECOLORS['black'])
                text_rect = text.get_rect()
                x_segment_length = self.display_width // 5
                x = x_segment_length * (snake.player_number + (snake.player_number - 1) * 2)
                text_rect.center = (x, font_size // 2)
                self.display.blit(text, text_rect)

    def draw_barriers(self):
        """
        Draws the level barriers of the given game
        """
        for barrier in self.nibbles.loaded_level.barriers:
            pygame.draw.rect(self.display, THECOLORS['coral'],
                             (barrier.column * self.pixel_size,
                              self.display_height - ((barrier.row + 1) * self.pixel_size),
                              self.pixel_size,
                              self.pixel_size))

    def draw_snakes(self):
        """
        Draws the snakes for the given game
        """
        for snake in self.nibbles.snakes:
            for coordinate in snake.body:
                pygame.draw.rect(self.display, snake.color,
                                 (coordinate.column * self.pixel_size,
                                  self.display_height - ((coordinate.row + 1) * self.pixel_size),
                                  self.pixel_size,
                                  self.pixel_size))

    def draw_food(self):
        """
        Draws the food as a number indicating its value for the given game
        """
        color = THECOLORS['yellow']
        font = pygame.font.Font('freesansbold.ttf', 18)
        text = font.render(str(self.nibbles.food.points), True, color)
        text_rect = text.get_rect()
        text_rect.center = (self.nibbles.food.column * self.pixel_size + self.pixel_size // 2,
                            self.display_height - (self.nibbles.food.row + 1) * self.pixel_size + self.pixel_size // 2)
        self.display.blit(text, text_rect)

    def draw_game_paused(self):
        """
        Draws a notification at the center of the screen saying that the game is paused
        """
        font_size = math.floor(self.STATS_BAR_HEIGHT / self.nibbles.board_height * self.display_height)
        font = pygame.font.Font('freesansbold.ttf', font_size)
        text = font.render('Game Paused', True, THECOLORS['white'], THECOLORS['black'])
        text_rect = text.get_rect()
        text_rect.center = (self.display_width // 2, self.display_height // 2)
        self.display.blit(text, text_rect)

    def draw_snake_death(self):
        """
        Draws a notification at the center of the screen saying that the game is paused
        """
        font_size = math.floor(self.STATS_BAR_HEIGHT / self.nibbles.board_height * self.display_height)
        font = pygame.font.Font('freesansbold.ttf', font_size)
        dead_snake = self.nibbles.killed_snakes[0]
        text = 'Bot Died' if not dead_snake.player_number else 'Player {} Died'.format(dead_snake.player_number)
        rendered_text = font.render(text, True, THECOLORS['white'], THECOLORS['black'])
        text_rect = rendered_text.get_rect()
        text_rect.center = (self.display_width // 2, self.display_height // 2)
        self.display.blit(rendered_text, text_rect)

    def draw_intro_screen(self):
        """
        The first display to be displayed. The intro screen.
        """
        intro_title = "Python Nibbles"
        intro_text_1 = "Nibbles is a game for one to eight player. Navigate your snakes"
        intro_text_2 = "around the game board trying to eat up numbers. The more numbers you eat"
        intro_text_3 = "up, the more points you gain and the longer your snake becomes."
        intro_continue_text = "Press any key to continue"

        intro_players = "How many players (1 to 2)? "
        if not self.nibbles.intro_2_players:
            intro_players += str(self.nibbles.number_of_players)
        intro_ai = "How many players does computer play (0 to 6)? "
        if not self.nibbles.intro_2_ai:
            intro_ai += str(self.nibbles.number_of_ai)
        intro_diff_1 = "Skill level (1 to 9)? "
        if not self.nibbles.intro_2_difficulty:
            intro_diff_1 += str(self.nibbles.game_difficulty)
        intro_diff_2 = "1 = Novice"
        intro_diff_3 = "3 = Expert"
        intro_diff_4 = "9 = Twiddle Fingers"
        intro_diff_5 = "Computer speed may affect your skill level"

        display_file_path = pathlib.Path(os.path.abspath(__file__)).parent
        display_file_path.resolve()
        intro_resource_dir = display_file_path.joinpath('resources/intro')

        background_1_path = intro_resource_dir.joinpath('border animation 1.png')
        background_2_path = intro_resource_dir.joinpath('border animation 2.png')
        scaled_size = (80 * self.display_scale, 50 * self.display_scale)
        background_animation_1 = pygame.transform.scale(pygame.image.load(str(background_1_path)), scaled_size)
        background_animation_2 = pygame.transform.scale(pygame.image.load(str(background_2_path)), scaled_size)

        self.display.fill(THECOLORS['black'])

        if self.use_alternate_border_animation:
            image_rect = background_animation_1.get_rect()
            image_rect = image_rect.move(0, (self.STATS_BAR_HEIGHT * self.display_scale))
            self.display.blit(background_animation_1, image_rect)
        else:
            image_rect = background_animation_2.get_rect()
            image_rect = image_rect.move(0, (self.STATS_BAR_HEIGHT * self.display_scale))
            self.display.blit(background_animation_2, image_rect)

        if self.nibbles.intro_1:
            font = pygame.font.Font('freesansbold.ttf', 50)
            title = font.render(intro_title, True, THECOLORS['white'], THECOLORS['black'])
            title_rect = title.get_rect()
            title_rect.center = (self.display_width // 2, 110)
            self.display.blit(title, title_rect)

            font = pygame.font.Font('freesansbold.ttf', 30)
            text_1 = font.render(intro_text_1, True, THECOLORS['white'], THECOLORS['black'])
            text_rect_1 = text_1.get_rect()
            text_rect_1.center = (self.display_width // 2, 276)
            self.display.blit(text_1, text_rect_1)

            text_2 = font.render(intro_text_2, True, THECOLORS['white'], THECOLORS['black'])
            text_rect_2 = text_2.get_rect()
            text_rect_2.center = (self.display_width // 2, 316)
            self.display.blit(text_2, text_rect_2)

            text_3 = font.render(intro_text_3, True, THECOLORS['white'], THECOLORS['black'])
            text_rect_3 = text_3.get_rect()
            text_rect_3.center = (self.display_width // 2, 356)
            self.display.blit(text_3, text_rect_3)

            continue_text = font.render(intro_continue_text, True, THECOLORS['white'], THECOLORS['black'])
            continue_text_rect = continue_text.get_rect()
            continue_text_rect.center = (self.display_width // 2, 700)
            self.display.blit(continue_text, continue_text_rect)

        if self.nibbles.intro_2_players or self.nibbles.intro_2_ai or self.nibbles.intro_2_difficulty:
            font = pygame.font.Font('freesansbold.ttf', 30)
            text = font.render(intro_players, True, THECOLORS['white'], THECOLORS['black'])
            text_rect = text.get_rect()
            text_rect.center = (self.display_width // 2, 200)
            self.display.blit(text, text_rect)

        if self.nibbles.intro_2_ai or self.nibbles.intro_2_difficulty:
            font = pygame.font.Font('freesansbold.ttf', 30)
            text = font.render(intro_ai, True, THECOLORS['white'], THECOLORS['black'])
            text_rect = text.get_rect()
            text_rect.center = (self.display_width // 2, 240)
            self.display.blit(text, text_rect)

        if self.nibbles.intro_2_difficulty:
            font = pygame.font.Font('freesansbold.ttf', 30)
            text = font.render(intro_diff_1, True, THECOLORS['white'], THECOLORS['black'])
            text_rect = text.get_rect()
            text_rect.center = (self.display_width // 2, 300)
            self.display.blit(text, text_rect)

            font = pygame.font.Font('freesansbold.ttf', 30)
            text = font.render(intro_diff_2, True, THECOLORS['white'], THECOLORS['black'])
            text_rect = text.get_rect()
            text_rect.center = (self.display_width // 2, 340)
            self.display.blit(text, text_rect)

            font = pygame.font.Font('freesansbold.ttf', 30)
            text = font.render(intro_diff_3, True, THECOLORS['white'], THECOLORS['black'])
            text_rect = text.get_rect()
            text_rect.center = (self.display_width // 2, 380)
            self.display.blit(text, text_rect)

            font = pygame.font.Font('freesansbold.ttf', 30)
            text = font.render(intro_diff_4, True, THECOLORS['white'], THECOLORS['black'])
            text_rect = text.get_rect()
            text_rect.center = (self.display_width // 2, 420)
            self.display.blit(text, text_rect)

            font = pygame.font.Font('freesansbold.ttf', 30)
            text = font.render(intro_diff_5, True, THECOLORS['white'], THECOLORS['black'])
            text_rect = text.get_rect()
            text_rect.center = (self.display_width // 2, 460)
            self.display.blit(text, text_rect)

        self.use_alternate_border_animation = not self.use_alternate_border_animation
