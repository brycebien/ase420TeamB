from themes import color_themes

class ThemeSelector:
    _instance = None

    @staticmethod
    def getInstance():
        if ThemeSelector._instance is None:
            ThemeSelector._instance = ThemeSelector()
        return ThemeSelector._instance
    
    def __init__(self):
        self.color_theme = color_themes[0]
    
    def set_theme(self, theme_choice):
        if theme_choice == "Classic":
            self.color_theme = color_themes[0]
        elif theme_choice == "Forest":
            self.color_theme = color_themes[1]
        elif theme_choice == "Pastel":
            self.color_theme = color_themes[2]
        elif theme_choice == "Vibrant":
            self.color_theme = color_themes[3]

'''class ThemeSelector:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ThemeSelector, cls).__new__(cls)
            cls._instance.color_theme = cls._instance.color_themes[0]
        return cls._instance

    def set_theme(self, theme_choice):
        # Your existing set_theme method goes here
        if theme_choice == "Classic":
            self.color_theme = self.color_themes[0]
        elif theme_choice == "Forest":
            self.color_theme = self.color_themes[1]
        elif theme_choice == "Pastel":
            self.color_theme = self.color_themes[2]
        elif theme_choice == "Vibrant":
            self.color_theme = self.color_themes[3]'''