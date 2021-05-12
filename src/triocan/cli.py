import logging

import click
import can
import trio

import triocan

logger = logging.getLogger(__name__)


@click.command()
def main():
    root_logger = logging.getLogger()
    log_level = logging.DEBUG

    stderr_handler = logging.StreamHandler()
    root_logger.addHandler(stderr_handler)

    root_logger.setLevel(log_level)
    stderr_handler.setLevel(log_level)

    trio.run(async_main)


async def async_main():
    can_bus = can.interface.Bus(bustype='socketcan', channel='can0')

    triocan_bus = triocan.Bus.build(bus=can_bus)

    async with triocan_bus.linked() as receive_channel:
        async with trio.open_nursery() as nursery:
            nursery.start_soon(send, triocan_bus)
            nursery.start_soon(print_incoming, receive_channel)

            await trio.sleep(1)

            nursery.cancel_scope.cancel()


async def print_incoming(receive_channel):
    logger.debug('starting loop')

    async for message in receive_channel:
        import threading
        logging.debug(
            'async_main %s %s',
            threading.get_ident() == threading.main_thread().ident,
            message,
        )


async def send(triocan_bus):
    while True:
        message = can.Message(
            arbitration_id=0x42,
            is_extended_id=False,
            dlc=0,
        )
        await triocan_bus.send(message)

        await trio.sleep(0.1)
