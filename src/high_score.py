import os

class HighScore:
    def __init__(self):
        self.score = 0
        if os.path.exists('highscore.txt'):
            with open ('highscore.txt', 'r') as file:
                self.high_score = int(file.read())
        else:
            with open('highscore.txt', 'w') as file:
                file.write('0')
                self.high_score = 0

    def update_score(self, amnt):
        self.score += amnt
        if self.score > self.high_score:
            self.high_score = self.score
            with open ('highscore.txt', 'w') as file:
                file.write(str(self.high_score))