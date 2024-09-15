from foundation.radiant.utils import environ
from confluent_kafka import Producer
import logging

level = logging.WARNING


########################################################################
class KafkaLogging(logging.Handler):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """"""
        super().__init__()

        self.topic = environ('WORKER_NAME', 'logs')
        formatter = logging.Formatter(f'%(levelname)s: {self.topic} [%(asctime)s]: %(message)s')
        self.setFormatter(formatter)
        self.producer = Producer({'bootstrap.servers': 'kafka-logs-service:9093'})

    # ----------------------------------------------------------------------
    def emit(self, record):
        """"""
        log_message = self.format(record)
        self.producer.produce(self.topic, value=log_message)
        self.producer.flush()

    # ----------------------------------------------------------------------
    @property
    def kafka_available(self):
        """"""
        try:
            self.producer.list_topics(timeout=0.5)
            return True
        except:
            return False


try:
    custom_handler = KafkaLogging()
    if custom_handler.kafka_available:
        custom_handler.setLevel(level)
        root_logger = logging.getLogger()
        root_logger.setLevel(level)
        root_logger.addHandler(custom_handler)
except Exception as e:
    logging.warning('Impossible to connect logging with Kafka')
    logging.warning(str(e))
