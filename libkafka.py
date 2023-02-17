from kafka import KafkaConsumer, KafkaProducer

class Kafka(object):
    _producer = None
    _consumer = None
    _DEFAULT_DELIMITER = None

    def __init__(self):
        super(Kafka, self).__init__()
        self._DEFAULT_DELIMITER = b'\x1f'.decode('ascii')

    def init_producer(self, **configs):
        self._producer = KafkaProducer(**configs)
        return self._producer

    def init_consumer(self, *topics, **configs):
        self._consumer = KafkaConsumer(*topics, **configs)
        return self._consumer

    def deinit_producer(self):
        self._producer = None

    def deinit_consumer(self):
        self._consumer = None

    def has_producer(self):
        return self._producer != None

    def has_consumer(self):
        return self._consumer != None

    def producer(self):
        if not self.has_producer():
            raise Exception("The producer hasn't been initialized!")
        return self._producer

    def consumer(self):
        if not self.has_consumer():
            raise Exception("The consumer hasn't been initialized!")
        return self._consumer

    def log(self, topic : str, version : int, logs : list, delimiter = None):
        if delimiter is None:
            delimiter = self._DEFAULT_DELIMITER
        message = self._build_log(version, logs, delimiter).encode('ascii')
        self.producer().send(topic, message)

    def get_log(self, blocking_mode = True, delimiter = None):
        if delimiter is None:
            delimiter = self._DEFAULT_DELIMITER
        message = self._get_message(blocking_mode)
        if message is None:
            return message
        return message.split(delimiter)

    def _get_message(self, blocking_mode = True):
        while(True):
            msg_pack = self.consumer().poll(timeout_ms=1000, max_records=1)
            for tp, messages in msg_pack.items():
                message = messages[0]
                try:
                    return message.value.decode('ascii')
                except Exception as e:
                    print(e)
                    return message.value
            if not blocking_mode:
                return None

    def _build_log(self, version : int, logs : list, delimiter : str):
        message = [str(version)]
        for log in logs:
            message.append(self._escape_delimiter(str(log), delimiter))
        return delimiter.join(message)

    def _escape_delimiter(self, string : str, delimiter : str):
        return string.replace(delimiter, " ")
