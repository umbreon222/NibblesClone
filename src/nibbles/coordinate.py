class Coordinate:
    """
    Represents a row and column based coordinate in the game
    """
    def __init__(self, row=0, column=0):
        """
        :param row: The row
        :param column: The column
        """
        self.row = row
        self.column = column

    def coordinates_equal(self, other):
        """
        Checks if two coordinates are equal by value

        :param other: Coordinate to compare with
        :return: A boolean representing if the two coordinates are equal by value
        """
        if isinstance(other, Coordinate):
            return (self.row, self.column) == (other.row, other.column)
        return False
