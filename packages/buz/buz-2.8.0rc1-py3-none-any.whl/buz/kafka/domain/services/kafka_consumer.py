from abc import abstractmethod, ABC
from typing import Callable, List

from buz.kafka.domain.models.consumer_initial_offset_position import ConsumerInitialOffsetPosition
from buz.kafka.domain.models.kafka_consumer_record import KafkaConsumerRecord

DEFAULT_NUMBER_OF_MESSAGES_TO_POLLING = 500


class KafkaConsumer(ABC):
    @abstractmethod
    def consume(
        self,
        *,
        topics: List[str],
        consumer_group: str,
        consumption_callback: Callable[[KafkaConsumerRecord], None],
        initial_offset_position: ConsumerInitialOffsetPosition = ConsumerInitialOffsetPosition.END,
        number_of_messages_to_polling: int = DEFAULT_NUMBER_OF_MESSAGES_TO_POLLING,
    ) -> None:
        pass

    def request_stop(self) -> None:
        """Request a graceful stop
        This method does not stop the consumer in a instantaneous way,
        it will finalize when the current task will be completed (eventually)
        """
        pass
