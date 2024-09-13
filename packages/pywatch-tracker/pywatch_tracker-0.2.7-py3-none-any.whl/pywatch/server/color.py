import itertools
import typing
from dataclasses import dataclass
from colour import color_scale
import colour

import numpy as np
from numpy import uint8


__all__ = ["Color", "ColorRange"]


class Color:
    red: uint8
    green: uint8
    blue: uint8

    def __init__(self, red: int, green: int, blue: int):
        self.red = uint8(red)
        self.green = uint8(green)
        self.blue = uint8(blue)

    @property
    def hex(self):
        res = "0x"
        for x in [self.red, self.green, self.blue]:
            res += '{:02X}'.format(x)

        return res

    @property
    def tuple(self):
        return int(self.red), int(self.green), int(self.blue)

    def __str__(self):
        res = "#"
        for x in [self.red, self.green, self.blue]:
            res += '{:02X}'.format(x)

        return res

    def __add__(self, other):
        return Color(self.red + other.red, self.green + other.green, self.blue + other.blue)

    def __mul__(self, other):
        return Color(self.red * other, self.green * other, self.blue * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def scale(self, other, alpha):
        return (1 - alpha) * self + alpha * other

    def range_to(self, other, size, func=lambda n: n):
        x = np.linspace(0, 1, size)
        alpha = func(x)
        alpha -= alpha.min()
        alpha /= alpha.max()

        return (self.scale(other, alpha) for alpha in alpha)

    def ranges_to(self, *other, size):
        size = int(size / len(other))

        colors = [self, *other]

        generators = []
        for i in range(len(colors) - 1):
            generators.append(colors[i].range_to(colors[i + 1], size))

        return itertools.chain(*generators)


@dataclass
class ColorRange:
    min: float
    max: float
    color1: Color
    color2: Color
    func: typing.Callable[[float], float] = lambda x: x

    def __post_init__(self):
        c1 = colour.Color(str(self.color1))
        c2 = colour.Color(str(self.color2))
        self.range = list(c1.range_to(c2, 1000))
        # self.range = color_scale(self.color1.tuple, self.color2.tuple, 1000)

    def __call__(self, value: float) -> str:
        if value < self.min:
            return self.color1.hex
        if value > self.max:
            return self.color2.hex

        value -= self.min
        value /= (self.max - self.min)
        return "0x" + self.range[int(value * 999)].hex.upper()[1:]

        # return self.color1.scale(self.color2, self.func(value))
