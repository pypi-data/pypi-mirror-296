from __future__ import annotations

from logging import Logger
from typing import Generic, List, Optional, TypeVar

from kafka import KafkaProducer

from buz.kafka.domain.models.kafka_supported_security_protocols import KafkaSupportedSecurityProtocols
from buz.kafka.infrastructure.serializers.byte_serializer import ByteSerializer
from buz.kafka.infrastructure.serializers.kafka_header_serializer import KafkaHeaderSerializer


T = TypeVar("T")


class KafkaPythonProducer(KafkaProducer, Generic[T]):
    def __init__(
        self,
        *,
        bootstrap_servers: List[str],
        client_id: str,
        logger: Logger,
        byte_serializer: ByteSerializer[T],
        security_protocol: KafkaSupportedSecurityProtocols,
        sasl_mechanism: Optional[str] = None,
        sasl_plain_username: Optional[str] = None,
        sasl_plain_password: Optional[str] = None,
        retries: int = 0,
        retry_backoff_ms: int = 100,
    ):
        self._logger = bootstrap_servers
        self.__byte_serializer = byte_serializer
        self.__header_serializer = KafkaHeaderSerializer()

        self.__kafkaProducer = KafkaProducer(
            client_id=client_id,
            bootstrap_servers=bootstrap_servers,
            security_protocol=security_protocol.value,
            sasl_mechanism=sasl_mechanism,
            sasl_plain_username=sasl_plain_username,
            sasl_plain_password=sasl_plain_password,
            retries=retries,
            retry_backoff_ms=retry_backoff_ms,
        )

    def produce(
        self,
        *,
        topic: str,
        message: T,
        partition_key: Optional[str] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> None:
        serialized_headers = self.__header_serializer.serialize(headers) if headers is not None else None

        self.__kafkaProducer.send(
            topic=topic,
            value=self.__byte_serializer.serialize(message),
            headers=serialized_headers,
            key=partition_key,
        )
