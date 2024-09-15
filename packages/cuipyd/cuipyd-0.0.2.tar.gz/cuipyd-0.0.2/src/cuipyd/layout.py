from cuipyd.ipane import IPane
from cuipyd.logging import log

class Layout(IPane):

    def __init__(self, name=None):
        super().__init__(name=name)
        self._children = []
        self._weights = []
        self._horizontal = True

    def _update_window_size(self, rows, cols, r_pos, c_pos):
        super()._update_window_size(rows, cols, r_pos, c_pos)
        self._resize()

    def _add_child(self, child:IPane, **kwargs):
        child._set_parent(self)
        if kwargs.get('weight', False):
            self._weights.append(int(kwargs['weight']))
        else:
            self._weights.append(1)
        self._children.append(child)
        self._resize()

    def _resize(self):
        y, x = self._window.getmaxyx()

        if self._horizontal:
            screen_sizes = self._get_real_weights(x, self._weights)
            start_col = 0
            for i in range(len(self._children)):
                child = self._children[i]
                width = screen_sizes[i]
                child._update_window_size(y, width, 0, start_col)
                start_col += width
        else:
            screen_sizes = self._get_real_weights(y, self._weights)
            start_row = 0
            for i in range(len(self._children)):
                child = self._children[i]
                height = screen_sizes[i]
                child._update_window_size(height, x, start_row, 0)
                start_row += height


    @staticmethod
    def _get_real_weights(size, weights):
        total_weight = sum(weights)
        if total_weight == 0:
            return []

        base_val = size // total_weight
        output_sizes = []
        for w in weights:
            output_sizes.append(w * base_val)
        
        total_size = sum(output_sizes)
        if total_size < size:
            diff = size - total_size
            for i in range(diff):
                output_sizes[i % len(output_sizes)] += 1

        return output_sizes

    def _render_frame(self, time_delta):
        if not self._is_active:
            return

        for child in self._children:
            if not child._is_active:
                continue
            child._render_frame(time_delta)
        self._window.refresh()

class HLayout(Layout):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class VLayout(Layout):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._horizontal = False

