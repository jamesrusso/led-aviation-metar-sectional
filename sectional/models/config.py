import yaml
from sectional.models import AirportCondition
from sectional.models import Color
from sectional.renderers import RendererFactory
from threading import Lock

class Configuration(object):
    instance = None

    def __new__(cls):
        if not Configuration.instance:
            Configuration.instance = Configuration.__Configuration()
        return Configuration.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, val):
        return setattr(self.instance, name, val)

    class __Configuration:
        def __init__(self):
            self.lock = Lock()
            self._config = {}
            self._condition_map = {}
            self._config['pixel_map'] = {}
            self.load_config()

        def load_config(self, path="./config/config.yaml"):
            self.lock.acquire()
            with open(path) as s:
                self._config = yaml.safe_load(s)

            if ('pixel_map' not in self._config):
                self._config['pixel_map'] = {}

            for condition in AirportCondition:
                self._condition_map[condition] = Color(self._config['conditions'][condition.value])
            self.lock.release()


        def save_config(self, path='./config/config.yaml'):
            self.lock.acquire()
            with open(path, 'w+') as s:
                yaml.dump(self._config, s)
            self.lock.release()

        def color_for_condition(self, condition):
            return self._condition_map[condition]

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
            return RendererFactory.create(self.pixelcount, self.renderer_config)

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
