import curses

from cuipyd.logging import log

class MainWindow():

    def __init__(self):
        self.children = []

    def _main_loop_internal(self):
        size = self._get_size()
        log("Something")
        log(str(size))

    def char_pressed(self):
        pass

    def loop(self):
        self._main_loop_internal()

    def terminate(self):
        curses.echo()
        curses.nocbreak()
        self._screen.keypad(False)
        curses.endwin()

    def _run_internal(self, *args, **kwargs):
        self._screen = curses.initscr()
        if curses.has_colors():
            curses.start_color()
        curses.noecho()
        curses.cbreak()
        self._screen.keypad(True)
        try:
            while True:
                self.loop()
        except KeyboardInterrupt:
            self.terminate()

    def run(self):
        curses.wrapper(self._run_internal)

    def _get_size(self):
        return self._screen.getmaxyx()


if __name__ == '__main__':
    MainWindow().run()
