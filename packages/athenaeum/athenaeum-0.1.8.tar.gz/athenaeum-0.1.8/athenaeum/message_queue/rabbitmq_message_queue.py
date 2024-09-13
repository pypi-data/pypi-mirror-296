import pika
import atexit
from abc import ABC, abstractmethod
from dynaconf.base import LazySettings
from typing import Optional, Dict, Any
from athenaeum.project import get_settings
from athenaeum.logger import logger


class RabbitmqMessageQueue(ABC):
    logger = logger

    queue_name: Optional[str] = None

    def __init__(self):
        self.connection: Optional[pika.adapters.blocking_connection.BlockingConnection] = None
        self.channel: Optional[pika.adapters.blocking_connection.BlockingChannel] = None

        self.connect()
        atexit.register(self.disconnect)

    @staticmethod
    def get_connection(settings_object: Optional[LazySettings] = None, settings_dict: Dict[str, Any] = None) -> \
            Optional[pika.adapters.blocking_connection.BlockingConnection]:
        settings_keys = ['RABBITMQ_USERNAME', 'RABBITMQ_PASSWORD', 'RABBITMQ_HOST', 'RABBITMQ_PORT', 'RABBITMQ_VHOST']
        if (settings := get_settings(settings_keys, settings_object, settings_dict)) is None:
            return

        func_config = {
            'username': settings['RABBITMQ_USERNAME'],
            'password': settings['RABBITMQ_PASSWORD'],
            'host': settings['RABBITMQ_HOST'],
            'port': settings['RABBITMQ_PORT'],
            'virtual_host': settings['RABBITMQ_VHOST'],
        }

        credentials = pika.PlainCredentials(func_config['username'], func_config['password'])
        parameters = pika.ConnectionParameters(func_config['host'], func_config['port'], func_config['virtual_host'],
                                               credentials=credentials, heartbeat=0)
        connection = pika.BlockingConnection(parameters)
        return connection

    def get_channel(self) -> Optional[pika.adapters.blocking_connection.BlockingChannel]:
        if self.connection is None:
            return
        channel = self.connection.channel()
        channel.basic_qos(prefetch_count=100)  # Unacked 100 messages
        channel.queue_declare(queue=self.queue_name, durable=True)
        return channel

    def connect(self):
        self.connection = self.get_connection()
        self.channel = self.get_channel()

    def disconnect(self):
        if self.channel:
            self.channel.close()
        if self.connection:
            self.connection.close()

    def send_message(self, message):
        self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=message)
        self.logger.debug(f'send_message message：`{message}`')

    def receive_message(self):
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.receive_message_callback)
        self.channel.start_consuming()

    @abstractmethod
    def receive_message_callback(self, ch, method, properties, body):
        self.logger.debug(f'receive_message_callback body：`{body}`')
        ch.basic_ack(delivery_tag=method.delivery_tag)
        # ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
        # ch.basic_reject(delivery_tag=method.delivery_tag, requeue=True)

    def delete_queue(self):
        self.channel.queue_delete(queue=self.queue_name)

    def purge_queue(self):
        self.channel.queue_purge(queue=self.queue_name)
