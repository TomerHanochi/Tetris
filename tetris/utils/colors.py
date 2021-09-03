class ColorsType(type):
    def __getattr__(cls, item) -> tuple[int, int, int]:
        try:
            return cls.palette[item]
        except KeyError:
            raise KeyError(f'{item} doesn\'t exist in the color palette')


class Colors(metaclass=ColorsType):
    palette = {
        'black': (0, 0, 0),
        'white': (255, 255, 255),
    }


if __name__ == '__main__':
    for color_name in Colors.palette:
        print(f'{color_name}: {getattr(Colors, color_name)}')
