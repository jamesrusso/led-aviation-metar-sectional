import colour


class Color(object):

    def __init__(self, val, blink=False):
        if (type(val) is tuple):
            self.rgb = (val[0], val[1], val[2])
        else:
            self.rgb = tuple([round(i * 255) for i in colour.Color(val).rgb])

        self._blink = blink

    @property
    def blink(self):
        return self._blink
        
    @property
    def html_color(self):
        return "#{:02x}{:02x}{:02x}".format(*self.rgb)

    @staticmethod
    def ALL_COLORS():
        return [Color.RED(), Color.GREEN(), Color.BLUE(), Color.MAGENTA(), Color.GRAY(), Color.YELLOW(), Color.DARK_YELLOW(), Color.WHITE(), Color.BLACK()]

    @staticmethod
    def RED():
        return Color((255, 0, 0))

    @staticmethod
    def GREEN():
        return Color((0, 255, 0))

    @staticmethod
    def BLUE():
        return Color((0, 0, 255))

    @staticmethod
    def MAGENTA():
        return Color((255, 0, 255))

    @staticmethod
    def OFF():
        return Color((0, 0, 0))

    @staticmethod
    def GRAY():
        return Color((50, 50, 50))

    @staticmethod
    def YELLOW():
        return Color((255, 255, 0))

    @staticmethod
    def DARK_YELLOW():
        return Color((20, 20, 0))

    @staticmethod
    def WHITE():
        return Color((255, 255, 255))

    @staticmethod
    def BLACK():
        return Color((0, 0, 0))

    def __clamp(self, minimum, value, maximum):
        """
        Makes sure the given value (middle param) is always between the maximum and minimum.

        Arguments:
            minimum {number} -- The smallest the value can be (inclusive).
            value {number} -- The value to clamp.
            maximum {number} -- The largest the value can be (inclusive).

        Returns:
            number -- The value within the allowable range.
        """

        if value < minimum:
            return minimum

        if value > maximum:
            return maximum

        return value

    def __interpolate(self, left_value, right_value, proportion):
        """
        Finds the spot between the two values.

        Arguments:
            left_value {number} -- The value on the "left" that 0.0 would return.
            right_value {number} -- The value on the "right" that 1.0 would return.
            proportion {float} -- The proportion from the left to the right hand side.

        >>> interpolate(0, 255, 0.5)
        127
        >>> interpolate(10, 20, 0.5)
        15
        >>> interpolate(0, 255, 0.0)
        0
        >>> interpolate(0, 255, 0)
        0
        >>> interpolate(0, 255, 1)
        255
        >>> interpolate(0, 255, 1.5)
        255
        >>> interpolate(0, 255, -0.5)
        0
        >>> interpolate(0, 255, 0.1)
        25
        >>> interpolate(0, 255, 0.9)
        229
        >>> interpolate(255, 0, 0.5)
        127
        >>> interpolate(20, 10, 0.5)
        15
        >>> interpolate(255, 0, 0.0)
        255
        >>> interpolate(255, 0, 0)
        255
        >>> interpolate(255, 0, 1)
        0
        >>> interpolate(255, 0, 1.5)
        0
        >>> interpolate(255, 0, -0.5)
        255
        >>> interpolate(255, 0, 0.1)
        229
        >>> interpolate(255, 0, 0.9)
        25

        Returns:
            float -- The number that is the given amount between the left and right.
        """

        left_value = self.__clamp(0.0, left_value, 255.0)
        right_value = self.__clamp(0.0, right_value, 255.0)
        proportion = self.__clamp(0.0, proportion, 1.0)

        if (left_value is None):
            raise ValueError("left value cannot be None")

        if (right_value is None):
            raise ValueError("right value cannot be None")

        if (proportion is None):
            raise ValueError("proportion cannot be None")

        return int(float(left_value) * (1 - float(proportion)) + (float(right_value) * float(proportion)))

    def fade_to(self, other_color, proportion):
        """
        Returns a color that is a mix between the this color and another color
        A given proportion of 0 would return the this color.
        A given proportion of 1 would return the other color.
        A given proportion of 0.5 would return a 50/50 mix.

        Works for RGB or ARGB, but both sides MUST have matching number of components.

        Arguments:
            other_color {float[]} -- The ending color.
            proportion {float} -- The mix between the two colors.

        Returns:
            Color -- The new color.
        """

        if (other_color is None):
            raise ValueError("other_color cannot be None")

        return Color(tuple([int(self.__interpolate(self.rgb[index], other_color.rgb[index], proportion)) for index in range(3)]))

    def __str__(self):
        return "({},{},{})".format(self.rgb[0], self.rgb[1], self.rgb[2])

    def __eq__(self, other):
        print("__eq__")
        if (type(other) is Color):
            return self.rgb[0] == other.rgb[0] and self.rgb[1] == other.rgb[1] and self.rgb[2] == other.rgb[2]

        return False

