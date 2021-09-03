class ColorPaletteType(type):
    def __getattr__(cls, item) -> tuple[int, int, int]:
        try:
            return cls.palette[item]
        except KeyError:
            raise KeyError(f'{item} doesn\'t exist in the color palette')


class ColorPalette(metaclass=ColorPaletteType):
    palette = {
        'black': (0, 0, 0),
        'white': (255, 255, 255),
    }


if __name__ == '__main__':
    for color_name in ColorPalette.palette:
        print(f'{color_name}: {getattr(ColorPalette, color_name)}')
