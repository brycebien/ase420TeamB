color_themes = [
        [
            (0, 0, 0),
            (120, 37, 179),
            (100, 179, 179),
            (80, 34, 22),
            (80, 134, 22),
            (180, 34, 22),
            (180, 34, 122),
            (128, 128, 128)
        ],
        [
            (0, 0, 0), 
            (25,39,13),
            (37,89,31),
            (129,140,60),
            (114,96,27),
            (89,58,14),
            (95,114,93),
            (128, 128, 128)
        ],
        [
            (0, 0, 0),
            (255,179,186),
            (255,223,186),
            (255,255,186),
            (186,255,201),
            (186,225,255),
            (236,96,100),
            (128, 128, 128)
        ],
        [
            (0, 0, 0),
            (0,120,255),
            (189,0,255),
            (255,154,0),
            (1,255,31),
            (227,255,0),
            (255,0,0),
            (128, 128, 128)
        ],
    ]

color_theme = color_themes[0]

def setTheme(themeChoice):
    if themeChoice == "Classic":
        color_theme = color_themes[0]
    elif themeChoice == "Forest":
        color_theme = color_themes[1]
    elif themeChoice == "Pastel":
        color_theme = color_themes[2]
    elif themeChoice == "Vibrant":
        color_theme = color_themes[3]

def getTheme()