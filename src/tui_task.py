# -*- coding: utf-8 -*-

from queue_consumer import queue_consumer

import sys
import inspect
import collections
import asyncio
import itertools
from ast import literal_eval

from prompt_toolkit.document import Document
from prompt_toolkit.formatted_text import to_formatted_text, HTML

import app_loggers
logger = app_loggers.tui_logger


class TaskState(object):
    def __init__(self):
        pass


class Task:
    def __init__(self, loglevel, config, queues, task_state):
        self.loglevel = loglevel
        self.config = config
        self.queues = queues
        self.task_state = task_state

        self.logger_sink = queue_consumer(self.queues['logger:in']) if 'logger:in' in self.queues else None
        self.control_sink = queue_consumer(self.queues['control:in']) if 'control:in' in self.queues else None

        self.tui_queue = asyncio.Queue()
        self.tui_sink = queue_consumer(self.tui_queue)

        # NB: I have access to those through wrapped application
        #self.candles_renderers = {p : CandlesRenderer(self.queues['rest:out'], p, logger=logger) for p in self.task_state.tabs}

        app_loggers.setup_logger(logger, loglevel)



    async def pull_control_sink(self):
        while True:
            try:
                async for cmd, e in self.control_sink:
                    if cmd == 'control':
                        if e['msg'] == 'some_command':
                            #self.on_some_command(e['payload/whatever...'])
                            pass
                        else:
                            logger.warning('control_sink: command {} unknown message {} :: {}'.format(cmd, msg, args))
                    else:
                        logger.warning('control_sink: unknown command {}'.format(cmd))
            except:
                the_type, the_value, the_traceback = sys.exc_info()
                logger.warning('{fn}: unexpected exception {ex} {val}, restarting coroutine.'.format(
                    fn=inspect.currentframe().f_code.co_name,
                    ex=str(the_type), val=str(the_value)))
        logger.info('pull_control_sink EXIT')



    async def pull_tui_sink(self):
        while True:
            try:
                async for cmd, e in self.tui_sink:
                    if cmd == 'ping':
                        pass
                    elif cmd == 'refresh':
                        self.on_tui_refresh(e)
                    else:
                        logger.warning('tui_sink: unknown command {} :: {}'.format(cmd, e))
            except:
                the_type, the_value, the_traceback = sys.exc_info()
                logger.warning('{fn}: unexpected exception {ex} {val}, restarting coroutine.'.format(
                    fn=inspect.currentframe().f_code.co_name,
                    ex=str(the_type), val=str(the_value)))
        logger.info('pull_tui_sink EXIT')


    async def pull_logger_sink(self):
        import logging
        import html

        colors = {
            logging.CRITICAL : 'Magenta',
            logging.ERROR : 'Red',
            logging.WARNING : 'Yellow',
            logging.INFO : 'White',
            logging.DEBUG : 'Grey',
        }

        """
        I need to replace `levelname` with color-formatted content.
        I can't use {levelname} combined with string.format because
        if the log message itself contains other `format` compatible
        substrings, e.g. because it has json in it, it will barf about
        not being able to substitute named arguments.
        Instead I will use two formatters, for head and tail parts around
        levelname, and then simply concatenate them.
        """
        formatter_head = logging.Formatter('%(asctime)s.%(msecs)03d ', datefmt='<Grey>%Y-%m-%d </Grey>%H:%M:%S')
        formatter_tail = logging.Formatter(' <LightSkyBlue>%(name)s</LightSkyBlue> %(message)s')

        depth = self.config.getint('tui', 'log_history_depth', fallback=50)
        fifo = collections.deque([], depth) # fixed size fifo container to keep max N log records

        while True:
            try:
                async for e in self.logger_sink:
                    document = self.logger_buffer.document
                    e.msg = html.escape(e.msg)
                    record_head = formatter_head.format(e)
                    record_tail = formatter_tail.format(e)
                    levelname = '<{color}><b>{level:8s}</b></{color}>'.format(color=colors[e.levelno], level=logging.getLevelName(e.levelno))
                    fifo.append(record_head + levelname + record_tail)
                    text = '\n'.join(fifo)
                    cursor_position = max(0, len(text) - len(fifo[-1]))
                    self.logger_buffer.set_document(Document(text, cursor_position=cursor_position), bypass_readonly=True)
            except:
                the_type, the_value, the_traceback = sys.exc_info()
                # note logging not logger
                logging.warning('{fn}: unexpected exception {ex} {val}, restarting coroutine.'.format(
                    fn=inspect.currentframe().f_code.co_name,
                    ex=str(the_type), val=str(the_value)))
        logger.info('pull_logger_sink EXIT')



    def run_task(self):
        from prompt_toolkit.eventloop import use_asyncio_event_loop

        from tui_app import make_tui_app

        use_asyncio_event_loop()

        logger.info('run_task ENTER')

        wrapped_application = make_tui_app(config=self.config, out_queue=self.tui_queue, state=self.task_state)
        application = wrapped_application.application

        self.logger_buffer = application.layout.get_buffer_by_name('logger_buffer')

        if self.logger_sink:
            asyncio.ensure_future(self.pull_logger_sink())
        if self.control_sink:
            asyncio.ensure_future(self.pull_control_sink())
        asyncio.ensure_future(self.pull_tui_sink())


        asyncio.get_event_loop().run_until_complete(
            application.run_async().to_asyncio_future()
        )
        logger.info('run_task EXIT')
