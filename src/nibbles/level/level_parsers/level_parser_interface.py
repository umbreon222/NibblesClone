class LevelParserInterface:
    """
    Represents a basic level parser
    """
    def set_data_source(self, level_width, level_height, path: str):
        """
        Sets the path where the data source is located

        :param: level_width: The width of the level
        :param: level_height: The height of the level
        :param: path: The path where the data source is located
        """
        pass

    def parse_levels(self) -> list:
        """
        Parses the levels from the current data source

        :returns: A list of levels
        """
        pass
