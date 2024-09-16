import asyncio
import curses
import traceback

from lyrics.listener.player import Player
from lyrics.display.window import Window


class App:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.player = Player()
        self.window = Window(stdscr, self.player)


    def start_pager(self):
        pass

    def stdout_lyrics(self):
        pass

    