import contextlib
import logging
import threading

import attr
import can
import trio

logger = logging.getLogger(__name__)


@attr.s
class Listener(can.Listener):
    callable = attr.ib()

    def __attrs_post_init__(self):
        super(Listener, self).__init__()

    def on_message_received(self, msg):
        self.callable(message=msg)


@attr.s
class Bus:
    bus = attr.ib(default=None)
    notifier = attr.ib(default=None)
    listener = attr.ib(default=None)
    incoming_send_channel = attr.ib(default=None)
    receive_buffer_length = attr.ib(default=0)

    @classmethod
    def build(cls, bus, receive_buffer_length=100):
        self = cls(
            bus=bus,
            receive_buffer_length=receive_buffer_length,
        )
        self.listener = Listener(callable=self._receive_in_thread)
        self.notifier = can.Notifier(bus=bus, listeners=[])

        return self

    @contextlib.asynccontextmanager
    async def linked(self):
        self.notifier.add_listener(self.listener)

        self.incoming_send_channel, receive_channel = (
            trio.open_memory_channel(self.receive_buffer_length)
        )

        async with self.incoming_send_channel, receive_channel:
            try:
                yield receive_channel
            finally:
                self.notifier.remove_listener(self.listener)

    async def _receive_in_trio(self, message):
        logging.debug(
            'receive_in_trio %s %s',
            threading.get_ident() == threading.main_thread().ident,
            message,
        )
        await self.incoming_send_channel.send(message)

    def _receive_in_thread(self, message):
        trio.from_thread.run(self._receive_in_trio, message)

    async def send(self, message):
        await trio.to_thread.run_sync(self.bus.send, message)
