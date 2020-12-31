from threading import Thread
from nibbles import Nibbles
from nibbles.directions import Directions
from nibbles.display import Display
import pygame
from pygame.locals import *
from pygame.color import THECOLORS


class NibblesGUI:
    """
    Represents a gui controller for the nibbles game
    """
    # These should probably be a class to avoid invalid control schemes
    PLAYER_CONTROLS = {
        1: {
            pygame.K_UP: Directions.VECTOR_UP,
            pygame.K_RIGHT: Directions.VECTOR_RIGHT,
            pygame.K_DOWN: Directions.VECTOR_DOWN,
            pygame.K_LEFT: Directions.VECTOR_LEFT
        },
        2: {
            pygame.K_w: Directions.VECTOR_UP,
            pygame.K_d: Directions.VECTOR_RIGHT,
            pygame.K_s: Directions.VECTOR_DOWN,
            pygame.K_a: Directions.VECTOR_LEFT
        }
    }

    SNAKE_COLORS = [
        THECOLORS['white'],
        THECOLORS['red'],
        THECOLORS['orangered'],
        THECOLORS['green'],
        THECOLORS['hotpink'],
        THECOLORS['yellow'],
        THECOLORS['darkviolet'],
        THECOLORS['cyan']
    ]

    def __init__(self, board_width, board_height, initial_game_difficulty, number_of_players, number_of_ai,
                 ai_difficulty_level, display_scale, refresh_rate, level_parser_type, initial_level_number, skip_intro):
        self.nibbles = Nibbles(self.SNAKE_COLORS, board_width, board_height, initial_game_difficulty, number_of_players,
                               number_of_ai, ai_difficulty_level, level_parser_type, initial_level_number, skip_intro)
        if not self.nibbles.intro:
            self.initialize_nibbles()
        self.display = Display(self.nibbles, display_scale, refresh_rate)

    def initialize_nibbles(self):
        """
        Initializes current nibbles level
        :return:
        """
        self.nibbles.initialize_level()
        self.hook_player_controls()

    @staticmethod
    def set_snake_direction(snake, update_data):
        """Sets the direction that the player controlled snake should move

        :param: snake: The snake that the player is controlling
        :param: update_data: A dictionary of data used to update the snake direction
        """
        key = update_data['key']
        controls = NibblesGUI.PLAYER_CONTROLS[snake.player_number]
        if key in controls.keys():
            snake.direction_to_move = controls[key]

    def hook_player_controls(self):
        """
        Hooks the update direction event so the player can control the direction of the snake
        """
        for snake in self.nibbles.snakes:
            if snake.player_number:
                snake.on_update_direction = self.set_snake_direction

    def calculate_ai_directions(self):
        """
        Calculates the movement direction for the ai players in the nibbles instance
        Note: Uses multi-threading because the hard ai difficulty level really needs the extra horse power
        """
        threads = []
        update_data = {'food': self.nibbles.food, 'collision_map': self.nibbles.collision_map}
        for snake in self.nibbles.snakes:
            if not snake.player_number:
                ai_update_thread = Thread(target=snake.update_direction, args=(update_data, ))
                ai_update_thread.start()
                threads.append(ai_update_thread)
        for thread in threads:
            thread.join()

    def handle_keyboard(self, events):
        """
        Handles the input from the keyboard and adjusts the direction of player controlled snakes

        :param: events: Array of pygame events
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                key = event.key
                for snake in self.nibbles.snakes:
                    if snake.player_number:
                        snake.update_direction({"key": key})
                if self.nibbles.intro:
                    if self.nibbles.intro_1:
                        self.nibbles.intro_1 = False
                        self.nibbles.intro_2_players = True
                    elif self.nibbles.intro_2_players:
                        if pygame.K_0 < key < pygame.K_3:
                            self.nibbles.intro_2_players = False
                            self.nibbles.intro_2_ai = True
                            self.nibbles.number_of_players = int(key - pygame.K_0)
                    elif self.nibbles.intro_2_ai:
                        if pygame.K_0 <= key <= pygame.K_6:
                            self.nibbles.intro_2_ai = False
                            self.nibbles.intro_2_difficulty = True
                            self.nibbles.number_of_ai = int(key - pygame.K_0)
                    elif self.nibbles.intro_2_difficulty:
                        if pygame.K_0 < key <= pygame.K_9:
                            self.nibbles.intro_2_difficulty = False
                            self.nibbles.intro = False
                            self.nibbles.game_difficulty = float(key - pygame.K_0)
                            self.initialize_nibbles()
                elif key == pygame.K_ESCAPE:
                    self.nibbles.paused = not self.nibbles.paused

    def game_loop(self):
        """
        The main game loop that calls the update methods
        """
        clock = pygame.time.Clock()
        while True:
            if self.nibbles.stopped:
                break
            if not self.nibbles.paused:
                self.calculate_ai_directions()
                self.nibbles.update()
                if self.nibbles.snake_reset_needed:
                    self.nibbles.reset_snakes()
            clock.tick(15 * ((1 + self.nibbles.game_difficulty) / 2))

    def start_nibbles(self):
        """
        Starts the nibbles game
        """
        game_thread = Thread(target=self.game_loop)
        game_thread.start()
        clock = pygame.time.Clock()
        while not self.nibbles.stopped:
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    self.nibbles.stopped = True
                    break
            self.handle_keyboard(events)
            self.display.draw_frame()
            clock.tick(self.display.refresh_rate)
        game_thread.join()
        pygame.quit()
