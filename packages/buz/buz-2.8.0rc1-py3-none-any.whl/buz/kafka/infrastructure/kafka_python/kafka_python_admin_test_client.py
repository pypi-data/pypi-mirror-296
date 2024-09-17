from __future__ import annotations

from logging import Logger
from typing import List, Optional, Union

from kafka import KafkaConsumer, KafkaProducer
from kafka.coordinator.assignors.range import RangePartitionAssignor

from buz.kafka.domain.services.kafka_admin_test_client import KafkaAdminTestClient
from buz.kafka.domain.services.kafka_consumer import DEFAULT_NUMBER_OF_MESSAGES_TO_POLLING
from buz.kafka.infrastructure.kafka_python.kafka_poll_record import KafkaPollRecord
from buz.kafka.domain.models.consumer_initial_offset_position import ConsumerInitialOffsetPosition
from buz.kafka.domain.models.kafka_supported_security_protocols import KafkaSupportedSecurityProtocols
from buz.kafka.infrastructure.kafka_python.kafka_python_admin_client import KafkaPythonAdminClient

CONSUMER_POLL_TIMEOUT_MS = 1000


class KafkaPythonAdminTestClient(KafkaPythonAdminClient, KafkaAdminTestClient):
    def __init__(
        self,
        *,
        bootstrap_servers: List[str],
        client_id: str,
        logger: Logger,
        security_protocol: KafkaSupportedSecurityProtocols,
        sasl_mechanism: Union[str, None] = None,
        sasl_plain_username: Optional[str] = None,
        sasl_plain_password: Optional[str] = None,
    ):
        super().__init__(
            client_id=client_id,
            bootstrap_servers=bootstrap_servers,
            logger=logger,
            security_protocol=security_protocol,
            sasl_mechanism=sasl_mechanism,
            sasl_plain_username=sasl_plain_username,
            sasl_plain_password=sasl_plain_password,
        )

    def send_message_to_topic(
        self,
        *,
        topic: str,
        message: bytes,
        headers: Optional[list[tuple[str, bytes]]] = None,
        partition_key: Optional[str] = None,
    ) -> None:
        producer = KafkaProducer(
            **self._generate_kafka_auth_configuration(),
        )

        producer.send(
            topic=topic,
            value=message,
            headers=headers,
            key=partition_key,
        )

        producer.close()

    def get_messages_from_topic(
        self,
        *,
        topic: str,
        consumer_group: str,
        max_number_of_messages_to_polling: int = DEFAULT_NUMBER_OF_MESSAGES_TO_POLLING,
        offset: ConsumerInitialOffsetPosition = ConsumerInitialOffsetPosition.BEGINNING,
    ) -> list[KafkaPollRecord]:
        consumer = KafkaConsumer(
            **self._generate_kafka_auth_configuration(),
            group_id=consumer_group,
            enable_auto_commit=True,
            auto_offset_reset="earliest" if offset == ConsumerInitialOffsetPosition.BEGINNING else "latest",
            partition_assignment_strategy=(RangePartitionAssignor,),
        )

        consumer.subscribe(topics=topic)

        records = list(
            consumer.poll(
                timeout_ms=CONSUMER_POLL_TIMEOUT_MS,
                max_records=max_number_of_messages_to_polling,
            ).values()
        )

        consumer.close()

        topic_records = records[0] if len(records) > 0 else []

        return topic_records

    def delete_all_resources(
        self,
    ) -> None:
        self.delete_topics(topics=self.get_topics())
        self._wait_for_cluster_update()
