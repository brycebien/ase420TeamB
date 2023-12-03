class LockedColor:
    def __init__(self):
        self.lockedColor=7
    def changeColor(self, figure):
        figure.color = self.lockedColor
    def setLockedColor(self, color):
        self.lockedColor = color