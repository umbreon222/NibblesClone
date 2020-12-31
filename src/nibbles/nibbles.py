import os
import pathlib
from random import Random
from nibbles.level.level_parsers.level_parser_builder import LevelParserBuilder
from nibbles.directions import Directions
from nibbles.snake_body import SnakeBody
from nibbles.snake import Snake
from nibbles.ai import Ai
from nibbles.food import Food
from nibbles.level import Level


class Nibbles:
    def __init__(self, snake_colors: list, board_width, board_height, initial_game_difficulty, number_of_players,
                 number_of_ai, ai_difficulty_level, level_parser_type, initial_level_number, skip_intro):
        """
        :param: snake_colors: A list of unique colors that the snakes can be, must be 8
        :param: board_width: The width of the game board
        :param: board_height: The height of the game board
        :param: initial_game_difficulty: A multiplier that speeds up or slows down game play
        :param: number_of_players: The number of human players, must be 2 or less
        :param: number_of_ai: The number of AI players, must be 6 or less
        :param: ai_difficulty level: The AiDifficultyLevel to set the AI to
        :param: level_parser_type: The type of the level parser to use when parsing levels
        :param: initial_level_number: The index of the level to play
        :param: skip_intro: Determines whether the intro should be played
        """
        self.stopped = False
        self.paused = True  # Start paused to give the players some time to figure out where they are
        self.intro = not skip_intro
        self.intro_1 = self.intro
        self.intro_2_players = False
        self.intro_2_ai = False
        self.intro_2_difficulty = False
        self.snake_reset_needed = False
        self.loaded_level = None
        self.snake_colors = snake_colors
        self.available_colors = snake_colors.copy()
        self.board_width = board_width
        self.board_height = board_height
        self.game_difficulty = initial_game_difficulty
        self.number_of_players = number_of_players
        self.number_of_ai = number_of_ai
        self.ai_difficulty_level = ai_difficulty_level
        self.collision_map = []
        self.snakes = []
        self.killed_snakes = []
        self.levels = self.parse_levels(level_parser_type)
        self.level_number = initial_level_number
        self.food = None

    @property
    def snake_colors(self):
        return self._snake_colors

    @snake_colors.setter
    def snake_colors(self, snake_colors):
        if len(snake_colors) != 8:
            raise ValueError("snake colors must contain 8 colors")
        self._snake_colors = snake_colors

    @property
    def levels(self):
        return self._levels

    @levels.setter
    def levels(self, levels):
        if len(levels) == 0 or not isinstance(levels[0], Level):
            raise ValueError("levels must contain at least one level")
        self._levels = levels

    @property
    def board_width(self):
        return self._board_width

    @board_width.setter
    def board_width(self, board_width):
        if not isinstance(board_width, int):
            raise ValueError("board width must be an integer")
        if board_width < 1:
            raise ValueError("board width must be greater than or equal to 1")
        self._board_width = board_width

    @property
    def board_height(self):
        return self._board_height

    @board_height.setter
    def board_height(self, board_height):
        if not isinstance(board_height, int):
            raise ValueError("board height must be an integer")
        if board_height < 1:
            raise ValueError("board height must be greater than or equal to 1")
        self._board_height = board_height

    @property
    def game_difficulty(self):
        return self._game_difficulty

    @game_difficulty.setter
    def game_difficulty(self, game_difficulty):
        if not isinstance(game_difficulty, float):
            raise ValueError("game difficulty must be a float")
        if game_difficulty <= 0:
            raise ValueError("game difficulty must be greater than 0")
        self._game_difficulty = game_difficulty

    @property
    def number_of_players(self):
        return self._number_of_players

    @number_of_players.setter
    def number_of_players(self, number_of_players):
        if not isinstance(number_of_players, int):
            raise ValueError("number of players must be an integer")
        if number_of_players < 0:
            raise ValueError("number of players must be non-negative")
        self._number_of_players = number_of_players

    @property
    def number_of_ai(self):
        return self._number_of_ai

    @number_of_ai.setter
    def number_of_ai(self, number_of_ai):
        if not isinstance(number_of_ai, int):
            raise ValueError("number of AI must be an integer")
        if number_of_ai < 0:
            raise ValueError("number of AI must be non-negative")
        self._number_of_ai = number_of_ai

    def create_collision_map(self):
        """
        Creates a 3D collision map

        :return: A 3D collision map
        """
        return [[[] for _ in range(self.board_height)] for _ in range(self.board_width)]

    def parse_levels(self, level_parser_type):
        """
        Parses levels from level resource folder using the specified level parser type

        :param level_parser_type: The level parser type to use
        :return: Parsed levels
        """
        level_parser_builder = LevelParserBuilder(level_parser_type)
        level_parser = level_parser_builder.build()
        nibbles_file_path = pathlib.Path(os.path.abspath(__file__)).parent
        nibbles_file_path.resolve()
        level_dir = nibbles_file_path.joinpath('resources/levels')
        level_parser.set_data_source(self.board_width, self.board_height, level_dir)
        return level_parser.parse_levels()

    def place_coordinate_into_collision_map(self, coordinate):
        """
        Places a coordinate into the collision map

        :param coordinate: The coordinate to place into to the collision map
        """
        self.collision_map[coordinate.column][coordinate.row].append(coordinate)

    def remove_coordinate_from_collision_map(self, coordinate):
        """
        Removes a coordinate from the collision map

        :param coordinate: The coordinate to remove from the collision map
        """
        self.collision_map[coordinate.column][coordinate.row].remove(coordinate)

    def initialize_barriers(self):
        """
        Places the barriers from the currently loaded level into the collision map
        """
        for barrier in self.loaded_level.barriers:
            self.place_coordinate_into_collision_map(barrier)

    def find_random_food_spawn(self):
        """
        Finds a random food spawn location that is not taken by any other game object

        :return: A random food spawn coordinate that is not taken by any other game object
        """
        random = Random()
        food_spawns = []
        for spawn in self.loaded_level.food_spawns:
            if len(self.collision_map[spawn.column][spawn.row]) == 0:
                food_spawns.append(spawn)
        if len(food_spawns) == 0:
            raise RuntimeError("Can't locate a valid spawn")
        return random.choice(food_spawns)

    def create_food(self):
        """
        Creates a new food item

        :return: The new food item
        """
        random = Random()
        food = Food(points=random.randint(1, 9))
        temp_coord = self.find_random_food_spawn()
        food.row = temp_coord.row
        food.column = temp_coord.column
        return food

    def reserve_random_color(self):
        """
        Returns a random choice from the available colors list and removes it from the list

        :return: A random choice from the available colors list and removes it from the list
        """
        random = Random()
        return self.available_colors.pop(random.randint(0, len(self.available_colors) - 1))

    def initialize_snakes(self):
        """
        Creates snakes and spawns them at the locations defined by the currently loaded level

        :param: number_of_players: Number of human players
        :param: number_of_ai: Number of AI
        """
        number_of_defined_spawns = len(self.loaded_level.initial_snake_head_spawns)
        if number_of_defined_spawns != 8:
            raise RuntimeError("Level does not contain 8 snake spawns")
        number_of_snakes_to_spawn = self.number_of_players + self.number_of_ai
        for i in range(number_of_snakes_to_spawn):
            head_spawn_coord = self.loaded_level.initial_snake_head_spawns[i]
            head = SnakeBody(head_spawn_coord.row, head_spawn_coord.column)
            self.snakes.append(Snake(head, self.reserve_random_color()))
            self.place_coordinate_into_collision_map(head)

    def initialize_level(self):
        """
        Loads the currently selected level number into the game
        """
        self.collision_map = self.create_collision_map()
        for level in self.levels:
            if level.number == self.level_number:
                self.loaded_level = level
        if not self.loaded_level:
            raise RuntimeError("tried to load level {0} which doesn't exist".format(self.level_number))
        self.initialize_barriers()
        self.initialize_snakes()
        for x in range(len(self.snakes)):
            if x < self.number_of_players:
                self.snakes[x].player_number = x + 1
                self.snakes[x].lives = 5
            else:
                self.snakes[x].on_update_direction = Ai.resolve_difficulty_level(self.ai_difficulty_level)
                self.snakes[x].lives = 2  # these guys are hard, give them less chances to make me cry
        self.food = self.create_food()
        self.place_coordinate_into_collision_map(self.food)

    def reset_snakes(self):
        """
        Resets snake sizes and locations back to how they were at the beginning of the level
        """
        self.paused = True
        self.snake_reset_needed = False
        for snake_index in range(len(self.snakes)):
            self.remove_snake_from_collision_map(self.snakes[snake_index])
            self.snakes[snake_index].reset()
            head_spawn_coord = self.loaded_level.initial_snake_head_spawns[snake_index]
            self.snakes[snake_index].head.row = head_spawn_coord.row
            self.snakes[snake_index].head.column = head_spawn_coord.column
            self.place_coordinate_into_collision_map(self.snakes[snake_index].head)

    def update_snake_position(self, snake):
        """
        Updates the given snake's position in the playable area

        :param: The snake to update the position of
        """
        if snake.direction_to_move == Directions.OPPOSITE_DIRECTIONS[snake.last_direction_moved]:
            snake.direction_to_move = snake.last_direction_moved
        end_piece = snake.body.pop(-1)
        self.remove_coordinate_from_collision_map(end_piece)
        end_piece.row = snake.head.row
        end_piece.column = snake.head.column
        snake.body.insert(0, end_piece)
        snake.head = end_piece
        snake.head.row += snake.direction_to_move[1]
        snake.head.row = self.board_height - 1 if snake.head.row < 0 else snake.head.row % self.board_height
        snake.head.column += snake.direction_to_move[0]
        snake.head.column = self.board_width - 1 if snake.head.column < 0 else snake.head.column % self.board_width
        self.place_coordinate_into_collision_map(snake.head)
        snake.last_direction_moved = snake.direction_to_move

    def increase_snake_length(self, snake):
        """
        Increases the length of the given snake

        :param snake: The snake to increase the length of
        """
        new_tail = SnakeBody(snake.body[-1].row, snake.body[-1].column)
        snake.body.append(new_tail)
        self.place_coordinate_into_collision_map(new_tail)

    def remove_snake_from_collision_map(self, snake):
        """
        Removes the given snake from the collision map

        :param snake: The snake to remove from the collision map
        """
        for body_piece in snake.body:
            self.remove_coordinate_from_collision_map(body_piece)

    def should_snake_lose_life(self, snake):
        """
        Checks if the current snake should lose a life

        :param: snake: The snake to check for death
        :return: A boolean representing if the snake should lose a life
        """
        head_playable_space = self.collision_map[snake.head.column][snake.head.row]
        if len(head_playable_space) > 1:
            for coord in head_playable_space:
                if coord != self.food and coord != snake.head:
                    return True
        return False

    def update(self):
        """
        The main game logic that updates each frame
        """
        self.killed_snakes.clear()
        for snake in self.snakes:
            self.update_snake_position(snake)
            if self.should_snake_lose_life(snake):
                snake.lose_life()
                self.killed_snakes.append(snake)
                self.snake_reset_needed = True
            if snake.head.coordinates_equal(self.food):
                for i in range(self.food.points):
                    self.increase_snake_length(snake)
                snake.score += self.food.points
                self.remove_coordinate_from_collision_map(self.food)
                self.food = self.create_food()
                self.place_coordinate_into_collision_map(self.food)
        for snake in self.killed_snakes:
            if not snake.alive:
                self.remove_snake_from_collision_map(snake)
                self.snakes.remove(snake)
                self.stopped = len(self.snakes) == 0  # game over
