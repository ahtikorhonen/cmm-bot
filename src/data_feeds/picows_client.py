from time import time_ns

import asyncio
import msgspec
from picows import ws_connect, WSFrame, WSTransport, WSListener, WSMsgType, WSCloseCode
from typing import Tuple, List, Dict, Union, Callable, Optional

RawWsPayload = bytearray
PayloadData = Dict[str, Union[int, float, str, Dict, List]]
QueuePayload = Tuple[int, int, PayloadData]


class RawWsConnection(WSListener):
    """
    Wrapper of WSListener class for PicoWs use.
    Copied from https://github.com/tarasko/picows/blob/master/examples/echo_client_cython.pyx.
    """
    def __init__(self, process_frame: Callable) -> None:
        super().__init__()
        self.transport: WSTransport = None
        self.process_frame = process_frame

        self.final_frame: RawWsPayload = bytearray()

    def on_ws_connected(self, transport: WSTransport):
        self.transport = transport

    def on_ws_frame(self, transport: WSTransport, frame: WSFrame):
        self.final_frame += frame.get_payload_as_memoryview()

        if frame.fin:
            self.process_frame(time_ns(), self.final_frame)
            self.final_frame.clear()


class SingleWsConnection:
    QUEUE_MAX_SIZE = 10000

    json_encoder = msgspec.json.Encoder()
    json_decoder = msgspec.json.Decoder()

    def __init__(self) -> None:
        """
        Initializes a single WebSocket connection.
        """
        self._running: bool = False
        self._ws_client: WSListener = None
        self._seq_id: int = 0
        self._conn_task: asyncio.Task = None
        self._queue = asyncio.Queue(self.QUEUE_MAX_SIZE)

    @property
    def running(self) -> bool:
        """
        Returns the websocket running state
        :return (bool): the websocket running state
        """
        return self._running

    @property
    def seq_id(self) -> int:
        """
        Returns the current sequence ID
        :return (int): The current sequence ID
        """
        return self._seq_id

    @property
    def queue(self) -> asyncio.Queue:
        """
        Returns the queue associated with this connection
        :return (asyncio.Queue): The queue used for incoming messages
        """
        return self._queue

    def _process_frame(self, time: int, final_frame: RawWsPayload) -> None:
        """
        Processes an incoming WebSocket frame
        :time (int): The timestamp of the frame
        :final_frame (RawWsPayload): The raw WebSocket frame payload
        """
        try:
            self._seq_id += 1
            q_payload: QueuePayload = (
                self._seq_id,
                time,
                self.json_decoder.decode(final_frame),
            )
            self._queue.put_nowait(q_payload)

        except asyncio.QueueFull:
            pass

        except Exception as e:
            pass

    def reset_seq_id(self) -> None:
        """
        Resets the sequence ID to 0.
        """
        self._seq_id = 0

    def send_data(
        self, payload: Dict, msg_type: Optional[int] = WSMsgType.TEXT
    ) -> None:
        """
        Sends a payload through the WebSocket connection
        :payload (dict): The payload to send
        """
        try:
            if self._ws_client.transport is not None:
                self._ws_client.transport.send(
                    msg_type, self.json_encoder.encode(payload)
                )
            else:
                raise ConnectionError("Connection not started yet.")

        except Exception as e:
            raise Exception(f"Failed to send data - {str(e)}")

    async def start(
        self,
        url: str,
        on_connect: Optional[List[Dict]] = None,
    ) -> None:
        """
        Starts the WebSocket connection and handles incoming messages
        :url (str): The URL of the WebSocket endpoint
        :on_connect (Optional[List[dict]]): A list of payloads to send upon connecting (default is None)
        """
        if self._running:
            return

        try:
            self._running = True
            self.url = url
            self.on_connect = on_connect if on_connect is not None else []

            (_, self._ws_client) = await ws_connect(
                lambda: RawWsConnection(self._process_frame), self.url
            )

            for payload in self.on_connect:
                self.send_data(payload)

            self._conn_task = asyncio.create_task(
                self._ws_client.transport.wait_disconnected()
            )

        except Exception as e:
            raise Exception(f"Failed to initialize the websocket connection - {str(e)}")

    async def restart(self) -> None:
        """
        Restart the WebSocket connection with the same args as when
        it was first started.
        """
        if not self._running:
            raise ConnectionError(f"Conn '{self._conn_id}' not started yet.")

        if self._ws_client is not None:
            self._ws_client.transport.send_close(WSCloseCode.OK)
            self._ws_client.transport.disconnect()

        if self._conn_task is not None:
            if not self._conn_task.done():
                self._conn_task.cancel()

        self._queue = asyncio.Queue(self.QUEUE_MAX_SIZE)

        self.reset_seq_id()

        (_, self._ws_client) = await ws_connect(
            lambda: RawWsConnection(self._process_frame), self.url
        )

        for payload in self.on_connect:
            self.send_data(payload)

        self._conn_task = asyncio.create_task(
            self._ws_client.transport.wait_disconnected()
        )

    def close(self) -> None:
        """
        Closes the WebSocket connection and cancels any ongoing tasks.
        """
        self._running = False

        if self._ws_client is not None:
            self._ws_client.transport.send_close(WSCloseCode.OK)
            self._ws_client.transport.disconnect()

        if self._conn_task is not None:
            self._conn_task.cancel()