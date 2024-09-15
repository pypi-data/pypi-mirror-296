import curses

from cuipyd.ipane import IPane
from cuipyd.logging import log

class Pane(IPane):

    def __init__(self, default_char=' ', name=None):
        super().__init__(name=name)
        assert len(default_char) == 1
        self.default_char = default_char

    def _refresh(self):
        pass

    def _render_frame(self, time_delta):
        y, x = self._window.getmaxyx()
        for r in range(y):
            for c in range(x):
                try:
                    self._window.addstr(r, c, self.default_char)
                    #self._window.addch(r, c, ord(self.default_char))
                except:
                    pass
        self._window.refresh()

