import random
import sys
sys.path.append('src')
from figures import Figures


class NextShape:
    MAX_FIGURE_INDEX = len(Figures) - 1
    def __init__(self):
        self.next_shape = None
        self.current_shape = None
        self.has_been_set = False
    
    def determineNext(self):
        if not self.has_been_set:
            self.current_shape = random.randint(0, self.MAX_FIGURE_INDEX)
            self.next_shape = random.randint(0, self.MAX_FIGURE_INDEX)
            self.has_been_set = True
            return self.current_shape
        else:
            self.current_shape = self.next_shape
            self.next_shape = random.randint(0, self.MAX_FIGURE_INDEX)
            return self.current_shape