from sectional.models import CategorySectional
from sectional.common import logging_helper
import logging
from sectional.webapp import webapp

LOGGER = logging.getLogger(__name__)

if (__name__ == "__main__"):
    logging_helper.initialize_logging()
    sectional = CategorySectional()
    sectional.initialize()
    sectional.start()
    webapp.app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False)