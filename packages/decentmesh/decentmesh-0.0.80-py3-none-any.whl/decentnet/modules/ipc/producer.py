import logging
from multiprocessing import Semaphore, shared_memory

from decentnet.consensus.block_sizing import BLOCK_PREFIX_LENGTH_BYTES, MAXIMUM_BLOCK_SIZE
from decentnet.modules.convert.byte_operations import int_to_bytes

logger = logging.getLogger(__name__)


class Producer:
    """
    Producer class that writes a message with a prefix (message size) to shared memory and signals the consumer using a semaphore.
    """

    def __init__(self, channel: str, semaphore: Semaphore) -> None:
        self.channel = channel
        self.semaphore = semaphore
        try:
            self.shm = shared_memory.SharedMemory(name=self.channel)
            logger.debug(f"Producer connected to existing shared memory: {self.channel}")
        except FileNotFoundError:
            self.shm = shared_memory.SharedMemory(create=True, size=MAXIMUM_BLOCK_SIZE, name=self.channel)
            logger.debug(f"Producer created new shared memory: {self.channel}")

    def publish(self, message: bytes) -> None:
        """
        Publish a single message to shared memory with a size prefix (3 bytes) and notify the consumer.

        Args:
            message (bytes): The message to be written to shared memory.
        """
        message_size = len(message)
        prefix_bytes = int_to_bytes(message_size).rjust(BLOCK_PREFIX_LENGTH_BYTES,
                                                        b"\x00")  # 3-byte prefix for size
        total_size = message_size + BLOCK_PREFIX_LENGTH_BYTES  # Total size of prefix + message

        if total_size > self.shm.size:
            raise ValueError(f"Message size exceeds shared memory size ({self.shm.size} bytes).")

        # Write the message with the size prefix
        self.shm.buf[:total_size] = prefix_bytes + message

        # Signal the consumer that new data is ready
        self.semaphore.release()
