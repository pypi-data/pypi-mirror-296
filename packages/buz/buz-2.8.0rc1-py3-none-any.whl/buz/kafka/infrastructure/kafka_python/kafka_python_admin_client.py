from __future__ import annotations

import re
from logging import Logger
from typing import List, Optional, Union

from kafka import KafkaClient
from kafka.admin import KafkaAdminClient as NativeKafkaPythonAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

from buz.kafka.domain.exceptions.topic_already_created_exception import KafkaTopicsAlreadyCreatedException
from buz.kafka.domain.models.kafka_supported_security_protocols import KafkaSupportedSecurityProtocols
from buz.kafka.domain.models.kafka_topic import KafkaTopic
from buz.kafka.domain.services.kafka_admin_client import KafkaAdminClient


INTERNAL_KAFKA_TOPICS = {"__consumer_offsets", "_schema"}
PYTHON_KAFKA_DUPLICATED_TOPIC_ERROR_CODE = 36
CONSUMER_POLL_TIMEOUT_MS = 1000


class KafkaPythonAdminClient(KafkaAdminClient):
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
        self._client_id = client_id
        self._bootstrap_servers = bootstrap_servers
        self._logger = bootstrap_servers
        self._sasl_mechanism = sasl_mechanism
        self._security_protocol = security_protocol
        self._sasl_plain_username = sasl_plain_username
        self._sasl_plain_password = sasl_plain_password

        self._kafka_admin = NativeKafkaPythonAdminClient(
            **self._generate_kafka_auth_configuration(),
        )

        self._kafka_client = KafkaClient(
            **self._generate_kafka_auth_configuration(),
        )

    def _generate_kafka_auth_configuration(self) -> dict:
        return {
            "client_id": self._client_id,
            "bootstrap_servers": self._bootstrap_servers,
            "security_protocol": self._security_protocol.value,
            "sasl_mechanism": self._sasl_mechanism,
            "sasl_plain_username": self._sasl_plain_username,
            "sasl_plain_password": self._sasl_plain_password,
        }

    def create_topics(
        self,
        *,
        topics: set[KafkaTopic],
    ) -> None:
        new_topics = [
            NewTopic(
                name=topic.name,
                num_partitions=topic.partitions,
                replication_factor=topic.replication_factor,
            )
            for topic in topics
        ]

        try:
            self._kafka_admin.create_topics(new_topics=new_topics)
        except TopicAlreadyExistsError as error:
            topic_names = self.__get_list_of_kafka_topics_from_topic_already_exists_error(error)
            raise KafkaTopicsAlreadyCreatedException(topic_names=topic_names)

    def __get_list_of_kafka_topics_from_topic_already_exists_error(self, error: TopicAlreadyExistsError) -> list[str]:
        message = str(error)
        response_message = re.search(r"topic_errors=\[.*?\]", message)
        topic_messages = re.findall(r"topic='[^']*', error_code=" + str(PYTHON_KAFKA_DUPLICATED_TOPIC_ERROR_CODE), response_message[0])  # type: ignore

        return [re.search("'.*'", topic_message)[0].strip("'") for topic_message in topic_messages]  # type: ignore

    def get_topics(
        self,
    ) -> set[str]:
        return set(self._kafka_admin.list_topics()) - INTERNAL_KAFKA_TOPICS

    def delete_topics(
        self,
        *,
        topics: set[str],
    ) -> None:
        self._kafka_admin.delete_topics(
            topics=topics,
        )

    def _wait_for_cluster_update(self) -> None:
        future = self._kafka_client.cluster.request_update()
        self._kafka_client.poll(future=future)
