import random
import time
import unittest
from multiprocessing import Process, Semaphore, Manager

from decentnet.consensus.block_sizing import MAXIMUM_BLOCK_SIZE
from decentnet.modules.ipc.consumer import Consumer
from decentnet.modules.ipc.producer import Producer


def generate_messages(num_messages: int) -> list:
    """
    Generate random messages beforehand, providing verbose output for each message.

    Args:
        num_messages (int): The number of random messages to generate.

    Returns:
        list: A list of random byte messages.
    """
    messages = []
    for i in range(num_messages):
        size = random.randint(1, MAXIMUM_BLOCK_SIZE)
        message = random.randbytes(size)
        messages.append(message)

        # Verbose output for each message
        print(f"Generated message {i + 1}/{num_messages} - Size: {size} bytes")

    print(f"Total {num_messages} messages generated.")
    return messages


def consumer_process(shm_key, semaphore, num_messages):
    """
    Function for consumer process to consume messages.
    """
    consumer = Consumer(shm_key, semaphore)
    for _ in range(num_messages):
        consumer.consume()


def producer_process(shm_key, semaphore, messages):
    """
    Function for producer process to publish pre-generated messages.

    Args:
        shm_key (str): Shared memory key.
        semaphore (Semaphore): Semaphore for signaling.
        messages (list): List of pre-generated messages.
    """
    producer = Producer(shm_key, semaphore)

    for message in messages:
        producer.publish(message)


class PerformanceTest(unittest.TestCase):

    def test_performance(self):
        """
        Test the performance of the Producer/Consumer message passing using shared memory and semaphore.
        Measures both the latency (time it takes for a message to reach the consumer)
        and the throughput (messages per second).
        """

        shared_mem_key = 'test_shared_memory_key'
        semaphore = Semaphore(0)  # Used for signaling new message availability

        # Number of messages to test throughput
        num_messages = 1000
        print("Generating messages...")
        manager = Manager()
        messages = manager.list(generate_messages(num_messages))

        # Create producer and consume

        # Start the timer for latency and throughput measurement
        start_time = time.perf_counter_ns()

        # Create consumer and producer processes
        consumer_proc = Process(target=consumer_process,
                                args=(shared_mem_key, semaphore, num_messages))
        producer_proc = Process(target=producer_process,
                                args=(shared_mem_key, semaphore, messages))

        # Start both processes
        consumer_proc.start()
        producer_proc.start()

        # Wait for both processes to finish
        producer_proc.join()
        consumer_proc.join()

        # End time after processes complete
        end_time = time.perf_counter_ns()

        # Calculate the time taken and throughput
        total_time = end_time - start_time

        # Latency per message (in nanoseconds)
        latency_per_message = total_time / num_messages

        # Throughput calculation: number of messages per second
        # Convert total_time to seconds by dividing by 1,000,000,000
        throughput = num_messages / (total_time / 1_000_000_000)

        # Output in milliseconds (convert from nanoseconds)
        print(f"Total time for {num_messages} messages: {total_time / 1_000_000:.6f} ms")
        print(f"Average latency per message: {latency_per_message / 1_000_000:.6f} ms")
        print(f"Throughput: {throughput:.6f} messages per second")


if __name__ == '__main__':
    unittest.main()
