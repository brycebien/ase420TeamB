import sys
sys.path.append('src')
from event_manager import EventManager

class Board:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = [[0] * width for _ in range(height)]
        self.line_manager = EventManager()

    def break_lines(self):
        lines_cleared = 0
        rows_to_remove = []

        for i in range(self.height - 1, -1, -1):
            if all(self.field[i]):
                rows_to_remove.insert(0, i)

        for row in rows_to_remove:
            del self.field[row]
            self.field.insert(0, [0] * self.width)
            lines_cleared += 1
        self.line_manager.notify(lines_cleared)
        return lines_cleared