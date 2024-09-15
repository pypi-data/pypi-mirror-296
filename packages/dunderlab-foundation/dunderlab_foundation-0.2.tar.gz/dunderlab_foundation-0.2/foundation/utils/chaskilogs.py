from foundation.radiant.utils import environ
import logging
import requests


########################################################################
class ChaskiLogging(logging.Handler):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """"""
        super().__init__()

        self.topic = environ('WORKER_NAME', 'logs')
        formatter = logging.Formatter(f'%(levelname)s: {self.topic} [%(asctime)s]: %(message)s')
        self.setFormatter(formatter)

    # ----------------------------------------------------------------------
    def emit(self, record):
        """"""
        try:
            log_message = self.format(record)
            params = {
                "topic": self.topic,
                "message": log_message,
            }
            requests.get("http://chaski-api-logger-worker:51115/", params=params)

        except Exception as e:
            logging.error(f"Error enviando el log a Chaski: {e}")


try:
    custom_handler = ChaskiLogging()
    custom_handler.setLevel(logging.INFO)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(custom_handler)
except Exception as e:
    logging.warning('Impossible to connect logging with Chaski')
    logging.warning(str(e))
