""" Python package for playing NYT games on the command line"""
from nyt_games_cli.main import NYTGames

__version__ = "0.0.2"

if __name__ == '__main__':
    NYTGames().loop()
