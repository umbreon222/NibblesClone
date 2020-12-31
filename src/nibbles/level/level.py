class Level:
    """
    Represents a game level for nibbles
    """
    def __init__(self, level_number, barriers=None, food_spawns=None, initial_snake_head_spawns=None):
        """
        :param level_number: The number of the level (must be unique)
        :param barriers: A list of Barriers
        :param food_spawns: A list of valid Coordinates to spawn food
        :param initial_snake_head_spawns: A list of valid Coordinates to spawn snakes
        """
        if barriers is None:
            barriers = []
        if food_spawns is None:
            food_spawns = []
        if initial_snake_head_spawns is None:
            initial_snake_head_spawns = []
        self.number = level_number
        self.barriers = barriers
        self.food_spawns = food_spawns
        self.initial_snake_head_spawns = initial_snake_head_spawns
