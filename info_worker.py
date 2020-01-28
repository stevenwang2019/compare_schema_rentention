import logging
import os
from Queue import Queue
from threading import Thread
from time import time
from process_yaml import *

diff_dir = 'diff'

wsp_root = '/mnt/data/whisper'
if(len(sys.argv) > 1):
    wsp_root = str(sys.argv[1])

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class InfoWorker(Thread):

    def __init__(self, queue, id):
        Thread.__init__(self)
        self.queue = queue
        self.id = id

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            wsp_file, archive = self.queue.get()
            try:
                if compare_whisper_info(wsp_file, archive) == 1 :
                    write_to = diff_dir+"/thread"+str(self.id)+".txt"
                    append_to_file(write_to, wsp_file)
            finally:
                self.queue.task_done()


def main():
    ts = time()
    archives = get_baseline_archives()
    remove_dir(diff_dir)
    create_dir(diff_dir)
    cmd = []
    cmd.append('find')
    cmd.append(wsp_root)
    cmd.append('-name')
    cmd.append('*.wsp')
    files, errs = exec_subprocess(cmd)
    # Create a queue to communicate with the worker threads
    queue = Queue()
    # Create 8 worker threads

    for x in range(8):
        worker = InfoWorker(queue, x)
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()
    # Put the tasks into the queue as a tuple
    for file in files.split('\n'):
        logger.info('Queueing {}'.format(file))
        archive = match_file_path(file, archives)
        queue.put((file, archive))
    # Causes the main thread to wait for the queue to finish processing all the tasks
    queue.join()
    logging.info('Took %s', time() - ts)

if __name__ == '__main__':
    main()