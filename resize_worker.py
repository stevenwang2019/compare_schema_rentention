import logging
import os
from Queue import Queue
from threading import Thread
from time import time
from process_yaml import *
import shared_vars

diff_dir = shared_vars.diff_dir

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ResizeWorker(Thread):

    def __init__(self, queue, id):
        Thread.__init__(self)
        self.queue = queue
        self.id = id

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            file, archive = self.queue.get()
            try:
                if shared_vars.resize:
                    resize_wsp(file, archive.resize_arg)
                if shared_vars.remove_bak:
                    os.remove(file)
            finally:
                self.queue.task_done()

def main():
    ts = time()
    archives = get_baseline_archives()
    df = open(shared_vars.diff_file, "r")
    # Create a queue to communicate with the worker threads
    queue = Queue()
    # Create 8 worker threads
    for x in range(8):
        worker = ResizeWorker(queue, x)
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()
    # Put the tasks into the queue as a tuple
    for file in df:
        logger.info('Queueing {}'.format(file))
        archive = match_file_path(file, archives)
        queue.put((file, archive))
    # Causes the main thread to wait for the queue to finish processing all the tasks
    queue.join()
    logging.info('Took %s', time() - ts)

if __name__ == '__main__':
    main()