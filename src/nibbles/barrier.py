from nibbles.coordinate import Coordinate


class Barrier(Coordinate):
    """
    Represents a barrier
    """
    def __init__(self, row=0, column=0):
        """
        :param row: The row of the barrier
        :param column: The column of the barrier
        """
        Coordinate.__init__(self, row, column)
