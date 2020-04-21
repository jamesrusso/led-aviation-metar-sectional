import yaml
from sectional.models import AirportCondition
from sectional.models import Color
from sectional.renderers import RendererFactory

from threading import Lock

DEFAULT_COLOR_FOR_CONDITION = { 
    AirportCondition.IFR: Color('#ff0000', blink=False),
    AirportCondition.INOP: Color('#000000', blink=False),
    AirportCondition.INVALID: Color('#ffc0cb', blink=True),
    AirportCondition.LIFR: Color('#ff00ff', blink=False),
    AirportCondition.MVFR: Color('#0000ff', blink=False),
    AirportCondition.NIGHT: Color('#ffff00', blink=False),
    AirportCondition.NIGHT_DARK: Color('#141400', blink=False),
    AirportCondition.SMOKE: Color('#323232', blink=False),
    AirportCondition.VFR: Color('#00ff00', blink=False)
}
DEFAULT_METAR_INOP_AGE = 180
DEFAULT_METAR_INVALID_AGE = 90
DEFAULT_METAR_REFRESH_INTERVAL =15
DEFAULT_NIGHT_LIGHTS = True
DEFAULT_PIXEL_COUNT = 50
DEFAULT_SUNRISE_REFRESH_INTERVAL = 1080

class Configuration(object):
    def __init__(self, config_path='./config/config.yaml'):
        self.lock = Lock()
        self._config = {}
        self._renderer = None
        self._config['pixel_map'] = {}
        self._config['conditions'] = {}
        self._conditions = {}
        self.__setup_defaults()
        self.path = config_path

    def __set_default(self, name, value): 
        if (name not in self._config):
            self._config[name] = value

    def __setup_defaults(self):
        self.__set_default('conditions', {})
        self.__set_default('pixel_map', {})
        self.__set_default('pixel_count', DEFAULT_PIXEL_COUNT)
        self.__set_default('renderer_config', {'hostname': '127.0.0.1', 'name': 'remote', 'port': 5006})
        self.__set_default('sunrise_refresh_interval', DEFAULT_SUNRISE_REFRESH_INTERVAL)
        self.__set_default('metar_inop_age', DEFAULT_METAR_INOP_AGE)
        self.__set_default('metar_invalid_age', DEFAULT_METAR_INVALID_AGE)
        self.__set_default('metar_refresh_interval', DEFAULT_METAR_REFRESH_INTERVAL)
        self.__set_default('night_lights', DEFAULT_NIGHT_LIGHTS)

        for condition in AirportCondition:
            color = DEFAULT_COLOR_FOR_CONDITION[condition]
            if (condition.value not in self._config['conditions']):
                self._config['conditions'][condition.value] = { 'color': color.html_color, 'blink': color.blink }

    def __generate_colors_for_conditions(self):
        self._conditions = {}
        for (key, value) in self._config['conditions'].items():
                self._conditions[key] = Color(value['color'], value['blink'])

    def load_config(self):
        self.lock.acquire()
        with open(self.path) as s:
            self._config = yaml.safe_load(s)
        self.__setup_defaults()
        self.__generate_colors_for_conditions()
        self.lock.release()

    def save_config(self, path='./config/config.yaml'):
        self.lock.acquire()
        with open(path, 'w+') as s:
            yaml.dump(self._config, s)
        self.lock.release()

    def get_color_for_condition(self, condition):
        return self.conditions[condition.value]

    def set_color_for_condition(self, condition, color):
        if (type(color) is not Color):
            ValueError('color must be of type Color')
        
        if (type(condition) is str):
            condition = AirportCondition(condition)

        self._config['conditions'][condition.name] = { 'color': color.html_color, 'blink': color.blink }
        self._conditions[condition.name] = color

    @property
    def conditions(self):
        return self._conditions

    @property
    def metar_refresh_interval(self):
        return self._config['metar_refresh_interval']

    @metar_refresh_interval.setter
    def metar_refresh_interval(self, val):
        self._config['metar_refresh_interval'] = int(val)

    @property
    def sunrise_refresh_interval(self):
        return self._config['sunrise_refresh_interval']

    @sunrise_refresh_interval.setter
    def sunrise_refresh_interval(self, val):
        self._config['sunrise_refresh_interval'] = int(val)

    @property
    def metar_invalid_age(self):
        return self._config['metar_invalid_age']

    @metar_invalid_age.setter
    def metar_invalid_age(self, val):
        self._config['metar_invalid_age'] = int(val)

    @property
    def metar_inop_age(self):
        return self._config['metar_inop_age']

    @metar_inop_age.setter
    def metar_inop_age(self, val):
        self._config['metar_inop_age'] = int(val)

    @property
    def night_lights(self):
        return self._config['night_lights']

    @property
    def setup_complete(self):
        return self._config['setup_complete']
    
    @setup_complete.setter
    def setup_complete(self, val):
        self._config['setup_complete'] = val

    @property
    def renderer(self):
        if (not self._renderer):
            self._renderer = RendererFactory.create(self.pixelcount, self.renderer_config)

        return self._renderer

    def set_airport_for_pixel(self, idx, icao_airport_code): 
        self._config['pixel_map'][idx] = icao_airport_code

    def get_airport_for_pixel(self, idx): 
        if (idx in self._config['pixel_map']):
            return self._config['pixel_map'][idx]
        else:
            return None
    
    def get_pixels_for_airport(self, icao_airport_code): 
            return [int(x[0]) for x in filter(lambda item: item[1] == icao_airport_code, self._config['pixel_map'].items())]

    @property
    def pixelcount(self):
        return int(self._config['pixelcount'])

    @pixelcount.setter
    def pixelcount(self, val):
        self._config['pixelcount'] = int(val)

    @property
    def renderer_config(self):
        return self._config['renderer_config']

    @property
    def airports(self):
        airports = {}
        for (pixel, icao_airport_code) in self._config['pixel_map'].items():
            if (icao_airport_code not in airports):
                airports[icao_airport_code] = [int(pixel)]
            else:
                airports[icao_airport_code].append(int(pixel))

        return airports
