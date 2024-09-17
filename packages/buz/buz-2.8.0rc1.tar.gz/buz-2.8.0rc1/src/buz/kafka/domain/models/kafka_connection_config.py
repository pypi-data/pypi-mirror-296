from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from buz.kafka.domain.models.kafka_supported_security_protocols import KafkaSupportedSecurityProtocols


@dataclass(frozen=True)
class KafkaConnectionConfig:
    bootstrap_servers: list[str]
    client_id: str
    security_protocol: KafkaSupportedSecurityProtocols
    user: Optional[str]
    password: Optional[str]
