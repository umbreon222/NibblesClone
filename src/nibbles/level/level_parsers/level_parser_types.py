from enum import Enum


class LevelParserTypes(Enum):
    """
    Represents different types of level parsers
    """
    PNG_PARSER = 'png_parser'

    def __str__(self):
        return self.value
