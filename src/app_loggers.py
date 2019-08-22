# -*- coding: utf-8 -*-

import logging
import datetime
import time
import os
import errno


main_logger = logging.getLogger('main')
queue_monitor_logger = logging.getLogger('queue_monitor')
tui_logger = logging.getLogger('tui')

asyncio_logger = logging.getLogger('asyncio')

loggers = (
    main_logger,
    queue_monitor_logger,
    tui_logger,
    asyncio_logger,
)

now_iso = datetime.datetime.fromtimestamp(time.time()).isoformat()

def setup_logger(logger, loglevel=logging.INFO):
    logger.setLevel(loglevel)


def attach_queue_handler(logger, queue):
    from logging.handlers import QueueHandler
    qh = QueueHandler(queue)
    logger.addHandler(qh)


def attach_file_handler(logger):
    try:
        os.makedirs('.logs')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)8s %(name)10s %(message)s', datefmt='%Y-%m-%dT%H:%M:%S')

    fh = logging.FileHandler(".logs/{}.log".format(now_iso))
    fh.setFormatter(formatter)
    logger.addHandler(fh)
