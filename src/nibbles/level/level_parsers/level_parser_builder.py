from nibbles.level.level_parsers.level_parser_types import LevelParserTypes
from nibbles.level.level_parsers.level_parser_interface import LevelParserInterface
from nibbles.level.level_parsers.png_level_parser import PNGLevelParser


class LevelParserBuilder:
    """
    Represents a way to dynamically create a level parser based on some input parameters
    """
    def __init__(self, level_parser_type: LevelParserTypes):
        """
        :param level_parser_type: The type of level parser to build
        """
        self.level_parser_type = level_parser_type

    def build(self) -> LevelParserInterface:
        """
        Initializes a level parser matching the input parameters
        :return: A level parser that matches the input parameters
        """
        if self.level_parser_type == LevelParserTypes.PNG_PARSER:
            return PNGLevelParser()
        else:
            raise RuntimeError("invalid level parser '{0}'".format(self.level_parser_type))
