from __future__ import annotations

from abc import ABC
from logging import Logger
from typing import Union

from buz.kafka.domain.models.kafka_connection_config import KafkaConnectionConfig
from buz.kafka.domain.models.kafka_supported_security_protocols import KafkaSupportedSecurityProtocols


SSASL_MECHANISM = "SCRAM-SHA-512"
AUTHENTICATION_PROTOCOL_VALUES = Union[str, KafkaSupportedSecurityProtocols, None]


class KafkaPythonClientFactory(ABC):
    def __init__(
        self,
        logger: Logger,
        kafka_connection_config: KafkaConnectionConfig,
    ):
        self._logger = logger
        self._kafka_connection_config = kafka_connection_config

    def _get_autentication_configuration_by_security_protocol(self) -> dict[str, AUTHENTICATION_PROTOCOL_VALUES]:
        security_protocol_to_authentication_configuration: dict[str, dict[str, AUTHENTICATION_PROTOCOL_VALUES]] = {
            KafkaSupportedSecurityProtocols.SASL_PLAINTEXT.value: {
                "security_protocol": KafkaSupportedSecurityProtocols.SASL_PLAINTEXT,
                "sasl_mechanism": SSASL_MECHANISM,
                "sasl_plain_username": self._kafka_connection_config.user,
                "sasl_plain_password": self._kafka_connection_config.password,
            },
            KafkaSupportedSecurityProtocols.SASL_SSL.value: {
                "security_protocol": KafkaSupportedSecurityProtocols.SASL_SSL,
                "sasl_mechanism": SSASL_MECHANISM,
                "sasl_plain_username": self._kafka_connection_config.user,
                "sasl_plain_password": self._kafka_connection_config.password,
            },
        }

        configuration = security_protocol_to_authentication_configuration.get(
            self._kafka_connection_config.security_protocol.value
        )

        if configuration is not None:
            return configuration

        return {"security_protocol": KafkaSupportedSecurityProtocols.PLAINTEXT}
