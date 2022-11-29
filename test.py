from colorthief import ColorThief

color_thief = ColorThief('pictures/TeStProfilePicture.png')

dominant_color = color_thief.get_color(quality=1)

print(dominant_color)