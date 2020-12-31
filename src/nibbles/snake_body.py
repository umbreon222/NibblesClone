from nibbles.coordinate import Coordinate


class SnakeBody(Coordinate):
    """
    Represents a snake body chunk
    """
    def __init__(self, row=0, column=0):
        """
        :param row: The row of the body chunk
        :param column: The column of the body chunk
        """
        Coordinate.__init__(self, row, column)
