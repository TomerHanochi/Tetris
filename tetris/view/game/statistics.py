from tetris.assets.assets import Fonts, Colors
from tetris.view.utils.view_object import ViewObject
from tetris.view.utils.context import Context
from tetris.model.model import Model
from tetris.consts import Consts


class Stats(ViewObject):
    def __init__(self, x: float, y: float, model: Model) -> None:
        # the stat name has to match the name of the attribute in the model
        self.stats = {
            stat: Fonts.statistic.render(stat.upper().replace('_', ' '), True, Colors.statistic)
            for stat in ('high_score', 'score', 'level', 'cleared')
        }
        # sets the widest rendered stat as the width of the stats object
        self.__w = max(self.stats.values(), key=lambda stat: stat.get_width()).get_width()
        # each stat value pair is the size of 4.5 times the font height
        self.__h = Fonts.statistic.get_height() * 4.5 * len(self.stats)
        self.__x = (Consts.SCREEN_WIDTH + x - self.w) * .5
        self.__y = (Consts.SCREEN_HEIGHT + y - self.h) * .5
        self.__model = model

    def draw(self) -> None:
        statistic_y = self.y
        for stat_name, rendered_stat in self.stats.items():
            # offset each stat so that it is easier to read
            statistic_y += rendered_stat.get_height() * 2.25
            Context.image(x=self.x + (self.w - rendered_stat.get_width()) * .5,
                       y=statistic_y, image=rendered_stat)

            stat_value = Fonts.statistic.render(str(getattr(self.model, stat_name)), True,
                                                Colors.statistic)
            # offset each stat value so that it is easier to read
            statistic_y += stat_value.get_height() * 1.25
            Context.image(self.x + (self.w - stat_value.get_width()) * .5, statistic_y, stat_value)

    @property
    def x(self) -> float:
        return self.__x

    @property
    def y(self) -> float:
        return self.__y

    @property
    def w(self) -> int:
        return self.__w

    @property
    def h(self) -> int:
        return self.__h

    @property
    def model(self) -> Model:
        return self.__model
