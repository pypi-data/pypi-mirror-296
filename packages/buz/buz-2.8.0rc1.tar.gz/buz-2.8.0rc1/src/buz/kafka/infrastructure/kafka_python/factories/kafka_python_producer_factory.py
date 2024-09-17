from logging import Logger

from buz.kafka.domain.models.kafka_connection_config import KafkaConnectionConfig
from buz.kafka.infrastructure.kafka_python.factories.kafka_python_client_factory import KafkaPythonClientFactory
from buz.kafka.infrastructure.kafka_python.kafka_python_producer import KafkaPythonProducer
from buz.kafka.infrastructure.serializers.byte_serializer import ByteSerializer
from buz.kafka.infrastructure.serializers.implementations.json_byte_serializer import JSONByteSerializer


class KafkaPythonProducerFactory(KafkaPythonClientFactory):
    def __init__(
        self,
        logger: Logger,
        kafka_connection_config: KafkaConnectionConfig,
        byte_serializer: ByteSerializer = JSONByteSerializer(),
    ):
        super().__init__(logger=logger, kafka_connection_config=kafka_connection_config)
        self._kafka_connection_config = kafka_connection_config
        self._byte_serializer = byte_serializer

    def build(self) -> KafkaPythonProducer:
        return KafkaPythonProducer(
            bootstrap_servers=self._kafka_connection_config.bootstrap_servers,
            client_id=self._kafka_connection_config.client_id,
            logger=self._logger,
            byte_serializer=self._byte_serializer,
            **self._get_autentication_configuration_by_security_protocol(),  # type: ignore
        )
