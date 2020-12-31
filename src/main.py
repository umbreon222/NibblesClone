from argparse import ArgumentParser
from nibbles.level.level_parsers.level_parser_types import LevelParserTypes
from nibbles.ai.ai_difficulty_levels import AiDifficultyLevel
from nibbles.nibbles_gui import NibblesGUI
BOARD_WIDTH = 80
BOARD_HEIGHT = 50


if __name__ == "__main__":
    arg_parser = ArgumentParser(description="Launch nibbles gui")
    arg_parser.add_argument('--level_dir', metavar='-ld', type=str, help='The path to the level data directory',
                            default=None)
    arg_parser.add_argument('--level_parser', metavar='-lp', type=LevelParserTypes,
                            help='The level parser to use (png_parser)', default="png_parser",
                            choices=[LevelParserTypes.PNG_PARSER])
    arg_parser.add_argument('--initial_level_number', metavar='-ln', type=int, help='The level number to play',
                            default=0)
    arg_parser.add_argument('--initial_game_difficulty', metavar='-d', type=float, help='The initial game difficulty',
                            default=1.0)
    arg_parser.add_argument('--number_of_players', metavar='-np', type=int, help='The number of human players',
                            default=1)
    arg_parser.add_argument('--number_of_ai', metavar='-na', type=int, help='The number of AI players',
                            default=0)
    arg_parser.add_argument('--ai_difficulty_level', metavar='-adl', type=AiDifficultyLevel,
                            help='The difficulty level of the ai (easy, intermediate, hard)', default="intermediate",
                            choices=[AiDifficultyLevel.EASY, AiDifficultyLevel.INTERMEDIATE, AiDifficultyLevel.HARD])
    arg_parser.add_argument('--display_scale', metavar='-ds', type=int, help='The multiplier for screen resolution',
                            default=15)
    arg_parser.add_argument('--refresh_rate', metavar='-rr', type=int, help='The screen refresh rate to use',
                            default=60)
    arg_parser.add_argument('--skip_intro', metavar='-si', type=bool, help='Should skip intro screen',
                            default=False)
    args = arg_parser.parse_args()
    nibbles_gui = NibblesGUI(board_width=BOARD_WIDTH, board_height=BOARD_HEIGHT,
                             initial_game_difficulty=args.initial_game_difficulty,
                             number_of_players=args.number_of_players, number_of_ai=args.number_of_ai,
                             ai_difficulty_level=args.ai_difficulty_level, display_scale=args.display_scale,
                             refresh_rate=args.refresh_rate, level_parser_type=args.level_parser,
                             initial_level_number=args.initial_level_number, skip_intro=args.skip_intro)
    nibbles_gui.start_nibbles()
