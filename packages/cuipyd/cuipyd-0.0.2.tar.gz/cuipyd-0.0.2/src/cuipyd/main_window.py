import curses
import threading
import time

from typing import Tuple

import setproctitle

from cuipyd.logging import log
from cuipyd.threads import StoppableLoopThread
from cuipyd.layout import Layout

class MainWindow():

    def __init__(self, title:str=None):
        self._children = []
        self._last_frame_time = time.time()
        self._min_frame_wait_time = 0.01
        self._prepare_curses()
        self._update_title(title)
        self._base_layout = None

    def set_root_layout(self, layout:Layout):
        self._base_layout = layout
        self._base_layout._set_parent(self)
        rows, cols = self._get_size()
        self._base_layout._update_window_size(rows, cols, 0, 0)

    @property
    def _root(self):
        return self

    @property
    def _window(self):
        return self._screen

    def _update_title(self, title):
        self._title = title
        if self._title:
            setproctitle.setproctitle(self._title)

    def _get_time_delta(self) -> float:
        now_time = time.time()
        time_delta = now_time - self._last_frame_time
        self._last_frame_time = now_time
        return time_delta

    def _render_loop(self) -> None:
        time.sleep(self._min_frame_wait_time)
        time_delta = self._get_time_delta()
        self._render_frame(time_delta)

    def _render_frame(self, time_delta):
        if self._base_layout:
            self._base_layout._render_frame(time_delta)
        self._screen.refresh()

    def _start_rendering(self) -> None:
        self._render_thread = StoppableLoopThread(target=self._render_loop)
        self._render_thread.start()

    def _stop_rendering(self) -> None:
        self._render_thread.stop()
        self._render_thread.join()

    def terminate(self) -> None:
        curses.echo()
        curses.nocbreak()
        self._screen.keypad(False)
        curses.endwin()

    def _prepare_curses(self) -> None:
        self._screen = curses.initscr()
        if curses.has_colors():
            curses.start_color()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self._screen.keypad(True)

    def _process_character(self, char) -> None:
        pass

    def _run_internal(self, *args, **kwargs) -> None:
        self._start_rendering()
        try:
            while True:
                ch = self._screen.getch()
                log(chr(ch))
                if ch == curses.KEY_RESIZE:
                    self._render_thread.pause()
                    log(str(self._base_layout))
                    size = self._get_size()
                    if self._base_layout is not None:
                        self._base_layout._update_window_size(size[0], size[1], 0, 0)
                    self._render_thread.unpause()
                else:
                    if chr(ch) == 'q':
                        self._stop_rendering()
                        self.terminate()
                    try:
                        self._process_character(ch)
                    except KeyboardInterrupt:
                        self._stop_rendering()
                        self.terminate()

        except KeyboardInterrupt:
            self._stop_rendering()
            self.terminate()

    def run(self):
        curses.wrapper(self._run_internal)

    """ Rows, Columns """
    def _get_size(self) -> Tuple[int, int]:
        return self._screen.getmaxyx()


if __name__ == '__main__':
    MainWindow().run()
