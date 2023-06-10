"""This module contains the queue name and callback function
"""

import aio_pika
import importlib

MY_QUEUE_NAME = 'image_generate'


async def image_generate_queue_callback(message: aio_pika.IncomingMessage):
    """Callback function for the queue

    This function will be called when a message is received from the queue."""
    try:
        generate_image = importlib.import_module("generate_image")
        print(f" [x] Received {message.body.decode()}")
        await message.ack()
        generate_image.generate_image(message.body.decode())
    except Exception as e:
        print("Error:", e)
        await message.reject(requeue=False)


def get_image_generate_queue() -> tuple[str, callable]:
    """Get the queue name and callback function

    This function will return the queue name and callback function."""
    return MY_QUEUE_NAME, image_generate_queue_callback
