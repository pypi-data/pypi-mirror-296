import curses
from typing import Union

from cuipyd.logging import log

class IPane():

    def __init__(self, name=None):
        self._pane_parent = None
        self._is_active = True
        self._window = None
        self._name = name

    def get_name(self):
        if self._name:
            return self._name
        return ""

    @property
    def _parent(self):
        return self._pane_parent

    @property
    def _root(self):
        return self._parent._root

    @property
    def _base_screen(self):
        return self._root._screen

    def _set_parent(self, parent):
        self._pane_parent = parent
        self._window = self._parent._window.derwin(0, 0)

    def _refresh(self):
        pass

    def _render_frame(self, time_delta):
        pass

    def _set_active(self, is_active):
        self._is_active = is_active

    def _update_window_size(self, rows, cols, r_pos, c_pos):
        if not self._window:
            return
        del self._window
        self._window = self._parent._window.derwin(rows, cols, r_pos, c_pos)

