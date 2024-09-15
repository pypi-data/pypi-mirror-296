from cuipyd.main_window import MainWindow
from cuipyd.ipane import IPane
from cuipyd.pane import Pane
from cuipyd.tuples import MathTup
from cuipyd.layout import VLayout, HLayout
from cuipyd.logging import log

class TestPane(Pane):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class TestWindow(MainWindow):

    def __init__(self):
        super().__init__()
        self.layout = HLayout(name="Base Layout")
        self.set_root_layout(self.layout)

        self.pane = TestPane(default_char='x', name="Xs")
        self.inner_layout = VLayout(name="Right Layout")

        self.layout._add_child(self.pane)
        #self.layout._add_child(self.pane2)
        self.layout._add_child(self.inner_layout)


        #self.pane2 = TestPane(parent=self.layout, default_char='o', name="Os")
        #
        self.pane2 = TestPane(default_char='', name="Os")
        self.pane3 = TestPane(default_char='i', name="Os")
        self.inner_layout._add_child(self.pane2)
        self.inner_layout._add_child(self.pane3)


    def _process_character(self, char):
        ch = chr(char)
        cs = [c._window.getmaxyx() for c in self._children]


if __name__ == '__main__':
    TestWindow().run()
