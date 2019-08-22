#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Console script for {{cookiecutter.project_slug}}."""
import sys
import logging
import argparse
import configparser
import asyncio

import app_loggers
from app_loggers import setup_logger, attach_queue_handler, attach_file_handler

from prompt_toolkit.eventloop.defaults import use_asyncio_event_loop
from prompt_toolkit.eventloop import ensure_future

logger = app_loggers.main_logger


def parse_arguments(cmdline_args):
    parser = argparse.ArgumentParser()

    parser.add_argument('--loglevel', '-l', type=str, choices=('error', 'warning', 'info', 'debug'), default='info')
    parser.add_argument('--loop-debug', '-L', action='store_true')

    args = parser.parse_args(cmdline_args)
    return args


def build_tui_queues(loop):
    rv = dict()

    for name in ['logger:in', 'control:in']:
        q = asyncio.Queue(loop=loop)
        rv[name] = q

    return rv


def read_config():
    builtin = """
    [DEFAULT]
    [logging]
    asyncio_level=ERROR
    [tui]
    full_screen=True
    mouse_support=False
    """

    config = configparser.ConfigParser()

    config.read_string(builtin)
    config.read('.tuiconfig')  ### TODO change this to sth meaningful for your app

    return config


def main(args=None):

    args = parse_arguments(args)
    loglevel = getattr(logging, args.loglevel.upper())
    setup_logger(logger, loglevel)

    config = read_config()

    loop = asyncio.new_event_loop()
    loop.set_debug(args.loop_debug)
    asyncio.set_event_loop(loop)

    queues = build_tui_queues(loop)

    for lg in app_loggers.loggers:
        attach_queue_handler(lg, queues['logger:in'])
        attach_file_handler(lg)

    asyncio_logger_level = getattr(logging, config['logging']['asyncio_level'].upper())
    setup_logger(app_loggers.asyncio_logger, asyncio_logger_level)


#    from core_task import Task as CoreTask
#    core = CoreTask(keys, loop, args.product_ids, loglevel, config=config, queues=queues)
#    ct = asyncio.ensure_future(core.main())

    from tui_task import TaskState as TuiTaskState, Task as TuiTask
    state = TuiTaskState()
    app = TuiTask(loglevel, config=config, queues=queues, task_state=state)

    app.run_task()

    return



if __name__ == "__main__":
    sys.exit(main()) # pragma: no cover
