from themes import color_themes

class ThemeSelector:
    _instance = None

    @staticmethod
    def getInstance():
        if ThemeSelector._instance is None:
            ThemeSelector()
        return ThemeSelector._instance
    
    def __init__(self):
        ThemeSelector._instance = self
        ThemeSelector._instance.color_theme = color_themes[0]
    
    def set_theme(self, theme_choice):
        if theme_choice == "Classic":
            self._instance.color_theme = color_themes[0]
        elif theme_choice == "Forest":
            self._instance.color_theme = color_themes[1]
        elif theme_choice == "Pastel":
            self._instance.color_theme = color_themes[2]
        elif theme_choice == "Vibrant":
            self._instance.color_theme = color_themes[3]
