from nibbles.coordinate import Coordinate


class Food(Coordinate):
    """
    Represents a food item
    """
    def __init__(self, row=0, column=0, points=1):
        """
        :param row: Row of the food item
        :param column: Column of the food item
        :param points: The amount of points awarded to a snake that eats this food item
        """
        Coordinate.__init__(self, row, column)
        self.points = points
