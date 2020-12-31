from nibbles.directions import Directions


class Snake:
    """
    Represents a snake containing a list of snake chunks
    """
    def __init__(self, head, color, lives=1, body=None, direction_to_move=Directions.VECTOR_LEFT, score=0,
                 player_number=None, on_update_direction=None):
        """
        :param: head: A SnakeBody representing where to place the snake's head
        :param: color: Color of the snake
        :param: lives: Number of lives to give the snake
        :param: body: A list of snake body chunks
        :param: direction_to_move: The direction to the snake wants to move
        :param: score: The current score of the snake
        :param: player_number: the player number of the snake (None if not player controlled)
        :param: update_direction_callback: The method that is called when the snakes direction should update
        """
        self.head = head
        self.color = color
        self.lives = lives
        self.body = body if body else [self.head]
        self.last_direction_moved = direction_to_move
        self.direction_to_move = direction_to_move
        self.score = score
        self.player_number = player_number
        self.alive = self.calculate_alive()
        self.on_update_direction = on_update_direction

    def lose_life(self):
        """
        Removes a life from the snake and updates the alive status
        """
        self.lives -= 1
        self.alive = self.calculate_alive()

    def calculate_alive(self):
        """
        Returns a boolean representing if the snake's lives are greater than 0

        :return: True if the snake's lives are greater than 0
        """
        return self.lives > 0

    def reset(self):
        """
        Resets the snakes length by removing all body pieces except the head
        """
        self.body.clear()
        self.body.append(self.head)

    def update_direction(self, update_data: dict):
        """
        Calls the update direction handler with update_data

        :param update_data: The data to update with
        """
        if self.on_update_direction:
            self.on_update_direction(self, update_data)
