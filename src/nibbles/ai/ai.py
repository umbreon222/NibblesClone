import math
from nibbles.directions import Directions
from nibbles.food import Food
from nibbles.ai.ai_difficulty_levels import AiDifficultyLevel
from nibbles.ai.a_star import AStar


class Ai:
    @staticmethod
    def is_in_bounds(direction_to_check, current_col, current_row, map_width, map_height):
        """
        Returns true if the current position plus the direction to check is within the map
        :param direction_to_check:
        :param current_col: The column of the current position
        :param current_row: The row of the current position
        :param map_width: Width of the map
        :param map_height: Height of the map
        :return: True if the current position plus the direction to check is within the map otherwise false
        """
        future_x = direction_to_check[0] + current_col
        future_y = direction_to_check[1] + current_row
        return 0 < future_x < map_width and 0 < future_y < map_height

    @staticmethod
    def easy_calculate_snake_direction(snake, update_data):
        """
        Calculates the direction that the snake AI should move without path finding, doesn't avoid obstacles

        :param: snake: The snake that the AI is controlling
        :param: update_data: A dictionary of data used to update the snake direction
        """
        food = update_data['food']
        current_row = snake.head.row
        current_col = snake.head.column
        if current_row != food.row:
            if current_row < food.row:
                if snake.last_direction_moved != Directions.OPPOSITE_DIRECTIONS[Directions.VECTOR_UP]:
                    snake.direction_to_move = Directions.VECTOR_UP
                else:
                    snake.direction_to_move = Directions.VECTOR_RIGHT
            else:
                if snake.last_direction_moved != Directions.OPPOSITE_DIRECTIONS[Directions.VECTOR_DOWN]:
                    snake.direction_to_move = Directions.VECTOR_DOWN
                else:
                    snake.direction_to_move = Directions.VECTOR_LEFT
        else:
            if current_col < food.column:
                if snake.last_direction_moved != Directions.OPPOSITE_DIRECTIONS[Directions.VECTOR_RIGHT]:
                    snake.direction_to_move = Directions.VECTOR_RIGHT
                else:
                    snake.direction_to_move = Directions.VECTOR_UP
            else:
                if snake.last_direction_moved != Directions.OPPOSITE_DIRECTIONS[Directions.VECTOR_LEFT]:
                    snake.direction_to_move = Directions.VECTOR_LEFT
                else:
                    snake.direction_to_move = Directions.VECTOR_DOWN

    @staticmethod
    def intermediate_calculate_snake_direction(snake, update_data):
        """
        Calculates the direction that the snake AI should move without path finding, avoids obstacles randomly

        :param: snake: The snake that the AI is controlling
        :param: update_data: A dictionary of data used to update the snake direction
        """
        current_row = snake.head.row
        current_col = snake.head.column
        collision_map = update_data['collision_map']
        map_width = len(collision_map)
        map_height = 0
        if map_width > 0:
            map_height = len(collision_map[0])
        Ai.easy_calculate_snake_direction(snake, update_data)  # use this as a base
        # then improve it by avoiding obstacles
        potential_next_coords = (current_col + snake.direction_to_move[0], current_row + snake.direction_to_move[1])
        space_to_move_to = collision_map[potential_next_coords[0]][potential_next_coords[1]]
        danger = False
        if len(space_to_move_to) > 0:
            for x in space_to_move_to:
                if not isinstance(x, Food):
                    danger = True
                    break
        if not danger:
            return
        for direction in Directions.DIRECTIONS:
            if (direction != Directions.OPPOSITE_DIRECTIONS[snake.last_direction_moved]
                    and Ai.is_in_bounds(direction, current_col, current_row, map_width, map_height)
                    and len(collision_map[current_col + direction[0]][current_row + direction[1]]) == 0):
                snake.direction_to_move = direction
                return
        print("intermediate AI is stumped")

    class SnakeSolver(AStar):
        def __init__(self, grid, illegal_coordinate):
            self.grid = grid
            self.illegal_coordinate = illegal_coordinate
            self.width = len(self.grid)
            self.height = len(self.grid[0])

        def heuristic_cost_estimate(self, n1, n2):
            """
            Computes the 'direct' distance between two (x,y) tuples
            """
            (x1, y1) = n1
            (x2, y2) = n2
            euclidean_distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            return euclidean_distance

        def distance_between(self, n1, n2):
            """
            this method always returns 1, as two 'neighbors' are always adjacent
            """
            return 1

        def neighbors(self, node):
            """
            for a given coordinate in the maze, returns up to 4 adjacent(north,east,south,west)
            nodes that can be reached (=any adjacent coordinate that is not a wall)
            """
            x, y = node
            neighbors = [(nx, ny) for nx, ny in [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)] if
                         0 <= nx < self.width and 0 <= ny < self.height
                         and (nx, ny) != self.illegal_coordinate
                         and (len(self.grid[nx][ny]) == 0 or isinstance(self.grid[nx][ny][0], Food))]
            return neighbors

    @staticmethod
    def hard_calculate_snake_direction(snake, update_data):
        """
        Calculates the direction that the snake AI should move using A*
        NOTE: This will probably not get done during the projects time frame but if I get bored, who knows.

        :param: snake: The snake that the AI is controlling
        :param: update_data: A dictionary of data used to update the snake direction
        """
        food = update_data['food']
        curr_pos = (snake.head.column, snake.head.row)
        collision_map = update_data['collision_map']
        opposite_direction = Directions.OPPOSITE_DIRECTIONS[snake.last_direction_moved]
        illegal_coordinate = (curr_pos[0] + opposite_direction[0], curr_pos[1] + opposite_direction[1])
        path = Ai.SnakeSolver(collision_map, illegal_coordinate).astar(curr_pos, (food.column, food.row))
        if path and len(path) > 1:
            next_location = path[1]
            direction = (next_location[0] - curr_pos[0], next_location[1] - curr_pos[1])
            snake.direction_to_move = direction
            return
        print("hard AI is stumped")

    @staticmethod
    def resolve_difficulty_level(ai_difficulty_level):
        """
        Returns the correct 'calculate_snake_direction' method based on the provided ai difficulty level

        :param ai_difficulty_level: The AiDifficultyLevel to return a 'calculate_snake_direction' method for
        :return: The correct 'calculate_snake_direction' method based on the provided ai difficulty level
        """
        if ai_difficulty_level == AiDifficultyLevel.EASY:
            return Ai.easy_calculate_snake_direction
        elif ai_difficulty_level == AiDifficultyLevel.INTERMEDIATE:
            return Ai.intermediate_calculate_snake_direction
        elif ai_difficulty_level == AiDifficultyLevel.HARD:
            return Ai.hard_calculate_snake_direction
        raise RuntimeError("invalid ai difficulty level '{0}'".format(ai_difficulty_level))
