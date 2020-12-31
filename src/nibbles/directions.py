class Directions:
    """
    Represents directions as 2D vectors
    """
    VECTOR_UP = (0, 1)
    VECTOR_DOWN = (0, -1)
    VECTOR_LEFT = (-1, 0)
    VECTOR_RIGHT = (1, 0)

    OPPOSITE_DIRECTIONS = {
        VECTOR_UP: VECTOR_DOWN,
        VECTOR_DOWN: VECTOR_UP,
        VECTOR_LEFT: VECTOR_RIGHT,
        VECTOR_RIGHT: VECTOR_LEFT
    }

    DIRECTIONS = [
        VECTOR_UP,
        VECTOR_DOWN,
        VECTOR_LEFT,
        VECTOR_RIGHT
    ]

