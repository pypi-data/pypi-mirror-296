from logging import Logger

from buz.kafka.domain.models.kafka_connection_config import KafkaConnectionConfig
from buz.kafka.domain.services.kafka_admin_test_client import KafkaAdminTestClient
from buz.kafka.infrastructure.kafka_python.factories.kafka_python_admin_client_factory import (
    KafkaPythonAdminClientFactory,
)
from buz.kafka.infrastructure.kafka_python.kafka_python_admin_test_client import KafkaPythonAdminTestClient


class KafkaPythonAdminClientTestFactory(KafkaPythonAdminClientFactory):
    def __init__(
        self,
        logger: Logger,
        kafka_connection_config: KafkaConnectionConfig,
    ):
        super().__init__(logger=logger, kafka_connection_config=kafka_connection_config)

    def build(self) -> KafkaAdminTestClient:
        return KafkaPythonAdminTestClient(
            bootstrap_servers=self._kafka_connection_config.bootstrap_servers,
            client_id=self._kafka_connection_config.client_id,
            logger=self._logger,
            **self._get_autentication_configuration_by_security_protocol(),  # type: ignore
        )
