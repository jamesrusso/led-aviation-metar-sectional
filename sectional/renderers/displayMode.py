
class DisplayFactory:
    @classmethod
    def create(cls, configuration, pixel_count, display, airports):
        self.configuration = configuration
        self.display = display
        self.pixel_count = pixel_count
        self.airports = airports

        if (display == 'metar' or display == 1):
            from sectional.renderers.metar import displayMetar
            return displayMetar(pixel_count, airports, configuration)
        elif (display == 'visited') or display == 2):
            from sectional.renderers.visited import displayVisited
            return displayVisited(pixel_count, airports, configuration)
        else:
            raise ValueError("Unknown display mode: {}".format(display))




