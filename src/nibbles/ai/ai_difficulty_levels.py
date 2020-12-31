from enum import Enum


class AiDifficultyLevel(Enum):
    """
    Represents difficulty levels of the AI
    """
    EASY = 'easy'
    INTERMEDIATE = 'intermediate'
    HARD = 'hard'

    def __str__(self):
        return self.value
