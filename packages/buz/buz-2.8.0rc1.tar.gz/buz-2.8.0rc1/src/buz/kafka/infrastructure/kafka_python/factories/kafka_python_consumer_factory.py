from __future__ import annotations

from logging import Logger
from typing import Type, Tuple

from kafka.coordinator.assignors.abstract import AbstractPartitionAssignor
from kafka.coordinator.assignors.roundrobin import RoundRobinPartitionAssignor

from buz.kafka.domain.models.kafka_connection_config import KafkaConnectionConfig
from buz.kafka.domain.services.kafka_consumer import KafkaConsumer
from buz.kafka.infrastructure.kafka_python.factories.kafka_python_client_factory import KafkaPythonClientFactory
from buz.kafka.infrastructure.kafka_python.kafka_python_consumer import KafkaPythonConsumer
from buz.kafka.infrastructure.serializers.byte_serializer import ByteSerializer
from buz.kafka.infrastructure.serializers.implementations.json_byte_serializer import JSONByteSerializer
from buz.kafka.infrastructure.serializers.kafka_header_serializer import KafkaHeaderSerializer


class KafkaPythonConsumerFactory(KafkaPythonClientFactory):
    def __init__(
        self,
        logger: Logger,
        kafka_connection_config: KafkaConnectionConfig,
        kafka_partition_assignors: Tuple[Type[AbstractPartitionAssignor], ...] = (),
        byte_serializer: ByteSerializer = JSONByteSerializer(),
        header_serializer: KafkaHeaderSerializer = KafkaHeaderSerializer(),
    ):
        super().__init__(logger=logger, kafka_connection_config=kafka_connection_config)
        self._kafka_partition_assignors = self.__select_partition_assignors(kafka_partition_assignors)
        self._kafka_connection_config = kafka_connection_config
        self._byte_serializer = byte_serializer
        self._header_serializer = header_serializer

    def __select_partition_assignors(
        self, kafka_partition_assignors: Tuple[Type[AbstractPartitionAssignor], ...]
    ) -> Tuple[Type[AbstractPartitionAssignor], ...]:
        # Order matters. The Consumer will try to use the left-most assignor.
        # The assignor used by the GroupCoordinator is agreed between all consumers in group.
        # The list is used to support rolling-updates.

        default_assignors = [RoundRobinPartitionAssignor]

        partition_assignors: list[Type[AbstractPartitionAssignor]] = list(kafka_partition_assignors)
        partition_assignors.extend(default_assignors)

        return tuple(partition_assignors)

    def build(self) -> KafkaConsumer:
        return KafkaPythonConsumer(
            bootstrap_servers=self._kafka_connection_config.bootstrap_servers,
            client_id=self._kafka_connection_config.client_id,
            partition_assignors=self._kafka_partition_assignors,
            logger=self._logger,
            byte_serializer=self._byte_serializer,
            **self._get_autentication_configuration_by_security_protocol(),  # type: ignore
        )
