import logging
import time
from multiprocessing import Semaphore, shared_memory

from decentnet.consensus.block_sizing import BLOCK_PREFIX_LENGTH_BYTES, MAXIMUM_BLOCK_SIZE
from decentnet.consensus.byte_conversion_constants import ENDIAN_TYPE

logger = logging.getLogger(__name__)


class Consumer:
    """
    Consumer class that reads messages from shared memory when signaled by the producer.
    Reads the message size prefix (3 bytes) first, then the actual message.
    """

    def __init__(self, channel: str, semaphore: Semaphore, timeout: int = 30) -> None:
        self.channel = channel
        self.semaphore = semaphore
        self.shm = None

        # Attempt to connect to shared memory with a timeout
        start_time = time.time()
        while True:
            try:
                self.shm = shared_memory.SharedMemory(name=self.channel)
                logger.debug(f"Consumer connected to existing shared memory: {self.channel}")
                break
            except FileNotFoundError:
                self.shm = shared_memory.SharedMemory(create=True, size=MAXIMUM_BLOCK_SIZE, name=self.channel)
                logger.debug(f"Consumer created new shared memory: {self.channel}")

    def consume(self) -> bytes:
        """
        Wait for a signal from the producer, read the message size prefix (3 bytes), and then the message.

        Returns:
            bytes: The message read from shared memory.
        """
        # Wait until the producer signals with the semaphore
        self.semaphore.acquire()

        # Read the size prefix (first 3 bytes)
        prefix = bytes(self.shm.buf[:BLOCK_PREFIX_LENGTH_BYTES])
        message_size = int.from_bytes(prefix, byteorder=ENDIAN_TYPE,
                                      signed=False)  # Convert prefix to integer

        # Read the actual message based on the size
        message = self.shm.buf[BLOCK_PREFIX_LENGTH_BYTES:BLOCK_PREFIX_LENGTH_BYTES + message_size].tobytes()

        return message
