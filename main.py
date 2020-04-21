from sectional.models import CategorySectional, Configuration
from sectional.common import logging_helper
import logging
from sectional.webapp import webapp

LOGGER = logging.getLogger(__name__)

if (__name__ == "__main__"):
    logging_helper.initialize_logging()
    configuration = Configuration()
    configuration.load_config()
    sectional = CategorySectional(configuration=configuration)
    sectional.initialize()
    sectional.start()
    webapp.sectional = sectional
    webapp.app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False)