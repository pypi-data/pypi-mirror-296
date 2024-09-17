from __future__ import annotations

from logging import Logger
from typing import Callable, List, Type, Tuple, Union, cast

from kafka import KafkaConsumer, TopicPartition, OffsetAndMetadata
from kafka.coordinator.assignors.abstract import AbstractPartitionAssignor
from kafka.coordinator.assignors.range import RangePartitionAssignor

from buz.kafka.domain.models.kafka_supported_security_protocols import KafkaSupportedSecurityProtocols
from buz.kafka.infrastructure.kafka_python.exception.consumer_interrupted_exception import (
    ConsumerInterruptedException,
)
from buz.kafka.infrastructure.serializers.byte_serializer import ByteSerializer
from buz.kafka.infrastructure.serializers.implementations.json_byte_serializer import JSONByteSerializer
from buz.kafka.infrastructure.serializers.kafka_header_serializer import KafkaHeaderSerializer
from buz.kafka.domain.models.kafka_consumer_record import KafkaConsumerRecord
from buz.kafka.infrastructure.kafka_python.kafka_poll_record import KafkaPollRecord
from buz.kafka.domain.models.consumer_initial_offset_position import ConsumerInitialOffsetPosition
from buz.kafka.domain.services.kafka_consumer import (
    DEFAULT_NUMBER_OF_MESSAGES_TO_POLLING,
)


CONSUMER_POLL_TIMEOUT_MS = 1000
# https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html#kafka.KafkaConsumer.poll
SESSION_TIMEOUT_MS = 10000
# https://docs.confluent.io/platform/current/installation/configuration/consumer-configs.html#session-timeout-ms


class KafkaPythonConsumer(KafkaConsumer):
    def __init__(
        self,
        *,
        client_id: str,
        bootstrap_servers: List[str],
        logger: Logger,
        security_protocol: KafkaSupportedSecurityProtocols,
        sasl_mechanism: Union[str, None] = None,
        sasl_plain_username: Union[str, None] = None,
        sasl_plain_password: Union[str, None] = None,
        partition_assignors: Tuple[Type[AbstractPartitionAssignor], ...] = (RangePartitionAssignor,),
        byte_serializer: ByteSerializer = JSONByteSerializer(),
    ):
        self._client_id = client_id
        self._bootstrap_servers = bootstrap_servers
        self._logger = logger
        self._sasl_mechanism = sasl_mechanism
        self._security_protocol = security_protocol
        self._sasl_plain_username = sasl_plain_username
        self._sasl_plain_password = sasl_plain_password
        self._partition_assignors = partition_assignors
        self.__byte_serializer = byte_serializer
        self.__header_serializer = KafkaHeaderSerializer()

        self._gracefully_stop = False

    def consume(
        self,
        *,
        topics: List[str],
        consumer_group: str,
        consumption_callback: Callable[[KafkaConsumerRecord], None],
        initial_offset_position: ConsumerInitialOffsetPosition = ConsumerInitialOffsetPosition.BEGINNING,
        number_of_messages_to_polling: int = DEFAULT_NUMBER_OF_MESSAGES_TO_POLLING,
    ) -> None:
        self._gracefully_stop = False

        consumer = self.__generate_consumer(
            consumer_group=consumer_group,
            initial_offset_position=initial_offset_position,
        )

        topics_pattern = "|".join(topics)

        consumer.subscribe(topics=topics_pattern)

        while True:
            try:
                if self._gracefully_stop is True:
                    raise ConsumerInterruptedException("The consumer execution was interrupted")

                consumer_metadata: dict[str, str] = {}
                poll_results = consumer.poll(
                    timeout_ms=CONSUMER_POLL_TIMEOUT_MS,
                    max_records=number_of_messages_to_polling,
                )

                for topic_partition, consumer_records in poll_results.items():
                    for consumer_record in consumer_records:
                        kafka_poll_record = cast(KafkaPollRecord, consumer_record)
                        if kafka_poll_record.value is not None:
                            consumption_callback(
                                KafkaConsumerRecord(
                                    value=self.__byte_serializer.unserialize(kafka_poll_record.value),
                                    headers=self.__header_serializer.unserialize(kafka_poll_record.headers),
                                )
                            )

                        self.__mark_record_as_consumed(consumer_metadata, kafka_poll_record)

                        if self._gracefully_stop is True:
                            raise ConsumerInterruptedException("The consumer execution was interrupted")

                consumer.commit()

            except ConsumerInterruptedException:
                self.__close_consumer(consumer, consumer_metadata)
                return
            except Exception:
                self.__close_consumer(consumer, consumer_metadata)
                raise

    def __generate_consumer(
        self,
        *,
        consumer_group: str,
        initial_offset_position: ConsumerInitialOffsetPosition,
    ) -> KafkaConsumer:
        auto_offset_rest = (
            "earliest" if initial_offset_position == ConsumerInitialOffsetPosition.BEGINNING else "latest"
        )

        return KafkaConsumer(
            bootstrap_servers=self._bootstrap_servers,
            security_protocol=self._security_protocol.value,
            sasl_mechanism=self._sasl_mechanism,
            sasl_plain_username=self._sasl_plain_username,
            sasl_plain_password=self._sasl_plain_password,
            client_id=self._client_id,
            group_id=consumer_group,
            enable_auto_commit=False,
            auto_offset_reset=auto_offset_rest,
            session_timeout_ms=SESSION_TIMEOUT_MS,
            partition_assignment_strategy=list(self._partition_assignors),
        )

    def __mark_record_as_consumed(self, consumer_metadata: dict[str, str], consumer_record: KafkaPollRecord) -> None:
        """
        the committed offset should be
        the next message your application should consume, i.e.: last_offset + 1.
        """
        next_offset_to_be_consumed = consumer_record.offset + 1
        consumer_metadata[
            TopicPartition(topic=consumer_record.topic, partition=consumer_record.partition)
        ] = OffsetAndMetadata(next_offset_to_be_consumed, "")

    def __close_consumer(self, consumer: KafkaConsumer, consumer_metadata: dict) -> None:
        consumer.commit(offsets=consumer_metadata)

        self._logger.info("Closing Consumer's connection")
        consumer.close(autocommit=False)

    def request_stop(self) -> None:
        self._gracefully_stop = True
