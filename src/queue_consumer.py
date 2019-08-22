# -*- coding: utf-8 -*-

import asyncio

async def queue_consumer(q):
    """Consume from an asyncio.Queue, making it an async iterable"""
    while True:
        try:
            e = await q.get()
            yield e
        except:
            continue
