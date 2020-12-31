import pathlib
import re
from PIL import Image, ImageColor
from nibbles.coordinate import Coordinate
from nibbles.barrier import Barrier
from nibbles.level.level import Level
from nibbles.level.level_parsers.level_parser_types import LevelParserTypes
from nibbles.level.level_parsers.level_parser_interface import LevelParserInterface


class PNGLevelParser(LevelParserInterface):
    """
    Represents a level parser that can parse PNG images
    """
    PARSER_TYPE = LevelParserTypes.PNG_PARSER
    FILE_NAME_PATTERN = 'level_\\d+\\.png'
    FILE_NAME_REGEX = re.compile(FILE_NAME_PATTERN, flags=re.I)
    BARRIER_COLOR = ImageColor.getrgb("black")
    FOOD_SPAWN_COLOR = ImageColor.getrgb("white")
    INITIAL_SNAKE_HEAD_SPAWN_COLOR = ImageColor.getrgb("lime")

    def __init__(self):
        self.level_dir = None
        self.level_width = None
        self.level_height = None

    @staticmethod
    def parse_png_level(file_path, expected_width, expected_height):
        """
        Creates a Level using information stored inside the given PNG image

        :param file_path: The full file path to a valid PNG level
        :param expected_width: The expected width of the level
        :param expected_height: The expected height of the level
        :return: A Level created from information stored inside the given PNG image
        """
        def interpret_pixel(pixel, x, y):
            pixel = (pixel[0], pixel[1], pixel[2])  # strip alpha channel
            if pixel == PNGLevelParser.BARRIER_COLOR:
                barriers.append(Barrier(row=expected_height-y-1, column=x))
            elif pixel == PNGLevelParser.FOOD_SPAWN_COLOR:
                food_spawns.append(Coordinate(row=expected_height-y-1, column=x))
            elif pixel == PNGLevelParser.INITIAL_SNAKE_HEAD_SPAWN_COLOR:
                initial_snake_head_spawns.append(Coordinate(row=expected_height-y-1, column=x))

        level_number = int(file_path.stem.split('_')[1])
        barriers = []
        food_spawns = []
        initial_snake_head_spawns = []
        with Image.open(file_path) as image:
            width, height = image.size
            if width != expected_width or height != expected_height:
                raise ValueError("Level image must be {0}x{1}".format(expected_width, expected_height))
            pixels = image.load()
            for i in range(0, width):
                for j in range(0, height):
                    interpret_pixel(pixels[i, j], i, j)
        return Level(level_number, barriers, food_spawns, initial_snake_head_spawns)

    def set_data_source(self, level_width, level_height, path):
        """
        Sets the path where the data source is located

        :param: level_width: The width of the level
        :param: level_height: The height of the level
        :param: path: The path where the data source is located
        """
        self.level_width = level_width
        self.level_height = level_height
        level_dir = pathlib.Path(path)
        if not level_dir.exists() or not level_dir.is_dir():
            raise RuntimeError("the data source is not a valid directory")
        self.level_dir = level_dir
        pass

    def parse_levels(self) -> list:
        """
        Parses the levels from the current data source

        :returns: A list of levels
        """
        if not self.level_dir:
            raise RuntimeError("no data source set")
        if not self.level_width or not self.level_height:
            raise RuntimeError("level resolution not set")
        parsed_levels = []
        for child in self.level_dir.iterdir():
            if child.is_file() and self.FILE_NAME_REGEX.fullmatch(child.name):
                parsed_levels.append(self.parse_png_level(child, self.level_width, self.level_height))
        return parsed_levels
