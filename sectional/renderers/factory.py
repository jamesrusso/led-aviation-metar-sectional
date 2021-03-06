
class RendererFactory:
    @classmethod
    def create(cls, pixel_count, renderer_config):
        if (renderer_config['name'] == 'dummy'):
            from sectional.renderers.dummy import DummyRenderer
            return DummyRenderer(pixel_count)
        elif (renderer_config['name'] == 'ws2811'):
            from sectional.renderers.ws2811 import Ws2811Renderer
            return Ws2811Renderer(pixel_count, renderer_config['gpio_port'], renderer_config.get('pixel_order','GRB'))
        elif (renderer_config['name'] == 'ws2801'):
            from sectional.renderers.ws2801 import Ws2801Renderer
            return Ws2801Renderer(pixel_count, renderer_config('spi_port'), renderer_config('spi_device'))
        elif (renderer_config['name'] == 'remote'):
            from sectional.renderers.remote import RemoteRenderer
            return RemoteRenderer(renderer_config['hostname'], renderer_config['port'])
        else:
            raise ValueError("Unknown renderer {}".format(renderer_config['name']))
