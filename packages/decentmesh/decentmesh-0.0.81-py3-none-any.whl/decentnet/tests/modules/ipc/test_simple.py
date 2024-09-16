from multiprocessing import Process, Semaphore

from decentnet.modules.ipc.consumer import Consumer
from decentnet.modules.ipc.producer import Producer

if __name__ == '__main__':
    shared_mem_key = 'shared_memory_key'

    # Create a semaphore for signaling
    semaphore = Semaphore(0)  # Start with a locked semaphore (0)

    # Start producer and consumer processes
    producer = Producer(shared_mem_key, semaphore)
    consumer = Consumer(shared_mem_key, semaphore)

    producer_process = Process(target=producer.publish, args=(b"Hello from Producer!",))
    consumer_process = Process(target=consumer.consume)

    producer_process.start()
    consumer_process.start()

    producer_process.join()
    consumer_process.terminate()  # Stop the consumer after producer finishes

    # Cleanup shared memory
    producer.shm.close()
    producer.shm.unlink()  # Unlink shared memory when done
